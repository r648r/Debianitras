# 🤼 Procédure takedown clone e-commerce

## Vocabulaire

- **DSA** (Digital Services Act) : Régulation européenne visant à sécuriser l'environnement en ligne et à encadrer les grandes plateformes numériques.
- **Dark SEO** : Le black hat SEO est un ensemble de procédés et d’automatisations visant à exploiter les failles des algorithmes pour manipuler les résultats en sa faveur. Les sites s’adonnant à de telles pratiques peuvent se retrouver du jour au lendemain en première page Google, voire en première position. [...] Tous ceux qui s’en sont servis pour grimper artificiellement dans les SERPs sont alors démasqués par Google et sanctionnés. [Exemple d'outils idéale](https://search.google.com/search-console/welcome?hl=fr)
- **Hosting** **provider** (founisseur d'hébergement) : Service ou entreprise fournissant l'infrastructure physique pour stocker des sites web ou des données en ligne.
- **[httpx](https://github.com/projectdiscovery/httpx)** : Outil réalisé en go multi-usage permettant d'effectuer des requêtes HTTP, en utilisant la bibliothèque retryablehttp.
- **Registrars** (bureaux d'enregistrement de nom de domaine) : Entités autorisées à enregistrer et gérer des noms de domaine sur Internet.
- **Scammer** (escroc) : Individu utilisant des techniques frauduleuses pour tromper les autres et obtenir des informations ou de l'argent.
- **Scamma** (template d'escroquerie) : template utilisé et revendu entre scammer pour arnaquer simplement.
- **Takedown** (processus de suppression de site) : Processus consistant à retirer un contenu en ligne suite à une demande officielle ou pour non-respect des règles.
- **User-agent** : Information envoyée par un navigateur ou une application, identifiant l'appareil ou logiciel utilisé pour accéder à un service.
- **Whois** : Protocole utilisé pour obtenir des informations publiques sur l'enregistrement d'un domaine ou d'une adresse IP.

---

## Méthodologie

### Étape 1 Identifier et documenter les clones

- Se mettre sur une IP publique autre que celle de celle de votre entreprise (Partage de connection / VPN / Proxy / Routeur 4G / VPS ...)
  - Votre scan sera sinon bloquer par les scammers
  - Changer votre user agent de préférence avec un user-agent mobile (apple, android, qui permutte entre chaque requète)
  - Utiliser un navigateur dans un environnement virtualisé / dockerisé, pour ne pas donner son fingerprint web qui pour rappel nous identifie de manière unique.

- Rassemblez des preuves (Cette étape est traité dans ce document :  ## Scanning)
  - Identifiez l’hébergeur : Utilisez des protocoles tels que `Whois` pour déterminer l’hébergeur du site clone
  - Faire une énumération DNS (subfinder, bbot, oneForAll, dnstwist)
  - Centralisé cette énumération de manière prore
  - Utilisé [httpx](https://github.com/projectdiscovery/httpx) pour obtenir des preuves.
    - [Cette étape est traité dans une autre procédure dédier => (Pour les gens du technique)]()
  - Mettre en forme ces preuves.

- Utilisez [Wayback Machine](http://wayback.archive.org/) pour capturer des versions horodatées des pages les plus pertinantes, offrant des preuves historiques au cas où le contenu serait modifié ou supprimé plus tard.

#### Important

Il est impératif d'avoir au minima obtenue les information suivante pour passer à la suite :

- **Faire des replace de chaque variable dans le template qui suit**
- **URL(s)/IP incriminée(s)** : Listez toutes les URLs/IP des sites clones hébergés par l’hébergeur/proxy identifié.
- **Preuves** : Joignez des captures d’écran et des liens comparatifs avec votre site original.
- **Explication** : Décrivez de manière claire comment le contenu a été cloné et viole vos droits de propriété intellectuelle.

---

### Étape 2 Signalement à l’hébergeur/CDN/Proxy HTTPS du site clone et au registrar du domaine

Accédez à la plateforme de signalement d’abus de l’hébergeur :

- [Hosting provider takedown Cheat Sheet](https://community.bolster.ai/tag/hosting-provider)
- [Registrar DNS takedown Cheat Sheet](https://community.bolster.ai/c/registrar-phishing-takedowns/7)

#### Exemples d’hébergeurs populaires pour ce type d'usage

- **Alibaba Cloud** : [Alibaba Cloud Abuse Report](https://www.alibabacloud.com/en/report?_p_lc=1) => ([tuto](https://community.bolster.ai/t/how-to-article-takedown-phishing-urls-hosted-on-alibaba/39))
- **Cloudflare** : [Cloudflare abuse form](https://abuse.cloudflare.com/) => ([tuto](https://community.bolster.ai/t/help-with-removing-a-phishing-page-on-cloudflare/42))
- **DigitalOcean** : [DigitalOcean abuse form](https://www.digitalocean.com/company/contact/abuse) => ([tuto](https://community.bolster.ai/t/how-to-article-takedown-phishing-urls-hosted-on-digitalocean/183))
- **Amazon AWS** : [AWS abuse form](https://support.aws.amazon.com/#/contacts/report-abuse) => ([tuto](https://community.bolster.ai/t/how-to-do-a-phishing-takedown-on-amazon-aws-hosting/31))
- **OVHcloud** : [OVH abuse form](https://www.ovhcloud.com/en/abuse/) => ([tuto](https://community.bolster.ai/t/how-to-article-takedown-phishing-urls-hosted-on-ovh-hosting/34))
- **Google Cloud Platform** :[Google abuse form](https://support.google.com/code/contact/cloud_platform_report) => ([tuto](https://community.bolster.ai/t/google-hosting-services/49))

---

### Étape 3 Désindexation via Google Search et signalement des annonces publicitaires associer a l'ecommerce

- Ces 3 signalements sont complémentaire ils permettes le non référencement et bloque leur campagne de Dark SEO ()
  - [Google Search Central Reporting](https://developers.google.com/search/help/report-quality-issues?hl=fr)
  - [Faire un signalement Google ADs](https://support.google.com/legal/troubleshooter/1114905#ts=9814647)
  - [Faire un signalement Google Search](https://support.google.com/legal/troubleshooter/1114905#ts=9814647)

--

### Étape 4 Mettre la pression

Le plus important durant cette étape c'est de mettre le plus de préssion possible !!

#### Que doit t on soumettre ?

- Preuves : (captures d’écran, URLs des sites e-commerce frauduleux, et autres documents pertinents).
- Indiquez clairement la nature de la fraude, expliquant comment ces sites volent des clients en usurpant l’identité de votre entreprise. Par exemple en recopiant l'apparence d’un véritable site e-commerce et en collectant frauduleusement des informations de paiement ou des commandes.
- Lumen garantit une transparence avec une archive publique des signalements.
- Décrivez comment le site trompe les utilisateurs, par exemple en recopiant l'apparence d’un véritable site e-commerce et en collectant frauduleusement des informations de paiement ou des commandes.

- **Service gratuit** :
  - [Lumen Database](https://lumendatabase.org/) : Lumen garantit une transparence avec une archive publique des signalements. (Recommandé et utilisé par google)
  - [NetBeacon Reporting](https://netbeacon.org/) : "One Mission: Reduce DNS Abuse"
  - [FTC Report Fraud](https://reportfraud.ftc.gov/) : Pour maximiser la prise en compte
  - Mettre les liens dans [PhishReport](https://phish.report/) pour un signalement supplémentaire

## Mail template

- **Fournissez les informations suivantes** :
  - **URL des clones** : Les sites que vous souhaitez désindexer.
  - **Preuves** : Des captures d’écran et des liens démontrant le clonage du contenu.
  - **Déclaration sous serment** : Affirmez que vous êtes le propriétaire légitime du contenu cloné, sous peine de sanctions légales.

```text
Subject: Urgent Takedown Request for Cloned Website on [Platform Name]
Dear [Platform Support Team],
 
I am writing to report cloned websites hosted on your platform that infringe on our copyright and are being used for fraudulent activities, impersonating our e-commerce site to scam customers.
 
Details:
Original Website: [e.g., test.com]
Infringing URLs:
- [clone1.com]
- [clone2.com]
 
These sites violate our intellectual property under [applicable copyright law] and are damaging our brand while defrauding customers. We kindly request their immediate removal.
In accordance with Article 16 of the Digital Services Act (source), please find the following information:
(a) A sufficiently substantiated explanation of the reasons why the individual or entity alleges the information in question to be illegal content;
(b) A clear indication of the exact electronic location of that information, such as the exact URL or URLs, and, where necessary, additional information enabling the identification of the illegal content adapted to the type of content and to the specific type of hosting service;
(c) The name and email address of the individual or entity submitting the notice, except in the case of information considered to involve one of the offences referred to in Articles 3 to 7 of Directive 2011/93/EU;
Contact:
   - Name: [Your Name]
   - Email: [Your email]
(d) A statement confirming the bona fide belief of the individual or entity submitting the notice that the information and allegations contained therein are accurate and complete.
   I, [Your Name], hereby affirm that I have a bona fide belief that the information contained in this notice is accurate and complete to the best of my knowledge.
https://www.eu-digital-services-act.com/Digital_Services_Act_Article_16.html
 
We kindly request a confirmation of the takedown. Should you need further information, feel free to contact me.
Thank you for your attention to this matter.
Best regards,
[Your Full Name]
[Your Position]
[Your Company]
[Your Phone Number]
[Your email]
```

## Scanning

### Conseil

Ne pas bourriner comme un cochon, tu vas foiré tes scans
![alt text](image-.png)

### Problemes

1. **Anti-DDOs**

    - Il sera souvent difficile de faire du port scanning et surement pas très utile. L'attaquant utilise dans 99% des cas un proxy https chez un anti-ddos comme cloudfare ou autre anti DDOS provider
    - Scanner les port cloudfare va simplement nous aider à nous faire rate-limite en ayant obtenue aucune preuve.
    - Pour vous donner un ordre d'idée
    - [Cloudfare : pages.dev et workers.dev](https://community.bolster.ai/t/phishing-and-scams-on-cloudflare-pages-dev-and-workers-dev-domains/188)
    - [Service pas trop chère le top pour un attaquant : Gestion des bots par Cloudflare](https://www.cloudflare.com/fr-fr/application-services/products/bot-management/)

2. **User-agent**

    - On nous affiche ici une 500 alors que le status de la requète est 200. Cela a pour but d'évité au scammer se faire crawl par des debutants.

        - **Sans personnalisé UA**

        ```bash
        curl -D - https://nozfrance.ddd.com
        ```

        ```bash
        # réponse HTTP
        HTTP/2 200
        date: Tue, 22 Oct 2024 21:45:13 GMT
        content-type: text/html; charset=utf-8
        vary: Accept-Encoding
        execution-time: 0.0226709843
        trace_id: FCEE0242-B868-3BAB-362F-F6BBE21637A1
        set-cookie: oemsaas_global_visit_id=3A14EC6D-69C8-DE92-9553-8F3B039FB84D; expires=Fri, 20-Oct-2034 21:45:13 GMT; Max-Age=315360000; path=/
        cf-cache-status: DYNAMIC
        set-cookie: oemsaas_checkout_visit_id=7BA6CC5C-549E-8A63-D0A4-FD9349F9BA8C; expires=Fri, 20-Oct-2034 21:45:13 GMT; Max-Age=315360000; path=/
        set-cookie: oemsaas_global_visit_session=F3A9575B-AAA0-6233-2988-F19FCE8B4130; expires=Wed, 23-Oct-2024 21:45:13 GMT; Max-Age=86400; path=/
        set-cookie: PHPSESSID=a65b85b0144ff7426b3dfbd51a8e6f82; path=/
        set-cookie: __cf_bm=svpIlW60qChhalRFBcIbs8GPQ3dnVFSUy.b50s2eInw-1729633513-1.0.1.1-oZNxJDy2EfHbuzy7s0HfvzWa43gzID7wO0eIX7o8xXbimJNKK58Xnc_wU2mtfDP.GhB543OfWPLlmx2e2Hz.zg; path=/; expires=Tue, 22-Oct-24 22:15:13 GMT; domain=.nozfrance.ddd.com; HttpOnly; Secure; SameSite=None
        server: cloudflare
        cf-ray: 8d6cac513d55d120-CDG
        alt-svc: h3=":443"; ma=86400

        <html>
        <head><title>500 Internal Server Error</title></head>
        <body>
        <center><h1>500 Internal Server Error</h1></center>
        <hr><center>nginx/1.20.1</center>
        <script type='text/javascript'> var execution_time = 0.0226709843; </script></body>
        </html>%
        ```

        - **En personnalisant UA**

        ```bash
        curl -D - "https://nozfrance.ddd.com" -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        ```

        ```bash
        HTTP/2 200
        date: Tue, 22 Oct 2024 21:47:05 GMT
        content-type: text/html; charset=utf-8
        vary: Accept-Encoding
        set-cookie: _fbs_fbp=fb.1.1729633625029.4160003050; expires=Mon, 20-Jan-2025 21:47:05 GMT; Max-Age=7776000; path=/
        execution-time: 0.0756330490
        trace_id: 67A05EB6-FEA7-CFEA-BED4-AC6BBCF36A5A
        cf-cache-status: DYNAMIC
        set-cookie: oemsaas_global_visit_id=E201B5E5-BEDD-1E6A-CADE-ED6BEC4CE593; expires=Fri, 20-Oct-2034 21:47:05 GMT; Max-Age=315360000; path=/
        set-cookie: oemsaas_checkout_visit_id=72C29F71-6BCA-B1D6-C98B-146FEB9C43C6; expires=Fri, 20-Oct-2034 21:47:05 GMT; Max-Age=315360000; path=/
        set-cookie: oemsaas_global_visit_session=763F7CA8-0ED8-7D47-CB68-ED9A8D9BE49E; expires=Wed, 23-Oct-2024 21:47:05 GMT; Max-Age=86400; path=/
        set-cookie: utm_source=direct; expires=Thu, 21-Nov-2024 21:47:05 GMT; Max-Age=2592000; path=/
        set-cookie: utm_medium=default; expires=Thu, 21-Nov-2024 21:47:05 GMT; Max-Age=2592000; path=/
        set-cookie: utm_term=deleted; expires=Thu, 01-Jan-1970 00:00:01 GMT; Max-Age=0; path=/
        set-cookie: utm_campaign=deleted; expires=Thu, 01-Jan-1970 00:00:01 GMT; Max-Age=0; path=/
        set-cookie: utm_content=deleted; expires=Thu, 01-Jan-1970 00:00:01 GMT; Max-Age=0; path=/
        set-cookie: order_utm_history=%5B%7B%22utm_source%22%3A%22direct%22%2C%22utm_medium%22%3A%22default%22%2C%22utm_term%22%3A%22%22%2C%22utm_campaign%22%3A%22%
        22%2C%22utm_content%22%3A%22%22%2C%22source_device%22%3A%22computer%22%2C%22create_time%22%3A1729633625%2C%22expire_time%22%3A1732225625%7D%5D; path=/
        set-cookie: landing_page=aHR0cHM6Ly9ub3pmcmFuY2UuZGFsZWNvbnNob3BwaW5nLmNvbS8%3D; expires=Wed, 22-Oct-2025 21:47:05 GMT; Max-Age=31536000; path=/
        set-cookie: oemsaas_keep_alive=6217217A-AEBC-81A0-AA31-1EAA538598FD; expires=Tue, 22-Oct-2024 22:17:05 GMT; Max-Age=1800; path=/
        set-cookie: first_http_referer=null; expires=Thu, 21-Nov-2024 21:47:05 GMT; Max-Age=2592000; path=/
        set-cookie: first_visit_time=1729633625; expires=Fri, 20-Oct-2034 21:47:05 GMT; Max-Age=315360000; path=/
        set-cookie: PHPSESSID=ac675ab9c633d7e8b969be9b156c1998; path=/
        set-cookie: __cf_bm=mP2wybe_Br2ARX7BqZHqNiypFDr9pqHXzbwL3z2NQAI-1729633625-1.0.1.1-slK4FERlcgmF1iY9CPkFdpKWbIC01fjenzw9qrTUhgNHJwp_xBzs2VhebcbDpwISKkS3UTi_E
        QT_88pCKa1GOA; path=/; expires=Tue, 22-Oct-24 22:17:05 GMT; domain=.nozfrance.ddd.com; HttpOnly; Secure; SameSite=None
        server: cloudflare
        cf-ray: 8d6caf0bca649ef4-CDG
        alt-svc: h3=":443"; ma=86400

        <!DOCTYPE html>
        <html lang="en-US">

        <head>
            <meta charset="utf-8"/>
        <meta content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no" name="viewport">
        <meta content="yes" name="apple-mobile-web-app-capable">
        <meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible">
        <meta content="always" name="referrer">
        <meta content="en-US" http-equiv="content-language"/>
        [OMITTED SCAM]
        ```

### DNS

![alt text](338294387-de3e7f21-6f52-4ac4-8eab-367296cd385f.png)

1. Mettre les domaines de niveau 2 soit `aaa.com` qui nous ont été signalé dans une wordliste.

```bash
cat domains.l2.txt
    # aaa.com
    # bbb.com
    # ccc.com
    # ddd.com
    # eee.com
```

Dans mon cas j'en ai 5 domaines.

2. On utilise subfinder et bbot ou tout autre outils pour énumérer ces domaines. On peut également noté que subfinder utilise de nombreuse source publique comme [hackertarget] [digitorus] [leakix] [dnsdumpster]

```bash
cat domains.l2.txt | subfinder -all -recursive | tee domains.l3.txt
```

---

```bash
bbot -t aaa.com bbb.com ccc.com ddd.com eee.com -p subdomain-enum email-enum -o .
```

On merge les fichiers.

```bash
cat domains.l3.txt bbot-domain.txt | sort -u | tee domains.txt
```

J'obtient ici 160 sous-domaines.

---

### Dorking

- Ne pas faire cela inutillement
  - Consulter le `https://<domain.com>/robots.txt`
  - Si il contient ceci ne pas tester cette étape car inutile

```text
User-agent: *
Disallow: /
```

- [DorkSearch](https://dorksearch.com/)
- [all-google-dork](https://github.com/Proviesec/google-dorks/blob/main/all-google-dorks.txt)

---

### HTTP

#### Analyse à chaud

1. On prend une capture d'ecran sur les status 200.

    ```bash
    echo domains.txt | httpx -fr -sc -mc 200 -sr -random-agent | tee 200.domains.txt
    ```

- Flags
  - **-fr** --follow-redirects: Cette option permet à httpx de suivre les redirections HTTP jusqu'à ce que la réponse finale soit obtenue.
  - **-sc** --status-code: Affiche le code de statut HTTP de la réponse (200, 404, etc.).
  - **-mc** --match-code 200: Filtre uniquement les réponses qui correspondent au code de statut 200 (OK).
  - **-sr** --store-response: Stocke les réponses HTTP complètes (en-têtes et corps) dans un répertoire de sortie par défaut.
  - **-random-agent**: Utilise un user-agent aléatoire dans chaque requête HTTP pour éviter d'être identifié comme un bot.

2. On fait ensuite une pré-analyse des echanges http (header + body) dans le repertoire `./output` dans le but de trouver une chaine de texte qui identifie le scamma

    ```bash
    cat 200.domain.txt | wc -l
    #    65
    ```

    ```bash
    grep -rl '<mon motif ou regex qui cherche le scam>' ./output/ | wc -l
    #   65
    ```

   - Ces 65 réponses http en status 200 sont donc touts des scams du meme marketplace.

3. On fait une analyse beaucoup plus approfondie

    La commande utilise httpx pour faire 3 requette http seconde pour scanner des URLs, incluant IP, redirections, ASN, CDN, hachage, serveur, titre de page, timeouts looong (pour etre sur de ne rien louper), et résultats JSON avec 10 essais pour chaque erreur.

    ```bash
    cat domains.txt | httpx -rt 3 -pa -td -ip -irr -irh -include-chain -asn -cdn -hash simhash -sc -server -title -fr -random-agent -timeout 8 -retries 10 -rl 2 -j | tee full-scan.json
    ```

- Flags :

  - **-t** 200: Définit le nombre de threads à utiliser pour les requêtes HTTP (ici, 200).
  - **-pa**, --probe-all-ips: Envoie des requêtes HTTP à toutes les adresses IP associées à un même domaine.
  - **-td**, --tech-detect: Utilise Wappalyzer pour détecter les technologies présentes sur le site (frameworks, CMS, etc.).
  - **-ip**: Affiche l'adresse IP du domaine.
  - **-irr**, --include-response: Inclut la requête et la réponse HTTP (corps + en-têtes) dans le fichier de sortie JSON.
  - **-irh**, --include-response-header: Inclut uniquement les en-têtes HTTP dans la sortie JSON.
  - **-include-chain**: Inclut la chaîne complète de redirections HTTP dans le fichier de sortie.
  - **-asn**: Affiche les informations ASN (Autonomous System Number) pour le domaine.
  - **-cdn**: Indique si le domaine utilise un CDN (Content Delivery Network) ou un pare-feu applicatif.
  - **-hash simhash**: Calcule le hash [Simhash](http://static.googleusercontent.com/media/research.google.com/en//pubs/archive/33026.pdf) du corps de la réponse pour permettre une détection de ressemblance entre réponses http.
  - **-sc**, --status-code: Affiche le code de statut HTTP.
  - **-server**: Affiche le serveur HTTP utilisé (par exemple, Apache, Nginx).
  - **-title**: Affiche le titre de la page HTML.
  - **-timeout** 8: Définit un délai d'attente de 8 secondes pour chaque requête.
  - **-retries** 10: Effectue jusqu'à 10 tentatives en cas d'échec de la requête.
  - **-j**, --json: Enregistre les résultats en format JSON.
  - **-o** full-scan.json: Spécifie le fichier de sortie pour stocker les résultats au format JSON (full-scan.json).

#### Whois

Utilisé ce script réalisé par mes soins (C'est chat j'ai mentie):

```bash
#!/bin/bash

# Vérifier que le script est exécuté avec Bash version 4 ou supérieure
if ((BASH_VERSINFO[0] < 4)); then
  echo "Ce script nécessite Bash version 4 ou supérieure."
  exit 1
fi

# Déclaration des variables pour les statistiques
declare -A registrar_count
declare -A registrar_iana_count
declare -A admin_contact
declare -A admin_email_count
declare -A tech_contact
declare -A tech_email_count
declare -A creation_dates
declare -A expiration_dates
declare -A status_count
declare -A name_servers

# Fonction pour l'affichage formaté des tableaux
function format_table {
  printf "%-40s %-10s\n" "$1" "$2"
}

# Fonction pour extraire les informations WHOIS d'un domaine
function extract_whois_info {
  local domain="$1"
  local whois_output="$2"

  # Extraction des informations avec valeur par défaut "Unknown" si vide
  registrar=$(echo "$whois_output" | grep -i '^Registrar:' | awk -F: '{print $2}' | xargs)
  registrar=${registrar:-"Unknown"}

  registrar_iana=$(echo "$whois_output" | grep -i '^Registrar IANA ID:' | awk -F: '{print $2}' | xargs)
  registrar_iana=${registrar_iana:-"Unknown"}

  admin_name=$(echo "$whois_output" | grep -i '^Admin Name' | awk -F: '{print $2}' | xargs)
  admin_name=${admin_name:-"Unknown"}

  admin_email=$(echo "$whois_output" | grep -i '^Admin Email' | awk -F: '{print $2}' | xargs)
  admin_email=${admin_email:-"Unknown"}

  tech_name=$(echo "$whois_output" | grep -i '^Tech Name' | awk -F: '{print $2}' | xargs)
  tech_name=${tech_name:-"Unknown"}

  tech_email=$(echo "$whois_output" | grep -i '^Tech Email' | awk -F: '{print $2}' | xargs)
  tech_email=${tech_email:-"Unknown"}

  creation_date=$(echo "$whois_output" | grep -i '^Creation Date' | head -1 | awk -F: '{print $2}' | xargs)
  creation_date=${creation_date:-"Unknown"}

  expiration_date=$(echo "$whois_output" | grep -i -E '^Expiry Date|^Expiration Date' | head -1 | awk -F: '{print $2}' | xargs)
  expiration_date=${expiration_date:-"Unknown"}

  status=$(echo "$whois_output" | grep -i '^Status' | head -1 | awk -F: '{print $2}' | xargs)
  status=${status:-"Unknown"}

  ns=$(echo "$whois_output" | grep -i '^Name Server' | awk -F: '{print $2}' | xargs | tr '\n' ', ')
  ns=${ns:-"Unknown"}

  # Stockage des informations pour les statistiques en s'assurant que les clés ne sont pas vides
  registrar_count["$registrar"]=$(( ${registrar_count["$registrar"]} + 1 ))
  registrar_iana_count["$registrar_iana"]=$(( ${registrar_iana_count["$registrar_iana"]} + 1 ))
  admin_contact["$admin_name"]=$(( ${admin_contact["$admin_name"]} + 1 ))
  admin_email_count["$admin_email"]=$(( ${admin_email_count["$admin_email"]} + 1 ))
  tech_contact["$tech_name"]=$(( ${tech_contact["$tech_name"]} + 1 ))
  tech_email_count["$tech_email"]=$(( ${tech_email_count["$tech_email"]} + 1 ))
  creation_dates["$creation_date"]=$(( ${creation_dates["$creation_date"]} + 1 ))
  expiration_dates["$expiration_date"]=$(( ${expiration_dates["$expiration_date"]} + 1 ))
  status_count["$status"]=$(( ${status_count["$status"]} + 1 ))
  name_servers["$ns"]=$(( ${name_servers["$ns"]} + 1 ))

  # Affichage des informations détaillées
  echo "Domaine : $domain"
  echo "  Registrar : $registrar"
  echo "  Registrar IANA ID : $registrar_iana"
  echo "  Admin Name : $admin_name"
  echo "  Admin Email : $admin_email"
  echo "  Tech Name : $tech_name"
  echo "  Tech Email : $tech_email"
  echo "  Creation Date : $creation_date"
  echo "  Expiration Date : $expiration_date"
  echo "  Status : $status"
  echo "  Name Servers : $ns"
  echo "----------------------------------------"
}

# Fonction pour afficher les statistiques
function output_statistics {
  local title="$1"
  local -n stat_array=$2
  echo -e "\n$title"
  echo "--------------------------------------------------------"
  
  # Vérifier si le tableau est vide
  if [ ${#stat_array[@]} -eq 0 ]; then
    echo "Aucune donnée disponible."
    return
  fi

  # Trier les clés pour un affichage ordonné
  for key in $(echo "${!stat_array[@]}" | tr ' ' '\n' | sort); do
    format_table "$key" "${stat_array["$key"]}"
  done
}

# Lecture des noms de domaine depuis l'entrée standard ou depuis un fichier si fourni en argument
input_sources=()
if [ $# -gt 0 ]; then
  for file in "$@"; do
    if [ -f "$file" ]; then
      input_sources+=("$file")
    else
      echo "Fichier non trouvé : $file"
      exit 1
    fi
  done
else
  # Si aucun argument, lire depuis l'entrée standard
  input_sources=("-")
fi

# Lecture des noms de domaine
while IFS= read -r domain || [ -n "$domain" ]; do
  # Vérification que la ligne n'est pas vide
  if [[ -n "$domain" ]]; then
    # Récupération des données WHOIS pour le domaine
    whois_output=$(whois "$domain" 2>/dev/null)

    # Vérifier si la commande whois a réussi
    if [[ $? -ne 0 ]]; then
      echo "Erreur lors de la récupération des informations WHOIS pour le domaine : $domain"
      echo "----------------------------------------"
      continue
    fi

    # Extraction et affichage des informations WHOIS
    extract_whois_info "$domain" "$whois_output"
  fi
done < <(if [ "${input_sources[0]}" == "-" ]; then cat; else cat "${input_sources[@]}"; fi)

# Génération des statistiques récapitulatives
echo -e "\n--- Statistiques récapitulatives ---"

output_statistics "Registrar                              Nombre de domaines" registrar_count
output_statistics "Registrar IANA ID                      Nombre de domaines" registrar_iana_count
output_statistics "Admin Name                             Nombre de domaines" admin_contact
output_statistics "Admin Email                            Nombre de domaines" admin_email_count
output_statistics "Tech Name                              Nombre de domaines" tech_contact
output_statistics "Tech Email                             Nombre de domaines" tech_email_count
output_statistics "Dates de création                      Nombre de domaines" creation_dates
output_statistics "Dates d'expiration                     Nombre de domaines" expiration_dates
output_statistics "Statuts des domaines                   Nombre de domaines" status_count
output_statistics "Serveurs de noms                       Nombre de domaines" name_servers

echo "Analyse complète."
```

on l'utilise avec cette commmande

```bash
cat subs.tdv3.txt | ./whoisatorv4.sh -h
    # Usage: ./whoisatorv4.sh [domain_list_file]
    # 
    # Options:
    #   -h              Affiche cette aide et quitte.
    # 
    # Exemples d'utilisation :
    #   ./whoisatorv4.sh liste_de_domaines.txt
    #   cat liste_de_domaines.txt | ./whoisatorv4.sh
cat subs.tdv3.txt | ./whoisatorv4.sh | tee whois-report.txt
```

```text
----------------------------------------
Domaine : exemple.com
  Registrar : Registrar Inc
  Registrar IANA ID : 123
  Admin Name : [REDACTÉ]
  Admin Email : [REDACTÉ]
  Tech Name : [REDACTÉ]
  Tech Email : [REDACTÉ]
  Creation Date : 2023-01-01
  Status : ok
  Name Servers : ns1.exemple.com, ns2.exemple.com
----------------------------------------
Domaine : exemple.com
  Registrar : Registrar Inc
  Registrar IANA ID : 123
  Admin Name : [REDACTÉ]
  Admin Email : [REDACTÉ]
  Tech Name : [REDACTÉ]
  Tech Email : [REDACTÉ]
  Creation Date : 2023-01-01
  Status : ok
  Name Servers : ns1.exemple.com, ns2.exemple.com
----------------------------------------

--- Statistiques récapitulatives ---

Registrar                              Nombre de domaines
--------------------------------------------------------
Onlinenic Inc                            11

Registrar IANA ID                      Nombre de domaines
--------------------------------------------------------
82                                       11

Admin Name                             Nombre de domaines
--------------------------------------------------------
Wei Dfqsdfqs                             8
Xuan Ldsdsd                              1
Yang Sipci                               1
Yu Kdsqopjd                              1

Admin Email                            Nombre de domaines
--------------------------------------------------------
aaa@163.com                              8
bbb@163.com                              1
ccc@163.com                              1
ddd@163.com                              1

Tech Email                             Nombre de domaines
--------------------------------------------------------
aaa@163.com                              8
bbb@163.com                              1
ccc@163.com                              1
ddd@163.com                              1

Dates de création                      Nombre de domaines
--------------------------------------------------------
2024-01-30T04                            11

Statuts des domaines                   Nombre de domaines
--------------------------------------------------------
clientHold https                         8
ok https                                 3

Serveurs de noms                       Nombre de domaines
--------------------------------------------------------
eva.ns.cloudflare.com                    1
hold1.thdns.com                          3
hold2.thdns.com                          3
sasha.ns.cloudflare.com                  7
stan.ns.cloudflare.com                   1
watson.ns.cloudflare.com                 7
```

Dans mon cas cela prouve la correspondace d'un même acteurs à travers à travers les différent nom de domaine trouvé.

Il faudrait que je fasse une recherche de whois inverse avec les emails / nom des scammers.

## Analyse

### Modèle de la donnée

Voici un exemple de 403 obtenue.

```json
{
    "timestamp": "2024-10-23T11:04:12.736085488+02:00",
    "asn": {
        "as_number": "AS6969",
        "as_name": "cloudflarenet",
        "as_country": "US",
        "as_range": [
            "69.69.69.0/22",
            "111.111.111.0/24"
        ]
    },
    "hash": {
        "body_simhash": "6834550529580252698",
        "header_simhash": "10116137393624037359"
    },
    "cdn_name": "cloudflare",
    "cdn_type": "waf",
    "port": "443",
    "url": "https://scammer.com",
    "input": "scammer.com",
    "scheme": "https",
    "webserver": "cloudflare",
    "body": "error code: 1000",
    "content_type": "text/plain",
    "method": "GET",
    "host": "69.69.69.2",
    "path": "/",
    "header": {
        "alt_svc": "h3=\":443\"; ma=86400",
        "cache_control": "private, max-age=0, no-store, no-cache, must-revalidate, post-check=0, pre-check=0",
        "cf_cache_status": "DYNAMIC",
        "cf_ray": "8d708ef66da43ca1-CDG",
        "content_length": "16",
        "content_type": "text/plain; charset=UTF-8",
        "date": "Wed, 23 Oct 2024 09:04:13 GMT",
        "expires": "Thu, 01 Jan 1970 00:00:01 GMT",
        "nel": "{\"success_fraction\":0,\"report_to\":\"cf-nel\",\"max_age\":604800}",
        "referrer_policy": "same-origin",
        "report_to": "{\"endpoints\":[{\"url\":\"https:\\/\\/a.nel.cloudflare.com\\[...],\"group\":\"cf-nel\",\"max_age\":604800}",
        "server": "cloudflare",
        "server_timing": "cfL4;desc=\"?CP\u0026x=0\", cfL4;desc=\"?proto=TCP[...]cid=0000000000000000\u0026ts=0\u0026x=0\"",
        "vary": "Accept-Encoding",
        "x_frame_options": "SAMEORIGIN"
    },
    "raw_header": "HTTP/1.1 403 [...]",
    "request": "GET / HTTP/1.1\r\nHost: scammer.com\r\nUser-Agent: Mozilla/5.0 (Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0\rgzip\r\n\r\n",
    "time": "264.684579ms",
    "a": [
        "69.69.69.2",
        "188.114.100.2"
    ],
    "aaaa": [
        "2a06:b00b:b00b::2",
        "2a06:acab:acab::2"
    ],
    "tech": [
        "Cloudflare",
        "HTTP/3"
    ],
    "words": 3,
    "lines": 1,
    "status_code": 403,
    "content_length": 16,
    "failed": false,
    "cdn": true,
    "knowledgebase": {
        "PageType": "error",
        "pHash": 0
    },
    "resolvers": [
        "1.1.1.1:53",
        "1.0.0.1:53"
    ]
}
```

### JSON parsing



4. Quels serveurs web (basés sur l’en-tête server) sont utilisés ?
    Commande :

```bash
jq -r '.header.server // empty' full-scan.json | sort -u
   # cloudflare
```

1. Quel sont les IP hebergeant ces clones ?

```bash
jq -r 'select(.status_code == 200) | .a[], .aaaa[] // empty' full-scan.json | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}|([a-fA-F0-9:]+:+)+[a-fA-F0-9]+' | sort -u
    # 10.16.1.1
    # 10.17.2.2
    # 10.18.3.3
    # 10.19.4.4
    # 172.69.69.1
    # 172.69.69.10
    # 172.69.69.20
    # 2606:b00b:300c::1
    # 2606:b00b:300c::2
    # 2a06:98c1:cafe::1
    # 2a06:98c1:cafe::2
```

1. Quel est l'AS BGP de ces address ?

```bash
jq '.asn.as_number // empty' full-scan.json | sort -u
   # "AS6969"
   # "AS6868"
   # "AS6767"
```

2. Quelles sont les plages d’adresses IP associées aux AS ?

```bash
jq -r '.asn.as_range[] // empty' full-scan.json | sort -u
    # 10.16.0.0/14
    # 172.69.69.0/24
    # 2606:b00b:300c::/46
    # 2a06:98c1:cafe::/46
```

5. Quelles sont les URLs ?

```bash
jq -r '.url // empty' full-scan.json | sort -u
    # https://test.aaa.com
    # https://dev.aaa.com
    # https://mail.aaa.com
    # https://www.aaa.com
    # https://test.bbb.com
    # https://dev.bbb.com
    # https://mail.bbb.com
    # https://www.bbb.com
    # https://test.ccc.com
    # https://dev.ccc.com
    # https://mail.ccc.com
    # https://www.ccc.com
    # https://test.ddd.com
    # https://dev.ddd.com
    # https://mail.ddd.com
    # https://www.ddd.com
```

5. Quelles sont les domaines de niveau 2 consernés ?

```bash
jq -r '.url // empty' full-scan.json | sed -E 's|https://||' | sed -E 's|^[^.]+\.||' | sort -u | tee td.txt
    # aaa.com
    # bbb.com
    # ccc.com
    # ddd.com
```

On voit ici que des domaines sont manquant par rapport au début de notre analyse.

5. Quelles sont les mots utilisé pour les sous-domaines ?

```bash
jq -r '.url // empty' full-scan.json | sed -E 's|https://||' | sed -E 's|\..*||' | sort -u
    # test
    # dev
    # mail
    # www
```

10. Est ce que les simhash sont vraiment efficace ?

Ils ont le tous exactement le meme hash, il faudrait que je trouve un shodans censys qui me prenne ce type de hash en search bar.

```bash
 jq -r 'select((.hash.body_simhash | tonumber) > 6800000000000000000 and (.hash.body_simhash | tonumber) < 6900000000000000000) | "\(.url) \(.hash.body_simhash)"' full-scan.json | sort -u
    # https://mail.aaa.com 6834550529580252824
    # https://mail.ccc.com 6834550529580252824
    # https://dev.ddd.com 6834550529580252824
    # https://dev.aaa.com 6834550529580252824
    # https://dev.bbb.com 6834550529580252824
    # https://dev.ccc.com 6834550529580252824
    # https://www.ddd.com 6834550529580252824
    # https://www.aaa.com 6834550529580252824
    # https://www.bbb.com 6834550529580252824
    # https://www.ccc.com 6834550529580252824
    # [...]
```



6. Quelles technologies sont identifiées sur les serveurs (Cloudflare, HTTP/3, etc.) ?

```bash
jq -r '.tech[] // empty' full-scan.json | sort -u

   # Cloudflare
   # Cloudflare Bot Management
   # HTTP/3
   # PHP
```

7. Quels types de contenu sont renvoyés par les serveurs (basés sur l’en-tête content_type) ?

```bash
jq -r '.header.content_type // empty' full-scan.json | sort -u
   # text/html; charset=utf-8
   # text/plain; charset=UTF-8
```

### Analyse de code js

<https://watchjs.com/en/docs/introduction>
<https://gist.github.com/fuckup1337/49484c35c8ad8ae1d165ffe7d71375eb>
<https://github.com/semgrep/semgrep>
<https://www.bugbountyhunter.com/guides/?type=javascript_files>
<https://github.com/003random/getJS>

nuclei -l js.txt -t ~/nuclei-templates/exposures/

curl <https://destroy.ai> | getJS -header "User-Agent: foo bar" 

grep -r -E "aws_access_key|aws_secret_key|api key|passwd|pwd|heroku|slack|firebase|swagger|aws_secret_key|aws key|password|ftp password|jdbc|db|sql|secret jet|config|admin|pwd|json|gcp|htaccess|.env|ssh key|.git|access key|secret token|oauth_token|oauth_token_secret" /path/to/directory/*.js

gau paypalobjects.com |grep -iE '\.js'|grep -ivE '\.json'|sort -u  >> paypalJS.txt

 gau paypal.com |grep -iE '\.js'|grep -ivE '\.json'|sort -u  >> paypalJS.txt

cat paypalJS.txt|xargs -n2 -I @ bash -c 'echo -e "\n[URL] @\n";python3 linkfinder.py -i @ -o cli' >> paypalJSPathsWithUrl.txt 
cat paypalJSPathsWithUrl.txt|grep -iv '[URL]'||sort -u > paypalJSPathsNoUrl.txt
cat paypalJSPathsNoUrl.txt | python3 collector.py output

