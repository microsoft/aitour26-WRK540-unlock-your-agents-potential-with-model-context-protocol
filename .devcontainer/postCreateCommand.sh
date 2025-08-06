#!/usr/bin/env bash

echo "Preparing the Python environment..."

python -m pip install --upgrade pip

pip install --user -r requirements-dev.txt

pip install --user -r src/python/workshop/requirements.txt

pip install --user -r src/python/mcp_server/sales_analysis/requirements.txt

pip install --user -r src/shared/webapp/requirements.txt

echo "Python environment setup complete."

echo Installing devtunnels
curl -sL https://aka.ms/DevTunnelCliInstall | bash
echo "DevTunnels installed."

echo Setting up Aspire CLI
curl -sSL https://aspire.dev/install.sh | bash

echo Restoring .NET dependencies
dotnet restore src/csharp
