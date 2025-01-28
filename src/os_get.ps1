param (
    [string]$Uri
)

$Password = "9nys3us285"
$Username = "kpwoipavhb" 

if (-not $Uri) {
    Write-Host "Usage: .\os_get.ps1 -Uri <URL>"
    exit 1
}

try {
    # Create the credential object
    $SecurePassword = ConvertTo-SecureString $Password -AsPlainText -Force
    $Credential = New-Object PSCredential($Username, $SecurePassword)

    # Perform the request
    $Response = Invoke-WebRequest -Uri $Uri -Method Get -Credential $Credential -Verbose

    # Display the response content
    Write-Host "`nResponse Content:"
    Write-Host $Response.Content
}
catch {
    Write-Host "An error occurred:" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
