#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
source /usr/local/JSBach/conf/portal.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

# Procesar acciones (ej. desconectar usuario)
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
    echo "Location: portal-estat.cgi"
    echo ""
    exit 0
fi

cat << EOM
<html>
<head>
<style>
body { font-family: sans-serif; background: #0f172a; color: #e5e7eb; padding: 20px; }
h2 { border-left: 5px solid #38bdf8; padding-left: 10px; color: #7dd3fc; }
.card { background: rgba(30, 41, 59, 0.7); border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
.status-enabled { color: #4ade80; font-weight: bold; }
.status-disabled { color: #f87171; font-weight: bold; }
table { width: 100%; border-collapse: collapse; margin-top: 20px; }
th, td { padding: 12px; border-bottom: 1px solid #334155; text-align: left; }
th { color: #94a3b8; }
.btn { padding: 6px 12px; border-radius: 6px; cursor: pointer; border: none; font-size: 0.9em; }
.btn-danger { background: #ef4444; color: white; }
</style>
</head>
<body>
    <h2>Estado del Portal Cautivo</h2>

    <div class="card">
        <p>Estado General: $( [ "$ENABLED" -eq 1 ] && echo "<span class='status-enabled'>ACTIVO</span>" || echo "<span class='status-disabled'>INACTIVO</span>" )</p>
        <p>VLAN Asociada: <b>$VLAN_VID</b></p>
        <p>Sesiones Activas: <b>$(ls /usr/local/JSBach/run/portal/sessions | wc -l)</b></p>
    </div>

    <h3>Sesiones Activas</h3>
    <div class="card">
        <table>
            <thead>
                <tr>
                    <th>Usuario</th>
                    <th>IP</th>
                    <th>MAC</th>
                    <th>Conectado desde</th>
                    <th>Última actividad</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
EOM

for session_file in /usr/local/JSBach/run/portal/sessions/*; do
    [ -e "$session_file" ] || continue
    source "$session_file"
    start_fmt=$(date -d "@$START" "+%H:%M:%S")
    last_fmt=$(date -d "@$LAST" "+%H:%M:%S")
    echo "<tr>
            <td>$USER</td>
            <td>$IP</td>
            <td>$MAC</td>
            <td>$start_fmt</td>
            <td>$last_fmt</td>
            <td><button class='btn btn-danger' onclick=\"location.href='portal-estat.cgi?action=kill&ip=$IP&mac=$MAC'\">Desconectar</button></td>
          </tr>"
done

cat << EOM
            </tbody>
        </table>
    </div>
</body>
</html>
EOM
