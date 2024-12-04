#!/bin/bash
# Vérifier si le script est exécuté en tant que root
if [ "$EUID" -ne 0 ]; then
    echo "Veuillez exécuter ce script en tant que root."
    exit
fi

# Demander le domaine à l'utilisateur
read -p "Entrez le domaine (par exemple, https://exemple.com) : " EXAMPLE_COM

apt update && apt install -y redis-server apache2 curl nginx openssl

curl -s https://raw.githubusercontent.com/r648r/Debianitras/refs/heads/main/iii > /var/www/html/index.php
curl -s https://raw.githubusercontent.com/r648r/Debianitras/refs/heads/main/eee > /var/www/html/api-auth-error.html
curl -s https://raw.githubusercontent.com/r648r/Debianitras/refs/heads/main/fff > /var/www/html/api-forbidden.html

chown -R www-data:www-data /var/www/html

# Définir les permissions pour les répertoires et les fichiers dans /var/www/html
find /var/www/html -type d -exec chmod 755 {} \; 
find /var/www/html -type f -exec chmod 644 {} \;

# Activer les modules Apache nécessaires
a2enmod rewrite ssl headers
# Configurer Apache ports.conf
echo "Configuration d'Apache ports.conf..."
cat <<EOL | sudo tee /etc/apache2/ports.conf > /dev/null
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
echo "Création des répertoires pour les certificats SSL..."
sudo mkdir -p /etc/ssl/certs /etc/ssl/private

# Demander les informations pour les certificats SSL
echo "Veuillez entrer les informations pour les certificats SSL :"
read -p "Pays (Code ISO) : " COUNTRY
read -p "État : " STATE
read -p "Ville : " CITY
read -p "Organisation : " ORGANIZATION
read -p "Unité d'organisation : " ORG_UNIT
read -p "Nom commun (ex: localhost) : " COMMON_NAME

# Générer les certificats SSL pour les ports corrects
echo "Génération des certificats SSL..."
for PORT in 9091 9191 7000 5000; do
    sudo openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
        -keyout /etc/ssl/private/secure${PORT}.key \
        -out /etc/ssl/certs/secure${PORT}.crt \
        -subj "/C=${COUNTRY}/ST=${STATE}/L=${CITY}/O=${ORGANIZATION}/OU=${ORG_UNIT}/CN=${COMMON_NAME}"
done

# Définir les permissions et propriétaires pour les certificats SSL
echo "Définition des permissions pour les certificats SSL..."
# Certificats publics
sudo chown root:root /etc/ssl/certs/secure*.crt
sudo chmod 644 /etc/ssl/certs/secure*.crt

# Clés privées
sudo chown root:root /etc/ssl/private/secure*.key
sudo chmod 600 /etc/ssl/private/secure*.key

# Créer la configuration du site Apache
echo "Création de la configuration du site Apache..."
cat <<EOL | sudo tee /etc/apache2/sites-available/mega.conf > /dev/null
# Fichier : /etc/apache2/sites-available/mega.conf

# Définir le ServerName globalement
ServerName localhost

# VirtualHosts SSL et non-SSL combinés

# Port 7000 - Erreur 500 vers la page /index.php
<VirtualHost *:7000>
    ServerAdmin admin@patate.com
    DocumentRoot /var/www/html
    ServerName localhost

    RewriteEngine On
    RewriteCond %{REQUEST_URI} !^/index\.php$ [NC]
    RewriteRule ^.*\$ /index.php [R=500,L]

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
    RewriteRule ^.*\$ /api-auth-error.html [R=401,L]

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
    RewriteRule ^.*\$ /api-auth-error.html [R=401,L]

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
    RewriteRule ^.*\$ /api-forbidden.html [R=403,L]

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
    RewriteRule ^.*\$ /api-forbidden.html [R=403,L]

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
    RewriteRule ^.*\$ /api-internal-error.html [R=500,L]

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
echo "Activation du site Apache 'mega'..."
sudo a2ensite mega.conf

# Créer la configuration du site Nginx
echo "Création de la configuration du site Nginx..."
cat <<EOL | sudo tee /etc/nginx/sites-available/secure_ports.conf > /dev/null
# Configuration pour le port 7001 avec SSL
server {
    listen 7001 ssl;

    # Certificats pour SSL
    ssl_certificate /etc/ssl/certs/secure7001.crt;
    ssl_certificate_key /etc/ssl/private/secure7001.key;

    # Répertoire racine et index
    root /var/www/html;
    index index.html;

    # Configuration de base pour le port 7001
    server_name localhost;

    location / {
        try_files $uri $uri/ =404;
    }

    # Logs pour débogage
    error_log /var/log/nginx/error-7001.log;
    access_log /var/log/nginx/access-7001.log;
}

# Configuration pour le port 5001 avec SSL
server {
    listen 5001 ssl;

    # Certificats pour SSL
    ssl_certificate /etc/ssl/certs/secure5001.crt;
    ssl_certificate_key /etc/ssl/private/secure5001.key;

    # Répertoire racine et index
    root /var/www/html;
    index index.html;

    # Configuration de base pour le port 5001
    server_name localhost;

    location / {
        try_files $uri $uri/ =404;
    }

    # Logs pour débogage
    error_log /var/log/nginx/error-5001.log;
    access_log /var/log/nginx/access-5001.log;
}
EOL

# Activer le site Nginx en évitant l'erreur si le lien existe déjà
echo "Activation du site Nginx 'secure_ports'..."
if [ ! -L /etc/nginx/sites-enabled/secure_ports.conf ]; then
    sudo ln -s /etc/nginx/sites-available/secure_ports.conf /etc/nginx/sites-enabled/
else
    echo "Le lien symbolique '/etc/nginx/sites-enabled/secure_ports.conf' existe déjà. Skipping."
fi

# Tester les configurations Apache et Nginx
echo "Test des configurations Apache et Nginx..."
if sudo apachectl configtest; then
    echo "Configuration Apache OK."
    APACHE_STATUS=0
else
    echo "Erreur dans la configuration Apache."
    APACHE_STATUS=1
fi

if sudo nginx -t; then
    echo "Configuration Nginx OK."
    NGINX_STATUS=0
else
    echo "Erreur dans la configuration Nginx."
    NGINX_STATUS=1
fi

if [ "$APACHE_STATUS" -ne 0 ] || [ "$NGINX_STATUS" -ne 0 ]; then
    echo "Erreur dans la configuration. Veuillez vérifier et corriger les erreurs."
    exit 1
fi

# Activer et démarrer les services Apache et Nginx
echo "Activation et démarrage des services Apache et Nginx..."
sudo systemctl enable apache2
sudo systemctl enable nginx
sudo systemctl restart apache2
sudo systemctl restart nginx

echo "Configuration terminée avec succès."
