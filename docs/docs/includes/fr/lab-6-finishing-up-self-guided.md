C'est tout pour la partie lab de cet atelier. Lisez la suite pour les points clés à retenir et les ressources supplémentaires, mais d'abord faisons le ménage.

## Nettoyer GitHub CodeSpaces

### Sauvegarder vos modifications dans GitHub 

Vous pouvez sauvegarder toutes les modifications que vous avez apportées aux fichiers pendant l'atelier dans votre dépôt GitHub personnel en tant que fork. Cela facilite la réexécution de l'atelier avec vos personnalisations, et le contenu de l'atelier restera toujours disponible dans votre compte GitHub.

* Dans VS Code, cliquez sur l'outil "Contrôle de source" dans le panneau de gauche. C'est le troisième en partant du haut, ou vous pouvez utiliser le raccourci clavier <kbd>Control-Shift-G</kbd>.
* Dans le champ sous "Contrôle de source" saisissez `Agents Lab` et cliquez sur **✔️Commit**.
  * Cliquez sur **Oui** à l'invite "Il n'y a pas de modifications mises en scène à commiter."
* Cliquez sur **Synchroniser les modifications**.
  * Cliquez sur **OK** à l'invite "Cette action va tirer et pousser les commits depuis et vers origin/main".

Vous avez maintenant votre propre copie de l'atelier avec vos personnalisations dans votre compte GitHub.

### Supprimer votre codespace GitHub

Votre GitHub CodeSpace s'arrêtera de lui-même, mais il consommera une petite quantité de votre allocation de calcul et de stockage jusqu'à ce qu'il soit supprimé. (Vous pouvez voir votre utilisation dans votre [résumé de facturation GitHub](https://github.com/settings/billing/summary).) Vous pouvez supprimer le codespace en toute sécurité maintenant, comme suit :

* Visitez [github.com/codespaces](https://github.com/codespaces){:target="_blank"}
* En bas de la page, cliquez sur le menu "..." à droite de votre codespace actif
* Cliquez sur **Supprimer**
  * À l'invite "Êtes-vous sûr ?", cliquez sur **Supprimer**.

## Supprimer vos ressources Azure

La plupart des ressources que vous avez créées dans ce lab sont des ressources de paiement à l'usage, ce qui signifie que vous ne serez plus facturé pour les utiliser. Cependant, certains services de stockage utilisés par AI Foundry peuvent engendrer de petits frais récurrents. Pour supprimer toutes les ressources, suivez ces étapes :

* Visitez le [Portail Azure](https://portal.azure.com){:target="_blank"}
* Cliquez sur **Groupes de ressources**
* Cliquez sur votre groupe de ressources `rg-agent-workshop-****`
* Cliquez sur **Supprimer le groupe de ressources**
* Dans le champ en bas "Saisir le nom du groupe de ressources pour confirmer la suppression" saisissez `rg-agent-workshop-****`
* Cliquez sur **Supprimer**
  * À l'invite de confirmation de suppression, cliquez sur "Supprimer"

*Traduit en utilisant GitHub Copilot.*
