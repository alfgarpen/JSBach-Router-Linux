#!/bin/bash

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << EOM
<html>
<head>
<style>
body { font-family: sans-serif; background: #0f172a; color: #e5e7eb; padding: 20px; }
h2 { border-left: 5px solid #38bdf8; padding-left: 10px; color: #7dd3fc; }
.card { background: rgba(30, 41, 59, 0.7); border-radius: 12px; padding: 20px; margin-bottom: 20px; }
pre { background: #000; padding: 15px; border-radius: 8px; overflow-x: auto; color: #4ade80; }
</style>
</head>
<body>
    <h2>Seguridad y Logs del Portal</h2>

    <div class="card">
        <h3>Intentos de Autenticación</h3>
        <p>Próximamente: Registro de intentos fallidos y bloqueos temporales.</p>
    </div>

    <div class="card">
        <h3>Reglas de Firewall (Referencia)</h3>
        <pre>$(iptables -L PORTAL_AUTH -n 2>/dev/null || echo "Chain PORTAL_AUTH no activa")</pre>
    </div>
</body>
</html>
EOM
