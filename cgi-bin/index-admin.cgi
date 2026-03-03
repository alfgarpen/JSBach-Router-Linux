#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-Type:text/html;charset=utf-8"
/bin/cat << EOM

<html>
<head>
<title>Administrant el Router</title>
<meta http-equiv=Content-Type content="text/html; charset=windows-1252">
<meta content="MSHTML 6.00.2900.3660" name=GENERATOR>
<style>
/* === Base === */
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 20px;
  background: radial-gradient(circle at top, #020617, #000);
  color: #e5e7eb;
}

/* Título principal */
h1 {
  text-align: center;
  font-weight: 800;
  letter-spacing: 1px;
  color: #38bdf8;
  text-shadow: 0 0 12px rgba(56, 189, 248, 0.5);
  margin-bottom: 30px;
}

h2 {
  background: linear-gradient(90deg, #0f172a, #020617);
  padding: 8px 12px;
  border-left: 4px solid #22d3ee;
  color: #a5f3fc;
  margin-top: 30px;
}

/* Tabla contenedora */
table {
  border-collapse: collapse;
  margin: 0 auto 20px auto;
  width: 90%;
  background: rgba(15, 23, 42, 0.85);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 0 25px rgba(0,0,0,0.6);
}

td, th {
  border: 1px solid rgba(148, 163, 184, 0.2);
  padding: 10px 14px;
  text-align: left;
}

th {
  background: rgba(2, 6, 23, 0.9);
  color: #7dd3fc;
  font-weight: 600;
}

/* Botones */
button {
  background: linear-gradient(135deg, #0284c7, #22d3ee);
  color: #020617;
  border: none;
  padding: 10px 18px;
  margin: 6px;
  border-radius: 999px;
  font-weight: 700;
  letter-spacing: 0.5px;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(34, 211, 238, 0.5);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 22px rgba(34, 211, 238, 0.8);
}

button:active {
  transform: translateY(0);
  box-shadow: 0 3px 10px rgba(34, 211, 238, 0.4);
}

/* Botó de logout */
.btn-logout {
  background: linear-gradient(135deg, #7f1d1d, #ef4444) !important;
  box-shadow: 0 4px 15px rgba(239, 68, 68, 0.5) !important;
  margin-left: auto;
}
.btn-logout:hover {
  box-shadow: 0 6px 22px rgba(239, 68, 68, 0.8) !important;
}

/* Fila de botons: espai entre nav i logout */
.nav-row {
  display: flex;
  align-items: center;
  width: 100%;
}

/* Links heredados del body */
a {
  color: #e9ab17;
}
</style>

</head>
<body link="#E9AB17" vlink="#E9AB17" alink="#E9AB17">


EOM

echo "<h1 align="center">Administrant el Router "$HOSTNAME" amb "$PROJECTE"</h1>"

/bin/cat << EOM

<script>
function main(){
window.top.frames['menu'].location.href='/cgi-bin/cos-admin.cgi';
window.top.frames['body'].location.href='/cgi-bin/info.cgi';
}
function wan(){
window.top.frames['menu'].location.href='/cgi-bin/ifwan-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/ifwan.cgi?comand=estat&';
}
function enrutar(){
window.top.frames['menu'].location.href='/cgi-bin/enrutar-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/enrutar.cgi?comand=estat&';
}
function bridge(){
window.top.frames['menu'].location.href='/cgi-bin/bridge-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/bridge.cgi?comand=estat&';
}
function tallafocs(){
window.top.frames['menu'].location.href='/cgi-bin/tallafocs-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/tallafocs.cgi?comand=estat&';
}
function dmz(){
window.top.frames['menu'].location.href='/cgi-bin/dmz-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/dmz.cgi?comand=estat&';
}
function switchs(){
window.top.frames['menu'].location.href='/cgi-bin/switch-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/switch.cgi';
}
function dhcp(){
window.top.frames['menu'].location.href='/cgi-bin/dhcp-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/dhcp.cgi?comand=estat';
}
function wifi(){
window.top.frames['menu'].location.href='/cgi-bin/wifi-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/wifi.cgi?comand=estat&';
}
function portal(){
window.top.frames['menu'].location.href='/cgi-bin/portal-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/portal-estat.cgi';
}
</script>

<div class="nav-row">
  <button onclick="main()">Main Menu</button>
  <button onclick="wan()">WAN</button>
  <button onclick="enrutar()">ENRUTAR</button>
  <button onclick="bridge()">BRIDGE</button>
  <button onclick="tallafocs()">TALLAFOCS</button>
  <button onclick="dmz()">DMZ</button>
  <button onclick="switchs()">SWITCH</button>
  <button onclick="dhcp()">DHCP</button>
  <button onclick="wifi()">WIFI</button>
  <button onclick="portal()">PORTAL CAUTIU</button>
  <button class="btn-logout" onclick="window.top.location.href='/cgi-bin/logout.cgi'">🔒 Tancar sessió</button>
</div>

</body>
</html>

EOM


