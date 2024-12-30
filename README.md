## Update
```
asdf plugin add golang
asdf install golang latest
asdf global golang latest
go version
export PATH=$PATH:$(go env GOPATH)/bin
export PATH=$PATH:$(go env GOBIN)

echo 'export PATH=$PATH:$(go env GOPATH)/bin' > $HOME/.zshrc && source $HOME/.zshrc
echo 'export PATH=$PATH:$(go env GOBIN)' > $HOME/.zshrc && source $HOME/.zshrc

go install -v github.com/PentestPad/subzy@latest
go install -v github.com/tomnomnom/anew@latest
go install -v github.com/projectdiscovery/pdtm/cmd/pdtm@latest

pdtm -bp $(go env GOPATH)/bin -ua
pdtm -bp $(go env GOPATH)/bin -ia
```


## Cheat Sheet
```
python3 corsy.py -i /path/urls.txt --headers "User-Agent: GoogleBot\nCookie: SESSION=Hacked"
arjun -i srv-endpoint.txt -oT arjun_output.txt -m GET,POST -w $(fzf-wordlists) -t 10 --rate-limit 10 --headers 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' --stable
ffuf -w $(fzf-wordlists) -u http://www.razer.com/.ssh/FUZZ -fc 400,401,402,403,404,429,500,501,502,503 -recursion -recursion-depth 2 -e .html,.php,.txt,.pdf,.js,.css,.zip,.bak,.old,.log,.json,.xml,.config,.env,.asp,.aspx,.jsp,.gz,.tar,.sql,.db -ac -c -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0' -H 'X-Forwarded-For: 127.0.0.1' -H 'X-Originating-IP: 127.0.0.1' -H 'X-Forwarded-Host: localhost' -t 100 -r -o results.json
```

```
alias kali='sudo ssh -i ~/.ssh/raphael_ssh_ldlc_ecdsa -p 6941 raph@192.168.222.129 -L 420:127.0.0.1:420'
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


# Debianitras
```
# Define the path to your custom alias file
ALIAS_FILE="$HOME/.zsh_aliases_custom"

# Create or overwrite the alias file with your current aliases
cat <<EOL > $ALIAS_FILE
# Custom aliases
alias fzf-wordlists='find /opt/rockyou.txt /opt/seclists /usr/share/wordlists /usr/share/wfuzz /usr/share/dirb -type f | fzf'
alias fzf-n="find /opt/nuclei-templates/ coffinxp/ -type f -name "*.y*" | fzf"
alias fzf-w="find /opt/SecLists/ /opt/payloads/ -type f -name '*.txt' | fzf"
alias rml='sudo find /var/log -type f -name "*.log" | xargs -I {} sudo truncate -s 0 {}'
alias apt='nala'
alias sudo='sudo '
EOL

# Check if the alias file is already sourced in .zshrc
if ! grep -q "source $ALIAS_FILE" "$HOME/.zshrc"; then
  # If not, add the source command to .zshrc
  echo "source $ALIAS_FILE" >> "$HOME/.zshrc"
fi

# Reload .zshrc to apply the changes immediately
source "$HOME/.zshrc"
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
