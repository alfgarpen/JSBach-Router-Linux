#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

#Vull una pagina cgi amb bash per apache2 per linux que... primera seccio dos radius option, la #primera opcio "dhcp" i la segona "manual" cas de polsar algun dels dos, que per metode get es pase #mode=[dhcp o manual] Segona secció "Interfaç" Amb la funció: Interfaces_Ethernet() { for iface in #$(ip -o link show | awk -F': ' '{print $2}'); do if [[ "$iface" != "lo" ]]; then if ! iw dev 2>/#dev/null | grep -q "$iface"; then echo "$iface" fi fi done } amb la llista que me torne, crea una #llista de radius option i la que siga seleccionada torne per GET int="el nome de la targeta" I #tercera seccio: Estarà oculta i cas de seleccionar mode manual en la primera seccio, mostrar #quatre inptus de text, el primer de no ip i torna per metode get ip="la ip introduida", el segon #de nom mascara tornarà per get masc="la mascara introduida", el tercer de nom porta d'enllaç i #torna per GET pe="la ip introduida" i el darrer de nom dns i torna per get dns=" la ip introduida" #Acabarem amb un boto guardar que al polsar enllace amb la paguina guardar-ifwan.cgi

echo "Content-type: text/html"
echo ""

# --- Funció per obtenir interfícies Ethernet (sense lo ni wifi) ---
Interfaces_Ethernet() {
    for iface in $(ip -o link show | awk -F': ' '{print $2}'); do
        if [[ "$iface" != "lo" ]]; then
            if ! iw dev 2>/dev/null | grep -qw "$iface"; then
                echo "$iface"
            fi
        fi
    done
}

CONFIGURACIO=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli ifwan configurar mostrar)
conf_mode=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f1 )
conf_int=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f2 )
if [[ "$conf_mode" == "manual" ]] then
	conf_ip=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f3 )
	conf_masc=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f4 )
	conf_pe=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' '  -f5 )
	conf_dns=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' ' -f6 )
fi

# --- Inici HTML ---
cat <<'EOF'
<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<title>Configuració de la WAN</title>
<style>
/* === Base === */
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #020617, #000);
  color: #e5e7eb;
}

/* Título */
h2 {
  background: linear-gradient(90deg, #0f172a, #020617);
  padding: 12px 16px;
  border-left: 5px solid #22d3ee;
  border-radius: 8px;
  color: #7dd3fc;
  font-weight: 700;
  letter-spacing: 0.6px;
  box-shadow: 0 0 18px rgba(34, 211, 238, 0.25);
  margin-bottom: 24px;
}

/* Fieldsets como tarjetas */
fieldset {
  border: 1px solid rgba(148, 163, 184, 0.25);
  border-radius: 14px;
  padding: 16px 18px;
  margin-bottom: 22px;
  background: rgba(15, 23, 42, 0.85);
  box-shadow: 0 0 20px rgba(0,0,0,0.6);
}

legend {
  padding: 0 10px;
  font-weight: 700;
  color: #38bdf8;
  letter-spacing: 0.4px;
}

/* Radios */
input[type="radio"] {
  accent-color: #22d3ee;
  margin-right: 8px;
}

label {
  font-weight: 500;
  cursor: pointer;
}

/* Inputs text */
input[type="text"] {
  width: 280px;
  padding: 8px 10px;
  border-radius: 8px;
  border: 1px solid rgba(148, 163, 184, 0.3);
  background: #020617;
  color: #e5e7eb;
  font-family: monospace;
  box-shadow: inset 0 0 8px rgba(0,0,0,0.6);
}

input[type="text"]:focus {
  outline: none;
  border-color: #22d3ee;
  box-shadow: 0 0 10px rgba(34, 211, 238, 0.5);
}

/* Botón guardar */
input[type="submit"] {
  background: linear-gradient(135deg, #0284c7, #22d3ee);
  color: #020617;
  border: none;
  padding: 12px 26px;
  border-radius: 999px;
  font-weight: 800;
  letter-spacing: 0.6px;
  cursor: pointer;
  box-shadow: 0 4px 18px rgba(34, 211, 238, 0.6);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

input[type="submit"]:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 26px rgba(34, 211, 238, 0.9);
}

input[type="submit"]:active {
  transform: translateY(0);
  box-shadow: 0 3px 12px rgba(34, 211, 238, 0.4);
}

/* Sección manual (cuando aparece) */
#manual-section {
  animation: fadeIn 0.25s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-6px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>

<script>
function toggleManual() {
  const modeManual = document.getElementById("manual").checked;
  const manualSection = document.getElementById("manual-section");
  manualSection.style.display = modeManual ? "block" : "none";
}

  // Quan la pàgina es carrega, comprova l'estat i actualitza la visibilitat
  window.addEventListener("DOMContentLoaded", toggleManual);
  
</script>
</head>
<body>
<h2>Configuració de la interfície WAN</h2>

<form action="/cgi-bin/ifwan-guardar.cgi" method="get">
EOF

# --- SECCIÓ 1: MODE (DHCP o MANUAL) ---
cat <<'EOF'
<fieldset>
  <legend>Mode de configuració</legend>
EOF
	dhcp_check=""
	manual_check=""
	if [[ "$conf_mode" == "dhcp" ]] then
  		dhcp_check="checked"
	else
		manual_check="checked"
	fi
	
  echo '<input type="radio" id="dhcp" name="mode" value="dhcp" onclick="toggleManual()" '$dhcp_check'>'
cat <<'EOF' 
  <label for="dhcp">DHCP</label><br>
EOF
   echo '<input type="radio" id="manual" name="mode" value="manual" onclick="toggleManual()" '$manual_check'>'
cat <<'EOF'

  <label for="manual">Manual</label>
</fieldset>
EOF

# --- SECCIÓ 2: INTERFÍCIES ---
echo '<fieldset>'
echo '  <legend>Interfície</legend>'

for iface in $(Interfaces_Ethernet); do
    if [[ "$iface" == "$conf_int" ]] then 
    	echo "  <input type='radio' name='int' id='$iface' value='$iface' checked>"
    else
    	echo "  <input type='radio' name='int' id='$iface' value='$iface' >"
    fi
    echo "  <label for='$iface'>$iface</label><br>"
done


echo '</fieldset>'

# --- SECCIÓ 3: CONFIGURACIÓ MANUAL (OCULTA PER DEFECTE) ---
cat <<'EOF'
<fieldset id="manual-section" class="hidden">
  <legend>Configuració manual</legend>
  <label>IP:</label><br>
EOF
  echo '<input type="text" name="ip" value='$conf_ip'><br><br>'
cat <<'EOF'

  <label>Màscara:</label><br>
EOF
  echo ' <input type="text" name="masc" value='$conf_masc'><br><br>'
cat <<'EOF'

  <label>Porta d'enllaç:</label><br>
EOF
  echo ' <input type="text" name="pe" value='$conf_pe'><br><br>'
cat <<'EOF'

  <label>DNS:</label><br>
EOF
  echo ' <input type="text" name="dns" value='$conf_dns'><br><br>'
cat <<'EOF'

</fieldset>

<input type="submit" value="Guardar">
</form>
</body>
</html>
EOF

