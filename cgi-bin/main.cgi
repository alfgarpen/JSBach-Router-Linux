#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
source /usr/local/JSBach/conf/auth.sh

# ── Protecció: requereix sessió vàlida ────────────────────────
check_session

echo "Content-Type: text/html; charset=utf-8"
echo ""

/bin/cat << EOM

<html>
<head>

EOM
echo '<title>Administracio de '$HOSTNAME'</title>'
/bin/cat << EOM

<meta http-equiv=Content-Type content="text/html; charset=windows-1252">
<meta content="MSHTML 6.00.2900.3660" name=GENERATOR> 

<style type="text/css">
/* === Reset mental: seguimos en frames, pero con dignidad === */

body {
	margin: 0;
	background: #0f172a; /* azul oscuro tech */
	color: #e5e7eb;
	font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
	             Roboto, Ubuntu, Cantarell, "Helvetica Neue", Arial;
}

/* Estado del sistema */
.estado {
	font-size: 18px;
	font-weight: 700;
	color: #22d3ee; /* cian neón */
	letter-spacing: 0.5px;
	text-shadow: 0 0 6px rgba(34, 211, 238, 0.6);
}

/* Cabeceras */
.cabecera {
	font-size: 20px;
	font-weight: 600;
	color: #a7f3d0; /* verde suave */
	border-bottom: 2px solid rgba(167, 243, 208, 0.3);
	padding-bottom: 4px;
	margin-bottom: 8px;
}

/* Colores legacy, pero refinados */
.Estilo1 {
	color: #f472b6; /* magenta chill */
}

.Estilo2 {
	color: #e5e7eb; /* gris claro */
}

/* Detalles globales */
a {
	color: #38bdf8;
	text-decoration: none;
}

a:hover {
	text-decoration: underline;
}

/* Frames (sí, también se pueden ver decentes) */
frame {
	border-color: #1e293b;
	background-color: #020617;
}
</style>
</head> 

<frameset rows="18%,82%" frameborder="1">
<frame src="/cgi-bin/index-admin.cgi" name="menu-general" noresize="noresize">
<frameset cols="20%,80%">
<frame src="/cgi-bin/cos-admin.cgi" name="menu" noresize="noresize">
<frame src="/cgi-bin/info.cgi" name="body" noresize="noresize">
</frameset>

<noframes>
<body>Tu browser no soporta frames!</body>
</noframes>

</html>

EOM

