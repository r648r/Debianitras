function Find-SensitiveFiles {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Paths,
        
        [Parameter(Mandatory = $false)]
        [string]$OutputFile,
        
        [Parameter(Mandatory = $false)]
        [switch]$IncludeContent = $true,
        
        [Parameter(Mandatory = $false)]
        [switch]$CheckHidden = $true
    )

    # Définition complète des détecteurs
    $Detectors = @(
        @{ Name = "AWS Keys";                Extensions = @("*"); Patterns = @("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY") }
        @{ Name = "Azure Keys";              Extensions = @("*"); Patterns = @("AZURE_SUBSCRIPTION_ID", "AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET") }
        @{ Name = "Google Cloud Keys";       Extensions = @("*"); Patterns = @("GOOGLE_API_KEY", "GCP_SERVICE_ACCOUNT") }
        @{ Name = "Private Keys";            Extensions = @("*"); Patterns = @("BEGIN RSA PRIVATE KEY", "BEGIN DSA PRIVATE KEY", "BEGIN EC PRIVATE KEY", "PuTTY-User-Key-File", "BEGIN OPENSSH PRIVATE KEY") }
        @{ Name = "Database Credentials";    Extensions = @("*"); Patterns = @("datasource", "connectionstring", "DB_PASSWORD", "db_pass", "mysql", "postgres", "mongodb", "redis", "mssql", "oracle") }
        @{ Name = "FTP Credentials";         FileNames  = @("recentservers.xml", "sftp-config.json", "filezilla.xml", "proftpdpasswd") }
        @{ Name = "Jenkins Credentials";     FileNames  = @("credentials.xml", "jenkins.plugins.publish_over_ssh.BapSshPublisherPlugin.xml") }
        @{ Name = "RDP Passwords";           Extensions = @("*"); Patterns = @("password") }
        @{ Name = "SSH Keys";                FileNames  = @("id_rsa", "id_dsa", "id_ecdsa", "id_ed25519", "authorized_keys", "known_hosts") }
        @{ Name = "Browser Credentials";     FileNames  = @("logins.json", "key4.db", "cert9.db", "cookies.sqlite") }
        @{ Name = "PowerShell Credentials";  Extensions = @("*"); Patterns = @("-SecureString", "-AsPlainText", "Net.NetworkCredential") }
        @{ Name = "Sensitive Config Files";  Extensions = @("*"); Patterns = @("password", "private", "secret", "token", "key", "credential", "apikey", "auth") }
        @{ Name = "Git Credentials";         FileNames  = @(".git-credentials", ".gitconfig", "config") }
        @{ Name = "VPN Configs";             Extensions = @("*"); Patterns = @("auth-user-pass", "remote") }
        @{ Name = "Infrastructure As Code";  Extensions = @("*"); Patterns = @("provider", "variable", "output", "module") }
        @{ Name = "PHP Connection Strings";  Extensions = @("*"); Patterns = @("mysql_connect", "mysql_pconnect", "pg_connect", "pg_pconnect", "mysqli_connect") }
        @{ Name = "Memory Dump Files";       Extensions = @("*"); Patterns = @("crash", "dump", "memory") }
        @{ Name = "Shell History";           FileNames  = @(".bash_history", ".zsh_history", ".sh_history", "zhistory", "ConsoleHost_History.txt") }
        @{ Name = "Unattended Install Configs"; FileNames = @("unattend.xml", "autounattend.xml", "sysprep.inf") }
        @{ Name = "NTDS Database";           FileNames  = @("NTDS.dit") }
        @{ Name = "Hash Files";              Extensions = @("*"); Patterns = @("pot", "hashes", "pwdump") }
        @{ Name = "Azure App Credentials";   Extensions = @("*"); Patterns = @("client_id", "clientID", "tenant", "secret") }
        @{ Name = "Docker Secrets";          FileNames  = @("docker-compose.yml", "docker-compose.override.yml"); Patterns = @("secrets", "password", "token") }
        @{ Name = "Kubernetes Secrets";      FileNames  = @("kubeconfig", "config"); Patterns = @("apiVersion", "kind: Secret", "data") }
        @{ Name = "Windows Credentials";     FileNames  = @("webcredentials.xml", "credstore.json") }
        @{ Name = "CI/CD Pipeline Secrets";  FileNames  = @("gitlab-ci.yml", "bitbucket-pipelines.yml", "circleci.yml", "azure-pipelines.yml"); Patterns = @("secrets", "password", "apikey", "private") }
        @{ Name = "API Keys";                Extensions = @("*"); Patterns = @("api_key", "api_secret", "apikey", "apiToken", "authToken") }
        @{ Name = "JWT Tokens";              Extensions = @("*"); Patterns = @("eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.") }
        @{ Name = "Log Files";               Extensions = @("*"); Patterns = @("exception", "error", "failed", "critical", "warning") }
        @{ Name = "Email Credentials";       Extensions = @("*"); Patterns = @("smtp", "mailserver", "mail_username", "mail_password") }
        @{ Name = "Crypto Wallets";          Extensions = @("*"); Patterns = @("wallet.dat", "mnemonic", "seedphrase", "blockchain") }
        @{ Name = "Telegram Bot Tokens";     Extensions = @("*"); Patterns = @("bot_token", "telegram_api") }
        @{ Name = "Strange Extensions";      Extensions = @("sql", "p12", "bak", "log", "secret", "db", "backup", "config", "dll", "ini", "bat", "sh", "tar", "crt", "key", "pub", "asc", "env", "keytab", "csr", "pfx", "ppk", "vpn", "ovpn") }
    )

    # Extensions de fichiers à analyser pour le contenu
    $ContentCheckExtensions = @(
        ".txt", ".xml", ".ini", ".config", ".cfg", ".conf", 
        ".properties", ".yml", ".yaml", ".json", ".js", 
        ".ps1", ".bat", ".cmd", ".sh", ".php", ".asp", 
        ".aspx", ".html", ".htm", ".env"
    )

    $results = @()
    $totalFound = 0
    $errorCount = 0
    $detectedFiles = @{}  # Pour éviter les doublons

    Write-Host "🔍 Recherche de fichiers sensibles en cours..." -ForegroundColor Cyan

    foreach ($path in $Paths) {
        if (-not (Test-Path -Path $path)) {
            Write-Warning "Le chemin '$path' n'existe pas ou n'est pas accessible."
            continue
        }

        Write-Host "Analyse de $path..." -ForegroundColor Yellow

        try {
            # Paramètres pour Get-ChildItem
            $gciParams = @{
                Path = $path
                Recurse = $true
                ErrorAction = "SilentlyContinue"
                ErrorVariable = "errors"
            }

            # Inclure les fichiers cachés si demandé
            if ($CheckHidden) {
                $gciParams.Add("Force", $true)
            }

            $files = Get-ChildItem @gciParams -File
            
            foreach ($file in $files) {
                $filePath = $file.FullName
                $fileName = $file.Name
                $fileExt = [System.IO.Path]::GetExtension($filePath).TrimStart('.').ToLower()
                
                # Éviter de traiter plusieurs fois le même fichier
                if ($detectedFiles.ContainsKey($filePath)) {
                    continue
                }
                
                foreach ($detector in $Detectors) {
                    $matched = $false
                    $matchReason = ""
                    $matchedPattern = ""
                    
                    # Vérification par nom de fichier, si applicable
                    if ($detector.ContainsKey("FileNames") -and ($detector.FileNames -contains $fileName)) {
                        $matched = $true
                        $matchReason = "Nom de fichier"
                        $matchedPattern = "Nom de fichier: $fileName"
                    }
                    
                    # Vérification par extension dans "Strange Extensions"
                    if (-not $matched -and $detector.Name -eq "Strange Extensions" -and ($detector.Extensions -contains $fileExt)) {
                        $matched = $true
                        $matchReason = "Extension"
                        $matchedPattern = "Extension: .$fileExt"
                    }
                    
                    # Vérification par contenu (uniquement si demandé et pas encore trouvé)
                    if (-not $matched -and $IncludeContent -and $detector.ContainsKey("Patterns")) {
                        # Vérifier si l'extension est compatible
                        $canCheckContent = $true
                        if ($detector.ContainsKey("Extensions") -and ($detector.Extensions -ne "*") -and ($detector.Name -ne "Strange Extensions")) {
                            if (-not ($detector.Extensions -contains $fileExt)) {
                                $canCheckContent = $false
                            }
                        }
                        
                        if ($canCheckContent) {
                            # Ne pas vérifier les fichiers trop volumineux (>10MB)
                            $fileSize = $file.Length / 1MB
                            if ($fileSize -le 10) {
                                try {
                                    $content = Get-Content -Path $filePath -Raw -ErrorAction SilentlyContinue
                                    
                                    foreach ($pattern in $detector.Patterns) {
                                        if ($content -match $pattern) {
                                            $matched = $true
                                            $matchReason = "Contenu"
                                            
                                            # Extraire le contexte correspondant
                                            $matchContext = $content -split "\r?\n" | Select-String -Pattern $pattern -SimpleMatch -Context 0,0 | 
                                                ForEach-Object { $_.Line.Trim() } | Select-Object -First 1
                                            
                                            # Masquer les informations sensibles dans l'output
                                            $maskedMatch = $matchContext -replace "($pattern=?\s*['`"]?)[^'`")\s]+(['`")]|$)", '$1***MASQUÉ***$2'
                                            $matchedPattern = if ($maskedMatch) { $maskedMatch } else { "Motif: $pattern" }
                                            break  # Un match suffit
                                        }
                                    }
                                }
                                catch {
                                    $errorCount++
                                }
                            }
                        }
                    }
                    
                    # Si un match a été trouvé, ajouter aux résultats
                    if ($matched) {
                        $result = [PSCustomObject]@{
                            Path = $filePath
                            Type = $detector.Name
                            MatchMethod = $matchReason
                            Size = "{0:N2} KB" -f ($file.Length / 1KB)
                            LastModified = $file.LastWriteTime
                            MatchedContent = $matchedPattern
                        }
                        $results += $result
                        $totalFound++
                        $detectedFiles[$filePath] = $true
                        break  # Passer au fichier suivant
                    }
                }
            }
        }
        catch {
            Write-Warning "Erreur lors de l'analyse de '$path': $_"
            $errorCount++
        }

        # Comptabiliser les erreurs d'accès
        foreach ($err in $errors) {
            if ($err.CategoryInfo.Category -eq 'PermissionDenied') {
                $errorCount++
            }
        }
    }

    # Trier les résultats par type et date de modification
    $results = $results | Sort-Object -Property Type, LastModified -Descending

    # Afficher les résultats
    if ($results.Count -gt 0) {
        Write-Host "`n🚨 $totalFound fichiers sensibles détectés !`n" -ForegroundColor Red
        
        # Afficher un résumé par type de détection
        $summary = $results | Group-Object -Property Type | 
            Select-Object Name, Count | 
            Sort-Object -Property Count -Descending
            
        Write-Host "📊 Résumé par type de détection :" -ForegroundColor Cyan
        $summary | Format-Table -AutoSize
        
        # Afficher les résultats détaillés
        Write-Host "📋 Liste des fichiers sensibles :" -ForegroundColor Cyan
        $results | Format-Table -Property Path, Type, MatchMethod, Size, LastModified, MatchedContent -AutoSize
    }
    else {
        Write-Host "`n✅ Aucun fichier sensible détecté." -ForegroundColor Green
    }

    # Afficher les statistiques d'erreurs
    if ($errorCount -gt 0) {
        Write-Host "⚠️ $errorCount erreurs d'accès rencontrées lors de l'analyse." -ForegroundColor Yellow
    }

    # Exporter les résultats si demandé
    if ($OutputFile -and $results.Count -gt 0) {
        # Ajouter un timestamp au nom du fichier si non spécifié
        if (-not $OutputFile.Contains(".")) {
            $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
            $OutputFile = "$OutputFile-$timestamp.csv"
        }
        
        $results | Export-Csv -Path $OutputFile -NoTypeInformation -Encoding UTF8
        Write-Host "📄 Résultats exportés vers $OutputFile" -ForegroundColor Cyan
        
        # Exporter également le résumé
        $summaryFile = [System.IO.Path]::ChangeExtension($OutputFile, "summary.csv")
        $summary | Export-Csv -Path $summaryFile -NoTypeInformation -Encoding UTF8
        Write-Host "📄 Résumé exporté vers $summaryFile" -ForegroundColor Cyan
    }
    
    return $results
}

# Fonction en une ligne pour exécution rapide (sans installer de script)
function Find-SensitiveFilesQuick {
    [CmdletBinding()]
    param(
        [string[]]$Paths = @("C:\", "D:\"),
        [string]$Extensions = "config,txt,xml,ini,p12,pfx,key,pem,crt,cer,ppk,json,bat,ps1,php,aspx,env,bak"
    )
    
    $extFilter = ($Extensions -split "," | ForEach-Object { "*.$_" }) -join ","
    
    # Filtres de recherche pour CMD - motifs de sensibilité
    $searchPatterns = "pass,user,secret,token,key,cred,config,auth,api"
    
    foreach ($path in $Paths) {
        Write-Host "Analyse rapide de $path..." -ForegroundColor Yellow
        
        # Utiliser CMD DIR pour trouver les fichiers par extension et nom
        $cmdOutput = cmd /c "dir /S /B $path\*.$extFilter 2>nul | findstr /i `"$searchPatterns`" 2>nul"
        
        if ($cmdOutput) {
            Write-Host "Fichiers trouvés dans $path :" -ForegroundColor Red
            $cmdOutput -split "`r`n" | ForEach-Object { Write-Host "  - $_" -ForegroundColor Magenta }
        }
        else {
            Write-Host "Aucun fichier suspect trouvé dans $path" -ForegroundColor Green
        }
    }
}
