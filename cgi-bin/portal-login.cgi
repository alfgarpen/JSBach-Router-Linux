#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
source /usr/local/JSBach/conf/portal.conf

# Obtener IP del cliente (Apache la pasa como REMOTE_ADDR)
CLIENT_IP="$REMOTE_ADDR"

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Acceso a la Red</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            background: radial-gradient(circle, #1e293b, #0f172a); 
            color: white; 
        }
        .login-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            width: 100%;
            max-width: 400px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .logo { width: 80px; margin-bottom: 20px; }
        h1 { font-size: 1.5rem; margin-bottom: 10px; color: $PRIMARY_COLOR; }
        p { color: #94a3b8; margin-bottom: 30px; }
        .input-group { margin-bottom: 20px; text-align: left; }
        label { display: block; margin-bottom: 8px; font-size: 0.9rem; color: #cbd5e1; }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px;
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid #334155;
            border-radius: 8px;
            color: white;
            box-sizing: border-box;
        }
        .terms {
            margin-bottom: 25px;
            font-size: 0.85rem;
            color: #94a3b8;
            display: flex;
            align-items: flex-start;
            gap: 10px;
            text-align: left;
        }
        .btn-login {
            width: 100%;
            padding: 14px;
            background: $PRIMARY_COLOR;
            color: #0f172a;
            border: none;
            border-radius: 8px;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-login:hover { transform: scale(1.02); opacity: 0.9; }
    </style>
</head>
<body>
    <div class="login-card">
        <img src="$LOGO_URL" class="logo" onerror="this.src='https://cdn-icons-png.flaticon.com/512/3064/3064197.png'">
        <h1>$WELCOME_TEXT</h1>
        <p>Inicie sesión para acceder a Internet</p>

        <form method="POST" action="portal-do-login.cgi">
            <div class="input-group">
                <label>Usuario</label>
                <input type="text" name="user" required autofocus>
            </div>
            <div class="input-group">
                <label>Contraseña</label>
                <input type="password" name="pass" required>
            </div>
            
            <div class="terms">
                <input type="checkbox" name="accept_terms" required>
                <span>$TERMS_OF_USE</span>
            </div>

            <button type="submit" class="btn-login">CONECTAR</button>
        </form>
    </div>
</body>
</html>
EOM
