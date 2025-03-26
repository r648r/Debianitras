# Create in-scope filter with ia jq for domaine or ip

# Prompte

```
cat HTTP/inscope-url-or-sub.txt | sed 's#https\?://##g'| sed 's/:[0-9]\+$//' | awk -F. '{if (NF >= 2) {print $(NF-1) "." $NF} else {print $0}}' | sort -u | jq -R -s 'split("\n") | map(select(length > 0)) | {flags: "-iE", patterns: .}' | tee $HOME/.gf/scope-dns.json
```

## Domaine

cat HTTP/alive-inscope.txt → Lit le fichier des domaines
sed 's#https\?://##g' → Retire les https:// et http://
sed 's/:[0-9]\+$//' → Retire les ports (ex: ":8443")
awk -F. '{...}' → Extrait domaine base (ex: "aaaa.fr" depuis "www.aaaa.fr")
sort -u → Trie et supprime doublons
jq -R -s '...' → Convertit en JSON formaté pour GF
tee $HOME/.gf/scope-dns.json → Sauvegarde dans fichier GF
