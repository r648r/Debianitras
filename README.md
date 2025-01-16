## Install and update

### ZSHRC + Wordlist 
```bash
############################################
# 1) Variables et dossiers
############################################

############################################
# 2) Création des répertoires
############################################
echo "[*] Création des répertoires..."
sudo mkdir "$(mktemp -d)"
sudo mkdir -p "$TARGET_WORDLISTS"
sudo mkdir -p "$TARGET_NUCLEI"
sudo mkdir -p "$TOOLS_DIR"

############################################
# 3) Téléchargements avec curl
############################################
echo "[*] Téléchargement curl"
curl -s https://raw.githubusercontent.com/coffinxp/loxs/refs/heads/main/payloads/sqli/xor.txt > "$TARGET_WORDLISTS/xor-sqli.txt"
curl -s https://raw.githubusercontent.com/coffinxp/loxs/refs/heads/main/filter.sh -o "$TOOLS_DIR/filter.sh"

echo "[*] Installation de code-server..."
curl -fsSL https://code-server.dev/install.sh | sh

############################################
# 6) Ajout d'aliases dans ~/.zshrc
############################################
echo "[*] Mise à jour de ~/.zshrc avec de nouveaux alias..."
cat <<EOL >> "$HOME/.zshrc"

# ENV
TARGET_WORDLISTS="/usr/share/wordlists/coffinxp"
TARGET_NUCLEI="/root/nuclei-templates/coffinxp"
TOOLS_DIR="/root/Tools"

# Custom aliases
alias fzf-wordlists='find /opt/rockyou.txt /opt/seclists /usr/share/wordlists /usr/share/wfuzz /usr/share/dirb -type f | fzf'
alias fzf-n='find /root/nuclei-templates/ -type f -name "*.y*" | fzf'
alias rml='sudo find /var/log -type f -name "*.log" | xargs -I {} sudo truncate -s 0 {}'
alias gitssh='eval \$(ssh-agent -s) && ssh-add ~/.ssh/github'
alias vs='code-server'
alias ut='nuclei -update-templates && cd /root/nuclei-templates/coffinxp && pull --rebase && cd'

# Update
clone_or_update() {
  # Clone ou met à jour un dépôt Git
  local repo_url="$1"
  local target_dir="$2"

  if [ -d "$target_dir/.git" ]; then
    echo "[!] '$target_dir' existe déjà, mise à jour avec git pull..."
    (
      cd "$target_dir"
      git pull --rebase
    )
  else
    echo "[*] Clonage de '$repo_url' vers '$target_dir'..."
    git clone "$repo_url" "$target_dir"
  fi
}

clone_or_update "https://github.com/coffinxp/gFpattren.git" "$TMP/gFpattren"
clone_or_update "https://github.com/coffinxp/payloads.git" "$TARGET_WORDLISTS/payloads"
clone_or_update "https://github.com/coffinxp/oneListForall.git" "$TARGET_WORDLISTS/oneListForall"
clone_or_update "https://github.com/coffinxp/img-payloads.git" "$TARGET_WORDLISTS/img-payloads"
clone_or_update "https://github.com/coffinxp/nuclei-templates.git" "$TARGET_NUCLEI"

# Warp
printf '\eP\$f{"hook": "SourcedRcFileForWarp", "value": { "shell": "zsh"}}\x9c'
EOL

############################################
# 7) Nettoyage et configurations
############################################
echo "[*] Suppression des alias gf= et des variables superflues..."
sed -i '/^alias gf=/d' /root/.oh-my-zsh/plugins/git/git.plugin.zsh 2>/dev/null || true
sed -i '/^TIME_=/d; /^PROMPT=/d' ~/.zshrc

echo "[*] Déplacement des patterns gFpattren vers ~/.gf..."
mkdir -p "$HOME/.gf"
mv "$TMP/gFpattren/"* "$HOME/.gf" 2>/dev/null || true
rm -rf "$TMP"

############################################
# 8) Rechargement de la config
############################################
echo "[*] Rechargement de ~/.zshrc..."
source "$HOME/.zshrc"

echo "[✓] Installation terminée !"
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
