#!/bin/bash
# =============================================================
# logout.cgi — Cierra la sesión activa y redirige a login
# =============================================================

source /usr/local/JSBach/conf/auth.sh

COOKIE_EXPIRED=$(destroy_session | grep "^Set-Cookie:")

echo "Content-Type: text/html; charset=utf-8"
echo "$COOKIE_EXPIRED"
echo "Location: /cgi-bin/login.cgi"
echo ""
echo "<html><body>Sessio tancada. <a href='/cgi-bin/login.cgi'>Login</a>...</body></html>"
