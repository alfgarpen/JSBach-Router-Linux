#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

# Carregar funcions DHCP mitjançant el wrapper privilegiat
DHCP_EXEC="$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli dhcp"

echo "Content-Type: text/html; charset=utf-8"
echo ""

urldecode() {
    local data
    if [ -n "$1" ]; then data="$1"; else data=$(cat); fi
    data="${data//+/ }"
    printf '%b' "${data//%/\\x}"
}

# Capturar arguments manualment per seguretat
comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p' | urldecode)
vlan=$(echo "$QUERY_STRING" | sed -n 's/^.*vlan=\([^&]*\).*$/\1/p' | urldecode)
range_ini=$(echo "$QUERY_STRING" | sed -n 's/^.*range_ini=\([^&]*\).*$/\1/p' | urldecode)
range_fi=$(echo "$QUERY_STRING" | sed -n 's/^.*range_fi=\([^&]*\).*$/\1/p' | urldecode)
lease=$(echo "$QUERY_STRING" | sed -n 's/^.*lease=\([^&]*\).*$/\1/p' | urldecode)
gw=$(echo "$QUERY_STRING" | sed -n 's/^.*gw=\([^&]*\).*$/\1/p' | urldecode)
dns=$(echo "$QUERY_STRING" | sed -n 's/^.*dns=\([^&]*\).*$/\1/p' | urldecode)

/bin/cat << EOM
<html>
<head>
<style>
body {
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  margin: 32px;
  background: #0f172a;
  color: #f1f5f9;
  line-height: 1.6;
}

