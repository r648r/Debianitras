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

# Créer les répertoires pour les certificats SSL
mkdir -p /etc/ssl/certs /etc/ssl/private

# Générer les certificats SSL
for PORT in 9091 9191 7001 5001; do
    openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
        -keyout /etc/ssl/private/secure${PORT}.key \
        -out /etc/ssl/certs/secure${PORT}.crt \
        -subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORGANIZATION/OU=$ORG_UNIT/CN=$COMMON_NAME"
done


cat <<EOL > /etc/nginx/nginx.conf
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
        worker_connections 768;
}
http {
        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;
        types_hash_max_size 2048;
        server_tokens off;
        more_set_headers "Server: Nginx/0.6.36 (Debian)";
        include /etc/nginx/mime.types;
        default_type application/octet-stream;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
        ssl_prefer_server_ciphers on;
        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;
        gzip on;
        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
}
EOL


cat <<EOL > /etc/nginx/sites-available/notssl.conf
server {
    listen 7000;
    server_name localhost;

    root /var/www/html;
    index index.php;

    location / {
        rewrite ^.*$ /index.php redirect;
    }

    add_header X-Powered-By "Symfony 2.7 / PHP 5.4.0";
    add_header Server "nginx";

    error_page 500 /index.php;

    access_log off;
    error_log /dev/null warn;
}

server {
    listen 5000;
    server_name localhost;

    root /var/www/html;

    location / {
        rewrite ^.*$ /api-auth-error.html redirect;
    }

    error_page 401 /api-auth-error.html;

    access_log off;
    error_log /dev/null warn;
}

server {
    listen 8888;
    server_name localhost;

    root /var/www/html;

    location / {
        rewrite ^.*$ /api-auth-error.html redirect;
    }

    error_page 401 /api-auth-error.html;

    access_log off;
    error_log /dev/null warn;
}

server {
    listen 8989;
    server_name localhost;

    root /var/www/html;

    location / {
        rewrite ^.*$ /api-forbidden.html redirect;
    }

    error_page 403 /api-forbidden.html;

    access_log off;
    error_log /dev/null warn;
}

server {
    listen 9091 ssl;
    server_name localhost;

    ssl_certificate /etc/ssl/certs/secure9091.crt;
    ssl_certificate_key /etc/ssl/private/secure9091.key;

    root /var/www/html;

    location / {
        rewrite ^.*$ /api-forbidden.html redirect;
    }

    error_page 403 /api-forbidden.html;

    access_log off;
    error_log /dev/null warn;
}

server {
    listen 9191 ssl;
    server_name localhost;

    ssl_certificate /etc/ssl/certs/secure9191.crt;
    ssl_certificate_key /etc/ssl/private/secure9191.key;

    root /var/www/html;

    location / {
        rewrite ^.*$ /api-internal-error.html redirect;
    }

    error_page 500 /api-internal-error.html;

    access_log off;
    error_log /dev/null warn;
}

EOL

# Créer la configuration du site Nginx
cat <<EOL > /etc/nginx/sites-available/ssl.conf
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
ln -s /etc/nginx/sites-available/ssl.conf /etc/nginx/sites-enabled/
ln -s /etc/nginx/sites-available/notssl.conf /etc/nginx/sites-enabled/

curl -s https://raw.githubusercontent.com/r648r/Debianitras/refs/heads/main/iii > /var/www/html/index.html
curl -s https://raw.githubusercontent.com/r648r/Debianitras/refs/heads/main/eee > /var/www/html/api-auth-error.html
curl -s https://raw.githubusercontent.com/r648r/Debianitras/refs/heads/main/fff > /var/www/html/api-forbidden.html

sed -i 's/^bind 127\.0\.0\.1 ::1$/bind 0.0.0.0/' /etc/redis/redis.conf

# Activer les services
systemctl enable apache2 nginx redis-server

# Redémarrer les services
systemctl restart apache2 nginx

