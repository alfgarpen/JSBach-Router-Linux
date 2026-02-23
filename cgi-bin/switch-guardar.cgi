#!/bin/bash

# Source variables
source /usr/local/JSBach/conf/variables.conf 2>/dev/null

# Parse query string
nom=$(echo "$QUERY_STRING" | sed -n 's/^.*nom=\([^&]*\).*$/\1/p' | sed "s/%20/ /g")
ip=$(echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
user=$(echo "$QUERY_STRING" | sed -n 's/^.*user=\([^&]*\).*$/\1/p')
pass=$(echo "$QUERY_STRING" | sed -n 's/^.*pass=\([^&]*\).*$/\1/p')

echo "Content-Type:text/html;charset=utf-8"
echo ""

cat << EOM
<html>
<head>
<meta http-equiv="refresh" content="3; url=/cgi-bin/switch-menu.cgi">
<style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #0f172a, #000);
  color: #e5e7eb;
  text-align: center;
}
.message {
  padding: 20px;
  border-radius: 8px;
  background: rgba(15, 23, 42, 0.9);
  display: inline-block;
  margin-top: 50px;
}
.error { color: #f87171; }
.success { color: #4ade80; }
</style>
</head>
<body>
<div class="message">
EOM

if [ -x "$DIR/$PROJECTE/$DIR_SCRIPTS/switch" ]; then
    result=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/switch guardar "$nom" "$ip" "$user" "$pass")
    
    # Check if result contains "OK"
    if [[ "$result" == *"OK"* ]]; then
         echo "<h3 class='success'>Switch afegit correctament.</h3>"
         echo "<p>Redirigint al menú...</p>"
    else
         echo "<h3 class='error'>$result</h3>"
    fi
else
    echo "<h3 class='error'>Error: No s'ha trobat l'script del switch.</h3>"
fi

echo "</div></body></html>"
