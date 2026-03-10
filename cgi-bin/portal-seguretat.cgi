#!/bin/bash

echo "Content-type: text/html; charset=utf-8"
echo ""

# Sessions source
SESSION_DIR="/tmp/portal_sessions"
LOG_FILE="/usr/local/JSBach/logs/portal.log"

# Handle actions
if [ "$REQUEST_METHOD" = "GET" ]; then
    QS="$QUERY_STRING"
else
    read -n "$CONTENT_LENGTH" QS
fi

ACTION=$(echo "$QS" | grep -o 'action=[^&]*' | cut -d'=' -f2)
IP_ACTION=$(echo "$QS" | grep -o 'ip=[^&]*' | cut -d'=' -f2)
MAC_ACTION=$(echo "$QS" | grep -o 'mac=[^&]*' | cut -d'=' -f2)

if [ "$ACTION" = "kill" ] && [ -n "$IP_ACTION" ] && [ -n "$MAC_ACTION" ]; then
    sudo /usr/local/JSBach/scripts/portal deauth "$IP_ACTION" "$MAC_ACTION" > /dev/null 2>&1
    echo "Status: 302 Found"
    echo "Location: portal-seguretat.cgi"
    echo ""
    exit 0
fi

cat << EOM
<html>
<head>
<meta charset="utf-8">
<style>
    :root {
        --bg-color: #0f172a;
        --card-bg: rgba(30, 41, 59, 0.7);
        --accent: #38bdf8;
        --text-main: #e5e7eb;
        --text-dim: #94a3b8;
        --success: #4ade80;
        --error: #f87171;
    }
    body { 
        font-family: 'Inter', system-ui, -apple-system, sans-serif; 
        background: var(--bg-color); 
        color: var(--text-main); 
        padding: 30px; 
        margin: 0;
        line-height: 1.5;
    }
    h2 { 
        font-size: 1.875rem;
        font-weight: 700;
        color: var(--accent);
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    h2::before {
        content: '';
        display: block;
        width: 4px;
        height: 32px;
        background: var(--accent);
        border-radius: 4px;
    }
    .grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 24px;
    }
    .card { 
        background: var(--card-bg); 
        border-radius: 16px; 
        padding: 24px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(8px);
    }
    .card h3 {
        margin-top: 0;
        font-size: 1.25rem;
        color: var(--accent);
        margin-bottom: 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding-bottom: 12px;
    }
    .log-container {
        max-height: 400px;
        overflow-y: auto;
        background: #000;
        border-radius: 12px;
        padding: 15px;
        font-family: 'Fira Code', 'Courier New', monospace;
        font-size: 0.875rem;
    }
    .log-entry { margin-bottom: 4px; border-bottom: 1px solid #111; padding-bottom: 2px; }
    .log-success { color: var(--success); }
    .log-fail { color: var(--error); }
    .log-info { color: var(--text-dim); }

    table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    th { text-align: left; color: var(--text-dim); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; padding: 12px 8px; border-bottom: 2px solid rgba(255, 255, 255, 0.05); }
    td { padding: 12px 8px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); font-size: 0.9rem; }
    .badge {
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(56, 189, 248, 0.1);
        color: var(--accent);
    }
    .btn-logout {
        background: var(--error);
        color: white;
        border: none;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 600;
        cursor: pointer;
        transition: opacity 0.2s;
    }
    .btn-logout:hover { opacity: 0.8; }
    pre {
        background: #000;
        padding: 15px;
        border-radius: 12px;
        font-size: 0.8rem;
        color: #4ade80;
        overflow-x: auto;
    }
</style>
</head>
<body>
    <h2>Seguridad y Logs del Portal</h2>

    <div class="grid">
        <!-- Active Sessions -->
        <div class="card">
            <h3>Sesiones Activas</h3>
            <table>
                <thead>
                    <tr>
                        <th>Usuario</th>
                        <th>IP</th>
                        <th>MAC</th>
                        <th>Inicio</th>
                        <th>Acción</th>
                    </tr>
                </thead>
                <tbody>
EOM

# List active sessions
find "$SESSION_DIR" -type f 2>/dev/null | while read -r session; do
    unset USER IP MAC START
    source "$session"
    start_fmt=$(date -d "@$START" "+%H:%M:%S" 2>/dev/null || echo "$START")
    echo "<tr>
            <td><span class='badge'>$USER</span></td>
            <td>$IP</td>
            <td>$MAC</td>
            <td style='color: var(--text-dim)'>$start_fmt</td>
            <td><button class='btn-logout' onclick=\"location.href='portal-seguretat.cgi?action=kill&ip=$IP&mac=$MAC'\">Desconectar</button></td>
          </tr>"
done | sort

cat << EOM
                </tbody>
            </table>
        </div>

        <!-- Portal Logs -->
        <div class="card">
            <h3>Registro de Eventos (Últimos 50)</h3>
            <div class="log-container">
EOM

# Show last 50 logs with color coding
if [ -f "$LOG_FILE" ]; then
    tail -n 50 "$LOG_FILE" | tac | while read -r line; do
        class="log-info"
        [[ "$line" == *"[LOGIN-SUCCESS]"* ]] && class="log-success"
        [[ "$line" == *"[AUTH]"* ]] && class="log-success"
        [[ "$line" == *"[LOGIN-FAIL]"* ]] && class="log-fail"
        echo "<div class='log-entry $class'>$(echo "$line" | sed 's/</\&lt;/g; s/>/\&gt;/g')</div>"
    done
else
    echo "<div class='log-entry'>No se han encontrado registros aún.</div>"
fi

cat << EOM
            </div>
        </div>

        <!-- Firewall Rules -->
        <div class="card">
            <h3>Estado del Firewall (Chain PORTAL_AUTH)</h3>
            <pre>$(sudo iptables -L PORTAL_AUTH -n -v 2>/dev/null || echo "Chain PORTAL_AUTH no activa")</pre>
        </div>
    </div>
</body>
</html>
EOM
