

### Go

```bash
asdf plugin add golang
asdf install golang latest
asdf reshim

echo 'export PATH=$PATH:$GOBIN' >> $HOME/.zshrc && source $HOME/.zshrc
echo 'export GO111MODULE=on' >> $HOME/.zshrc && source $HOME/.zshrc

go install -v github.com/PentestPad/subzy@latest
go install -v github.com/tomnomnom/anew@latest
go install -v github.com/projectdiscovery/pdtm/cmd/pdtm@latest
go install -v github.com/tomnomnom/qsreplace@latest
go install -v github.com/hahwul/dalfox/v2@latest
go install -v github.com/003random/getJS/v2@latest
go install -v github.com/jaeles-project/gospider@latest
go install -v github.com/jaeles-project/jaeles@latest
go install -v github.com/tomnomnom/unfurl@latest
go install -v github.com/s0md3v/wl/cmd/wl@latest

pdtm -bp /root/.asdf/shims/ -ua
pdtm -bp /root/.asdf/shims/ -ia
nuclei -update-templates && mkdir -p root/nuclei-templates/coffinxp && git clone https://github.com/coffinxp/nuclei-templates.git /root/nuclei-templates/coffinxp
```

### Py

```bash
pipx install uro
pipx install urless
pipx install bbot
pipx install git+https://github.com/xnl-h4ck3r/waymore.git
pipx install git+https://github.com/xnl-h4ck3r/xnLinkFinder.git

git clone https://github.com/m4ll0k/SecretFinder.git /tmp/secretfinder
pip install -r /tmp/secretfinder/requirements.txt
sudo mkdir -p /opt/secretfinder
sudo cp /tmp/secretfinder/SecretFinder.py  /opt/secretfinder/secretfinder.py
sudo echo 'alias secretfinder="python3 /opt/secretfinder/secretfinder.py"'>>~/.zshrc

git clone https://github.com/GerbenJavado/LinkFinder.git
cd LinkFinder
sudo mkdir -p /opt/linkfinder
sudo cp linkfinder.py /opt/linkfinder/linkfinder.py
sudo echo 'alias linkfinder="python3 /opt/linkfinder/linkfinder.py"'>>~/.zshrc
source $HOME/.zshrc
```



## VsCode

```bash
curl -fsSL https://code-server.dev/install.sh | sh
```

## Bash ToolKit

```bash
wbm(){
  if [ -f wb.txt ]; then
    rm wb.txt
  fi
  while read -r d; do
    curl -sG "https://web.archive.org/cdx/search/cdx?url=*.$d&fl=original&collapse=urlkey&output=text"| grep -Eiv '\.(woff|css|png|svg|jpg|woff2|jpeg|gif|htm|html)$' | uro | tee -a wb.txt
  done < $1
}
```

### ZSHRC + Wordlist 

```bash
curl -s https://raw.githubusercontent.com/r648r/Debianitras/refs/heads/main/install.sh|bash && source $HOME/.zshrc
find . -type f -name ".DS_Store" -print0 | xargs -0 rm -rf
brew list | gum choose --no-limit | xargs brew uninstall
```

https://github.com/sudosuraj/Bounty-VPS/blob/main/bounty-vps.sh


## Cheat Sheet

