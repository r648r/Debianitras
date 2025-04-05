# Create in-scope filter with ia jq for domaine or ip

# Prompte

```
cat HTTP/inscope-url-or-sub.txt | sed 's#https\?://##g'| sed 's/:[0-9]\+$//' | awk -F. '{if (NF >= 2) {print $(NF-1) "." $NF} else {print $0}}' | sort -u | jq -R -s 'split("\n") | map(select(length > 0)) | {flags: "-iE", patterns: .}' | tee $HOME/.gf/scope-dns.json
```
```
cat subdomains.txt| httpx -ip | grep -E '(113\.246\.(2[4-9]|3[0-1])|163\.53\.247)\.' | sed 's#https\?://##g'| sed 's/:[0-9]\+$//'| anew ../HTTP/alive-inscope.txt

cat subdomains.txt | httpx -ip -ports http:80,https:443,http:8080,https:8080,http:8081,https:8081,http:9090,https:9091,http:9091,https:9091,https:4443,https:8443,https:9443| grep -E '(191\.216\.(3[4-9]|3[0-1])|162\.53\.247)\.' | awk '{print $1}' | sed 's#https\?://##g'| sed 's/:[0-9]\+$//' | anew HTTP/alive-inscope.txt
```

## Domaine

cat HTTP/alive-inscope.txt → Lit le fichier des domaines
sed 's#https\?://##g' → Retire les https:// et http://
sed 's/:[0-9]\+$//' → Retire les ports (ex: ":8443")
awk -F. '{...}' → Extrait domaine base (ex: "aaaa.fr" depuis "www.aaaa.fr")
sort -u → Trie et supprime doublons
jq -R -s '...' → Convertit en JSON formaté pour GF
tee $HOME/.gf/scope-dns.json → Sauvegarde dans fichier GF
