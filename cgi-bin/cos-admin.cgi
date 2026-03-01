#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

cat << 'EOF'
<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<title>Panell principal</title>

<style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #0f172a, #000);
  color: #e5e7eb;
}

h1 {
  color: #7dd3fc;
  margin-bottom: 10px;
}

.section {
  background: rgba(15, 23, 42, 0.9);
  border-radius: 12px;
  padding: 18px;
  margin-bottom: 20px;
  box-shadow: 0 0 20px rgba(34, 211, 238, 0.2);
}

.section h2 {
  margin-top: 0;
  color: #38bdf8;
}

.tip {
  margin-bottom: 8px;
}

.tip.warn { color: #fbbf24; }
.tip.danger { color: #f87171; }

.actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 14px;
  margin-top: 12px;
}

.actions button {
  background: linear-gradient(135deg, #0284c7, #22d3ee);
  color: #020617;
  border: none;
  padding: 14px;
  border-radius: 999px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(34, 211, 238, 0.5);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.actions button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(34, 211, 238, 0.8);
}

.footer {
  font-size: 0.9em;
  opacity: 0.7;
  margin-top: 30px;
}
</style>
</head>

<body>

<h1>🧠 Panell d'administració del sistema</h1>

<div class="section">
  <h2>💡 Consells generals</h2>
  <div class="tip">📡 Configura primer la <b>WAN</b> abans de tocar l’enrutament.</div>
  <div class="tip">🌉 Crea les <b>VLANs</b> abans de configurar el bridge.</div>
  <div class="tip warn">⚠️ No activis el <b>tallafocs</b> sense comprovar l’estat de les VLANs.</div>
  <div class="tip danger">🚨 No modifiquis la VLAN d’administració mentre hi estiguis connectat.</div>
</div>

<div class="section">
  <h2>📋 Ordre recomanat de configuració</h2>
  <div class="tip">1️⃣ WAN</div>
  <div class="tip">2️⃣ VLANs i Bridge</div>
  <div class="tip">3️⃣ Enrutament</div>
  <div class="tip">4️⃣ Tallafocs</div>
</div>

<div class="section">
  <h2>🚀 Accés ràpid</h2>
  <div class="actions">
    <button onclick="window.top.frames['menu'].location.href='/cgi-bin/ifwan-menu.cgi'">WAN</button>
    <button onclick="window.top.frames['menu'].location.href='/cgi-bin/bridge-menu.cgi'">VLAN / Bridge</button>
    <button onclick="window.top.frames['menu'].location.href='/cgi-bin/enrutar-menu.cgi'">Enrutament</button>
    <button onclick="window.top.frames['menu'].location.href='/cgi-bin/tallafocs-menu.cgi'">Tallafocs</button>
    <button onclick="window.top.frames['menu'].location.href='/cgi-bin/wifi-menu.cgi'">WiFi</button>
  </div>
</div>

<div class="section">
  <h2>🔐 Nota de seguretat</h2>
  <div class="tip warn">
    Qualsevol canvi de xarxa pot provocar pèrdua de connectivitat.
    Si això passa, revisa primer la configuració de la WAN i la VLAN d’administració.
  </div>
</div>

<div class="footer">
  Sistema d’administració de xarxa · Mode estudi / pràctiques
</div>

</body>
</html>
EOF
