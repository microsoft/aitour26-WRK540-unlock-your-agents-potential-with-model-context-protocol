#!/usr/bin/env bash

curl -sSL https://aspire.dev/install.sh | bash
echo "export PATH=\$HOME/.aspire/bin:\$PATH" >> ~/.zshrc

echo Restoring .NET dependencies
dotnet restore src/csharp

curl -LsSf https://astral.sh/uv/install.sh | sh
