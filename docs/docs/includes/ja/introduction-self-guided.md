## セルフガイド学習者

これらの指示は、事前設定されたラボ環境にアクセスできないセルフガイド学習者向けです。以下の手順に従って環境をセットアップし、ワークショップを開始してください。

## はじめに

このワークショップは、Azure AI Agents Service と関連する SDK について学習するよう設計されています。Azure AI Agents Service の特定の機能をハイライトする複数のラボで構成されています。各ラボは前のラボの知識と作業に基づいて構築されるため、順番に完了することを意図しています。

## 前提条件

1. Azure サブスクリプションへのアクセス。Azure サブスクリプションをお持の場合は、開始する前に[無料アカウント](https://azure.microsoft.com/free/){:target="_blank"}を作成してください。
1. GitHub アカウントが必要です。お持ちでない場合は、[GitHub](https://github.com/join){:target="_blank"}で作成してください。

## ワークショッププログラミング言語の選択

ワークショップは Python と C# の両方で利用できます。言語セレクタータブを使用して希望の言語を選択してください。ワークショップ途中で言語を切り替えないでください。

**希望の言語のタブを選択してください：**

=== "Python"
    ワークショップのデフォルト言語は **Python** に設定されています。
=== "C#"
    ワークショップのデフォルト言語は **C#** に設定されています。

## ワークショップを開く

このワークショップを実行する**推奨**方法は、**GitHub Codespaces** を使用することです。このオプションは、ワークショップを完了するために必要なすべてのツールとリソースを含む事前設定された環境を提供します。別の方法として、Visual Studio Code Dev Container と Docker を使用してワークショップをローカルで開くこともできます。両方のオプションについて以下で説明します。

!!! Note
    **Codespace または Dev Container のビルドには約5分かかります。プロセスを開始し、ビルド中に指示を読み続けることができます。**

=== "GitHub Codespaces"

    **Open in GitHub Codespaces** を選択して、GitHub Codespaces でプロジェクトを開きます。

    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol){:target="_blank"}

=== "VS Code Dev Container"

    <!-- !!! warning "Apple Silicon ユーザー"
        間もなく実行する自動デプロイメントスクリプトは Apple Silicon でサポートされていません。Dev Container の代わりに Codespaces または macOS からデプロイメントスクリプトを実行してください。 -->

    別の方法として、Visual Studio Code Dev Container を使用してプロジェクトをローカルで開くことができます。これは、[Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers){:target="_blank"}を使用してローカル VS Code 開発環境でプロジェクトを開きます。

    1. Docker Desktop を開始します（まだインストールされていない場合はインストールしてください）
    2. **Dev Containers Open** を選択して、VS Code Dev Container でプロジェクトを開きます。

        [![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol)

*Translated using GitHub Copilot and GPT-4o.*
