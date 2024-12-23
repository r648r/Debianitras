# kali
alias kali='sudo ssh -i ~/.ssh/raphael_ssh_ldlc_ecdsa -p 6941 raph@192.168.222.129 -L 420:127.0.0.1:420'


```
s $(go env GOPATH)/bin
mkdir ~/go-binaries-export
cp $(go env GOPATH)/bin/* ~/go-binaries-export/
tar -czvf go-binaries-export.tar.gz -C ~/go-binaries-export .

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
