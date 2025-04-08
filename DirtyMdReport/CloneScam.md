# RECON

## List most used technologies from wapanalyzer
```bash
jq -r '.tech[]' $FILE | sort | uniq -c | sort -nr
```

## Map CDN names to URLs (Potentially useful to find non-Cloudflare IPs)
```bash
jq -s 'group_by(.cdn_name) | map({cdn_name: .[0].cdn_name, hosts: map(.url)})' $FILE
```

## View URLs with status 200
```bash
jq -r 'select(.status_code == 200) | .url // empty' $FILE | sort -u
```

## View all IPv4 and IPv6 addresses behind status 200
```bash
jq -r 'select(.status_code == 200) | .a[], .aaaa[] // empty' full-scan.json | grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}|([a-fA-F0-9:]+:+)+[a-fA-F0-9]+' | sort -u
```

# HTTP STATUS

## Count and sort HTTP status codes
```bash
jq -r '.status_code' $FILE | sort | uniq -c | sort -nr
```

## Count and sort HTTP titles
```bash
jq -r '.. | objects | .title? // empty' $FILE | sort | uniq -c | sort -nr
```

```bash
jq -r '.. | objects | select(.title != null and .url != null) | "\(.title) \(.url)"' $FILE | sort | uniq | awk '{title_count[$1]++} END {for (title in title_count) print title_count[title], title}' | sort -nr
```

## Count and sort simhash occurrences
```bash
jq -r '.hash.body_simhash' $FILE | sort | uniq -c | sort -nr
```

# SIMHASH

## For each simhash, display page titles and related URLs
```bash
jq -s 'group_by(.hash.body_simhash) | map({body_simhash: .[0].hash.body_simhash, title: .[0].title, hosts: map(.input)})' $FILE
```

## Map simhash to page titles
```bash
jq -s 'group_by(.hash.body_simhash) | map({body_simhash: .[0].hash.body_simhash,titles: (map(.title) | unique),hosts: map(.input)})' $FILE
```

## Group URLs by identical body_simhash
```bash
jq -s 'group_by(.hash.body_simhash) | map({body_simhash: .[0].hash.body_simhash, hosts: map(.input)})' $FILE
```

# WHOIS

## Dump all whois information
```bash
cat Domain/domains.txt | whoisator
```

## Count and sort all emails used in whois by threat actors
```bash
grep -r "@" ./whois/ | awk -F ":" '{print $3}' | sed 's/ //g' | sort | uniq -c | sort -nr
```

# FUZZZ

## Fuzz vhost for each IP
```bash
while read -r ip; do ffuf -rate 80 -w /opt/seclists/Discovery/DNS/subdomains-top1million-20000.txt -u "https://$ip" -H "HOST: FUZZ.$ip" -o "${ip}.txt" -fs 26031,238 -fw 362,20 -fl 226,8; done < ip.txt
```

# WORDLIST

## Strip the wordlist
```bash
cat Domain/fqdn.txt | sed -E 's/^[^.]+\.(.*\..*)/\1/' | sort -u | anew Domain/domains.txt
```

## Merge domains with domains extracted from subdomains
```bash
cat Domain/fqdn.txt | sed -E 's/^[^.]+\.(.*\..*)/\1/' | sort -u | anew Domain/domains.txt
```

## Extract FQDNs from responses with status 200
```bash
jq -r 'select(.status_code == 200) | .body_fqdn // empty' "$FILE" | sort -u | tr -d '",{}[]' | grep -v "www." | grep -v "gstatic.com" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | anew Domain/fqdn.txt
```

## Extract domains from FQDNs
```bash
jq -r 'select(.status_code == 200) | .body_fqdn // empty' "$FILE" | sort -u | tr -d '",{}[]' | grep -v "www." | grep -v "gstatic.com" | sed -E 's/^[^.]+\.(.*\..*)/\1/' | sort -u | anew Domain/domains.txt
```

