#!/usr/bin/env bash

echo Setting up Aspire CLI
curl -sSL https://aspire.dev/install.sh | bash

echo "Adding Aspire to the zshrc"
echo 'export PATH="$HOME/.aspire/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

echo Restoring .NET dependencies
dotnet restore src/csharp
