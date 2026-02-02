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

/* Título / sección (por si luego añades h2) */
h2 {
  background: linear-gradient(90deg, #0f172a, #020617);
  padding: 10px 14px;
  border-left: 5px solid #22d3ee;
  border-radius: 6px;
  font-weight: 700;
  letter-spacing: 0.6px;
  color: #7dd3fc;
  box-shadow: 0 0 18px rgba(34, 211, 238, 0.25);
  margin-bottom: 18px;
}

/* Texto de salida del comando */
body {
  line-height: 1.7;
  font-size: 14px;
}

/* Si el comando devuelve tablas */
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

/* Estilo tipo consola si el output trae <pre> o <code> */
pre, code {
  background: #020617;
  color: #a5f3fc;
  padding: 12px 16px;
  border-radius: 10px;
  display: block;
  margin: 16px 0;
  box-shadow: inset 0 0 12px rgba(56, 189, 248, 0.15);
  overflow-x: auto;
}

/* Botones heredados (por si aparecen en el output) */
button {
  background: linear-gradient(135deg, #0284c7, #22d3ee);
  color: #020617;
  border: none;
  padding: 8px 16px;
  margin: 6px 4px;
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(34, 211, 238, 0.5);
}
</style>

</head>
<body>
EOM

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

echo "<h2>$comand</h2>" 
echo "<h3>$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli enrutar $comand) </h3><br>"


/bin/cat << EOM
</body>
</html>
EOM

