# kali
alias kali='sudo ssh -i ~/.ssh/raphael_ssh_ldlc_ecdsa -p 6941 raph@192.168.222.129 -L 420:127.0.0.1:420'


# Debianitras
Remove log 
sudo find /var/log -type f -name "*.log" | xargs -I {} sudo truncate -s 0 {}

Alias
apt install nala
alias apt="nala"
alias sudo="sudo "

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
