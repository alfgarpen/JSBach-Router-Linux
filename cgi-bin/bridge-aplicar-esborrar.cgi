#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
RUTA="$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli"

urldecode() {
    local data="${1//+/ }"
    printf '%b' "${data//%/\\x}"
}

echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <title>Esborrar VLAN</title>

<style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #0f172a, #000);
  color: #e5e7eb;
}

.container {
  max-width: 900px;
  margin: auto;
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

.info {
  margin-bottom: 14px;
  font-size: 14px;
  color: #cbd5f5;
}

.info span {
  color: #22d3ee;
  font-weight: 700;
}

pre {
  background: rgba(15, 23, 42, 0.85);
  border-radius: 8px;
  padding: 14px;
  font-size: 14px;
  overflow-x: auto;
  box-shadow: inset 0 0 12px rgba(0,0,0,0.6);
}

button {
  background: linear-gradient(135deg, #0284c7, #22d3ee);
  color: #020617;
  border: none;
  padding: 8px 16px;
  margin-top: 16px;
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

</head>
<body>

<div class="container">
  <h2>Resultat de l’eliminació de VLAN</h2>
EOM

# Extreiem els valors del QUERY_STRING
nom=$(echo "$QUERY_STRING" | sed -n 's/^.*nom=\([^&]*\).*$/\1/p')
vid=$(echo "$QUERY_STRING" | sed -n 's/^.*vid=\([^&]*\).*$/\1/p')
ipmasc=$(echo "$QUERY_STRING" | sed -n 's/^.*ipmasc=\([^&]*\).*$/\1/p')
ippe=$(echo "$QUERY_STRING" | sed -n 's/^.*ippe=\([^&]*\).*$/\1/p')

# Decodifiquem
nom=$(urldecode "$nom")
ipmasc=$(urldecode "$ipmasc")
ippe=$(urldecode "$ippe")

echo "<div class='info'>S’ha eliminat la VLAN amb VID <span>$vid</span></div>"

echo "<pre>"
echo "$($RUTA bridge configurar esborrar vlan $vid)"
echo "</pre>"

echo "<button onclick=\"location.href='/cgi-bin/bridge-configurar.cgi'\">Tornar al gestor de VLANs</button>"

/bin/cat << EOM
</div>
</body>
</html>
EOM
