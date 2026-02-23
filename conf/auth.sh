#!/bin/bash
# =============================================================
# auth.sh — Librería de autenticación y gestión de sesiones
# JSBach CGI System
# Uso: source /usr/local/JSBach/conf/auth.sh
# =============================================================

SESSION_DIR=/tmp/jsbach_sessions
SESSION_TTL=3600          # segundos (1 hora)
SESSION_COOKIE=SESSIONID
LOGIN_URL=/cgi-bin/login.cgi
USERS_FILE=/usr/local/JSBach/conf/users.conf

# ------------------------------------------------------------------
# _get_session_id  → extrae el SESSION_ID de la cookie HTTP_COOKIE
# ------------------------------------------------------------------
_get_session_id() {
    local cookies="${HTTP_COOKIE:-}"
    local sid=""
    # Recorre cada par cookie=valor
    IFS=';' read -ra parts <<< "$cookies"
    for part in "${parts[@]}"; do
        # Elimina espacios
        part="${part#"${part%%[![:space:]]*}"}"
        local name="${part%%=*}"
        local val="${part#*=}"
        if [[ "$name" == "$SESSION_COOKIE" ]]; then
            # Valida formato: solo hex lowercase 64 chars
            if [[ "$val" =~ ^[0-9a-f]{64}$ ]]; then
                sid="$val"
            fi
            break
        fi
    done
    echo "$sid"
}

# ------------------------------------------------------------------
# check_session  → valida sesión activa; si no existe/expira → login
# ------------------------------------------------------------------
check_session() {
    local sid
    sid=$(_get_session_id)

    if [[ -z "$sid" ]]; then
        _redirect_to_login
        exit 0
    fi

    local session_file="${SESSION_DIR}/${sid}"
    if [[ ! -f "$session_file" ]]; then
        _redirect_to_login
        exit 0
    fi

    local ts now age
    ts=$(cat "$session_file" 2>/dev/null)
    now=$(date +%s)
    age=$(( now - ts ))

    if (( age > SESSION_TTL )); then
        rm -f "$session_file"
        _redirect_to_login
        exit 0
    fi

    # Renovar timestamp (sesión deslizante)
    echo "$now" > "$session_file"
}

# ------------------------------------------------------------------
# create_session USUARIO → crea sesión y emite Set-Cookie
# ------------------------------------------------------------------
create_session() {
    local user="${1:-}"
    # Asegura directorio de sesiones con permisos seguros
    mkdir -p "$SESSION_DIR"
    chmod 700 "$SESSION_DIR"

    local sid
    sid=$(openssl rand -hex 32)
    local session_file="${SESSION_DIR}/${sid}"
    echo "$(date +%s)" > "$session_file"
    chmod 600 "$session_file"

    # Emitir cookie HttpOnly; sin Secure porque puede ser HTTP local
    echo "Set-Cookie: ${SESSION_COOKIE}=${sid}; Path=/; HttpOnly; SameSite=Strict"
    echo "X-Session-User: ${user}"
}

# ------------------------------------------------------------------
# destroy_session → elimina sesión y expira cookie
# ------------------------------------------------------------------
destroy_session() {
    local sid
    sid=$(_get_session_id)
    if [[ -n "$sid" ]]; then
        rm -f "${SESSION_DIR}/${sid}"
    fi
    # Expirar cookie enviando fecha en el pasado
    echo "Set-Cookie: ${SESSION_COOKIE}=deleted; Path=/; HttpOnly; SameSite=Strict; Expires=Thu, 01 Jan 1970 00:00:00 GMT"
}

# ------------------------------------------------------------------
# validate_credentials USUARIO CONTRASEÑA → 0 éxito, 1 fallo
# ------------------------------------------------------------------
validate_credentials() {
    local input_user="${1:-}"
    local input_pass="${2:-}"

    # Sanitización básica: solo alfanumérico + algunos chars para usuario
    if ! [[ "$input_user" =~ ^[a-zA-Z0-9_]{1,32}$ ]]; then
        return 1
    fi
    # La contraseña puede tener más caracteres pero limitamos a 128
    if (( ${#input_pass} > 128 )); then
        return 1
    fi

    if [[ ! -f "$USERS_FILE" ]]; then
        return 1
    fi

    while IFS=: read -r stored_user stored_salt stored_hash remainder; do
        # Saltar líneas de comentario o vacías
        [[ "$stored_user" =~ ^[[:space:]]*# ]] && continue
        [[ -z "$stored_user" ]] && continue

        if [[ "$stored_user" == "$input_user" ]]; then
            # Calcular hash de salt+contraseña
            local computed_hash
            computed_hash=$(printf '%s%s' "$stored_salt" "$input_pass" | sha256sum | awk '{print $1}')
            if [[ "$computed_hash" == "$stored_hash" ]]; then
                return 0
            fi
            return 1
        fi
    done < "$USERS_FILE"

    # Usuario no encontrado — misma respuesta que pass incorrecta (timing safe aprox.)
    return 1
}

# ------------------------------------------------------------------
# _redirect_to_login → emite cabeceras de redirección a login
# ------------------------------------------------------------------
_redirect_to_login() {
    echo "Content-Type: text/html; charset=utf-8"
    echo "Location: ${LOGIN_URL}"
    echo ""
    echo "<html><body>Redirigint a <a href='${LOGIN_URL}'>login</a>...</body></html>"
}
