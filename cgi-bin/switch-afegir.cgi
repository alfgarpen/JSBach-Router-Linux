#!/bin/bash

source /usr/local/JSBach/conf/variables.conf 2>/dev/null

echo "Content-Type:text/html;charset=utf-8"
echo ""

cat << EOM
<html>
<head>
<style>
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
               Roboto, Ubuntu, Cantarell, Arial, sans-serif;
  margin: 24px;
  background: radial-gradient(circle at top, #0f172a, #000);
  color: #e5e7eb;
}

h2 {
  background: linear-gradient(90deg, #0f172a, #020617);
  padding: 12px 16px;
  border-left: 5px solid #22d3ee;
  border-radius: 8px;
  color: #7dd3fc;
  margin-bottom: 20px;
}

form {
  background: rgba(15, 23, 42, 0.9);
  padding: 30px;
  border-radius: 12px;
  max-width: 500px;
  margin: auto;
  box-shadow: 0 0 25px rgba(0,0,0,0.6);
}

label {
  display: block;
  margin-bottom: 8px;
  color: #38bdf8;
  font-weight: 600;
}

input[type="text"], input[type="password"] {
  width: 100%;
  padding: 12px;
  margin-bottom: 20px;
  border: 1px solid #334155;
  border-radius: 6px;
  background: #020617;
  color: #e5e7eb;
}

input[type="submit"] {
  background: linear-gradient(135deg, #0284c7, #22d3ee);
  color: #020617;
  border: none;
  padding: 12px 24px;
  border-radius: 999px;
  font-weight: 800;
  cursor: pointer;
  width: 100%;
  transition: transform 0.1s;
}

input[type="submit"]:hover {
  transform: scale(1.02);
}
</style>
</head>
<body>
<h2>Afegir Switch</h2>

<form action="/cgi-bin/switch-guardar.cgi" method="GET">
  <label for="nom">Nom del Switch:</label>
  <input type="text" id="nom" name="nom" required placeholder="Ex: Switch-Principal">

  <label for="ip">Adreça IP:</label>
  <input type="text" id="ip" name="ip" required placeholder="Ex: 192.168.1.10">

  <label for="user">Usuari:</label>
  <input type="text" id="user" name="user" required placeholder="admin">

  <label for="pass">Contrasenya:</label>
  <input type="password" id="pass" name="pass" required placeholder="secret">

  <input type="submit" value="Guardar Switch">
</form>

<div style="text-align:center; margin-top:20px;">
  <a href="/cgi-bin/switch-estat.cgi" style="color: #38bdf8;">Tornar al menú</a>
</div>

</body>
</html>
EOM
