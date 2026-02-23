#!/bin/bash

source /usr/local/JSBach/conf/variables.conf


echo "Content-type: text/html; charset=utf-8"
echo ""


int=$(echo "$QUERY_STRING" | sed -n 's/^.*int=\([^&]*\).*$/\1/p')

echo "<html><head><title>Modificar VLAN</title>"
echo "<meta charset='utf-8'>"
echo "<style>
/* === Base === */
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #020617, #000);
  color: #e5e7eb;
}

/* Títulos */
h2 {
  background: linear-gradient(90deg, #0f172a, #020617);
  padding: 12px 16px;
  border-left: 5px solid #22d3ee;
  border-radius: 8px;
  font-weight: 700;
  letter-spacing: 0.6px;
  color: #7dd3fc;
  box-shadow: 0 0 18px rgba(34, 211, 238, 0.25);
  margin-bottom: 22px;
}

/* Tablas */
table {
  border-collapse: collapse;
  margin-bottom: 20px;
  width: 70%;
  background: rgba(15, 23, 42, 0.9);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 0 22px rgba(0,0,0,0.6);
}

th, td {
  border: 1px solid rgba(148, 163, 184, 0.2);
  padding: 10px 12px;
  font-family: monospace;
  font-size: 14px;
  text-align: center;
}

th {
  background: rgba(2, 6, 23, 0.95);
  color: #38bdf8;
  font-weight: 600;
}

/* Inputs */
input[type="text"] {
  width: 95%;
  padding: 8px 10px;
  border-radius: 8px;
  border: 1px solid rgba(148, 163, 184, 0.3);
  background: #020617;
  color: #e5e7eb;
  font-family: monospace;
  box-shadow: inset 0 0 10px rgba(0,0,0,0.6);
  text-align: center;
}

input[type="text"]:focus {
  outline: none;
  border-color: #22d3ee;
  box-shadow: 0 0 12px rgba(34, 211, 238, 0.5);
}

/* Inputs numéricos VLAN */
input.vlan {
  width: 100px;
}

/* Botón */
button {
  background: linear-gradient(135deg, #0284c7, #22d3ee);
  color: #020617;
  border: none;
  padding: 10px 20px;
  margin-top: 10px;
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(34, 211, 238, 0.5);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 22px rgba(34, 211, 238, 0.8);
}
</style>
"
echo "</head><body>"

VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar bridge)"
linia_int=$(echo "$VLAN_DATA" | grep -E "^${int};")
VLAN_UNTAG=$(echo "$linia_int"|cut -d';' -f2)
if [[ -z "$VLAN_UNTAG" ]]; then
	   VLAN_UNTAG=0
fi
VLAN_TAG=$(echo "$linia_int"|cut -d';' -f3)
if [[ -z "$VLAN_TAG" ]]; then
	   VLAN_TAG=0
fi

echo "<h2>Modificar Tag-Untag</h2>"
echo "<form action='/cgi-bin/bridge-guardar-taguntag.cgi' method='get'>"
echo "<table>"
echo "<tr><th>Interfaç</th><th>Untag</th><th>Tag</th></tr>"
echo "<tr>"


echo "<td><input type='text' name='int' value='$int' style='width: 250px;' readonly></td>"   
echo "<td><input type='text' class='untag' name='untag' value='$VLAN_UNTAG'></td>"
echo "<td><input type='text' class='tag' name='tag' value='$VLAN_TAG'></td>"
echo "</tr>"
echo "</table>"
echo "<button type='submit'>Guardar</button>"
echo "</form>"

echo "</body></html>"