```bash
# Fast net recon
nmap -v --privileged -n -PE \
-PS21-23,25,53,80,88,110-111,113,115,135,139,143,220,264,389,443,445,449,524,585,636,993,995,1433,1521,1723,3306,3389,5900,8080,9100 \
-PU53,67-69,111,123,135,137-139,161-162,445,500,514,520,631,1434,1701,1900,4500,5353,49152 \
-sS -sU \
-p T:21-23,25,80,110,113,115,139,143,220,264,443,445,449,524,585,993,995,1433,1521,1723,8080,9100,U:123,2049,69,161,500,1900,5353 \
--max-retries 3 --min-rtt-timeout 100ms --max-rtt-timeout 1250ms --initial-rtt-timeout 100ms \
--defeat-rst-ratelimit --open -O --osscan-guess --max-os-tries 1 -oA discover 192.168.0.0/16 172.16.0.0/12 10.0.0.0/8

nmap -v --privileged -n -PE -PS21-23,25,53,80,88,110-111,113,115,135,139,143,220,264,389,443,445,449,524,585,636,993,995,1433,1521,1723,3306,3389,5900,8080,9100 -PU53,67-69,111,123,135,137-139,161-162,445,500,514,520,631,1434,1701,1900,4500,5353,49152 -sS -sU -p T:21-23,25,80,110,113,115,139,143,220,264,443,445,449,524,585,993,995,1433,1521,1723,8080,9100,U:123,2049,69,161,500,1900,5353 --max-retries 3 --min-rtt-timeout 100ms --max-rtt-timeout 1250ms --initial-rtt-timeout 100ms --defeat-rst-ratelimit --open -O --osscan-guess --max-os-tries 1 -oA discover-canton -iL

# LDAP dump and load to bh
mkdir LDAP && neo4j start && rusthound -d "$DOMAIN" -u "$USER"@"$DOMAIN" -p "$PASSWORD" --zip --ldaps --adcs --old-bloodhound && unzip *.zip && bloodhound-import -du neo4j -dp exegol4thewin *.json && bloodhound &> /dev/null &
python3 Get-GPPPassword.py "$USER@$DC_IP" -dc-ip "$DC_IP" -hashes $NT_HASH
Get-GPPPassword "$DOMAIN"/"$USER":"$PASSWORD"@"$DC_HOST"
ldapsearch -x -H "ldap://$DC_IP" -D "AAAAAAA" -w "$PASSWORD" -b "DC=QG,DC=ENTERPRISE,DC=COM" "(objectClass=computer)" name dNSHostName | grep 'dNSHostName' | awk '{print $2}' | tee machines.txt

# Git
trufflehog git https://github.com/aFuckingGitRepo.git --results=verified,unknown

# HTTP
## Filter out of scope ans (regex->IA verify with bloc ip and grep color)
cat ip-range.txt HTTPX.txt | grep -E '(193\.255\.(2[4-9]|3[0-1])|160\.255\.247)\.'

## Recon
cat DNS/subdomains.txt | httpx -sc 200,301,302,304,403,401,405,500,502,503  -random-agent  -threads 100 | awk '{print $1}' | anew alive-sub.txt
httpx -ip -sc -fr -td -title -ports http:80,https:443,http:8080,https:8080,http:8081,https:8081,http:9090,https:9091,http:9091,https:9091,https:4443,https:8443,https:9443 -random-agent -H 'X-Forwarded-For: 127.0.0.1' -H 'X-Originating-IP: 127.0.0.1' -H 'X-Forwarded-Host: localhost' -threads 100 | anew td-urls.txt
cat td-urls.txt | grep "200" | awk '{print $1}' | sort -u | katana -d 5 -kf -jsl -jc -fx -ef woff,css,png,svg,jpg,woff2,jpeg,gif,svg -o crawl.txt -rl 60 | tee katana-crawl.txt
arjun -i URL/SRV/asp-shit.txt -m GET -w /usr/share/wordlists/burp-param.txt -t 10 --rate-limit 10 -d 2 --stable -d 2 -oJ arjun_asp-shit-get.txt -c 100
ffuf -w $(fzf-wordlists) -u $URL -fc 400,401,402,403,404,429,500,501,502,503 -recursion -recursion-depth 2 -e .html,.php,.txt,.pdf,.js,.css,.zip,.bak,.old,.log,.json,.xml,.config,.env,.asp,.aspx,.jsp,.gz,.tar,.sql,.db -ac -c -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0' -H 'X-Forwarded-For: 127.0.0.1' -H 'X-Originating-IP: 127.0.0.1' -H 'X-Forwarded-Host: localhost' -t 100 -r -o results.json
python3 corsy.py -i /path/urls.txt --headers "User-Agent: GoogleBot\nCookie: SESSION=ffffffffffffffff"
wpscan --url https://site.com --disable-tls-checks --api-token <here> -e at -e ap -e u --enumerate ap --plugins-detection aggressive --force

# DNS
bbot -t evil.com 0.0.0.0/0 -p subdomain-enum cloud-enum
w=$(fzf-w); while read domain; do gobuster dns -q -r 8.8.8.8,1.1.1.1,1.0.0.1,9.9.9.9,8.8.4.4 -d "$domain" -w $w -t 1 --delay 0.1s -o "gobuster-${domain}.txt"; done < DNS/l2-in-scope.txt

## Other
curl -X POST "$URL" \
     -d "aaaaa=bbbbb" \
     -s -L -o /dev/null -D -
jq -r "path(..) | [.[] | tostring] | join(\".\")" deepseek_output.json


##XSS
cat /workspace/Externe/DNS/subdomains.txt | assetfinder --subs-only | httprobe | while read -r url; do
    xss1=$(curl -s -L "$url" -H 'X-Forwarded-For: fuckaliceandbob.space' | grep xss)
    xss2=$(curl -s -L "$url" -H 'X-Forwarded-Host: fuckaliceandbob.space' | grep xss)
    xss3=$(curl -s -L "$url" -H 'Host: fuckaliceandbob.space' | grep xss)
    xss4=$(curl -s -L "$url" --request-target "http://burpcollaborator/" --max-time 2)
    
    echo -e "\e[1;32m$url\e[0m\n\
    Method[1] X-Forwarded-For: xss+ssrf => $xss1\n\
    Method[2] X-Forwarded-Host: xss+ssrf ==> $xss2\n\
    Method[3] Host: xss+ssrf ==> $xss3\n\
    Method[4] GET http://fuckaliceandbob.space HTTP/1.1\n"
done

## Wb
curl "https://web.archive.org/cdx/search/cdx?url=*.$domain/*&collapse=urlkey&output=text&fl=original&filter=original:.*\.(xls|xml|xlsx|json|pdf|sql|doc|docx|pptx|txt|git|zip|tar\.gz|tgz|bak|7z|rar|log|cache|secret|db|backup|yml|gz|config|csv|yaml|md|md5|exe|dll|bin|ini|bat|sh|tar|deb|rpm|iso|img|env|apk|msi|dmg|tmp|crt|pem|key|pub|asc)$" -o filtered_urls.txt
cat wb.txt | grep -Eo '\.(xls|xml|xlsx|json|pdf|sql|doc|docx|pptx|txt|zip|tgz|bak|7z|rar|log|cache|secret|db|backup|yml|gz|config|csv|yaml|md|md5|exe|dll|bin|ini|bat|sh|tar|deb|rpm|iso|img|apk|msi|dmg|tmp|crt|pem|key|pub|asc|env|passwd|htpasswd|htaccess|keytab|csr|pfx|ppk)$'
cat wb.txt | sort -u | uro | grep -Eo '\.(xls|xml|xlsx|json|
pdf|sql|doc|docx|pptx|txt|zip|tar\.gz|tgz|bak|7z|rar|log|cache|secret|db|backup|yml|gz|config|csv|yaml|md|md5|exe|dll|bin|ini|bat|sh|tar|deb|rpm|iso|img|apk|msi|dmg|tmp|crt|pem|key|pub|asc|env|passwd|htpasswd|htaccess|keytab|csr|pfx|ppk)$' | sort | uniq -c | sort -rn
```

