#!/bin/bash

source /usr/local/JSBach/conf/variables.conf


echo "Content-type: text/html; charset=utf-8"
echo ""


QUERY_STRING=${QUERY_STRING:-$1}  
VID=$(echo "$QUERY_STRING" | sed -n 's/.*vid=\([0-9]*\).*/\1/p')

echo "<html><head><title>Esborrar  VLAN</title>"
echo "<meta charset='utf-8'>"
echo "<style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #020617, #000);
  color: #e5e7eb;
}

h2 {
  background: linear-gradient(90deg, #0f172a, #020617);
  padding: 12px 16px;
  border-left: 5px solid #ef4444; /* rojo para alerta */
  border-radius: 8px;
  font-weight: 700;
  letter-spacing: 0.6px;
  color: #fca5a5;
  box-shadow: 0 0 18px rgba(239, 68, 68, 0.25);
  margin-bottom: 22px;
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

input {
  width: 95%;
  padding: 6px;
  font-size: 14px;
  background: rgba(15, 23, 42, 0.7);
  color: #38bdf8;
  border: 1px solid #22d3ee;
  border-radius: 4px;
}

input[readonly] {
  background: rgba(15, 23, 42, 0.5);
  color: #a1a1aa;
  border: 1px solid #6b7280;
}

button {
  background: linear-gradient(135deg, #ef4444, #f87171);
  color: #020617;
  border: none;
  padding: 10px 20px;
  margin-top: 10px;
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(239, 68, 68, 0.5);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 22px rgba(239, 68, 68, 0.8);
}
</style>
"
echo "</head><body>"

VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar vlan)"
mapfile -t VLANS <<< "$VLAN_DATA"

FOUND_LINE=""
for line in "${VLANS[@]}"; do
    IFS=';' read -r nom vid subnet gw _ <<< "$line"
    if [ "$vid" == "$VID" ]; then
        FOUND_LINE="$line"
        break
    fi
done

if [ -z "$FOUND_LINE" ]; then
    echo "<p><b>Error:</b> No s'ha trobat cap VLAN amb VID = $VID</p>"
    echo "</body></html>"
    exit 0
fi

IFS=';' read -r nom vid subnet gw _ <<< "$FOUND_LINE"

echo "<h2>Esborrar VLAN</h2>"
echo "<form action='/cgi-bin/bridge-aplicar-esborrar.cgi' method='get'>"
echo "<table>"
echo "<tr><th>Nom</th><th>VID</th><th>IP/Subxarxa</th><th>IP/PE</th></tr>"
echo "<tr>"
# Nom ara també més ample
echo "<td><input type='text' name='nom' value='$nom' style='width: 250px;' readonly></td>"
# VID només lectura
echo "<td><input type='text' name='vid' value='$vid' readonly></td>"
# Camps IP més amplis
echo "<td><input type='text' class='ip' name='ipmasc' value='$subnet' readonly></td>"
echo "<td><input type='text' class='ip' name='ippe' value='$gw' readonly></td>"
echo "</tr>"
echo "</table>"
echo "<button type='submit'>Esborrar</button>"
echo "</form>"

echo "</body></html>"

