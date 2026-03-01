#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

/bin/cat << EOM

<html>
<head>
<meta http-equiv=Content-Type content="text/html; charset=windows-1252">
<style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #0f172a, #000);
  color: #e5e7eb;
}

.container {
  max-width: 500px;
  margin: auto;
}

h2 {
  background: linear-gradient(90deg, #0f172a, #020617);
  padding: 12px 16px;
  border-left: 5px solid #22d3ee;
  border-radius: 8px;
  font-weight: 700;
  letter-spacing: 0.6px;
  color: #7dd3fc;
  box-shadow: 0 0 18px rgba(34, 211, 238, 0.25);
  margin-bottom: 20px;
}

.menu {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

a {
  text-decoration: none;
}

.button {
  display: block;
  text-align: center;
  background: linear-gradient(135deg, #0284c7, #22d3ee);
  color: #020617;
  padding: 10px 18px;
  border-radius: 999px;
  font-weight: 800;
  letter-spacing: 0.4px;
  box-shadow: 0 4px 12px rgba(34, 211, 238, 0.5);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(34, 211, 238, 0.8);
}

.danger {
  background: linear-gradient(135deg, #dc2626, #f87171);
  box-shadow: 0 4px 12px rgba(248, 113, 113, 0.5);
}

.danger:hover {
  box-shadow: 0 6px 18px rgba(248, 113, 113, 0.8);
}

.success {
  background: linear-gradient(135deg, #16a34a, #4ade80);
  box-shadow: 0 4px 12px rgba(74, 222, 128, 0.5);
}

.success:hover {
  box-shadow: 0 6px 18px rgba(74, 222, 128, 0.8);
}
</style>
</head>
<body>
<div class="container">
  <h2>Control de WiFi</h2>

  <div class="menu">
    <a href="/cgi-bin/wifi.cgi?comand=iniciar" target="body">
      <div class="button success">WiFi Iniciar Service</div>
    </a>
    
    <a href="/cgi-bin/wifi.cgi?comand=aturar" target="body">
      <div class="button danger">WiFi Aturar Service</div>
    </a>
    
    <a href="/cgi-bin/wifi.cgi?comand=reiniciar" target="body">
      <div class="button danger">WiFi Reiniciar Service</div>
    </a>

    <a href="/cgi-bin/wifi.cgi?comand=estat" target="body">
      <div class="button">Estat i Informació</div>
    </a>

    <a href="/cgi-bin/wifi.cgi?comand=config_ap" target="body">
      <div class="button">Configuració Access Point</div>
    </a>

    <a href="/cgi-bin/wifi.cgi?comand=config_xarxa" target="body">
      <div class="button">Configuració de Xarxa (Bridge)</div>
    </a>

    <a href="/cgi-bin/wifi.cgi?comand=config_dhcp" target="body">
      <div class="button">Configuració DHCP</div>
    </a>

    <a href="/cgi-bin/wifi.cgi?comand=diagnostic" target="body">
      <div class="button">Diagnòstic</div>
    </a>
  </div>
</div>
</body>
</html>

EOM
