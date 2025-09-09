这就是本工作坊实验部分的全部内容。请继续阅读关键要点和其他资源，但首先让我们进行清理工作。

## 清理 GitHub CodeSpaces

### 在 GitHub 中保存您的更改

您可以将在工作坊期间对文件所做的任何更改作为 fork 保存到您的个人 GitHub 仓库中。这使得您能够轻松地使用自定义设置重新运行工作坊，并且工作坊内容将始终在您的 GitHub 账户中可用。

* 在 VS Code 中，点击左侧面板中的"Source Control"工具。它是从上往下第三个，或者您可以使用键盘快捷键 <kbd>Control-Shift-G</kbd>。
* 在"Source Control"下的字段中输入 `Agents Lab` 并点击 **✔️Commit**。
  * 对提示"There are no staged changes to commit."点击 **Yes**。
* 点击 **Sync Changes**。
  * 对提示"This action will pull and push commits from and to origin/main"点击 **OK**。

现在您的 GitHub 账户中有了包含您自定义设置的工作坊副本。

### 删除您的 GitHub codespace

您的 GitHub CodeSpace 会自动关闭，但在删除之前，它会消耗少量的计算和存储配额。（您可以在您的 [GitHub 账单摘要](https://github.com/settings/billing/summary) 中查看使用情况。）您现在可以安全地删除 codespace，操作如下：

* 访问 [github.com/codespaces](https://github.com/codespaces){:target="_blank"}
* 在页面底部，点击您活动 codespace 右侧的"..."菜单
* 点击 **Delete**
  * 在"Are you sure?"提示时，点击 **Delete**。

## 删除您的 Azure 资源

您在此实验中创建的大多数资源都是按使用付费的资源，这意味着您不会因使用它们而被进一步收费。但是，AI Foundry 使用的一些存储服务可能会产生小额持续费用。要删除所有资源，请按照以下步骤操作：

* 访问 [Azure 门户](https://portal.azure.com){:target="_blank"}
* 点击 **Resource groups**
* 点击您的资源组 `rg-agent-workshop-****`
* 点击 **Delete Resource group**
* 在底部的字段"Enter resource group name to confirm deletion"中输入 `rg-agent-workshop-****`
* 点击 **Delete**
  * 在删除确认提示时，点击 "Delete"

*使用 GitHub Copilot 翻译。*
