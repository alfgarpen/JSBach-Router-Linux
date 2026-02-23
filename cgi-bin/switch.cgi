#!/bin/bash

echo "Content-Type:text/html;charset=utf-8"
echo ""

cat << EOM
<html>
<head>
<meta http-equiv="refresh" content="0; url=/cgi-bin/switch-estat.cgi">
</head>
<body>
Check <a href="/cgi-bin/switch-estat.cgi">here</a> if you are not redirected.
</body>
</html>
EOM
