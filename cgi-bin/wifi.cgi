#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <title>WiFi Admin Shell</title>
 <style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #020617, #000);
  color: #e5e7eb;
}

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

pre {
  background: #020617;
  color: #a5f3fc;
  padding: 18px 20px;
  border-radius: 14px;
  font-family: monospace;
  font-size: 14px;
  line-height: 1.6;
  box-shadow: inset 0 0 18px rgba(56, 189, 248, 0.15), 0 0 24px rgba(0,0,0,0.7);
  overflow-x: auto;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

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

input[type=text], input[type=password], select {
  width: 100%;
  padding: 10px;
  margin: 6px 0 16px 0;
  display: inline-block;
  border: 1px solid #38bdf8;
  border-radius: 6px;
  box-sizing: border-box;
  background: #0f172a;
  color: #e5e7eb;
}

input[type=submit] {
  width: 100%;
  background-color: #0284c7;
  color: white;
  padding: 14px 20px;
  margin: 8px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

input[type=submit]:hover {
  background-color: #0369a1;
}

.form-container {
  border-radius: 10px;
  background-color: rgba(15, 23, 42, 0.9);
  padding: 20px;
}

</style>
</head>
<body>
EOM

urldecode() {
    local data="${1//+/ }"      # Canvia + per espai
    printf '%b' "${data//%/\\x}" # Converteix %xx en caràcters
}

# Parse query string parameters
comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')
comand=$(urldecode "$comand")

case "$comand" in
  estat|iniciar|aturar|reiniciar|diagnostic|fix_apply)
    echo "<h2>Resposta del sistema</h2>"
    echo "<pre>"
    echo "$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi "$comand")"
    echo "</pre>"
    ;;
    
  config_ap)
    echo "<h2>Configuració Access Point</h2>"
    CURRENT_WIFI_CONF=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi config_ap_read)
    SSID=$(echo "$CURRENT_WIFI_CONF" | grep -m1 "ssid" | cut -d'=' -f2)
    CHANNEL=$(echo "$CURRENT_WIFI_CONF" | grep -m1 "channel=" | cut -d'=' -f2)
    HW_MODE=$(echo "$CURRENT_WIFI_CONF" | grep -m1 "hw_mode" | cut -d'=' -f2)
    COUNTRY=$(echo "$CURRENT_WIFI_CONF" | grep -m1 "country_code" | cut -d'=' -f2)
    WPA=$(echo "$CURRENT_WIFI_CONF" | grep -m1 "wpa=" | cut -d'=' -f2)
    WPA_PASS=$(echo "$CURRENT_WIFI_CONF" | grep -m1 "wpa_passphrase" | cut -d'=' -f2)
    
    echo '<div class="form-container">'
    echo '<form action="/cgi-bin/wifi.cgi" method="GET">'
    echo '<input type="hidden" name="comand" value="config_ap_save" />'
    
    echo '<label>SSID:</label>'
    echo "<input type=\"text\" name=\"ssid\" value=\"$SSID\" required />"
    
    echo '<label>Canal (Channel):</label>'
    echo "<input type=\"text\" name=\"channel\" value=\"$CHANNEL\" required />"
    
    echo '<label>Mode (hw_mode - b/g/a):</label>'
    echo "<input type=\"text\" name=\"hw_mode\" value=\"$HW_MODE\" required />"
    
    echo '<label>Codi del País (Country Code):</label>'
    echo "<input type=\"text\" name=\"country_code\" value=\"$COUNTRY\" required />"
    
    echo '<label>WPA (1=WPA, 2=WPA2, 3=WPA3):</label>'
    echo "<input type=\"text\" name=\"wpa\" value=\"$WPA\" />"
    
    echo '<label>Contrasenya WPA:</label>'
    echo "<input type=\"text\" name=\"wpa_passphrase\" value=\"$WPA_PASS\" />"
    
    echo '<input type="submit" value="Guardar i Reiniciar Hostapd">'
    echo '</form>'
    echo '</div>'
    ;;
    
  config_ap_save)
    echo "<h2>Desant la configuració AP</h2>"
    SSID=$(echo "$QUERY_STRING" | sed -n 's/^.*ssid=\([^&]*\).*$/\1/p')
    SSID=$(urldecode "$SSID")

    CHANNEL=$(echo "$QUERY_STRING" | sed -n 's/^.*channel=\([^&]*\).*$/\1/p')
    CHANNEL=$(urldecode "$CHANNEL")

    HW_MODE=$(echo "$QUERY_STRING" | sed -n 's/^.*hw_mode=\([^&]*\).*$/\1/p')
    HW_MODE=$(urldecode "$HW_MODE")

    COUNTRY=$(echo "$QUERY_STRING" | sed -n 's/^.*country_code=\([^&]*\).*$/\1/p')
    COUNTRY=$(urldecode "$COUNTRY")

    WPA=$(echo "$QUERY_STRING" | sed -n 's/^.*wpa=\([^&]*\).*$/\1/p')
    WPA=$(urldecode "$WPA")

    WPA_PASS=$(echo "$QUERY_STRING" | sed -n 's/^.*wpa_passphrase=\([^&]*\).*$/\1/p')
    WPA_PASS=$(urldecode "$WPA_PASS")
    
    echo "<pre>"
    echo "$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi config_ap_save "$SSID" "$CHANNEL" "$HW_MODE" "$COUNTRY" "$WPA" "$WPA_PASS")"
    echo "</pre>"
    ;;
    
  config_xarxa)
    echo "<h2>Configuració de Bridge</h2>"
    CURRENT_BRIDGE=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi config_xarxa_read)
    
    echo '<div class="form-container">'
    echo '<form action="/cgi-bin/wifi.cgi" method="GET">'
    echo '<input type="hidden" name="comand" value="config_xarxa_save" />'
    
    echo '<label>Bridge Mestre (Deixar buit per desvincular):</label>'
    echo "<input type=\"text\" name=\"bridge\" value=\"$CURRENT_BRIDGE\" placeholder=\"ex. br0\" />"
    echo '<p style="font-size: 12px; color: #94a3b8;">Bridges disponibles actualment:</p>'
    echo "<pre>$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi diagnostic_bridges)</pre>"
    
    echo '<input type="submit" value="Aplicar">'
    echo '</form>'
    echo '</div>'
    ;;
    
  config_xarxa_save)
    echo "<h2>Aplicant configuració Bridge</h2>"
    BRIDGE=$(echo "$QUERY_STRING" | sed -n 's/^.*bridge=\([^&]*\).*$/\1/p')
    BRIDGE=$(urldecode "$BRIDGE")
    
    echo "<pre>"
    echo "$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi config_xarxa_save "$BRIDGE")"
    echo "</pre>"
    ;;
    
  config_dhcp)
    echo "<h2>Configuració DHCP per WiFi</h2>"
    DHCP_CONF=$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi config_dhcp_read)

    STATUS=$(echo "$DHCP_CONF" | awk '{print $1}')
    R_INI=$(echo "$DHCP_CONF" | awk '{print $2}')
    R_FI=$(echo "$DHCP_CONF" | awk '{print $3}')
    LEASE=$(echo "$DHCP_CONF" | awk '{print $4}')
    GW=$(echo "$DHCP_CONF" | awk '{print $5}')
    DNS=$(echo "$DHCP_CONF" | awk '{print $6}')

    # Detectar si és ACTIVAT via bridge VLAN (ACTIVAT_BRIDGE:br0.X)
    BRIDGE_VLAN=$(echo "$STATUS" | grep -oP '(?<=ACTIVAT_BRIDGE:)\S+')
    STATUS_BASE=$(echo "$STATUS" | cut -d':' -f1)

    if [ -n "$BRIDGE_VLAN" ]; then
      # WiFi bridged: mostrar info del bridge VLAN, sense formulari de modificació directa
      echo '<div class="form-container">'
      echo '<p>Estat actual: <strong style="color:#4ade80;">✅ ACTIVAT (via bridge)</strong></p>'
      echo "<p style='color:#94a3b8; font-size:13px;'>La interfície WiFi és membre del bridge <strong style='color:#38bdf8;'>$BRIDGE_VLAN</strong>. El DHCP dels clients WiFi és gestionat pel rang d'aquesta VLAN.</p>"
      echo '<table>'
      echo '<tr><th>Paràmetre</th><th>Valor</th></tr>'
      echo "<tr><td>Interfície VLAN</td><td>$BRIDGE_VLAN</td></tr>"
      echo "<tr><td>Rang DHCP</td><td>$R_INI &ndash; $R_FI</td></tr>"
      echo "<tr><td>Temps de Lease</td><td>$LEASE</td></tr>"
      echo "<tr><td>Gateway</td><td>$GW</td></tr>"
      echo "<tr><td>DNS</td><td>$DNS</td></tr>"
      echo '</table>'
      echo "<p style='margin-top:14px; color:#94a3b8; font-size:12px;'>Per canviar el rang, usa el menú <strong>DHCP → Configurar</strong> seleccionant la VLAN <strong>$BRIDGE_VLAN</strong>.</p>"
      echo '</div>'
    else
      # WiFi no bridged (o desactivat): mostrar formulari de configuració directa
      if [ -z "$STATUS_BASE" ] || [ "$STATUS_BASE" = "DESACTIVAT" ]; then
          STATUS_DIS="DESACTIVAT"
          STATUS_VAL="0"
      else
          STATUS_DIS="ACTIVAT"
          STATUS_VAL="1"
      fi

      echo '<div class="form-container">'
      echo "<p>Estat actual: <strong>$STATUS_DIS</strong></p>"
      echo '<form action="/cgi-bin/wifi.cgi" method="GET">'
      echo '<input type="hidden" name="comand" value="config_dhcp_save" />'

      echo '<label>Activar DHCP Wifi (1 per activar, 0 per desactivar):</label>'
      echo "<input type=\"text\" name=\"status\" value=\"$STATUS_VAL\" required />"

      echo '<label>IP Inici:</label>'
      echo "<input type=\"text\" name=\"r_ini\" value=\"$R_INI\" />"

      echo '<label>IP Final:</label>'
      echo "<input type=\"text\" name=\"r_fi\" value=\"$R_FI\" />"

      echo '<label>Temps de Lease (ex: 12h):</label>'
      echo "<input type=\"text\" name=\"lease\" value=\"$LEASE\" />"

      echo '<label>Gateway (Router IP, sense màscara):</label>'
      echo "<input type=\"text\" name=\"gw\" value=\"$GW\" placeholder=\"ex: 10.0.3.1\" />"

      echo '<label>DNS Server:</label>'
      echo "<input type=\"text\" name=\"dns\" value=\"$DNS\" />"

      echo '<input type="submit" value="Guardar i reiniciar Dnsmasq">'
      echo '</form>'
      echo '</div>'
    fi
    ;;
    
  config_dhcp_save)
    echo "<h2>Aplicant configuració DHCP</h2>"
    STATUS=$(echo "$QUERY_STRING" | sed -n 's/^.*status=\([^&]*\).*$/\1/p')
    STATUS=$(urldecode "$STATUS")

    R_INI=$(echo "$QUERY_STRING" | sed -n 's/^.*r_ini=\([^&]*\).*$/\1/p')
    R_INI=$(urldecode "$R_INI")

    R_FI=$(echo "$QUERY_STRING" | sed -n 's/^.*r_fi=\([^&]*\).*$/\1/p')
    R_FI=$(urldecode "$R_FI")

    LEASE=$(echo "$QUERY_STRING" | sed -n 's/^.*lease=\([^&]*\).*$/\1/p')
    LEASE=$(urldecode "$LEASE")

    GW=$(echo "$QUERY_STRING" | sed -n 's/^.*gw=\([^&]*\).*$/\1/p')
    GW=$(urldecode "$GW")

    DNS=$(echo "$QUERY_STRING" | sed -n 's/^.*dns=\([^&]*\).*$/\1/p')
    DNS=$(urldecode "$DNS")
    
    echo "<pre>"
    echo "$("$DIR"/"$PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi config_dhcp_save "$STATUS" "$R_INI" "$R_FI" "$LEASE" "$GW" "$DNS")"
    echo "</pre>"
    ;;
    
  *)
    echo "<h2>Error</h2>"
    echo "<pre>Comanda no reconeguda o falta de paràmetres ($comand).</pre>"
    ;;
esac

echo "</body>"
echo "</html>"
EOM
