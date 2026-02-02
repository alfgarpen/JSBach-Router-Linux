#!/bin/bash

source /usr/local/JSBach/conf/variables.conf


echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<html><head><title>Crear VLAN</title>"
echo "<meta charset='utf-8'>"
 
cat $DIR/$PROJECTE/$DIR_CGI/$CSS_CGI_BIN
 
echo "</head><body>"

echo "<h2>Afegir ip a ip_wls</h2>"
echo "<form action='/cgi-bin/tallafocs-ports-wls.cgi' method='get'>"
echo "<input type='hidden' name='accio' value='afegir_port_wls'>"
echo "<table>"
echo "<tr><th>protocol</th><th>port</th></tr>"
echo "<tr>"
echo "<td><input type='text' name='protocol' value='' style='width: 250px;'></td>"
echo "<td><input type='text' name='port' value='' ></td>"
echo "</tr>"
echo "</table>"
echo "<button type='submit'>Afegir</button>"
echo "</form>"

echo "</body></html>"