## CVE 2 template

```bash
cvemap -l 100  -q 'cvss_score:>7 vuln_status:confirmed is_remote:true is_template:false is_poc:true sort_asc:age_in_days' -j | tee CVE2template.json
```
```bash
jq -r '
  (["CVE ID", "Vendor", "CVSS", "PoC URL"]),
  (.[] | 
    select(.cvss_metrics.cvss31.vector? and (.cvss_metrics.cvss31.vector | contains("AV:N") and contains("PR:N") and contains("UI:N"))) |
    . as $cve |
    (.poc // [])[] |  
    [$cve.cve_id, 
     ($cve.cpe.vendor // "N/A"), 
     ($cve.cvss_metrics.cvss31.score | tostring), 
     .url]) |
  @tsv' CVE2template.json | column -t -s $'\t'
```

##  systemctl search

```bash
sudo systemctl --failed
sudo systemctl list-units --type=service
sudo systemctl list-units --type=service --state=active

sudo systemctl list-dependencies nginx
sudo systemctl set-default multi-user.target
sudo systemctl isolate multi-user.target
```

## goatsysctl for fast file serving

```
# goatsysctl
net.ipv4.tcp_max_syn_backlog = 40000
net.core.somaxconn = 40000
net.core.wmem_default = 8388608
net.core.rmem_default = 8388608
net.ipv4.tcp_sack = 1
net.ipv4.tcp_window_scaling = 1
net.ipv4.tcp_fin_timeout = 15
net.ipv4.tcp_keepalive_intvl = 30
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_moderate_rcvbuf = 1
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_mem = 134217728 134217728 134217728
net.ipv4.tcp_rmem = 4096 277750 134217728
net.ipv4.tcp_wmem = 4096 277750 134217728
net.core.netdev_max_backlog = 300000
net.ipv4.ip_local_port_range = 1025 65535
```

