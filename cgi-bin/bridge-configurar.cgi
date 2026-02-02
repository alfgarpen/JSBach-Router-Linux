#!/bin/bash

source /usr/local/JSBach/conf/variables.conf


echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<html><head><title>Gestió de VLANs</title>"
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
  width: 80%;
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
  padding: 8px 16px;
  margin-right: 6px;
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

button:last-child {
  background: linear-gradient(135deg, #16a34a, #4ade80);
  box-shadow: 0 4px 16px rgba(22, 163, 74, 0.5);
}

button:last-child:hover {
  box-shadow: 0 6px 22px rgba(22, 163, 74, 0.8);
}
</style>
"
echo "</head><body>"

# -------------------------------------------------------------------
# Aquí posem la comanda o fitxer que genera les VLANs
# -------------------------------------------------------------------
VLAN_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge configurar mostrar vlan)"


# Llegim totes les línies en un array
mapfile -t VLANS <<< "$VLAN_DATA"

# Comprovem que tinguem almenys dues línies
if [ "${#VLANS[@]}" -lt 2 ]; then
    echo "<p><b>Error:</b> no hi ha prou VLANs definides.</p>"
    echo "</body></html>"
    exit 0
fi


mostrar_vlan_tabla() {
  local nom_buscat="$1"

  for line in "${VLANS[@]}"; do
    IFS=';' read -r nom vid subnet gw _ <<< "$line"
    if [ "$nom" = "$nom_buscat" ]; then
      echo "<table>"
      echo "<tr><th>Nom</th><th>VID</th><th>Subxarxa</th><th>Gateway</th><th>Accions</th></tr>"
      echo "<tr><td>$nom</td><td>$vid</td><td>$subnet</td><td>$gw</td>"
      echo "<td><button onclick=\"location.href='/cgi-bin/bridge-modificar.cgi?vid=$vid'\">Modificar</button></td></tr>"
      echo "</table>"
      return
    fi
  done
}

# -------------------------------------------------------------------
# VLAN ADMINISTRACIÓ (primera línia)
# -------------------------------------------------------------------
echo "<h2>VLAN ADMINISTRACIÓ</h2>"
mostrar_vlan_tabla "$VLAN_ADMIN_NAME"


# -------------------------------------------------------------------
# VLAN DMZ (segona línia)
# -------------------------------------------------------------------
echo "<h2>VLAN DMZ</h2>"
mostrar_vlan_tabla "$VLAN_DMZ_NAME"

# -------------------------------------------------------------------
# Altres VLANS (de la tercera en avant)
# -------------------------------------------------------------------
echo "<h2>VLANS</h2>"
echo "<table>"
echo "<tr><th>Nom</th><th>VID</th><th>Subxarxa</th><th>Gateway</th><th>Accions</th></tr>"

for line in "${VLANS[@]}"; do
  IFS=';' read -r nom vid subnet gw _ <<< "$line"

  # Saltamos Admin y DMZ
  [ "$nom" = "$VLAN_ADMIN_NAME" ] && continue
  [ "$nom" = "$VLAN_DMZ_NAME" ] && continue

  echo "<tr><td>$nom</td><td>$vid</td><td>$subnet</td><td>$gw</td>"
  echo "<td>"
  echo "<button onclick=\"location.href='/cgi-bin/bridge-modificar.cgi?vid=$vid'\">Modificar</button>"
  echo "<button onclick=\"location.href='/cgi-bin/bridge-esborrar.cgi?vid=$vid'\">Esborrar</button>"
  echo "</td></tr>"
done

echo "</table>"
# -------------------------------------------------------------------
# Botó final
# -------------------------------------------------------------------
echo "<button onclick=\"location.href='/cgi-bin/bridge-nova-vlan.cgi'\">Crear nova VLAN</button>"

echo "</body></html>"
