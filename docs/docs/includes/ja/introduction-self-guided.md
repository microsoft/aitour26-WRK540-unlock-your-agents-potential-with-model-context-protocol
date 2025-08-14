## セルフガイド学習者

これらの指示は、事前設定されたラボ環境にアクセスできないセルフガイド学習者向けです。環境を設定してワークショップを開始するために、以下の手順に従ってください。

## はじめに

このワークショップは、Azure AI エージェントサービスと関連するSDKについて学習することを目的として設計されています。複数のラボで構成され、それぞれがAzure AI エージェントサービスの特定の機能にフォーカスしています。各ラボは前のラボの知識と作業に基づいて構築されるため、順番に完了することを意図しています。

## 前提条件

1. Azure サブスクリプションへのアクセス。Azure サブスクリプションがない場合は、開始前に[無料アカウント](https://azure.microsoft.com/free/){:target="_blank"}を作成してください。
1. GitHub アカウントが必要です。アカウントがない場合は、[GitHub](https://github.com/join){:target="_blank"}で作成してください。

## ワークショッププログラミング言語の選択

ワークショップはPythonとC#の両方で利用可能です。言語セレクタータブを使用して、お好みの言語を選択してください。なお、ワークショップの途中で言語を切り替えないでください。

**お好みの言語のタブを選択してください：**

=== "Python"
    ワークショップのデフォルト言語は **Python** に設定されています。
=== "C#"
    ワークショップのデフォルト言語は **C#** に設定されています。

## ワークショップを開く

推奨：**GitHub Codespaces**、必要なすべてのツールが事前設定された環境を提供します。または、Visual Studio Code **Dev Container** と **Docker** でローカル実行。以下のタブを使用して選択してください。

!!! Tip
    Codespaces または Dev Container のビルドには約5分かかります。ビルドを開始してから、完了するまで**読み続けて**ください。

=== "GitHub Codespaces"

    **GitHub Codespaces で開く**を選択して、GitHub Codespaces でプロジェクトを開きます。

    [![GitHub Codespaces で開く](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol){:target="_blank"}



=== "VS Code Dev Container"

    <!-- !!! warning "Apple Silicon ユーザー"
        まもなく実行する自動デプロイメントスクリプトは、Apple Silicon ではサポートされていません。Dev Container の代わりに、Codespaces または macOS からデプロイメントスクリプトを実行してください。 -->

    または、Visual Studio Code Dev Container を使用してプロジェクトをローカルで開くこともできます。これにより、[Dev Containers 拡張機能](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers){:target="_blank"}を使用してローカル VS Code 開発環境でプロジェクトが開きます。

    1. Docker Desktop を起動します（まだインストールされていない場合はインストールしてください）
    2. **Dev Containers で開く**を選択して、VS Code Dev Container でプロジェクトを開きます。

        [![Dev Containers で開く](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol)

*GitHub Copilot を使用して翻訳されました。*