## Shodan Dork
```
http.html:"/wp-content/"
https://hunter.how/list?searchValue=product.name%3D%22Percona%20PMM%22
```

## initframfs
```bash
fsck -y /dev/sdX
echo b > /proc/sysrq-trigger
```

## SSH

/etc/ssh/sshd_config
```init
# This sshd was compiled with PATH=/usr/local/bin:/usr/bin:/bin:/usr/games
Port 6941
PermitRootLogin yes
PubkeyAuthentication yes
PasswordAuthentication no
AuthorizedKeysFile      .ssh/authorized_keys
Banner /etc/banner
KbdInteractiveAuthentication no
X11Forwarding no
ChallengeResponseAuthentication no
UsePAM no


# Allow client to pass locale environment variables
AcceptEnv LANG LC_*

# override default of no subsystems
Subsystem       sftp    /usr/lib/openssh/sftp-server
```

### hardening

```bash
rm /etc/ssh/ssh_host_*
ssh-keygen -t rsa -b 4096 -f /etc/ssh/ssh_host_rsa_key -N ""
ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N ""
echo -e "\nHostKey /etc/ssh/ssh_host_ed25519_key\nHostKey /etc/ssh/ssh_host_rsa_key" >> /etc/ssh/sshd_config
awk '$5 >= 3071' /etc/ssh/moduli > /etc/ssh/moduli.safe
mv /etc/ssh/moduli.safe /etc/ssh/moduli
echo -e "# Restrict key exchange, cipher, and MAC algorithms, as per sshaudit.com\n# hardening guide.\n
KexAlgorithms sntrup761x25519-sha512@openssh.com,curve25519-sha256,curve25519-sha256@libssh.org,gss-curve25519-sha256-,diffie-hellman-group16-sha512,gss-group16-sha512-,diffie-hellman-group18-sha512,diffie-hellman-group-exchange-sha256\n\nCiphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-gcm@openssh.com,aes128-ctr\n\nMACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,umac-128-etm@openssh.com\n\nHostKeyAlgorithms sk-ssh-ed25519-cert-v01@openssh.com,ssh-ed25519-cert-v01@openssh.com,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-256-cert-v01@openssh.com,sk-ssh-ed25519@openssh.com,ssh-ed25519,rsa-sha2-512,rsa-sha2-256\n\nRequiredRSASize 3072\n\nCASignatureAlgorithms sk-ssh-ed25519@openssh.com,ssh-ed25519,rsa-sha2-512,rsa-sha2-256\n\nGSSAPIKexAlgorithms gss-curve25519-sha256-,gss-group16-sha512-\n\nHostbasedAcceptedAlgorithms sk-ssh-ed25519-cert-v01@openssh.com,ssh-ed25519-cert-v01@openssh.com,sk-ssh-ed25519@openssh.com,ssh-ed25519,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-512,rsa-sha2-256-cert-v01@openssh.com,rsa-sha2-256\n\nPubkeyAcceptedAlgorithms sk-ssh-ed25519-cert-v01@openssh.com,ssh-ed25519-cert-v01@openssh.com,sk-ssh-ed25519@openssh.com,ssh-ed25519,rsa-sha2-512-cert-v01@openssh.com,rsa-sha2-512,rsa-sha2-256-cert-v01@openssh.com,rsa-sha2-256\n\n" > /etc/ssh/sshd_config.d/ssh-audit_hardening.conf
service ssh restart
DEBIAN_FRONTEND=noninteractive apt install -q -y iptables netfilter-persistent iptables-persistent
iptables -I INPUT -p tcp --dport 22 -m state --state NEW -m recent --set
iptables -I INPUT -p tcp --dport 22 -m state --state NEW -m recent --update --seconds 10 --hitcount 10 -j DROP
ip6tables -I INPUT -p tcp --dport 22 -m state --state NEW -m recent --set
ip6tables -I INPUT -p tcp --dport 22 -m state --state NEW -m recent --update --seconds 10 --hitcount 10 -j DROP
service netfilter-persistent save
systemctl restart sshd
```

