#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
source /usr/local/JSBach/conf/portal.conf

read -n "$CONTENT_LENGTH" POST_DATA

# Función de extracción de POST mejorada
get_val() {
    local key="$1"
    local val=$(echo "$POST_DATA" | tr '&' '\n' | grep "^${key}=" | head -n1 | cut -d'=' -f2-)
    if [ -z "$val" ]; then
        echo ""
    else
        echo "$val" | python3 -c "import sys, urllib.parse; print(urllib.parse.unquote_plus(sys.stdin.read().strip()))"
    fi
}

USER_IN=$(get_val "user")
PASS_IN=$(get_val "pass")
CLIENT_IP="$REMOTE_ADDR"

# Obtener MAC más robustamente
# Primero intentamos con ip neigh que es más moderno
CLIENT_MAC=$(ip neigh show "$CLIENT_IP" | awk '{print $5}' | grep -oE '([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}')
if [ -z "$CLIENT_MAC" ]; then
    # Fallback a arp
    CLIENT_MAC=$(arp -an "$CLIENT_IP" | awk '{print $4}' | grep -oE '([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}')
fi

# Brute-force protection check
LOCKOUT_FILE="/usr/local/JSBach/run/portal/failed_attempts/${CLIENT_IP//./_}"
if [ -f "$LOCKOUT_FILE" ]; then
    last_fail=$(stat -c %Y "$LOCKOUT_FILE")
    now=$(date +%s)
    diff=$((now - last_fail))
    fails=$(cat "$LOCKOUT_FILE")
    
    if [ "$fails" -ge "$FAILED_ATTEMPTS_LIMIT" ]; then
        if [ "$diff" -lt "$LOCKOUT_TIME" ]; then
            echo "Content-type: text/html; charset=utf-8"
            echo ""
            cat << EOM
            <html>
            <head>
                <style>
                    body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; text-align: center; margin: 0; }
                    .error { color: #f87171; font-size: 1.5rem; font-weight: bold; }
                    .card { background: rgba(255,255,255,0.05); padding: 40px; border-radius: 20px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }
                </style>
            </head>
            <body>
                <div class="card">
                    <div class="error">⚠ Acceso Bloqueado Temporalmente</div>
                    <p>Demasiados intentos fallidos. Por favor, inténtelo de nuevo en unos minutos.</p>
                </div>
            </body>
            </html>
EOM
            exit 0
        else
            # Lockout expired, reset
            rm -f "$LOCKOUT_FILE"
        fi
    fi
fi

VALID=0

# Validación básica contra portal_users.conf
while IFS=: read -r stored_user stored_salt stored_hash remainder; do
    [[ "$stored_user" =~ ^[[:space:]]*# ]] && continue
    [[ -z "$stored_user" ]] && continue
    
    if [ "$stored_user" == "$USER_IN" ]; then
        computed_hash=$(printf '%s%s' "$stored_salt" "$PASS_IN" | sha256sum | awk '{print $1}')
        if [ "$computed_hash" == "$stored_hash" ]; then
            VALID=1
            break
        fi
    fi
done < /usr/local/JSBach/conf/portal_users.conf

# IMPORTANTE: No imprimir NADA hasta enviar el header
echo "Content-type: text/html; charset=utf-8"
echo ""

if [ "$VALID" -eq 1 ]; then
    # Reset failed attempts on success
    rm -f "$LOCKOUT_FILE"
    
    # Log success
    echo "$(date '+%Y-%m-%d %H:%M:%S') [LOGIN-SUCCESS] User: $USER_IN, IP: $CLIENT_IP" >> /usr/local/JSBach/logs/portal.log

    # Autenticar en el backend (redirigir salida a /dev/null para no romper el header CGI)
    if [ -n "$CLIENT_MAC" ]; then
        sudo /usr/local/JSBach/scripts/portal auth "$CLIENT_IP" "$CLIENT_MAC" "$USER_IN" > /dev/null 2>&1
    fi
    
    cat << EOM
    <html>
    <head>
        <meta http-equiv="refresh" content="3;url=http://www.google.com">
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; text-align: center; margin: 0; }
            .success { color: #4ade80; font-size: 2rem; font-weight: bold; }
            .card { background: rgba(255,255,255,0.05); padding: 40px; border-radius: 20px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="success">✓ Acceso Concedido</div>
            <p>Disfrute de su conexión. Redirigiendo...</p>
        </div>
    </body>
    </html>
EOM
else
    # Register failure
    fails=1
    if [ -f "$LOCKOUT_FILE" ]; then
        fails=$(cat "$LOCKOUT_FILE")
        fails=$((fails + 1))
    fi
    echo "$fails" > "$LOCKOUT_FILE"
    
    # Log failure
    echo "$(date '+%Y-%m-%d %H:%M:%S') [LOGIN-FAIL] User: $USER_IN, IP: $CLIENT_IP (Attempt $fails)" >> /usr/local/JSBach/logs/portal.log

    cat << EOM
    <html>
    <head>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; text-align: center; margin: 0; }
            .error { color: #f87171; font-size: 1.5rem; font-weight: bold; }
            .card { background: rgba(255,255,255,0.05); padding: 40px; border-radius: 20px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }
            .btn { background: #38bdf8; color: #0f172a; padding: 12px 24px; border-radius: 8px; text-decoration: none; display: inline-block; margin-top: 20px; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="error">✗ Error de Autenticación</div>
            <p>El usuario o la contraseña no son válidos.</p>
            <a href="portal-login.cgi" class="btn">Volver a intentar</a>
        </div>
    </body>
    </html>
EOM
fi
