#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
RUTA="$DIR/$PROJECTE/$DIR_SCRIPTS/client_srv_cli"

echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <title>Estat general del sistema</title>

<style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #0f172a, #000);
  color: #e5e7eb;
}

h1 {
  margin-bottom: 20px;
  color: #7dd3fc;
}

.section {
  background: rgba(15, 23, 42, 0.85);
  border-radius: 12px;
  padding: 16px 18px;
  margin-bottom: 18px;
  box-shadow: 0 0 20px rgba(34, 211, 238, 0.25);
}

.section h2 {
  margin-top: 0;
  margin-bottom: 10px;
  border-left: 5px solid #22d3ee;
  padding-left: 12px;
  color: #7dd3fc;
}

pre {
  background: #020617;
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
  color: #e5e7eb;
  font-size: 14px;
}

.ok { color: #4ade80; font-weight: 700; }
.err { color: #f87171; font-weight: 700; }
</style>
</head>
<body>

<h1>📡 Estat general del sistema</h1>
EOM

# ---------- WAN ----------
WAN_EST=$($RUTA ifwan estat 2>/dev/null)
echo "<div class='section'>"
echo "<h2>Interfície WAN</h2>"
echo "<pre>$WAN_EST</pre>"
echo "</div>"

# ---------- ENRUTAMENT ----------
ENR_EST=$($RUTA enrutar estat 2>/dev/null)
echo "<div class='section'>"
echo "<h2>Enrutament</h2>"
echo "<pre>$ENR_EST</pre>"
echo "</div>"

# ---------- BRIDGE ----------
BR_EST=$($RUTA bridge estat 2>/dev/null)
echo "<div class='section'>"
echo "<h2>Bridge</h2>"
echo "<pre>$BR_EST</pre>"
echo "</div>"

# ---------- TALLAFOCS ----------
TF_EST=$($RUTA tallafocs estat 2>/dev/null)
echo "<div class='section'>"
echo "<h2>Tallafocs</h2>"
echo "<pre>$TF_EST</pre>"
echo "</div>"

/bin/cat << EOM
</body>
</html>
EOM
