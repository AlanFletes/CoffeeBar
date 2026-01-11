<#
.SYNOPSIS
    CoffeeBar Wrapper for PowerShell
    Enables environment refresh via Chocolatey's RefreshEnv if available
#>
param(
    [Parameter(ValueFromRemainingArguments=$true)]
    $ScriptArgs
)

$OriginalLocation = Get-Location
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Join-Path $ScriptDir ".."

Set-Location $ProjectRoot

# Run the Python application
# We use & to run the command and pass all arguments
python -m src.main @ScriptArgs
$PythonExitCode = $LASTEXITCODE

Set-Location $OriginalLocation

# Check if the command was "use" and Python succeeded
if ($ScriptArgs -and $ScriptArgs[0] -eq "use" -and $PythonExitCode -eq 0) {
    # Check for Chocolatey's RefreshEnv alias or command
    if (Get-Command refreshenv -ErrorAction SilentlyContinue) {
        Write-Host "`n[CoffeeBar] Chocolatey detected. Refreshing environment..." -ForegroundColor ConsoleColor
        refreshenv
    } else {
        # Fallback: Try to refresh Env vars manually if Refreshenv is missing
        # This is a lightweight refresh logic for current session
        Write-Host "`n[CoffeeBar] Refreshing environment variables..." -ForegroundColor DarkGray
        
        $env:JAVA_HOME = [System.Environment]::GetEnvironmentVariable("JAVA_HOME", "User")
        
        # Reload Path (Machine + User)
        $MachinePath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
        $UserPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
        $env:Path = "$MachinePath;$UserPath"
        
        Write-Host "Done." -ForegroundColor DarkGray
    }
}

exit $PythonExitCode