## Strip URL scheme
```bash
sed 's/^https:\/\///' AAA.txt
```

# LOOPING

## Recursive domain discovery and scanning pipeline
```bash
jq -r 'select(.status_code == 200) | .body_fqdn // empty' "$FILE" | sort -u | tr -d '",{}[]' | grep -v "www." | grep -v "gstatic.com" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | anew Domain/fqdn.txt | tee always-more-subz.txt | sed -E 's/^[^.]+\.(.*\..*)/\1/' | sort -u | anew Domain/domains.txt | tee always-more-domains.txt | subfinder -all -recursive | anew Domain/fqdn.txt | tee forever-more-subz-to-crawl.txt | httpx -td -ip -irr -irh -include-chain -cdn -hash simhash -sc -server -efqdn -favicon -jarm -title -fr -random-agent -timeout 10 -retries 5 -rl 2 -delay 2 -j | tee fullv6-always-more.json
```

## Process workflow
```
# On merge notre json précédent avec le nouveau -> on delete le repertoire whois -> on recommance le whoisator -> on grep les emails -> on fait un whoislookup sur l'email -> on trouve de nouveau domaine associer au whois -> on trouve les sous-domaines -> on crawl les domaines en mettant tout dans un json
```

# Email Frequency Counts

```
 114 rengmizhi7587@163.com
  39 dudoujiao11@163.com
  36 ntph750hz@163.com
  30 upaumo9273uq@163.com
  24 zhaolufen7656@163.com
  18 tuidaofang182@163.com
  18 brhly9235790@163.com
  15 nuorangyan5495@163.com
   3 gushiyi21@163.com
```

```
 120 zhaolufen7656@163.com
 120 tuidaofang182@163.com
 117 rengmizhi7587@163.com
 117 dudoujiao11@163.com
 114 ntph750hz@163.com
 111 upaumo9273uq@163.com
 108 brhly9235790@163.com
 105 nuorangyan5495@163.com
  99 gushiyi21@163.com
```

# Domains by Registrar

## GoDaddy.com, LLC (Registrar Abuse Contact Email: abuse@godaddy.com)
```
baheivasell.com
baleameecoms.com
balemsbuy.com
bamahamcom.com
banacceshop.com
barapripro.com
baredeslike.com
batavibiz.com
bazaserauto.com
betazafcommerce.com
betejolstocks.com
bewinyifinternet.com
dalekyoestores.com
damecyneshop.com
danegurlike.com
danezanbuy.com
dareazasell.com
darekaicool.com
dazadeuestores.com
debervpbiz.com
dewebeibest.com
dobantamnet.com
dolebropro.com
domepaosell.com
domeshamarketing.com
domoguypro.com
doreloilike.com
dotapeasell.com
dotejasmy.com
dozereetrade.com
gamahnabusiness.com
gamahumcool.com
gameisrbest.com
gamotaueshops.com
garekyubiz.com
gateiriauto.com
gobenulfecoms.com
gomatatbuy.com
gomesagcommerce.com
gomoyrastocks.com
gopaniktop.com
gosezevinternet.com
gotelylfind.com
gowajuicommerce.com
gowinnolgold.com
labenmeecool.com
lanejeatop.com
lapavismarketing.com
laraaugla.com
laredajtrade.com
lawinvvla.com
mabereffbest.com
mabintsefun.com
maheivyestores.com
mamemavmarket.com
manasyecommerce.com
mazeallinternet.com
nabenvidmarket.com
nabinfaiestores.com
naserusecom.com
nawagwebusiness.com
nawetobstocks.com
nawinjuvcom.com
nazethefun.com
rahenaklike.com
ramabobusiness.com
ramejusbiz.com
ramereetrade.com
ramexhegold.com
rapasebbest.com
rapazeplove.com
ratatauecoms.com
razediocom.com
sabanneistocks.com
saberroaecom.com
salejalbuy.com
sanagiuinternet.com
sanaporgo.com
sateroocom.com
sawintinbiz.com
taberartbest.com
taheyeotrading.com
tamoquatop.com
taroflocool.com
taselavmy.com
tazasamecoms.com
toracramarket.com
tozajemla.com
zahestafind.com
zahetoymarketing.com
zametrueshops.com
zarekirmarket.com
zatanidlove.com
zawaallinternet.com
zawaaricool.com
zawageonet.com
zawefracommerce.com
zebanfoulike.com
zemekelcool.com
zezetiscomping.com
```

