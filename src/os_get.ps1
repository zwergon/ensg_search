# Copyright © 2025 IFP Energies nouvelles (IFPEN), Rueil-Malmaison, France.
# This course material was created by IFP Energies nouvelles (IFPEN) and 
# is intended for educational purposes. Unauthorized reproduction, distribution, 
# or modification without explicit permission is prohibited.

param (
    [string]$Uri
)


# Vérification des paramètres
if (-not $Uri) {
    Write-Host "Usage: .\os_get.ps1 -Uri <URL>"
    exit 1
}

# Récupération des credentials
$Username = "kpwoipavhb" 
$Password = $env:OSPASSWD

if (-not $Password) {
    Write-Host "Erreur: la variable d'environnement OSPASSWD n'est pas définie." -ForegroundColor Red
    exit 1
}

# Construction de l'en-tête d'authentification
$authValue = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("$Username`:$Password"))
$headers = @{
    Authorization = "Basic $authValue"
}

try {
    # Exécution de la requête GET avec Basic Auth
    $Response = Invoke-WebRequest -Uri $Uri -Method Get -Headers $headers

    # Affichage de la réponse
    Write-Host "`nResponse Content:"
    Write-Host $Response.Content
}
catch {
    Write-Host "Une erreur s'est produite:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
