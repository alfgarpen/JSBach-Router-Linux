#!/bin/bash

source /usr/local/JSBach/conf/variables.conf


echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <title>Gestió de Tallafocs</title>

<style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #0f172a, #000);
  color: #e5e7eb;
}

.container {
  max-width: 1000px;
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
  margin-bottom: 14px;
}

pre {
  background: rgba(15, 23, 42, 0.9);
  border-radius: 10px;
  padding: 16px;
  font-size: 14px;
  overflow-x: auto;
  box-shadow: inset 0 0 14px rgba(0,0,0,0.7);
  border: 1px solid rgba(34, 211, 238, 0.25);
}

button {
  background: linear-gradient(135deg, #0284c7, #22d3ee);
  color: #020617;
  border: none;
  padding: 8px 18px;
  margin-top: 18px;
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
  <h2>Resultat de la comanda del Tallafocs</h2>
EOM

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')


echo "<pre>$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs $comand) </pre><br>"


/bin/cat << EOM
</body>
</html>
EOM

