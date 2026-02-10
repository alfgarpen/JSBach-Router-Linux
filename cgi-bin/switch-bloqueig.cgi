#!/bin/bash

source /usr/local/JSBach/conf/variables.conf 2>/dev/null

# Get query string parameters
action=$(echo "$QUERY_STRING" | sed -n 's/^.*action=\([^&]*\).*$/\1/p')

echo "Content-Type:text/html;charset=utf-8"
echo ""

cat << EOM
<html>
<head>
<style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #0f172a, #000);
  color: #e5e7eb;
}

h2 {
  background: linear-gradient(90deg, #0f172a, #020617);
  padding: 12px 16px;
  border-left: 5px solid #22d3ee;
  border-radius: 8px;
  color: #7dd3fc;
  margin-bottom: 20px;
}

pre {
  background: #020617;
  color: #a5f3fc;
  padding: 18px 20px;
  border-radius: 14px;
  font-family: monospace;
  border: 1px solid rgba(148, 163, 184, 0.2);
}
</style>
</head>
<body>
EOM

if [ "$action" == "apply" ]; then
    echo "<h2>Aplicant Bloqueig de MACs</h2>"
elif [ "$action" == "remove" ]; then
    echo "<h2>Eliminant Bloqueig de MACs</h2>"
else
    echo "<h2>Acció desconeguda</h2>"
    echo "</body></html>"
    exit 0
fi

echo "<pre>"
if [ -x "$DIR/$PROJECTE/$DIR_SCRIPTS/switch" ]; then
    echo "$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/switch bloqueig "$action")"
else
    echo "Error: No s'ha trobat l'script del switch."
fi
echo "</pre>"
echo "<a href='/cgi-bin/switch-menu.cgi'>Tornar al menú</a>"
echo "</body></html>"
