#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

# Carregar funcions DHCP
DHCP_SCRIPT="$DIR/$PROJECTE/$DIR_SCRIPTS/dhcp"

echo "Content-Type: text/html; charset=utf-8"
echo ""

# Capturar arguments
QUERY_STRING_PROCESSED=$(echo "$QUERY_STRING" | sed 's/&/ /g')
for ATTR in $QUERY_STRING_PROCESSED; do
    export "$ATTR"
done

/bin/cat << EOM
<html>
<head>
<style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #0f172a, #000);
  color: #e5e7eb;
}

h1, h2, h3 { color: #7dd3fc; }

pre {
  background: #020617;
  color: #a5f3fc;
  padding: 18px 20px;
  border-radius: 14px;
  font-family: monospace;
  border: 1px solid rgba(148, 163, 184, 0.2);
  white-space: pre-wrap;
}

.vlan-card {
  background: rgba(15, 23, 42, 0.85);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 20px;
}

input[type="text"] {
  background: #020617;
  color: #e5e7eb;
  border: 1px solid #334155;
  padding: 8px 12px;
  border-radius: 6px;
  margin: 4px;
}

button {
  background: linear-gradient(135deg, #0284c7, #22d3ee);
  color: #020617;
  border: none;
  padding: 8px 16px;
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
}

.msg-success { color: #4ade80; font-weight: bold; }
.msg-error { color: #f87171; font-weight: bold; }
</style>
</head>
<body>
EOM

case "$comand" in
    estat)
        echo "<h1>Estat del Servei DHCP</h1>"
        echo "<h2>dnsmasq status:</h2>"
        echo "<pre>"
        systemctl status dnsmasq | head -n 10
        echo "</pre>"
        echo "<h2>Habilitat al l'arrencada:</h2>"
        echo "<pre>"
        systemctl is-enabled dnsmasq
        echo "</pre>"
        ;;

    iniciar)
        echo "<h1>Iniciant Servei...</h1>"
        if bash "$DHCP_SCRIPT" iniciar; then
            echo "<p class='msg-success'>Servei iniciat correctament.</p>"
            systemctl enable dnsmasq > /dev/null 2>&1
        else
            echo "<p class='msg-error'>Error al iniciar el servei.</p>"
        fi
        ;;

    aturar)
        echo "<h1>Aturant Servei...</h1>"
        if bash "$DHCP_SCRIPT" aturar; then
            echo "<p class='msg-success'>Servei aturat correctament.</p>"
            systemctl disable dnsmasq > /dev/null 2>&1
        else
            echo "<p class='msg-error'>Error al aturar el servei.</p>"
        fi
        ;;

    configuracio)
        echo "<h1>Configuració per VLAN</h1>"
        # Detectar interfaces br0.*
        INTERFACES=$(ip link show | grep -o 'br0\.[0-9]\+' | sort -u)
        
        for IFACE in $INTERFACES; do
            echo "<div class='vlan-card'>"
            echo "<h3>VLAN: $IFACE</h3>"
            
            # Llegir valors actuals
            INFO=$(bash "$DHCP_SCRIPT" consultar "$IFACE")
            RANGE_INI=$(echo "$INFO" | awk '{print $1}')
            RANGE_FI=$(echo "$INFO" | awk '{print $2}')
            LEASE=$(echo "$INFO" | awk '{print $3}')
            GW=$(echo "$INFO" | awk '{print $4}')
            DNS=$(echo "$INFO" | awk '{print $5}')

            cat << EOK
            <form action="/cgi-bin/dhcp.cgi" method="GET">
                <input type="hidden" name="comand" value="guardar">
                <input type="hidden" name="vlan" value="$IFACE">
                Range Start: <input type="text" name="range_ini" value="$RANGE_INI" size="15">
                Range End: <input type="text" name="range_fi" value="$RANGE_FI" size="15"><br>
                Lease: <input type="text" name="lease" value="$LEASE" size="5">
                Gateway: <input type="text" name="gw" value="$GW" size="15">
                DNS: <input type="text" name="dns" value="$DNS" size="15"><br><br>
                <button type="submit">Aplicar Canvis</button>
            </form>
EOK
            echo "</div>"
        done
        ;;

    guardar)
        echo "<h1>Aplicant Canvis a $vlan...</h1>"
        # Aquí vlan, range_ini, range_fi, lease, gw, dns venen del GET
        if bash "$DHCP_SCRIPT" configurar "$vlan" "$range_ini" "$range_fi" "$lease" "$gw" "$dns"; then
            echo "<p class='msg-success'>Configuració aplicada amb èxit.</p>"
        else
            echo "<p class='msg-error'>Error al aplicar la configuració. Revisa la sintaxi o els valors.</p>"
        fi
        ;;

    restaurar)
        echo "<h1>Restaurant Còpia de Seguretat...</h1>"
        if bash "$DHCP_SCRIPT" restaurar; then
            echo "<p class='msg-success'>Configuració restaurada correctament.</p>"
        else
            echo "<p class='msg-error'>No s'ha pogut restaurar el backup.</p>"
        fi
        ;;

    *)
        echo "<h1>Benvingut al Menú DHCP</h1>"
        echo "<p>Selecciona una operació del menú de l'esquerra.</p>"
        ;;
esac

echo "</body></html>"
