That's all for the lab portion of this workshop. Read on for key takeaways and additional resources, but first let's tidy up.

## Star the GitHub Repository

If you have a GitHub account, you can "star" this repository to make it easy for you to find again in the future.

* Visit the GitHub repository at: [github.com/gloveboxes/Unlock-your-agents-potential-with-Model-Context-Protocol-PostgreSQL-Workshop](https://github.com/gloveboxes/Unlock-your-agents-potential-with-Model-Context-Protocol-PostgreSQL-Workshop){:target="_blank"}
* Log into your GitHub account
* Click **Star** in the top right

To find this workshop again in the future, click your GitHub profile picture in the top-right and click **Your stars**.

## Clean up GitHub CodeSpaces

### Save your changes in GitHub 

You can save any changes you have made to files during the workshop to your personal GitHub repository as a fork. This makes it easy to re-run the workshop with your customizations, and the workshop content will always remain available in your GitHub account.

* In VS Code, click the "Source Control" tool in the left pane. It's the third one down, or you can use the keyboard shortcut <kbd>Control-Shift-G</kbd>.
* In the field under "Source Control" enter `Agents Lab` and click **✔️Commit**.
  * Click **Yes** to the prompt "There are no staged changes to commit."
* Click **Sync Changes**.
  * Click **OK** to the prompt "This action will pull and push commits from and to origin/main".

You now have your own copy of the workshop with your customizations in your GitHub account.

### Delete your GitHub codespace

Your GitHub CodeSpace will shut down by itself, but it will consume a small amount of your compute and storage allotment until it is deleted. (You can see your usage in your [GitHub Billing summary](https://github.com/settings/billing/summary).) You can safely delete the codespace now, as follows:

* Visit [github.com/codespaces](https://github.com/codespaces){:target="_blank"}
* At the bottom of the page, click the "..." menu to the right of your active codespace
* Click **Delete**
  * At the "Are you sure?" prompt, click **Delete**.

## Delete your Azure resources

Most of the resources you created in this lab are pay-as-you-go resources, meaning you won't be charged any more for using them. However, some storage services used by AI Foundry may incur small ongoing charges. To delete all resources, follow these steps:

* Visit the [Azure Portal](https://portal.azure.com){:target="_blank"}
* Click **Resource groups**
* Click on your resource group `rg-agent-workshop-****`
* Click **Delete Resource group**
* In the field at the bottom "Enter resource group name to confirm deletion" enter `rg-agent-workshop-****`
* Click **Delete**
  * At the Delete Confirmation prompt, click "Delete"