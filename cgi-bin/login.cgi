#!/bin/bash
# =============================================================
# login.cgi — Página de autenticación JSBach
# =============================================================

source /usr/local/JSBach/conf/auth.sh
source /usr/local/JSBach/conf/variables.conf

# ── Leer el método HTTP ──────────────────────────────────────
METHOD="${REQUEST_METHOD:-GET}"

# ── POST: procesar credenciales ──────────────────────────────
if [[ "$METHOD" == "POST" ]]; then
    # Leer body (Content-Length bytes)
    CONTENT_LENGTH="${CONTENT_LENGTH:-0}"
    if (( CONTENT_LENGTH > 0 && CONTENT_LENGTH < 4096 )); then
        read -r -n "$CONTENT_LENGTH" POST_DATA
    else
        POST_DATA=""
    fi

    # Decodificar URL-encoding de forma segura (sin eval)
    _urldecode() {
        local encoded="${1//+/ }"
        printf '%b' "${encoded//%/\\x}"
    }

    # Extraer campos usuario y contraseña
    INPUT_USER=""
    INPUT_PASS=""
    IFS='&' read -ra fields <<< "$POST_DATA"
    for field in "${fields[@]}"; do
        name="${field%%=*}"
        val="${field#*=}"
        case "$name" in
            usuario) INPUT_USER=$(_urldecode "$val") ;;
            password) INPUT_PASS=$(_urldecode "$val") ;;
        esac
    done

    # Validar credenciales
    if validate_credentials "$INPUT_USER" "$INPUT_PASS"; then
        # Crear sesión y redirigir
        COOKIE_HEADER=$(create_session "$INPUT_USER" | grep "^Set-Cookie:")
        echo "Content-Type: text/html; charset=utf-8"
        echo "$COOKIE_HEADER"
        echo "Location: /cgi-bin/main.cgi"
        echo ""
        echo "<html><body>Accés correcte. <a href='/cgi-bin/main.cgi'>Continuar</a>...</body></html>"
        exit 0
    else
        ERROR_MSG="Credencials incorrectes. Torna-ho a intentar."
    fi
fi

# ── GET (o POST fallido): mostrar formulari ──────────────────
echo "Content-Type: text/html; charset=utf-8"
echo ""

cat << HTMLEOF
<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Accés — Administració ${HOSTNAME}</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: radial-gradient(ellipse at top, #0f172a 0%, #020617 60%, #000 100%);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
                   Roboto, Ubuntu, Cantarell, Arial, sans-serif;
      color: #e5e7eb;
    }

    .card {
      width: 100%;
      max-width: 420px;
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid rgba(34, 211, 238, 0.2);
      border-radius: 18px;
      padding: 40px 36px;
      box-shadow: 0 0 40px rgba(34, 211, 238, 0.15),
                  0 0 80px rgba(2, 132, 199, 0.1);
    }

    .logo {
      text-align: center;
      margin-bottom: 28px;
    }

    .logo h1 {
      font-size: 2rem;
      font-weight: 800;
      letter-spacing: 2px;
      background: linear-gradient(90deg, #38bdf8, #22d3ee, #a78bfa);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      text-shadow: none;
    }

    .logo p {
      font-size: 0.85rem;
      color: #64748b;
      margin-top: 4px;
      letter-spacing: 0.5px;
    }

    .error {
      background: rgba(248, 113, 113, 0.15);
      border: 1px solid rgba(248, 113, 113, 0.4);
      border-radius: 10px;
      padding: 10px 14px;
      color: #fca5a5;
      font-size: 0.88rem;
      margin-bottom: 20px;
      text-align: center;
    }

    label {
      display: block;
      font-size: 0.8rem;
      font-weight: 600;
      color: #7dd3fc;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin-bottom: 6px;
    }

    input[type="text"],
    input[type="password"] {
      width: 100%;
      background: rgba(2, 6, 23, 0.8);
      border: 1px solid rgba(148, 163, 184, 0.2);
      border-radius: 10px;
      padding: 12px 14px;
      color: #e5e7eb;
      font-size: 0.95rem;
      outline: none;
      transition: border-color 0.2s, box-shadow 0.2s;
      margin-bottom: 18px;
    }

    input[type="text"]:focus,
    input[type="password"]:focus {
      border-color: #22d3ee;
      box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.15);
    }

    input[type="submit"] {
      width: 100%;
      background: linear-gradient(135deg, #0284c7, #22d3ee);
      color: #020617;
      border: none;
      border-radius: 999px;
      padding: 13px;
      font-size: 1rem;
      font-weight: 700;
      letter-spacing: 0.5px;
      cursor: pointer;
      box-shadow: 0 4px 20px rgba(34, 211, 238, 0.45);
      transition: transform 0.15s ease, box-shadow 0.15s ease;
      margin-top: 6px;
    }

    input[type="submit"]:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 28px rgba(34, 211, 238, 0.7);
    }

    input[type="submit"]:active {
      transform: translateY(0);
      box-shadow: 0 3px 12px rgba(34, 211, 238, 0.4);
    }

    .footer {
      text-align: center;
      margin-top: 22px;
      font-size: 0.8rem;
      color: #334155;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="logo">
      <h1>🔐 JSBach</h1>
      <p>Sistema d'administració de xarxa</p>
    </div>

HTMLEOF

# Mostrar error si el hay
if [[ -n "${ERROR_MSG:-}" ]]; then
    echo "    <div class=\"error\">⚠️ ${ERROR_MSG}</div>"
fi

cat << HTMLEOF
    <form method="POST" action="/cgi-bin/login.cgi" autocomplete="off">
      <label for="usuario">Usuari</label>
      <input type="text"
             id="usuario"
             name="usuario"
             maxlength="32"
             required
             autofocus
             spellcheck="false"
             autocomplete="username">

      <label for="password">Contrasenya</label>
      <input type="password"
             id="password"
             name="password"
             maxlength="128"
             required
             autocomplete="current-password">

      <input type="submit" value="Iniciar sessió →">
    </form>

    <div class="footer">Accés restringit · Només personal autoritzat</div>
  </div>
</body>
</html>
HTMLEOF
