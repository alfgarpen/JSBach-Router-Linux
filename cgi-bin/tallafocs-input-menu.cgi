#!/bin/bash

# Source variables
source /usr/local/JSBach/conf/variables.conf

# Output HTTP headers
echo "Content-type: text/html; charset=utf-8"
echo ""

# Output HTML Header
/bin/cat << EOM
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Configuración de reglas INPUT por VLAN</title>
    <style>
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Ubuntu, Cantarell, Arial, sans-serif;
            margin: 0;
            min-height: 100vh;
            background: radial-gradient(circle at top, #0f172a, #000);
            color: #e5e7eb;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 20px;
        }

        h1 {
            color: #38bdf8;
            margin-bottom: 40px;
            font-weight: 700;
            text-align: center;
            text-shadow: 0 0 20px rgba(56, 189, 248, 0.3);
            font-size: 2rem;
            letter-spacing: -0.5px;
        }

        .table-container {
            width: 100%;
            max-width: 1200px;
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            border: 1px solid rgba(56, 189, 248, 0.1);
            overflow: hidden;
            box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.5);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }

        th {
            background: rgba(2, 6, 23, 0.8);
            color: #94a3b8;
            font-weight: 600;
            padding: 20px 24px;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 1px;
            border-bottom: 1px solid rgba(56, 189, 248, 0.1);
        }

        td {
            padding: 20px 24px;
            border-bottom: 1px solid rgba(56, 189, 248, 0.05);
            vertical-align: middle;
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:hover td {
            background: rgba(56, 189, 248, 0.02);
        }

        .vlan-name {
            font-weight: 600;
            color: #f8fafc;
            font-size: 1.1rem;
            margin-bottom: 4px;
        }
        
        .vlan-id {
            font-size: 0.85rem; 
            color: #64748b;
        }

        .actions {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }

        a.btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 10px 16px;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid transparent;
            cursor: pointer;
            text-align: center;
            white-space: nowrap;
            flex: 1;
        }

        /* Permitir todo: Green/Emerald */
        .btn-allow-all {
            background: rgba(16, 185, 129, 0.1);
            color: #34d399;
            border-color: rgba(16, 185, 129, 0.2);
        }
        .btn-allow-all:hover {
            background: rgba(16, 185, 129, 0.2);
            color: #6ee7b7;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
        }

        /* Bloquear web router: Orange/Amber */
        .btn-block-web {
            background: rgba(245, 158, 11, 0.1);
            color: #fbbf24;
            border-color: rgba(245, 158, 11, 0.2);
        }
        .btn-block-web:hover {
            background: rgba(245, 158, 11, 0.2);
            color: #fcd34d;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);
        }

        /* Ping y DHCP: Blue/Sky */
        .btn-minimal {
            background: rgba(14, 165, 233, 0.1);
            color: #38bdf8;
            border-color: rgba(14, 165, 233, 0.2);
        }
        .btn-minimal:hover {
            background: rgba(14, 165, 233, 0.2);
            color: #7dd3fc;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.2);
        }

        /* Bloquear todo: Red/Rose */
        .btn-block-all {
            background: rgba(225, 29, 72, 0.1);
            color: #fb7185;
            border-color: rgba(225, 29, 72, 0.2);
        }
        .btn-block-all:hover {
            background: rgba(225, 29, 72, 0.2);
            color: #fda4af;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(225, 29, 72, 0.3);
        }

    </style>
</head>
<body>

    <h1>Gestión de Firewall INPUT por VLAN</h1>

    <div class="table-container">
        <table>
            <thead>
                <tr>
                    <th style="width: 25%">VLAN</th>
                    <th style="width: 75%">Acciones de control</th>
                </tr>
            </thead>
            <tbody>
EOM

# Loop through bridge.conf to generate rows.
# Conf format: name;id;ip/mask;gateway;
if [ -f "$DIR/$PROJECTE/$DIR_CONF/$BRIDGE_CONF" ]; then
    # We use a while loop with file descriptor redirection to avoid subshells losing variables if we needed them, 
    # but here just catting is fine.
    
    grep -v '^#' "$DIR/$PROJECTE/$DIR_CONF/$BRIDGE_CONF" | while IFS=';' read -r nom vid ip gateway rest; do
        if [ ! -z "$nom" ] && [ ! -z "$vid" ]; then
            cat << ROW
                <tr>
                    <td>
                        <div class="vlan-name">$nom</div>
                        <div class="vlan-id">ID: $vid</div>
                    </td>
                    <td>
                        <div class="actions">
                            <a href="/cgi-bin/tallafocs-input.cgi?accio=input_allow_router&id=$vid" class="btn btn-allow-all" title="Permitir todo el tráfico al router">
                                Permitir todo
                            </a>
                            <a href="/cgi-bin/tallafocs-input.cgi?accio=input_block_router&id=$vid" class="btn btn-block-web" title="Bloquear acceso web (80/443)">
                                Bloquear Web
                            </a>
                            <a href="/cgi-bin/tallafocs-input.cgi?accio=input_minimal&id=$vid" class="btn btn-minimal" title="Permitir solo Ping y DHCP">
                                Solo Ping/DHCP
                            </a>
                            <a href="/cgi-bin/tallafocs-input.cgi?accio=input_drop_all&id=$vid" class="btn btn-block-all" title="Bloquear todo el tráfico">
                                Bloquear todo
                            </a>
                        </div>
                    </td>
                </tr>
ROW
        fi
    done
else
    echo "<tr><td colspan='2' style='text-align:center; padding: 30px; color: #94a3b8;'>Archiu de configuració no trobat.</td></tr>"
fi

cat << EOM
            </tbody>
        </table>
    </div>

</body>
</html>
EOM
