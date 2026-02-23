#!/bin/bash

source /usr/local/JSBach/conf/variables.conf


echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<html><head><title>Obrir nou servei</title>"
echo "<meta charset='utf-8'>"
echo "<style>
/* === Base === */
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #020617, #000);
  color: #e5e7eb;
}

/* Títulos */
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

/* Tablas */
table {
  border-collapse: collapse;
  margin-bottom: 20px;
  width: 70%;
  background: rgba(15, 23, 42, 0.9);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 0 22px rgba(0,0,0,0.6);
}

th, td {
  border: 1px solid rgba(148, 163, 184, 0.2);
  padding: 10px 12px;
  font-family: monospace;
  font-size: 14px;
}

th {
  background: rgba(2, 6, 23, 0.95);
  color: #38bdf8;
  text-align: left;
  font-weight: 600;
}

/* Inputs */
input[type=\"text\"] {
  width: 95%;
  padding: 8px 10px;
  border-radius: 8px;
  border: 1px solid rgba(148, 163, 184, 0.3);
  background: #020617;
  color: #e5e7eb;
  font-family: monospace;
  box-shadow: inset 0 0 10px rgba(0,0,0,0.6);
}

input[type=\"text\"]:focus {
  outline: none;
  border-color: #22d3ee;
  box-shadow: 0 0 12px rgba(34, 211, 238, 0.5);
}

/* Inputs IP específicos */
input.ipdmz {
  width: 200px;
}

/* Botón */
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
"
 
echo "</head><body>"

echo "<h2>Obrir nou servei</h2>"
echo "<form action='/cgi-bin/dmz-agregar.cgi' method='get'>"
echo "<table>"
echo "<tr><th>Port</th><th>Protocol</th><th>IP servidor</th></tr>"
echo "<tr>"
# port
echo "<td><input type='text' name='port' value='' style='width: 250px;'></td>"
# protocol
echo "<td><input type='text' name='proto' value='' ></td>"
# IP més amplis
echo "<td><input type='text' class='ipdmz' name='ipdmz' value=''></td>"
echo "</tr>"
echo "</table>"
echo "<button type='submit'>Obrir</button>"
echo "</form>"

echo "</body></html>"
