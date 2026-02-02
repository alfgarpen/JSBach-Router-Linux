#!/bin/bash

source /usr/local/JSBach/conf/variables.conf


echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <title>Hola món CGI</title>
 <style>
/* === Base === */
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #020617, #000);
  color: #e5e7eb;
}

/* Títulos (por si luego los usas) */
h2 {
  background: linear-gradient(90deg, #0f172a, #020617);
  padding: 12px 16px;
  border-left: 5px solid #22d3ee;
  border-radius: 8px;
  color: #7dd3fc;
  font-weight: 700;
  letter-spacing: 0.6px;
  box-shadow: 0 0 18px rgba(34, 211, 238, 0.25);
  margin-bottom: 18px;
}

/* Consola real */
pre {
  background: #020617;
  color: #a5f3fc;
  padding: 18px 20px;
  border-radius: 14px;
  font-family: monospace;
  font-size: 14px;
  line-height: 1.6;
  box-shadow:
    inset 0 0 18px rgba(56, 189, 248, 0.15),
    0 0 24px rgba(0,0,0,0.7);
  overflow-x: auto;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

/* Scrollbar discreta (si el navegador lo soporta) */
pre::-webkit-scrollbar {
  height: 8px;
}

pre::-webkit-scrollbar-thumb {
  background: rgba(56, 189, 248, 0.4);
  border-radius: 6px;
}

/* Tablas por si el comando devuelve alguna */
table {
  border-collapse: collapse;
  margin: 20px auto;
  width: 95%;
  background: rgba(15, 23, 42, 0.9);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 0 22px rgba(0,0,0,0.6);
}

td, th {
  border: 1px solid rgba(148, 163, 184, 0.2);
  padding: 10px 14px;
  text-align: left;
  font-family: monospace;
}

th {
  background: rgba(2, 6, 23, 0.95);
  color: #38bdf8;
  font-weight: 600;
}
</style>

</head>
<body>
EOM

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

echo "<pre>"
echo "$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge "$comand")"
echo "</pre>"



/bin/cat << EOM
</body>
</html>
EOM

