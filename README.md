## Install and update

### Tools
```bash
wbm(){
  while read -r d; do
    curl -sG "https://web.archive.org/cdx/search/cdx" \
      --data-urlencode "url=*.$d/*" \
      --data-urlencode "collapse=urlkey" \
      --data-urlencode "output=text" \
      --data-urlencode "fl=original" \
    | grep -Eiv '\.(woff|css|png|svg|jpg|woff2|jpeg|gif)$' | tee -a wb.txt
  done < $1
  cat wb.txt | wc -l
  echo "cat wb.txt | uro | grep -E '\.xls|\.xml|\.xlsx|\.json|\.pdf|\.sql|\.doc|\.docx|\.pptx|\.txt|\.zip|\.tar\.gz|\.tgz|\.bak|\.7z|\.rar|\.log|\.cache|\.secret|\.db|\.backup|\.yml|\.gz|\.config|\.csv|\.yaml|\.md|\.md5|\.exe|\.dll|\.bin|\.ini|\.bat|\.sh|\.tar|\.deb|\.rpm|\.iso|\.img|\.apk|\.msi|\.dmg|\.tmp|\.crt|\.pem|\.key|\.pub|\.asc'"
}
```

### GO
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
go install github.com/jaeles-project/jaeles@latest

pdtm -bp /root/.asdf/shims/ -ua
pdtm -bp /root/.asdf/shims/ -ia
nuclei -update-templates && mkdir -p root/nuclei-templates/coffinxp && git clone https://github.com/coffinxp/nuclei-templates.git /root/nuclei-templates/coffinxp
```

### ZSHRC + Wordlist 
```bash
curl -s https://raw.githubusercontent.com/r648r/Debianitras/refs/heads/main/install.sh|bash && source $HOME/.zshrc
```

### VsCode
```bash
curl -fsSL https://code-server.dev/install.sh | sh
```

## Cheat Sheet
```bash
# HTTP
httpx -ports https:443,http:80,http:8080,https:8080,http:9090,https:9090,https:8443 -follow-redirects -threads 100 -td | tee td-urls.txt
cat td-urls.txt | grep "200" | awk '{print $1}' | sort -u | katana -d 5 -kf -jsl -jc -fx -ef woff,css,png,svg,jpg,woff2,jpeg,gif,svg -o crawl.txt -rl 60 | tee katana-crawl.txt
arjun -i srv-endpoint.txt -oT arjun_output.txt -m GET,POST -w $(fzf-wordlists) -t 10 --rate-limit 10 --headers 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' --stable
ffuf -w $(fzf-wordlists) -u $URL -fc 400,401,402,403,404,429,500,501,502,503 -recursion -recursion-depth 2 -e .html,.php,.txt,.pdf,.js,.css,.zip,.bak,.old,.log,.json,.xml,.config,.env,.asp,.aspx,.jsp,.gz,.tar,.sql,.db -ac -c -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0' -H 'X-Forwarded-For: 127.0.0.1' -H 'X-Originating-IP: 127.0.0.1' -H 'X-Forwarded-Host: localhost' -t 100 -r -o results.json
python3 corsy.py -i /path/urls.txt --headers "User-Agent: GoogleBot\nCookie: SESSION=ffffffffffffffff"
```

## systemctl
```
sudo systemctl --failed
sudo systemctl list-units --type=service
sudo systemctl list-units --type=service --state=active

sudo systemctl list-dependencies nginx
sudo systemctl set-default multi-user.target
sudo systemctl isolate multi-user.target

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

/etc/ssh/sshd_config
```
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
