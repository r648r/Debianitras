#!/bin/bash
if [ "$EUID" -ne 0 ]; then
    echo "Veuillez exécuter ce script en tant que root."
    exit
fi

HONEYPOT_DIR="/opt/redis_honeypot"
HONEYPOT_USER="redis_honeypot"
REDIS_CONF="/etc/redis/redis_honeypot.conf"
DUMP_FILE="$HONEYPOT_DIR/dump.rdb"
REDIS_PORT="6379"
REDIS_PASSWORD="SuperWeakPassword123"
read -p "Pays (Code ISO) : " COUNTRY
read -p "État : " STATE
read -p "Ville : " CITY
read -p "Organisation : " ORGANIZATION
read -p "Unité d'organisation : " ORG_UNIT
read -p "Nom commun (ex: localhost) : " COMMON_NAME

# Mettre à jour les paquets et installer les dépendances
apt update && apt install -y redis-server apache2 curl nginx openssl
echo "Installation terminée : Redis, Apache2, cURL et Nginx sont installés."

# Chemins et configurations
# Fonction pour afficher les messages
log() {
    echo -e "\e[1;32m[INFO]\e[0m $1"
}

error() {
    echo -e "\e[1;31m[ERROR]\e[0m $1"
    exit 1
}

# Vérifier si le script est exécuté en tant que root
if [ "$(id -u)" -ne 0 ]; then
    error "Ce script doit être exécuté avec les droits root."
fi

# Étape 1 : Installer Redis
log "Installation de Redis..."
apt update && apt install -y redis-server || error "Échec de l'installation de Redis."

# Étape 2 : Créer l'utilisateur et le répertoire pour le honeypot
log "Création de l'utilisateur et du répertoire pour le honeypot..."
useradd -r -s /bin/false $HONEYPOT_USER || log "Utilisateur existant."
mkdir -p $HONEYPOT_DIR
chown $HONEYPOT_USER:$HONEYPOT_USER $HONEYPOT_DIR

# Étape 3 : Configurer Redis pour le honeypot
log "Configuration de Redis pour le honeypot..."
cat > $REDIS_CONF <<EOL
bind 0.0.0.0
protected-mode no
port $REDIS_PORT
requirepass "$REDIS_PASSWORD"
dir $HONEYPOT_DIR
dbfilename "dump.rdb"

# Désactiver les commandes critiques
rename-command CONFIG ""
rename-command SHUTDOWN ""
rename-command FLUSHALL ""
rename-command FLUSHDB ""
rename-command DEBUG ""

# Simulations crédibles
notify-keyspace-events KEA
logfile /dev/null
maxmemory 50mb
maxclients 10
EOL

# Étape 4 : Générer un fichier dump.rdb crédible
log "Génération de données crédibles pour un e-commerce..."
# Démarrer Redis temporairement
redis-server --daemonize yes --port 6380 --requirepass "$REDIS_PASSWORD"
sleep 2

# Ajouter des données factices pour un e-commerce
redis-cli -p 6380 -a "$REDIS_PASSWORD" <<EOL
SET "user:1001" "Raphael Jamis"
SET "user:1002" "Jane Dedand"
SET "user:1003" "Alice Johnson"
HSET "product:2001" "name" "Laptop" "price" "1200" "stock" "45"
HSET "product:2002" "name" "Smartphone" "price" "800" "stock" "150"
HSET "product:2003" "name" "Headphones" "price" "150" "stock" "80"
LPUSH "orders" '{"order_id": "3001", "user": "1001", "product": "2001", "quantity": "1", "total": "1200"}'
LPUSH "orders" '{"order_id": "3002", "user": "1003", "product": "2002", "quantity": "2", "total": "1600"}'
SET "stats:total_sales" "2800"
SET "stats:active_users" "150"
EOL

# Sauvegarder les données dans dump.rdb
log "Sauvegarde des données dans dump.rdb..."
redis-cli -p 6380 -a "$REDIS_PASSWORD" SAVE
mv /var/lib/redis/dump.rdb $DUMP_FILE
chown $HONEYPOT_USER:$HONEYPOT_USER $DUMP_FILE

# Arrêter Redis temporaire
redis-cli -p 6380 -a "$REDIS_PASSWORD" SHUTDOWN
sleep 2

# Étape 5 : Configurer le service systemd pour le honeypot
log "Configuration du service systemd pour le honeypot..."
cat > /etc/systemd/system/redis_honeypot.service <<EOL
[Unit]
Description=Redis Honeypot Service
After=network.target

[Service]
ExecStart=/usr/bin/redis-server $REDIS_CONF
User=$HONEYPOT_USER
Group=$HONEYPOT_USER
RuntimeDirectory=redis_honeypot
ProtectSystem=full
ProtectHome=yes
NoNewPrivileges=yes
PrivateTmp=yes
ReadOnlyPaths=/
ReadWritePaths=$HONEYPOT_DIR

[Install]
WantedBy=multi-user.target
EOL

# Étape 6 : Activer et démarrer le service
log "Activation et démarrage du honeypot Redis..."
systemctl daemon-reload
systemctl enable redis_honeypot
systemctl start redis_honeypot

# Vérification du service
systemctl status redis_honeypot --no-pager

log "Honeypot Redis configuré avec succès !"
log "Adresse : 0.0.0.0:$REDIS_PORT"
log "Mot de passe : $REDIS_PASSWORD"

# Activer les modules Apache nécessaires
a2enmod rewrite ssl headers

# Configurer les ports Apache
cat <<EOL > /etc/apache2/ports.conf
Listen 0.0.0.0:8888
Listen 0.0.0.0:8989
Listen 0.0.0.0:7000
Listen 0.0.0.0:5000

<IfModule ssl_module>
    Listen 0.0.0.0:9091
    Listen 0.0.0.0:9191
</IfModule>
EOL

# Créer les répertoires pour les certificats SSL
mkdir -p /etc/ssl/certs /etc/ssl/private

# Générer les certificats SSL
for PORT in 9091 9191 7001 5001; do
    openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
        -keyout /etc/ssl/private/secure${PORT}.key \
        -out /etc/ssl/certs/secure${PORT}.crt \
        -subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORGANIZATION/OU=$ORG_UNIT/CN=$COMMON_NAME"
done

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
    Header set X-Powered-By "Symfony 2.7 / PHP 5.4.0" 
    Header set Server "Apache/2.2.15 (Unix)"

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

# Port 8888 - Erreur 401 vers la page /api-auth-error.html
<VirtualHost *:8888>
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

# Port 8989 - Erreur 403 vers la page /api-forbidden.html
<VirtualHost *:8989>
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
    add_header X-Powered-By "PHP/5.4.0"; 
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
    add_header X-Powered-By "PHP/5.4.0"; 
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

curl -s https://raw.githubusercontent.com/r648r/Debianitras/refs/heads/main/iii > /var/www/html/index.php
curl -s https://raw.githubusercontent.com/r648r/Debianitras/refs/heads/main/eee > /var/www/html/api-auth-error.html
curl -s https://raw.githubusercontent.com/r648r/Debianitras/refs/heads/main/fff > /var/www/html/api-forbidden.html

sed -i 's/^bind 127\.0\.0\.1 ::1$/bind 0.0.0.0/' /etc/redis/redis.conf

# Activer les services
systemctl enable apache2 nginx redis-server

# Redémarrer les services
systemctl restart apache2 nginx

