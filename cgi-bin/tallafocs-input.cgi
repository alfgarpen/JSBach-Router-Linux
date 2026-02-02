#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="1; url=/cgi-bin/tallafocs-input-menu.cgi">
  <title>Aplicant política INPUT</title>

  <style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 0;
  min-height: 100vh;
  background: radial-gradient(circle at top, #020617, #000);
  color: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card {
  background: rgba(2, 6, 23, 0.9);
  padding: 24px 28px;
  border-radius: 14px;
  box-shadow: 0 0 28px rgba(56, 189, 248, 0.3);
  width: 540px;
}

h2 {
  margin: 0 0 12px 0;
  color: #7dd3fc;
  border-left: 5px solid #38bdf8;
  padding-left: 12px;
  letter-spacing: 0.6px;
}

pre {
  background: #020617;
  padding: 14px;
  border-radius: 8px;
  color: #a5f3fc;
  overflow-x: auto;
  font-size: 13px;
  box-shadow: inset 0 0 14px rgba(56, 189, 248, 0.2);
}

.loader {
  margin-top: 14px;
  font-size: 13px;
  color: #94a3b8;
}
  </style>
</head>
<body>

<div class="card">
  <h2>Aplicando reglas INPUT del router</h2>
EOM

##################################
# Leer parámetros GET
##################################
accio=$(echo "$QUERY_STRING" | sed -n 's/^.*accio=\([^&]*\).*$/\1/p')
id=$(echo "$QUERY_STRING" | sed -n 's/^.*id=\([^&]*\).*$/\1/p')

##################################
# Ejecutar tallafocs
##################################
echo "<pre>$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar "$accio" "$id")</pre>"

echo "<div class='loader'>Actualizando reglas INPUT…</div>"

/bin/cat << EOM
</div>

</body>
</html>
EOM
