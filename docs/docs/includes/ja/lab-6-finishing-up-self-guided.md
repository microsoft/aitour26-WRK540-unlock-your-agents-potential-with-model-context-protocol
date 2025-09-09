このワークショップのラボ部分は以上です。主なポイントと追加リソースについて読み進めてください。しかし、まず最初に片付けをしましょう。

## GitHub CodeSpacesのクリーンアップ

### GitHubで変更を保存する

ワークショップ中にファイルに加えた変更を、フォークとして個人のGitHubリポジトリに保存することができます。これにより、カスタマイズしたワークショップを簡単に再実行でき、ワークショップのコンテンツは常にGitHubアカウントで利用可能な状態が維持されます。

* VS Codeで、左ペインの「Source Control」ツールをクリックします。下から3番目にあるか、キーボードショートカット<kbd>Control-Shift-G</kbd>を使用できます。
* 「Source Control」の下のフィールドに`Agents Lab`と入力し、**✔️Commit**をクリックします。
  * 「There are no staged changes to commit.」のプロンプトで**Yes**をクリックします。
* **Sync Changes**をクリックします。
  * 「This action will pull and push commits from and to origin/main」のプロンプトで**OK**をクリックします。

これで、カスタマイズしたワークショップのコピーがGitHubアカウントに保存されました。

### GitHub codespaceを削除する

GitHub CodeSpaceは自動的にシャットダウンしますが、削除されるまでコンピューティングとストレージの少量の割り当てを消費します。（使用状況は[GitHub請求サマリー](https://github.com/settings/billing/summary)で確認できます。）以下の手順で安全にcodespaceを削除できます：

* [github.com/codespaces](https://github.com/codespaces){:target="_blank"}を訪問する
* ページ下部で、アクティブなcodespaceの右側の「...」メニューをクリックします
* **Delete**をクリックします
  * 「Are you sure?」のプロンプトで、**Delete**をクリックします。

## Azureリソースを削除する

このラボで作成したリソースのほとんどは従量課金制のリソースで、使用に対してこれ以上課金されることはありません。ただし、AI Foundryで使用される一部のストレージサービスは、わずかな継続課金が発生する可能性があります。すべてのリソースを削除するには、以下の手順に従ってください：

* [Azure Portal](https://portal.azure.com){:target="_blank"}を訪問する
* **Resource groups**をクリックします
* リソースグループ`rg-agent-workshop-****`をクリックします
* **Delete Resource group**をクリックします
* 下部の「Enter resource group name to confirm deletion」フィールドに`rg-agent-workshop-****`と入力します
* **Delete**をクリックします
  * 削除確認プロンプトで「Delete」をクリックします