## OnlineNIC, Inc. (Registrar Abuse Contact Email: abuse@onlinenic.com)
```
babandiaestores.com
babenadomarketing.com
babenduapro.com
babenvasgo.com
baberedtlike.com
baberjrlike.com
babinlantop.com
baheravsell.com
bamarudcool.com
bamoaxetrading.com
baneastestore.com
banejactop.com
baneosvauto.com
baparamshow.com
bapatifcommerce.com
bapawedgold.com
barequatop.com
barofayestores.com
barophueshop.com
batakyoestores.com
batemeecool.com
bausacfind.com
bazajoebuy.com
beberrapeshop.com
beletjshopping.com
bemakurla.com
bemebrifun.com
bemotieestores.com
benakrecool.com
benaniamy.com
beneleetrade.com
bereevdtop.com
berofattrade.com
besekeyla.com
betamescom.com
betaximestore.com
beweeulsell.com
bewinhoueshops.com
bezaartbest.com
```
*[List continues with many more domains]*

## eName Technology Co., Ltd. (Registrar Abuse Contact Email: abuse@ename.com)
```
staticscc.com
staticsdd.com
staticsee.com
```

## Cosmotown Inc. (abuse@cosmotown.com)
```
babanakisell.shop
bamahamcom.shop
banacceshop.shop
baseliocool.shop
berepeasell.shop
bewinyifinternet.shop
dabanlacinternet.shop
dabinmsbuy.shop
danezanbuy.shop
darekaicool.shop
datechibest.shop
debervpbiz.shop
depaambcommerce.shop
dolebropro.shop
dotapeasell.shop
dotejasmy.shop
dowamirgold.shop
dowinsirpro.shop
ganaaunhome.shop
gonebisgo.shop
gorajaknet.shop
gorophyinternet.shop
gosezevinternet.shop
gotelylfind.shop
goweachbuy.shop
lawarogfun.shop
lawinvvla.shop
maheivyestores.shop
mapabrifun.shop
nabenvidmarket.shop
napaanemarket.shop
natetwycool.shop
nawagwebusiness.shop
nawemjcomping.shop
raberbulla.shop
ralehasgo.shop
ranasustrade.shop
razadawbest.shop
sanaporgo.shop
satagangold.shop
tabintimhome.shop
tateterhome.shop
tozajemla.shop
zahetoymarketing.shop
zawaaricool.shop
zazeorkauto.shop
zesetygo.shop
```

## Unknown (Inconnu)
```
aberartbest-211026.com
aberartbest-313579.com
aberartbest-313606.com
aberartbest-313632.com
aberartbest-313637.com
aberartbest-313799.com
aberartbest-313803.com
aberartbest-313813.com
aberartbest.com
ahedawbest.com
amofitgold.com
anaruseshop.com
atabifcommerce.com
ausiinbusiness.com
awamarmy.com
azasamecoms.com
inconnus
manasymerce.com
obervancommerce.com
obingemcool.com
olegibpro.com
oparoscom.com
orebecauto.com
oreirvestores.com
oustoalove.com
oweindcom.com
owinluilike.com
rahetastop-313787.com
rahetastop-313795.com
taberartbest-211026.com
taberartbest-313579.com
taberartbest-313606.com
taberartbest-313632.com
taberartbest-313637.com
taberartbest-313799.com
taberartbest-313803.com
taberartbest-313813.com
zawefrmerce.com
zebenruumarket-313790.com
```
