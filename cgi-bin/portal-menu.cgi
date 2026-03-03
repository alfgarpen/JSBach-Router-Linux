#!/bin/bash

 source /usr/local/JSBach/conf/variables.conf

 /bin/cat << EOM

 <html>
 <head>
 <meta charset="utf-8">
 <style>
 body {
   font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Ubuntu, Cantarell, Arial, sans-serif;
   margin: 24px;
   background: radial-gradient(circle at top, #0f172a, #000);
   color: #e5e7eb;
 }
 .container { max-width: 500px; margin: auto; }
 h2 {
   background: linear-gradient(90deg, #0f172a, #020617);
   padding: 12px 16px;
   border-left: 5px solid #38bdf8;
   border-radius: 8px;
   font-weight: 700;
   color: #7dd3fc;
   box-shadow: 0 0 18px rgba(56, 189, 248, 0.25);
   margin-bottom: 20px;
 }
 .menu { display: flex; flex-direction: column; gap: 14px; }
 a { text-decoration: none; }
 .button {
   display: block;
   text-align: center;
   background: linear-gradient(135deg, #0284c7, #38bdf8);
   color: #020617;
   padding: 10px 18px;
   border-radius: 999px;
   font-weight: 800;
   box-shadow: 0 4px 12px rgba(56, 189, 248, 0.5);
   transition: transform 0.15s ease, box-shadow 0.15s ease;
 }
 .button:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(56, 189, 248, 0.8); }
 </style>
 </head>
 <body>
 <div class="container">
   <h2>Portal Cautivo</h2>

   <div class="menu">
     <a href="/cgi-bin/portal-estat.cgi" target="body">
       <div class="button">Estado</div>
     </a>

     <a href="/cgi-bin/portal-config.cgi" target="body">
       <div class="button">Configuración General</div>
     </a>

     <a href="/cgi-bin/portal-usuaris.cgi" target="body">
       <div class="button">Gestión de Usuarios</div>
     </a>

     <a href="/cgi-bin/portal-seguretat.cgi" target="body">
       <div class="button">Seguridad y Logs</div>
     </a>
   </div>
 </div>
 </body>
 </html>
 
EOM