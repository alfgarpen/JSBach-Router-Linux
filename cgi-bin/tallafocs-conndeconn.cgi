#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="1; url=/cgi-bin/tallafocs-configuracio.cgi">
  <title>Aplicant canvis</title>

  <style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 0;
  min-height: 100vh;
  background: radial-gradient(circle at top, #0f172a, #000);
  color: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card {
  background: rgba(15, 23, 42, 0.85);
  padding: 24px 28px;
  border-radius: 12px;
  box-shadow: 0 0 25px rgba(34, 211, 238, 0.25);
  width: 520px;
}

h2 {
  margin: 0 0 12px 0;
  color: #7dd3fc;
  border-left: 5px solid #22d3ee;
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
  box-shadow: inset 0 0 12px rgba(34, 211, 238, 0.15);
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
  <h2>Aplicant configuració del tallafocs</h2>
EOM

accio=$(echo "$QUERY_STRING" | sed -n 's/^.*accio=\([^&]*\).*$/\1/p')
id=$(echo "$QUERY_STRING" | sed -n 's/^.*id=\([^&]*\).*$/\1/p')

echo "<pre>$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar $accio $id)</pre>"
echo "<div class='loader'>Redirigint a configuració…</div>"

/bin/cat << EOM
</div>

</body>
</html>
EOM




