#!/bin/bash

# Carreguem variables d'entorn
source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<html><head><title>Configuració DMZ</title>"
echo "<meta charset='utf-8'>"
echo "<style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\",
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
  margin-bottom: 20px;
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
  background: linear-gradient(135deg, #dc2626, #ef4444); /* Vermell per eliminar */
  color: #fff;
  border: none;
  padding: 8px 16px;
  margin-right: 6px;
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(220, 38, 38, 0.5);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 22px rgba(220, 38, 38, 0.8);
}

/* Botó verd per afegir */
.btn-add {
  background: linear-gradient(135deg, #16a34a, #4ade80);
  box-shadow: 0 4px 16px rgba(22, 163, 74, 0.5);
  color: #020617;
}

.btn-add:hover {
  box-shadow: 0 6px 22px rgba(22, 163, 74, 0.8);
}

</style>
"
echo "</head><body>"

# -------------------------------------------------------------------
# Obtenim la llista de serveis DMZ
# -------------------------------------------------------------------
DMZ_DATA="$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dmz configurar mostrar)"

echo "<h2>Serveis DMZ Configurats</h2>"

# Llegim totes les línies en un array
mapfile -t SERVEIS <<< "$DMZ_DATA"

if [ "${#SERVEIS[@]}" -eq 0 ] || [ -z "$DMZ_DATA" ]; then
    echo "<p>No hi ha serveis configurats actualment.</p>"
else
    echo "<table>"
    echo "<tr><th>Port</th><th>Protocol</th><th>IP Servidor (DMZ)</th><th>Accions</th></tr>"

    for line in "${SERVEIS[@]}"; do
        # Assumim format: PORT;PROTO;IP
        IFS=';' read -r port proto ipdmz _ <<< "$line"
        
        # Si la línia està buida, salta
        [ -z "$port" ] && continue

        echo "<tr>"
        echo "<td>$port</td>"
        echo "<td>$proto</td>"
        echo "<td>$ipdmz</td>"
        echo "<td>"
        # Botó eliminar
        echo "<button onclick=\"location.href='/cgi-bin/dmz-eliminar.cgi?port=$port&proto=$proto&ipdmz=$ipdmz'\">Eliminar</button>"
        echo "</td>"
        echo "</tr>"
    done
    echo "</table>"
fi

# -------------------------------------------------------------------
# Botó per afegir nou servei
# -------------------------------------------------------------------
echo "<br>"
echo "<button class='btn-add' onclick=\"location.href='/cgi-bin/dmz-nou-servei.cgi'\">Obrir nou servei</button>"

echo "</body></html>"
