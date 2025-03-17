# Méthodologie Simplifiée de Chasse aux Expositions d'API

## Vue d'ensemble du processus
0. **Choisir une cible** [Privée, WordPress, etc.]
1. **Reconnaissance** - Identifier tous les sous-domaines cibles
2. **Collecte d'URLs** - Rassembler toutes les URLs potentielles
3. **Extraction JavaScript** - Filtrer et collecter les fichiers JS
4. **Découverte de clés d'API** - Analyser les fichiers avec des outils spécialisés
5. **Validation des secrets** - Confirmer les clés découvertes
6. **Téléchargement et analyse locale** - Rechercher des modèles de données sensibles
7. **Extraction de liens** - Identifier les endpoints potentiels

## Phase 1: Reconnaissance initiale

```bash

# 2. Découverte de sous-domaines
subfinder -d domai.com -all -recursive | anew subs.txt

# 3. Vérification des points d'entrée HTTP actifs
subfinder -d domai.com -all -recursive | anew subs.txt | httpx -ct -ip -sc -fr -td -title -ports 80,443,3000,4443,5000,5001,7001,7002,7070,7443,8080,8081,8082,8443,8888,9000,9001,9090,9091,9200,9443,10000,10443 -mc 200,301,302,304,401,403,405,500,502,503 -retries 3 -timeout 10 -random-agent | anew alive-subs.txt
```

## Phase 2: Collecte d'URLs

```bash
# 4. Collecte d'URLs historiques avec Wayback Machine
cat subs.txt | waybackurls -no-subs | anew wayback.txt

# 5. Collecte d'URLs avec GAU (GetAllUrls)
cat subs.txt | gau --threads 5 -o gau.txt

# 6. Crawling avec Katana (première passe)
cat subs.txt | katana -d 5 -kf -jsl -jc -fx -ef woff,css,png,svg,jpg,woff2,jpeg,gif,svg -random-agent -o katana1.txt

# 7. Crawling avec Katana (seconde passe avec stratégie différente)
cat subs.txt | katana  -d 5 -kf -jsl -jc -fx -ef woff,css,png,svg,jpg,woff2,jpeg,gif,svg -s breadth-first -random-agent -o katana2.txt

# 8. Crawling avec Gospider
cat subs.txt | gospider -w -a -d 5 --js --robots --sitemap -K 2 -t 20 -o gospider.txt

# 9. Crawling avec Hakrawler
cat subs.txt | hakrawler -d 5 -t 20 -subs | tee hakrawler.txt
```

## Phase 3: Trie des URLs

- Todo 

```bash

# 10. Filtrage des fichiers JavaScript
cat Externe/HTTP/Crawl/* | grep "\.js" | sort -u | tee alljs.txt
cat Externe/HTTP/Crawl/gospider.txt | grep "\[javascript\]" | sort -u | awk -F " - " '{print $2}' | anew alljs.txt
cat Externe/HTTP/Crawl/gospider.txt | grep "\[href\] \- javascript"| sort -u | awk -F ' - ' '{print $2}' | anew all-inlinejs.txt
cat Externe/HTTP/Crawl/gospider.txt | grep "\[form\]"| sort -u | awk -F ' - ' '{print $2}' | uro | anew form.txt
cat Externe/HTTP/Crawl/gospider.txt | grep "\[aws-s3\]"| sort -u | awk -F ' - ' '{print $2}' | anew aws-s3.txt
cat Externe/HTTP/Crawl/gospider.txt | grep "\[linkfinder\]"| sort -u | awk -F ' - ' '{print $2}' | anew linkfinder.txt
cat Externe/HTTP/Crawl/gospider.txt | grep "\[robots\]"| sort -u | awk -F ' - ' '{print $2}' | anew robots.txt
cat Externe/HTTP/Crawl/gospider.txt | grep "\[subdomains\]"| sort -u | awk -F ' - ' '{print $2}' | anew Externe/DNS/subdomains.txt


# X. Valider le type de contenu JavaScript pour confirmer les fichiers JS légitimes
while read -r url; do 
    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q 200 && \
       curl -s -I "$url" | grep -iq 'Content-Type:.*\(text/javascript\|application/javascript\)'; then 
        echo "$url" 
    fi 
done < jsfiles.txt > livejsfiles.txt


## curl
mkdir -p js_files; while IFS= read -r url || [ -n "$url" ]; do filename=$(basename "$url"); echo "Downloading $filename JS..."; curl -sSL "$url" -o "downloaded_js_files/$filename"; done < "$1"; echo "Download complete."

## wget
sed -i 's/\r//' js.txt && for i in $(cat liveJS.txt); do wget "$i"; done
```

