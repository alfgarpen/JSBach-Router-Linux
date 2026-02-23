#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
RUTA="$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli"

urldecode() {
    local data="${1//+/ }"      # Canvia + per espai
    printf '%b' "${data//%/\\x}" # Converteix %xx en caràcters
}


echo "Content-type: text/html; charset=utf-8"
echo ""


/bin/cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <title>Guardant VLAN</title>
  <meta http-equiv="refresh" content="2; url=/cgi-bin/bridge-configurar.cgi">

  <style>
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
  margin-bottom: 22px;
}

pre {
  background: rgba(15, 23, 42, 0.9);
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 0 18px rgba(0,0,0,0.5);
  color: #38bdf8;
  font-family: monospace;
  overflow-x: auto;
}

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

</head>
<body>
EOM

# Extreiem els valors del QUERY_STRING
nom=$(echo "$QUERY_STRING" | sed -n 's/^.*nom=\([^&]*\).*$/\1/p')
vid=$(echo "$QUERY_STRING" | sed -n 's/^.*vid=\([^&]*\).*$/\1/p')
ipmasc=$(echo "$QUERY_STRING" | sed -n 's/^.*ipmasc=\([^&]*\).*$/\1/p')
ippe=$(echo "$QUERY_STRING" | sed -n 's/^.*ippe=\([^&]*\).*$/\1/p')


# Decodifiquem els valors
nom=$(urldecode "$nom")
ipmasc=$(urldecode "$ipmasc")
ippe=$(urldecode "$ippe")


echo "<pre>"
echo "$($RUTA bridge configurar guardar vlan $nom $vid $ipmasc $ippe)"
echo "</pre>"
echo "<h2>Guardant la Configuració...</h2>"

/bin/cat << EOM
</body>
</html>
EOM