/etc/sudoers
```
adduser raphzer -G sudo
```
`%sudo ALL=NOPASSWD: ALL`

/etc/banner
```
 __________________
< AAAAAAAAAAAAAAAA >
 ------------------
                       \                    ^    /^
                        \                  / \  // \
                         \   |\___/|      /   \//  .\
                          \  /O  O  \__  /    //  | \ \           *----*
                            /     /  \/_/    //   |  \  \          \   |
                            @___@`    \/_   //    |   \   \         \/\ \
                           0/0/|       \/_ //     |    \    \         \  \
                       0/0/0/0/|        \///      |     \     \       |  |
                    0/0/0/0/0/_|_ /   (  //       |      \     _\     |  /
                 0/0/0/0/0/0/`/,_ _ _/  ) ; -.    |    _ _\.-~       /   /
                             ,-}        _      *-.|.-~-.           .~    ~
            \     \__/        `/\      /                 ~-. _ .-~      /
             \____(oo)           *.   }            {                   /
             (    (--)          .----~-.\        \-`                 .~
             //__\\  \__ Ack!   ///.----..<        \             _ -~
            //    \\               ///-._ _ _ _ _ _ _{^ - - - - ~
```

/etc/systemd/system/update-issue-ip.service
```
[Unit]
Description=Met jour l'adresse IP dans /etc/issue
After=multi-user.target

[Service]
Type=oneshot
ExecStart= /usr/bin/bash /usr/local/bin/update_issue_ip.sh
```

.zshrc
```
export ZSH="$HOME/.oh-my-zsh"
export EDITOR='nano'
export PATH="$PATH:/root/.local/bin"

# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="evan"
plugins=(git)
source $ZSH/oh-my-zsh.sh

```


## Brouillon

```bash
cat allurls.txt | grep -i -E "\.js" | egrep -v "\.json" | httpx -mc 200 | anew jsfiles.txt

while read -r url; do
  if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q 200 && \
     curl -s -I "$url" | grep -iq 'Content-Type:.*\(text/javascript\|application/javascript\)'; then
    echo "$url"
  fi
done < jsfiles.txt > livejsfiles.txt


# https://github.com/m4ll0k/SecretFinder

cat jsfiles.txt | while read url; do python3 secretfinder.py -i $url -o cli >> secrets.txt; done

nuclei -l jsfiles.txt -t /home/enma/nuclei-templates/http/exposures/ -o jsecrets.txt

cat jsfiles.txt | while read url; do linkfinder -i $url -o cli >> endpoints-js.txt; done

cat jsfiles.txt | xargs -I{} python3 /opt/linkfinder/linkfinder.py -i {} -o cli | anew endpoints-js.txt


# Download JS Files

## curl
mkdir -p js_files; while IFS= read -r url || [ -n "$url" ]; do filename=$(basename "$url"); echo "Downloading $filename JS..."; curl -sSL "$url" -o "downloaded_js_files/$filename"; done < "$1"; echo "Download complete."

## wget
sed -i 's/\r//' js.txt && for i in $(cat liveJS.txt); do wget "$i"; done
```


### Warp

.warp/keybindings.yaml
```yaml
---
"terminal:copy_commands": alt-c
"pane_group:navigate_next": alt-n
"terminal:copy": alt-a
"workspace:show_settings_warpify_page": alt-i
"pane_group:add_left": cmd-e
"terminal:copy_outputs": alt-o
"workspace:new_tab": cmd-t
"workspace:activate_next_tab": alt-shift-N
"pane_group:add_down": cmd-o
"editor_view:down": none
```

![image](https://github.com/user-attachments/assets/e52b4921-4260-49ba-81b4-6e33222875f9)