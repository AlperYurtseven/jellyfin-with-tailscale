# Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
# 1 KERELİK ELLE ÜSTTEKİ KOMUTU ÇALIŞTIR
# Yedek tarihi ve klasörleri
$backupDate = Get-Date -Format "yyyy-MM-dd"
$baseBackupPath = "$HOME\docker-volume-backups\$backupDate"
$namedPath = "$baseBackupPath\named"
$unnamedPath = "$baseBackupPath\unnamed"

New-Item -ItemType Directory -Path $namedPath -Force | Out-Null
New-Item -ItemType Directory -Path $unnamedPath -Force | Out-Null

# Bypass edilecek volume'ler (burada ister script içinden ister dosyadan)
$bypassList = @("codeyzerflix_mongodb_data")  # <- burada manuel tanımlı liste
# $bypassList = Get-Content ".\bypass.txt"  # <- alternatif olarak dosyadan oku

# Tüm volume isimlerini al
$volumes = docker volume ls -q

foreach ($volume in $volumes) {
    if ($bypassList -contains $volume) {
        Write-Host "Bypass edilen volume: $volume" -ForegroundColor Cyan
        continue
    }

    # Unnamed kontrolü
    if ($volume -match '^[a-f0-9]{64}$') {
        Write-Host "Unnamed volume bulundu: $volume (unnamed klasörüne yedekleniyor)" -ForegroundColor Yellow
        $targetPath = $unnamedPath
    }
    else {
        Write-Host "Yedekleniyor: $volume (named)"
        $targetPath = $namedPath
    }

    docker run --rm `
        -v "${volume}:/volume" `
        -v "${targetPath}:/backup" `
        alpine `
        sh -c "cd /volume && tar czf /backup/${volume}.tar.gz ."
}

Write-Host "`Yedekleme tamamlandı!"
Write-Host "Adlandırılmış volume'ler: $namedPath"
Write-Host "Unnamed volume'ler:      $unnamedPath"
