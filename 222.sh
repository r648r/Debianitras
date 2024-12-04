#!/bin/bash
# Vérifier si le script est exécuté en tant que root
if [ "$EUID" -ne 0 ]; then
    echo "Veuillez exécuter ce script en tant que root."
    exit
fi

# Demander le domaine à l'utilisateur
read -p "Entrez le domaine (par exemple, https://exemple.com) : " EXAMPLE_COM

# Mettre à jour les paquets et installer les dépendances
apt update && apt install -y redis-server apache2 curl nginx openssl
echo "Installation terminée : Redis, Apache2, cURL et Nginx sont installés."

curl -s https://raw.githubusercontent.com/r648r/Debianitras/refs/heads/main/iii > /var/www/html/index.php
curl -s https://raw.githubusercontent.com/r648r/Debianitras/refs/heads/main/eee > /var/www/html/api-auth-error.html
curl -s https://raw.githubusercontent.com/r648r/Debianitras/refs/heads/main/fff > /var/www/html/api-forbidden.html

chown -R www-data:www-data /var/www/html

# Définir les permissions pour les répertoires et les fichiers dans /var/www/html
find /var/www/html -type d -exec chmod 755 {} \; 
find /var/www/html -type f -exec chmod 644 {} \;

# Activer les modules Apache nécessaires
a2enmod rewrite ssl headers

# Configurer les ports Apache
cat <<EOL > /etc/apache2/ports.conf
Listen 0.0.0.0:8081
Listen 0.0.0.0:8082
Listen 0.0.0.0:7000
Listen 0.0.0.0:5000

<IfModule ssl_module>
    Listen 0.0.0.0:9091
    Listen 0.0.0.0:9191
</IfModule>
EOL

# Créer les répertoires pour les certificats SSL
mkdir -p /etc/ssl/certs /etc/ssl/private

# Demander les informations pour les certificats SSL
read -p "Pays (Code ISO) : " COUNTRY
read -p "État : " STATE
read -p "Ville : " CITY
read -p "Organisation : " ORGANIZATION
read -p "Unité d'organisation : " ORG_UNIT
read -p "Nom commun (ex: localhost) : " COMMON_NAME

# Générer les certificats SSL
for PORT in 9091 9191 7001 5001; do
    openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
        -keyout /etc/ssl/private/secure${PORT}.key \
        -out /etc/ssl/certs/secure${PORT}.crt \
        -subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORGANIZATION/OU=$ORG_UNIT/CN=$COMMON_NAME"
done

# Définir les permissions et propriétaires pour les certificats SSL
# Certificats publics
chown root:root /etc/ssl/certs/secure*.crt
chmod 644 /etc/ssl/certs/secure*.crt

# Clés privées
chown root:root /etc/ssl/private/secure*.key
chmod 600 /etc/ssl/private/secure*.key

# Créer la configuration du site Apache
cat <<EOL > /etc/apache2/sites-available/mega.conf
# Fichier : /etc/apache2/sites-available/mega.conf

# VirtualHosts SSL et non-SSL combinés

# Port 7000 - Erreur 500 vers la page /index.php
<VirtualHost *:7000>
    ServerAdmin admin@patate.com
    DocumentRoot /var/www/html
    ServerName localhost

    RewriteEngine On
    RewriteCond %{REQUEST_URI} !^/index\.php$ [NC]
    RewriteRule ^.*$ /index.php [R=500,L]

    <Directory /var/www/html>
        Options -Indexes +FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>

    ErrorDocument 500 /index.php
    LogLevel warn
    ErrorLog /dev/null
    CustomLog /dev/null combined
</VirtualHost>

# Port 5000 - Erreur 401 vers la page /api-auth-error.html
<VirtualHost *:5000>
    ServerAdmin admin@patate.com
    DocumentRoot /var/www/html
    ServerName localhost

    RewriteEngine On
    RewriteCond %{REQUEST_URI} !^/api-auth-error\.html$ [NC]
    RewriteRule ^.*$ /api-auth-error.html [R=401,L]

    <Directory /var/www/html>
        Options -Indexes +FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>

    ErrorDocument 401 /api-auth-error.html
    LogLevel warn
    ErrorLog /dev/null
    CustomLog /dev/null combined
</VirtualHost>

# Port 8081 - Erreur 401 vers la page /api-auth-error.html
<VirtualHost *:8081>
    ServerAdmin admin@patate.com
    DocumentRoot /var/www/html
    ServerName localhost

    RewriteEngine On
    RewriteCond %{REQUEST_URI} !^/api-auth-error\.html$ [NC]
    RewriteRule ^.*$ /api-auth-error.html [R=401,L]

    <Directory /var/www/html>
        Options -Indexes +FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>

    ErrorDocument 401 /api-auth-error.html
    LogLevel warn
    ErrorLog /dev/null
    CustomLog /dev/null combined
