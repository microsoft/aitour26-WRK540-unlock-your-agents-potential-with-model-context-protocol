Questo è tutto per la parte lab di questo workshop. Continua a leggere per i punti chiave e le risorse aggiuntive, ma prima facciamo un po' di pulizia.

## Pulire GitHub CodeSpaces

### Salvare le tue modifiche in GitHub 

Puoi salvare eventuali modifiche che hai apportato ai file durante il workshop nel tuo repository GitHub personale come fork. Questo rende facile riese- eseguire il workshop con le tue personalizzazioni, e il contenuto del workshop rimarrà sempre disponibile nel tuo account GitHub.

* In VS Code, clicca sullo strumento "Source Control" nel pannello sinistro. È il terzo dall'alto, oppure puoi usare la scorciatoia da tastiera <kbd>Control-Shift-G</kbd>.
* Nel campo sotto "Source Control" inserisci `Agents Lab` e clicca **✔️Commit**.
  * Clicca **Sì** al prompt "There are no staged changes to commit."
* Clicca **Sync Changes**.
  * Clicca **OK** al prompt "This action will pull and push commits from and to origin/main".

Ora hai la tua copia del workshop con le tue personalizzazioni nel tuo account GitHub.

### Eliminare il tuo GitHub codespace

Il tuo GitHub CodeSpace si spegnerà da solo, ma consumerà una piccola quantità della tua assegnazione di calcolo e storage finché non verrà eliminato. (Puoi vedere il tuo utilizzo nel tuo [Riepilogo fatturazione GitHub](https://github.com/settings/billing/summary).) Puoi eliminare il codespace in sicurezza ora, come segue:

* Visita [github.com/codespaces](https://github.com/codespaces){:target="_blank"}
* Nella parte inferiore della pagina, clicca il menu "..." a destra del tuo codespace attivo
* Clicca **Delete**
  * Al prompt "Are you sure?", clicca **Delete**.

## Eliminare le tue risorse Azure

La maggior parte delle risorse che hai creato in questo lab sono risorse pay-as-you-go, il che significa che non ti verranno addebitati costi aggiuntivi per averle utilizzate. Tuttavia, alcuni servizi di storage utilizzati da AI Foundry potrebbero incorrere in piccoli costi continui. Per eliminare tutte le risorse, segui questi passaggi:

* Visita il [Portale Azure](https://portal.azure.com){:target="_blank"}
* Clicca **Gruppi di risorse**
* Clicca sul tuo gruppo di risorse `rg-agent-workshop-****`
* Clicca **Elimina gruppo di risorse**
* Nel campo in basso "Enter resource group name to confirm deletion" inserisci `rg-agent-workshop-****`
* Clicca **Elimina**
  * Al prompt di Conferma eliminazione, clicca "Elimina"
