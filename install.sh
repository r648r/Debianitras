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