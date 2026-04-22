Set-Location $PSScriptRoot

$principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Start-Process -FilePath powershell -Verb RunAs -ArgumentList '-ExecutionPolicy', 'Bypass', '-File', "`"$PSCommandPath`""
    exit
}

$listener = netstat -ano | Select-String '127.0.0.1:8000' | Select-Object -First 1

if ($listener) {
    $parts = ($listener.ToString() -split '\s+') | Where-Object { $_ }
    $pid = $parts[-1]

    if ($pid -match '^\d+$') {
        $process = Get-Process -Id $pid -ErrorAction SilentlyContinue

        if ($process -and $process.ProcessName -eq 'python') {
            Stop-Process -Id $pid -Force
            Start-Sleep -Seconds 1
        }
    }
}

python -B .\launcher_web\app.py
