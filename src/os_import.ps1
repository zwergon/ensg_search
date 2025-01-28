param (
    [string]$FilePath
)
$Uri = "https://ensg-search-9642476797.eu-central-1.bonsaisearch.net:443/_bulk"
$Password = "9nys3us285"
$Username = "kpwoipavhb" 
$contentType = "application/json"



if (-not $FilePath) {
    Write-Host "Usage: .\os_import.ps1 -FilePath <filepath>"
    exit 1
}

# Charger le fichier bulk
$bulkData = Get-Content -Path $filePath -Raw
$headers = @{
    Authorization = "Basic " + [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("kpwoipavhb:9nys3us285"))
}


try {
    # Create the credential object
    $SecurePassword = ConvertTo-SecureString $Password -AsPlainText -Force
    $Credential = New-Object PSCredential($Username, $SecurePassword)

    # Perform the request
    $Response = Invoke-WebRequest -Uri $Uri -Method Post -Credential $Credential -Body $bulkData -ContentType $contentType -Headers $headers

    # Display the response content
    Write-Host $Response
}
catch {
    Write-Host "An error occurred:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