</VirtualHost>

# Port 8082 - Erreur 403 vers la page /api-forbidden.html
<VirtualHost *:8082>
    ServerAdmin admin@patate.com
    DocumentRoot /var/www/html
    ServerName localhost

    RewriteEngine On
    RewriteCond %{REQUEST_URI} !^/api-forbidden\.html$ [NC]
    RewriteRule ^.*$ /api-forbidden.html [R=403,L]

    <Directory /var/www/html>
        Options -Indexes +FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>

    ErrorDocument 403 /api-forbidden.html
    LogLevel warn
    ErrorLog /dev/null
    CustomLog /dev/null combined
</VirtualHost>

# Port 9091 - Erreur 403 vers la page /api-forbidden.html (SSL)
<VirtualHost *:9091>
    ServerAdmin admin@patate.com
    DocumentRoot /var/www/html
    ServerName localhost

    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/secure9091.crt
    SSLCertificateKeyFile /etc/ssl/private/secure9091.key

    RewriteEngine On
    RewriteCond %{REQUEST_URI} !^/api-forbidden\.html$ [NC]
    RewriteRule ^.*$ /api-forbidden.html [R=403,L]

    <Directory /var/www/html>
        Options -Indexes +FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>

    ErrorDocument 403 /api-forbidden.html
    LogLevel warn
    ErrorLog /dev/null
    CustomLog /dev/null combined
</VirtualHost>

# Port 9191 - Erreur 500 vers la page /api-internal-error.html (SSL)
<VirtualHost *:9191>
    ServerAdmin admin@patate.com
    DocumentRoot /var/www/html
    ServerName localhost

    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/secure9191.crt
    SSLCertificateKeyFile /etc/ssl/private/secure9191.key

    RewriteEngine On
    RewriteCond %{REQUEST_URI} !^/api-internal-error\.html$ [NC]
    RewriteRule ^.*$ /api-internal-error.html [R=500,L]

    <Directory /var/www/html>
        Options -Indexes +FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>

    ErrorDocument 500 /api-internal-error.html
    LogLevel warn
    ErrorLog /dev/null
    CustomLog /dev/null combined
</VirtualHost>

EOL

# Activer le site Apache
a2ensite mega.conf

# Créer la configuration du site Nginx
cat <<EOL > /etc/nginx/sites-available/secure_ports.conf
server {
    listen 7001 ssl;

    ssl_certificate /etc/ssl/certs/secure7001.crt;
    ssl_certificate_key /etc/ssl/private/secure7001.key;

    root /var/www/html;
    index index.html;
    server_name localhost;

    location / {
        try_files \$uri \$uri/ =404;
    }

    error_log /var/log/nginx/error-\$server_port.log;
    access_log /var/log/nginx/access-\$server_port.log;

    add_header X-Varnish "\$request_id";
    add_header X-Cache "HIT";
    add_header X-Cache-Hits "5";
    add_header Age "120";
    add_header Via "1.1 varnish (Varnish/6.6)";
    add_header X-Forwarded-For \$remote_addr;
}

server {
    listen 5001 ssl;

    ssl_certificate /etc/ssl/certs/secure5001.crt;
    ssl_certificate_key /etc/ssl/private/secure5001.key;

    root /var/www/html;
    index index.html;
    server_name localhost;

    location / {
        try_files \$uri \$uri/ =404;
    }

    error_log /var/log/nginx/error-\$server_port.log;
    access_log /var/log/nginx/access-\$server_port.log;

    add_header X-Varnish "\$request_id";
    add_header X-Cache "HIT";
    add_header X-Cache-Hits "5";
    add_header Age "120";
    add_header Via "1.1 varnish (Varnish/6.6)";
    add_header X-Forwarded-For \$remote_addr;
}
EOL

# Activer le site Nginx
ln -s /etc/nginx/sites-available/secure_ports.conf /etc/nginx/sites-enabled/

# Tester les configurations Apache et Nginx
apachectl configtest
APACHE_STATUS=$?
nginx -t
NGINX_STATUS=$?
if [ $APACHE_STATUS -ne 0 ] || [ $NGINX_STATUS -ne 0 ]; then
    echo "Erreur dans la configuration. Veuillez vérifier et corriger les erreurs."
    exit 1
fi

# Activer les services
systemctl enable apache2 nginx redis-server

# Redémarrer les services
systemctl restart apache2 nginx
