#!/usr/bin/env pwsh

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TunnelJsonFile = "dev_tunnel.json"

# Function to get tunnel ID from dev_tunnel.json file
function Get-TunnelIdFromJson {
    if (Test-Path $TunnelJsonFile) {
        try {
            $tunnelData = Get-Content $TunnelJsonFile | ConvertFrom-Json
            $tunnelId = $tunnelData.tunnel.tunnelId
            if ($tunnelId -and $tunnelId -ne "null") {
                Write-Host "Found tunnel ID in $TunnelJsonFile`: $tunnelId" -ForegroundColor Yellow
                return $tunnelId
            } else {
                Write-Warning "Could not extract tunnel ID from $TunnelJsonFile"
                return $null
            }
        } catch {
            Write-Warning "Error reading $TunnelJsonFile`: $_"
            return $null
        }
    } else {
        Write-Warning "$TunnelJsonFile not found"
        return $null
    }
}

# Function to check if DevTunnel is already running (cross-platform)
function Test-DevTunnelRunning {
    try {
        if ($IsWindows -or $PSVersionTable.PSVersion.Major -le 5) {
            # Windows
            $processes = Get-Process | Where-Object { $_.ProcessName -like "*devtunnel*" -and $_.CommandLine -like "*host*" }
            return $processes.Count -gt 0
        } else {
            # Linux/macOS
            $processes = Get-Process | Where-Object { $_.ProcessName -like "*devtunnel*" }
            if ($processes.Count -gt 0) {
                # Additional check using ps to verify command line on Unix systems
                $psOutput = & ps aux | Select-String "devtunnel host"
                return $psOutput.Count -gt 0
            }
            return $false
        }
    } catch {
        # Fallback: try to find process using cross-platform approach
        try {
            $null = & pgrep -f "devtunnel host" 2>$null
            return $LASTEXITCODE -eq 0
        } catch {
            return $false
        }
    }
}

# Function to get running DevTunnel process ID
function Get-DevTunnelProcessId {
    try {
        if ($IsWindows -or $PSVersionTable.PSVersion.Major -le 5) {
            # Windows
            $process = Get-Process | Where-Object { $_.ProcessName -like "*devtunnel*" } | Select-Object -First 1
            return $process.Id
        } else {
            # Linux/macOS - try pgrep first
            try {
                $pid = & pgrep -f "devtunnel host" 2>$null
                if ($LASTEXITCODE -eq 0) {
                    return $pid
                }
            } catch {
                # Fallback to Get-Process
                $process = Get-Process | Where-Object { $_.ProcessName -like "*devtunnel*" } | Select-Object -First 1
                return $process.Id
            }
        }
    } catch {
        return $null
    }
}

# Function to test if tunnel exists
function Test-TunnelExists {
    param($tunnelId)
    
    try {
        $null = & devtunnel show $tunnelId 2>$null
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

# Function to create and host new tunnel
function New-DevTunnel {
    Write-Host "Creating new DevTunnel on port 8000..." -ForegroundColor Green
    
    try {
        $tunnelJson = & devtunnel create --allow-anonymous --json
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create tunnel"
        }
        
        $tunnelData = $tunnelJson | ConvertFrom-Json
        $newTunnelId = $tunnelData.tunnel.tunnelId
        
        if ($newTunnelId -and $newTunnelId -ne "null") {
            Write-Host "Created tunnel with ID: $newTunnelId" -ForegroundColor Green
            
            # Create port
            & devtunnel port create $newTunnelId -p 8000
            if ($LASTEXITCODE -ne 0) {
                Write-Warning "Failed to create port for tunnel $newTunnelId"
            }
            
            # Save tunnel info
            & devtunnel show $newTunnelId --json | Out-File -FilePath $TunnelJsonFile -Encoding UTF8
            
            # Host the tunnel
            Write-Host "Hosting tunnel: $newTunnelId" -ForegroundColor Green
            & devtunnel host $newTunnelId --allow-anonymous 2>&1 | Tee-Object -FilePath "dev_tunnel.log"
        } else {
            throw "Failed to extract tunnel ID from created tunnel"
        }
    } catch {
        Write-Error "Failed to create tunnel: $_"
        Write-Host "Check that devtunnel is authenticated:" -ForegroundColor Yellow
        Write-Host "devtunnel login" -ForegroundColor Cyan
    }
}

# Main script logic
Write-Host "Starting DevTunnel management script..." -ForegroundColor Cyan

# Get tunnel ID from JSON file
$tunnelId = Get-TunnelIdFromJson

# Check if DevTunnel is already running
if (Test-DevTunnelRunning) {
    $pid = Get-DevTunnelProcessId
    Write-Host "DevTunnel is already running (PID: $pid)" -ForegroundColor Yellow
    Write-Host "Connect via existing tunnel" -ForegroundColor Green
} else {
    if ($tunnelId) {
        Write-Host "Checking if tunnel exists: $tunnelId" -ForegroundColor Cyan
        
        # Check if the tunnel exists using devtunnel show
        Write-Host "Testing if tunnel $tunnelId exists..." -ForegroundColor Cyan
        if (Test-TunnelExists $tunnelId) {
            Write-Host "Tunnel exists, hosting: $tunnelId" -ForegroundColor Green
            & devtunnel host $tunnelId --allow-anonymous 2>&1 | Tee-Object -FilePath "dev_tunnel.log"
        } else {
            Write-Host "Tunnel not found: $tunnelId" -ForegroundColor Yellow
            New-DevTunnel
        }
    } else {
        Write-Host "No tunnel ID found, starting new DevTunnel on port 8000..." -ForegroundColor Cyan
        New-DevTunnel
    }
}