## Phase 3: Analyse des fichiers JavaScript

```bash
# 13. Analyse avec Mantra
cat alljs.txt | mantra

# 14. Analyse des sous-domaines avec Cariddi
cat subs.txt | cariddi -s -e -err-info -debug -intensive

# 15. Analyse des fichiers JS avec Cariddi
cat alljs.txt | cariddi -s -e -err-info -debug -intensive
# Note: Si vous rencontrez des problèmes avec cet outil, vous pouvez passer à l'étape suivante

# 16. Analyse avec JSLeak
cat alljs.txt | jsleak -s -l -k

# 17. Analyse avec Nuclei (templates pour expositions)
cat alljs.txt | nuclei -t /root/nuclei-templates/exposures

# 18. Analyse avec SecretFinder (export HTML)
python3 SecretFinder.py -i alljs.txt -e

# 19. Analyse approfondie avec LazyEgg
cat alljs.txt | xargs -I{} bash -c 'echo -e "\ntarget : {}\n" && python3 lazyegg.py "{}" --js_urls --domains --ips --leaked_creds --local_storage'

# 20. Exécution de SecretFinder avec sortie CLI
cat alljs.txt | while read url; do python3 SecretFinder.py -i $url -o cli; done

# 21. Utilisation de SecretFinder (https://github.com/m4ll0k/SecretFinder)
cat jsfiles.txt | while read url; do python3 secretfinder.py -i $url -o cli >> secrets.txt; done

# 22. Exécution de Nuclei avec des templates d'exposition spécifiques sur les fichiers JS
nuclei -l jsfiles.txt -t /home/enma/nuclei-templates/http/exposures/ -o jsecrets.txt
```

## Phase 4: Téléchargement et analyse locale

```bash
# 23. Téléchargement des fichiers JS
wget -i alljs.txt -P jsfiles/

# 24. Recherche de motifs sensibles dans les fichiers téléchargés
grep -r -E "aws_access_key|aws_secret_key|api_key|passwd|pwd|heroku|slack|firebase|swagger|aws_secret_key|aws_key|password|ftp password|jdbc|db|sql|secret|jwt|config|admin|pwd|json|gcp|htaccess|.env|ssh_key|git|access_key|secret_token|oauth_token|oauth_token_secret|smtp" jsfiles/

# 25. Extraction des endpoints avec LinkFinder
python3 LinkFinder.py -i alljs.txt -o cli

# 26. Extraction supplémentaire d'endpoints en utilisant LinkFinder avec une méthode différente
cat jsfiles.txt | while read url; do linkfinder -i $url -o cli >> endpoints-js.txt; done

# 27. Extraction alternative d'endpoints avec LinkFinder depuis le chemin Python
cat jsfiles.txt | xargs -I{} python3 /opt/linkfinder/linkfinder.py -i {} -o cli | anew endpoints-js.txt
```

## Astuces supplémentaires

1. **Organisation des résultats**:
   - Gardez tous vos fichiers de sortie dans des dossiers séparés et bien nommés
   - Utilisez des scripts pour automatiser les tâches répétitives
   - Documentez vos découvertes avec des PoC
   - [Google Maps API Key](https://r0b0ts.medium.com/how-i-proved-impact-with-google-map-api-key-7aa801616abb)
2. **Optimisation des recherches**:
   - Combinez les résultats de plusieurs outils pour une meilleure couverture
   - Filtrez les faux positifs avec des outils de validation
   - Ne vous fiez pas aux résultats d'un seul outil
   - Vérifiez toujours les secrets découverts pour vous assurer qu'ils sont valides

3. **Analyse iterative**:
   - Cicler les phases : Collecte d'URLs -> Analyse js = + d'URL -> Collecte d'URLs ->Analyse js
