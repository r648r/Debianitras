## Install and update

### ZSHRC + Wordlist 
```bash
TMP="$(mktemp -d)"

mkdir -p /usr/share/wordlists/coffinxp
mkdir -p root/nuclei-templates/coffinxp
mkdir /root/Tools

curl -s https://raw.githubusercontent.com/coffinxp/loxs/refs/heads/main/payloads/sqli/xor.txt > /usr/share/wordlists/coffinxp/xor-sqli.txt
curl -s https://raw.githubusercontent.com/coffinxp/loxs/refs/heads/main/filter.sh -o  /root/Tools/filter.sh
curl -fsSL https://code-server.dev/install.sh | sh

git clone https://github.com/coffinxp/gFpattren.git "$TMP"
git clone https://github.com/coffinxp/payloads.git /usr/share/wordlists/coffinxp
git clone https://github.com/coffinxp/oneListForall /usr/share/wordlists/coffinxp
git clone https://github.com/coffinxp/img-payloads /usr/share/wordlists/coffinxp
git clone https://github.com/coffinxp/nuclei-templates.git /root/nuclei-templates/coffinxp

cat <<EOL >> $HOME/.zshrc
# Custom aliases
alias fzf-wordlists='find /opt/rockyou.txt /opt/seclists /usr/share/wordlists /usr/share/wfuzz /usr/share/dirb -type f | fzf'
alias fzf-n='find /root/nuclei-templates/  -type f -name "*.y*" | fzf'
alias rml='sudo find /var/log -type f -name "*.log" | xargs -I {} sudo truncate -s 0 {}'
alias gitssh='eval $(ssh-agent -s) && ssh-add ~/.ssh/github'
alias vs='code-server'
alias ut='nuclei -update-templates && git clone https://github.com/coffinxp/nuclei-templates.git /root/nuclei-templates/coffinxp'

# Warp
printf '\eP$f{"hook": "SourcedRcFileForWarp", "value": { "shell": "zsh"}}\x9c'
EOL

sed -i '/^alias gf=/d' /root/.oh-my-zsh/plugins/git/git.plugin.zsh
sed -i '/^TIME_=/d; /^PROMPT=/d' ~/.zshrc && source ~/.zshrc
mv $TMP/gFpattren/* $HOME/.gf
rm -rf "$TMP"
source $HOME/.zshrc
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
nuclei -update-templates && mkdir -p root/nuclei-templates/coffinxp && git clone https://github.com/coffinxp/nuclei-templates.git /root/nuclei-templates/coffinxp'
```

### VsCode
```bash
curl -fsSL https://code-server.dev/install.sh | sh
```

## Cheat Sheet
```bash
python3 corsy.py -i /path/urls.txt --headers "User-Agent: GoogleBot\nCookie: SESSION=ffffffffffffffff"
arjun -i srv-endpoint.txt -oT arjun_output.txt -m GET,POST -w $(fzf-wordlists) -t 10 --rate-limit 10 --headers 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' --stable
ffuf -w $(fzf-wordlists) -u $URL -fc 400,401,402,403,404,429,500,501,502,503 -recursion -recursion-depth 2 -e .html,.php,.txt,.pdf,.js,.css,.zip,.bak,.old,.log,.json,.xml,.config,.env,.asp,.aspx,.jsp,.gz,.tar,.sql,.db -ac -c -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0' -H 'X-Forwarded-For: 127.0.0.1' -H 'X-Originating-IP: 127.0.0.1' -H 'X-Forwarded-Host: localhost' -t 100 -r -o results.json
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
