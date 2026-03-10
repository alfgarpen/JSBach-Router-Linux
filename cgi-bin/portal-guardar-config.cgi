#!/bin/bash

# Leer datos POST de forma robusta
if [ "$CONTENT_LENGTH" -gt 0 ]; then
    POST_DATA=$(dd bs=1 count="$CONTENT_LENGTH" 2>/dev/null)
fi

CONF_FILE="/usr/local/JSBach/conf/portal.conf"
SCRIPT_PORTAL="/usr/local/JSBach/scripts/portal"

# Función simple para extraer valores de POST_DATA
get_val() {
    local val=$(echo "$POST_DATA" | grep -oP "(?<=^|&)$1=[^&]*" | cut -d'=' -f2)
    [ -z "$val" ] && echo "" || echo "$val" | python3 -c "import sys, urllib.parse; print(urllib.parse.unquote_plus(sys.stdin.read().strip()))"
}

ENABLED=$(get_val "ENABLED")
VLAN_VID=$(get_val "VLAN_VID")
SESSION_TIMEOUT=$(get_val "SESSION_TIMEOUT")
IDLE_TIMEOUT=$(get_val "IDLE_TIMEOUT")
WALLED_GARDEN=$(get_val "WALLED_GARDEN")
WELCOME_TEXT=$(get_val "WELCOME_TEXT")
PRIMARY_COLOR=$(get_val "PRIMARY_COLOR")

# Obtener IP de la pasarela para esta VLAN para el LOGIN_URL
VLAN_GATEWAY=$(grep ";$VLAN_VID;" "/usr/local/JSBach/conf/bridge.conf" | cut -d';' -f4 | cut -d'/' -f1)
[ -z "$VLAN_GATEWAY" ] && VLAN_GATEWAY="10.0.3.1" # Fallback

# Redirección de vuelta a la config con mensaje
echo "Content-type: text/html"
echo "Location: portal-config.cgi?msg=saved"
echo ""

# Guardar y aplicar mediante el wrapper privilegiado
/usr/local/JSBach/scripts/client_srv_cli portal configurar "$ENABLED" "$VLAN_VID" "$SESSION_TIMEOUT" "$IDLE_TIMEOUT" "$WALLED_GARDEN" "$WELCOME_TEXT" "$PRIMARY_COLOR"
