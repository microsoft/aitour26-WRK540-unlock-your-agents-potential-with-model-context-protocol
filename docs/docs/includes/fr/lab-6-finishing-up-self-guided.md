C'est tout pour la partie laboratoire de cet atelier. Continuez à lire pour les points clés à retenir et les ressources supplémentaires, mais d'abord, faisons un peu de nettoyage.

## Nettoyer les GitHub CodeSpaces

### Sauvegarder vos modifications dans GitHub

Vous pouvez sauvegarder toutes les modifications que vous avez apportées aux fichiers pendant l'atelier dans votre dépôt GitHub personnel comme un fork. Cela facilite la réexécution de l'atelier avec vos personnalisations, et le contenu de l'atelier restera toujours disponible dans votre compte GitHub.

* Dans VS Code, cliquez sur l'outil "Source Control" dans le panneau de gauche. C'est le troisième en descendant, ou vous pouvez utiliser le raccourci clavier <kbd>Control-Shift-G</kbd>.
* Dans le champ sous "Source Control" entrez `Agents Lab` et cliquez sur **✔️Commit**.
  * Cliquez sur **Yes** à l'invite "There are no staged changes to commit."
* Cliquez sur **Sync Changes**.
  * Cliquez sur **OK** à l'invite "This action will pull and push commits from and to origin/main".

Vous avez maintenant votre propre copie de l'atelier avec vos personnalisations dans votre compte GitHub.

### Supprimer votre codespace GitHub

Votre GitHub CodeSpace s'arrêtera tout seul, mais il consommera une petite partie de votre allocation de calcul et de stockage jusqu'à ce qu'il soit supprimé. (Vous pouvez voir votre utilisation dans votre [résumé de facturation GitHub](https://github.com/settings/billing/summary).) Vous pouvez supprimer le codespace en toute sécurité maintenant, comme suit :

* Visitez [github.com/codespaces](https://github.com/codespaces){:target="_blank"}
* En bas de la page, cliquez sur le menu "..." à droite de votre codespace actif
* Cliquez sur **Delete**
  * À l'invite "Are you sure?", cliquez sur **Delete**.

## Supprimer vos ressources Azure

La plupart des ressources que vous avez créées dans ce laboratoire sont des ressources de paiement à l'utilisation, ce qui signifie que vous ne serez plus facturé pour les utiliser. Cependant, certains services de stockage utilisés par AI Foundry peuvent engendrer de petits frais continus. Pour supprimer toutes les ressources, suivez ces étapes :

* Visitez le [Portail Azure](https://portal.azure.com){:target="_blank"}
* Cliquez sur **Resource groups**
* Cliquez sur votre groupe de ressources `rg-agent-workshop-****`
* Cliquez sur **Delete Resource group**
* Dans le champ en bas "Enter resource group name to confirm deletion" entrez `rg-agent-workshop-****`
* Cliquez sur **Delete**
  * À l'invite de Confirmation de Suppression, cliquez sur "Delete"

*Traduit en utilisant GitHub Copilot et GPT-4o.*
