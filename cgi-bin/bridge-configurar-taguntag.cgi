#!/bin/bash


source /usr/local/JSBach/conf/variables.conf
source $DIR/$PROJECTE/$DIR_CONF/$CONF_IFWAN

Interfaces_Ethernet() {
    for iface in $(ip -o link show | awk -F': ' '{print $2}'); do
        if [[ "$iface" != "lo" ]] && [[ "$iface" != "$IFW_IFWAN" ]] && [[ $iface != br0* ]]; then
            if ! iw dev 2>/dev/null | grep -qw "$iface"; then
                echo "$iface"
            fi
        fi
    done
}


echo "Content-type: text/html; charset=utf-8"
echo ""

VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar bridge)"

/bin/cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <title>Hola món CGI</title>
EOM
echo "<style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #0f172a, #000);
  color: #e5e7eb;
}

h2 {
  background: linear-gradient(90deg, #0f172a, #020617);
  padding: 12px 16px;
  border-left: 5px solid #22d3ee;
  border-radius: 8px;
  font-weight: 700;
  letter-spacing: 0.6px;
  color: #7dd3fc;
  box-shadow: 0 0 18px rgba(34, 211, 238, 0.25);
  margin-bottom: 12px;
}

table {
  border-collapse: collapse;
  margin-bottom: 20px;
  width: 60%;
  background: rgba(15, 23, 42, 0.85);
  border-radius: 8px;
  overflow: hidden;
}

td, th {
  border: 1px solid #999;
  padding: 6px 10px;
  text-align: left;
  color: #e5e7eb;
}

th {
  background: rgba(34, 211, 238, 0.15);
}

button {
  background: linear-gradient(135deg, #0284c7, #22d3ee);
  color: #020617;
  border: none;
  padding: 6px 14px;
  margin: 0 4px;
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(34, 211, 238, 0.5);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(34, 211, 238, 0.8);
}
</style>
"
echo "</head><body>"


echo "<h2>Configuració Tag-Untag</h2>"

echo "<table>"
echo "<tr><th>Interfaç</th><th>UNTAG</th><th>TAG</th><th></th></tr>"
for iface in $(Interfaces_Ethernet); do
	echo "<tr><td>$iface</td>"
	linia_int=$(echo "$VLAN_DATA" | grep -E "^${iface};")
	VLAN_UNTAG=$(echo "$linia_int"|cut -d';' -f2)
	if [[ -z "$VLAN_UNTAG" ]]; then
	    echo "<td>0</td>"
	else
	    echo "<td>$VLAN_UNTAG</td>"
	fi
	VLAN_TAG=$(echo "$linia_int"|cut -d';' -f3)
	if [[ -z "$VLAN_TAG" ]]; then
	    echo "<td>0</td>"
	else
	    echo "<td>$VLAN_TAG</td>"
	fi
	echo "<td><button onclick=\"location.href='/cgi-bin/bridge-modificar-taguntag.cgi?int=$iface'\">Modificar</button></td></tr>"
done
echo "</table>"

/bin/cat << EOM
</body>
</html>
EOM



