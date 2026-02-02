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

/* Título principal */
h2 {
  background: linear-gradient(90deg, #0f172a, #020617);
  padding: 12px 16px;
  border-left: 5px solid #22d3ee;
  border-radius: 8px;
  color: #7dd3fc;
  font-weight: 800;
  letter-spacing: 0.6px;
  box-shadow: 0 0 18px rgba(34, 211, 238, 0.25);
  margin-bottom: 22px;
}

/* Texto de resumen de parámetros */
body {
  font-size: 14px;
  line-height: 1.7;
}

/* Salida del comando (modo consola elegante) */
pre, code {
  background: #020617;
  color: #a5f3fc;
  padding: 12px 16px;
  border-radius: 10px;
  display: block;
  margin: 16px 0;
  box-shadow: inset 0 0 12px rgba(56, 189, 248, 0.15);
  font-family: monospace;
}

/* Tablas (por si el backend devuelve alguna) */
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

/* Botones (por si aparecen en la salida) */
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

echo "<h2>Guardant la configuració</h2>"

mode=$(echo "$QUERY_STRING" | sed -n 's/^.*mode=\([^&]*\).*$/\1/p')
int=$(echo "$QUERY_STRING" | sed -n 's/^.*int=\([^&]*\).*$/\1/p')
if [[ "$mode" == "manual" ]] then
	ip=$(echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
	masc=$(echo "$QUERY_STRING" | sed -n 's/^.*masc=\([^&]*\).*$/\1/p')
	pe=$(echo "$QUERY_STRING" | sed -n 's/^.*pe=\([^&]*\).*$/\1/p')
	dns=$(echo "$QUERY_STRING" | sed -n 's/^.*dns=\([^&]*\).*$/\1/p')
fi

if [[ ! -z $ip ]] then
	ipmas=$ip/$masc
fi

ordre="ifwan configurar $mode $int $ipmas $pe $dns"

echo "<br>"
echo "$mode $int $ipmas $pe $dns"
echo "<br>"

echo "$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli $ordre) <br>"

/bin/cat << EOM
</body>
</html>
EOM