h1 { color: #22d3ee; font-size: 1.8rem; margin-bottom: 24px; border-bottom: 2px solid #334155; padding-bottom: 12px; }
h2 { color: #94a3b8; font-size: 1.2rem; }

pre {
  background: #020617;
  color: #38bdf8;
  padding: 20px;
  border-radius: 12px;
  font-family: 'Cascadia Code', 'Fira Code', monospace;
  border: 1px solid #1e293b;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
  overflow-x: auto;
}

.msg-success { color: #4ade80; background: rgba(74, 222, 128, 0.1); padding: 12px; border-radius: 8px; border-left: 4px solid #4ade80; margin: 16px 0; }
.msg-error { color: #f87171; background: rgba(248, 113, 113, 0.1); padding: 12px; border-radius: 8px; border-left: 4px solid #f87171; margin: 16px 0; }
.status-badge { display: inline-block; padding: 4px 12px; border-radius: 999px; font-weight: bold; font-size: 0.8rem; text-transform: uppercase; }
.bg-on { background: #064e3b; color: #6ee7b7; }
.bg-off { background: #7f1d1d; color: #fca5a5; }

.vlan-card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
  transition: transform 0.2s;
}
.vlan-card:hover { transform: translateY(-4px); border-color: #22d3ee; }

input[type="text"] {
  background: #020617;
  color: #f1f5f9;
  border: 1px solid #334155;
  padding: 10px 14px;
  border-radius: 8px;
  margin: 8px 0;
  width: auto;
}
input[type="text"]:focus { outline: none; border-color: #22d3ee; }

button {
  background: linear-gradient(135deg, #0284c7, #06b6d4);
  color: #fff;
  border: none;
  padding: 12px 24px;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}
button:hover { filter: brightness(1.1); box-shadow: 0 4px 12px rgba(6, 182, 212, 0.4); }

.back-btn { display: inline-block; margin-top: 20px; color: #38bdf8; text-decoration: none; font-weight: 600; }
</style>
</head>
<body>
EOM

# Funció per comprovar el servidor de gestió
check_srv() {
    if ! timeout 0.5 nc -z 127.0.0.1 1234 > /dev/null 2>&1; then
        echo "<div class='msg-error'><strong>CRÍTIC:</strong> El servidor de gestió no respon. Si us plau, reinicia el servei <code>jsbach_srv</code> mitjançant la consola.</div>"
        return 1
    fi
    return 0
}

case "$comand" in
    estat)
        echo "<h1>Estat del Servei DHCP</h1>"
        if check_srv; then
            $DHCP_EXEC estat
        fi
        ;;

    iniciar)
        echo "<h1>Iniciant Servei...</h1>"
        if check_srv; then
            echo "<pre>"
            OUT=$($DHCP_EXEC iniciar)
            echo "$OUT"
            echo "</pre>"
            if echo "$OUT" | grep -q "Servei iniciat"; then
                echo "<p class='msg-success'>El servei s'ha iniciat correctament i s'ha habilitat per a l'arrencada.</p>"
            else
                echo "<p class='msg-error'>S'ha produït un error al intentar iniciar el servei.</p>"
            fi
        fi
        ;;

    reiniciar)
        echo "<h1>Reiniciant Servei...</h1>"
        if check_srv; then
            echo "<pre>"
            OUT=$($DHCP_EXEC reiniciar)
            echo "$OUT"
            echo "</pre>"
            if echo "$OUT" | grep -q "Servei reiniciat"; then
                echo "<p class='msg-success'>El servei s'ha reiniciat correctament.</p>"
            else
                echo "<p class='msg-error'>Error al reiniciar el servei.</p>"
            fi
        fi
        ;;

    aturar)
        echo "<h1>Aturant Servei...</h1>"
        if check_srv; then
            echo "<pre>"
            OUT=$($DHCP_EXEC aturar)
            echo "$OUT"
            echo "</pre>"
            if echo "$OUT" | grep -q "Servei aturat"; then
                echo "<p class='msg-success'>El servei s'ha aturat i s'ha deshabilitat de l'arrencada.</p>"
            else
                echo "<p class='msg-error'>No s'ha pogut aturar el servei.</p>"
            fi
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
            if check_srv; then
                INFO=$($DHCP_EXEC consultar "$IFACE")
                RANGE_INI=$(echo "$INFO" | awk '{print $1}')
                RANGE_FI=$(echo "$INFO" | awk '{print $2}')
                LEASE=$(echo "$INFO" | awk '{print $3}')
                GW=$(echo "$INFO" | awk '{print $4}')
                DNS=$(echo "$INFO" | awk '{print $5}')

                cat << EOK
                <form action="/cgi-bin/dhcp.cgi" method="GET">
                    <input type="hidden" name="comand" value="guardar">
                    <input type="hidden" name="vlan" value="$IFACE">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div>Inici Rang: <br><input type="text" name="range_ini" value="$RANGE_INI"></div>
                        <div>Final Rang: <br><input type="text" name="range_fi" value="$RANGE_FI"></div>
                        <div>Gateway: <br><input type="text" name="gw" value="$GW"></div>
                        <div>DNS: <br><input type="text" name="dns" value="$DNS"></div>
                        <div>Lease (ex: 12h): <br><input type="text" name="lease" value="$LEASE"></div>
                    </div>
                    <br>
                    <button type="submit">Aplicar Canvis</button>
                </form>
EOK
            fi
            echo "</div>"
        done
        ;;

    guardar)
        echo "<h1>Aplicant Canvis a $vlan...</h1>"
        if check_srv; then
            echo "<pre>"
            OUT=$($DHCP_EXEC configurar "$vlan" "$range_ini" "$range_fi" "$lease" "$gw" "$dns")
            echo "$OUT"
            echo "</pre>"
            if echo "$OUT" | grep -q "ERROR"; then
                echo "<p class='msg-error'>Error al aplicar la configuració: $(echo "$OUT" | grep "ERROR")</p>"
            else
                echo "<p class='msg-success'>Configuració aplicada amb èxit a la interfície $vlan.</p>"
            fi
        fi
        ;;

    restaurar)
        echo "<h1>Restaurant Còpia de Seguretat...</h1>"
        if check_srv; then
            echo "<pre>"
            OUT=$($DHCP_EXEC restaurar)
            echo "$OUT"
            echo "</pre>"
            if echo "$OUT" | grep -q "correctament"; then
                echo "<p class='msg-success'>Còpia de seguretat restaurada correctament.</p>"
            else
                echo "<p class='msg-error'>No s'ha trobat cap còpia de seguretat o ha fallat la restauració.</p>"
            fi
        fi
        ;;

    *)
        echo "<h1>Benvingut al Menú DHCP</h1>"
        echo "<p>Selecciona una operació del menú de l'esquerra per començar.</p>"
        ;;
esac

echo "</body></html>"
