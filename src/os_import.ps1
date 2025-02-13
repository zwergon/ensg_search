# Copyright © 2025 IFP Energies nouvelles (IFPEN), Rueil-Malmaison, France.
# This course material was created by IFP Energies nouvelles (IFPEN) and 
# is intended for educational purposes. Unauthorized reproduction, distribution, 
# or modification without explicit permission is prohibited.

param (
    [string]$FilePath
)

$Uri = "https://ensg-search-9642476797.eu-central-1.bonsaisearch.net:443/_bulk"
$Username = "kpwoipavhb" 
$Password = $env:OSPASSWD
$contentType = "application/json"

if (-not $FilePath) {
    Write-Host "Usage: .\os_import.ps1 -FilePath <filepath>"
    exit 1
}

# Charger le fichier bulk
try {
    $bulkData = Get-Content -Path $FilePath -Raw
}
catch {
    Write-Host "Erreur lors de la lecture du fichier : $FilePath" -ForegroundColor Red
    Write-Host $_.Exception.Message
    exit 1
}

# Construire l'en-tête d'authentification
$authValue = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("$Username`:$Password"))
$headers = @{
    Authorization  = "Basic $authValue"
    "Content-Type" = $contentType
}

try {
    # Envoi de la requête
    $Response = Invoke-WebRequest -Uri $Uri -Method Post -Body $bulkData -Headers $headers

    # Vérification du statut HTTP
    if ($Response.StatusCode -ge 200 -and $Response.StatusCode -lt 300) {
        Write-Host "Importation réussie !" -ForegroundColor Green
        Write-Host "Réponse : $($Response.Content)"
    }
    else {
        Write-Host "Erreur lors de l'importation. Code HTTP : $($Response.StatusCode)" -ForegroundColor Yellow
        Write-Host "Réponse : $($Response.Content)"
    }
}
catch {
    Write-Host "Une erreur est survenue lors de l'importation." -ForegroundColor Red
    Write-Host $_.Exception.Message
}

