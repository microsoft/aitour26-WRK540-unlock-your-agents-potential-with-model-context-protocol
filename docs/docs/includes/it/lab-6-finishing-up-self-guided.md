Questo è tutto per la porzione lab di questo workshop. Continua a leggere per i punti chiave e risorse aggiuntive, ma prima facciamo un po' di pulizia.

## Pulisci GitHub CodeSpaces

### Salva le tue modifiche in GitHub 

Puoi salvare qualsiasi modifica che hai fatto ai file durante il workshop nel tuo repository GitHub personale come fork. Questo rende facile rieseguire il workshop con le tue personalizzazioni, e il contenuto del workshop rimarrà sempre disponibile nel tuo account GitHub.

* In VS Code, clicca lo strumento "Source Control" nel pannello di sinistra. È il terzo dall'alto, oppure puoi usare la scorciatoia da tastiera <kbd>Control-Shift-G</kbd>.
* Nel campo sotto "Source Control" inserisci `Agents Lab` e clicca **✔️Commit**.
  * Clicca **Yes** al prompt "There are no staged changes to commit."
* Clicca **Sync Changes**.
  * Clicca **OK** al prompt "This action will pull and push commits from and to origin/main".

Ora hai la tua copia del workshop con le tue personalizzazioni nel tuo account GitHub.

### Elimina il tuo codespace GitHub

Il tuo GitHub CodeSpace si spegnerà da solo, ma consumerà una piccola quantità della tua allocazione di calcolo e storage finché non viene eliminato. (Puoi vedere il tuo utilizzo nel tuo [riassunto fatturazione GitHub](https://github.com/settings/billing/summary).) Puoi eliminare in sicurezza il codespace ora, come segue:

* Visita [github.com/codespaces](https://github.com/codespaces){:target="_blank"}
* In fondo alla pagina, clicca il menu "..." a destra del tuo codespace attivo
* Clicca **Delete**
  * Al prompt "Are you sure?", clicca **Delete**.

## Elimina le tue risorse Azure

La maggior parte delle risorse che hai creato in questo lab sono risorse pay-as-you-go, il che significa che non ti verranno addebitati altri costi per usarle. Tuttavia, alcuni servizi di storage usati da AI Foundry potrebbero incorrere in piccoli costi ricorrenti. Per eliminare tutte le risorse, segui questi passaggi:

* Visita il [Portale Azure](https://portal.azure.com){:target="_blank"}
* Clicca **Resource groups**
* Clicca sul tuo gruppo di risorse `rg-agent-workshop-****`
* Clicca **Delete Resource group**
* Nel campo in fondo "Enter resource group name to confirm deletion" inserisci `rg-agent-workshop-****`
* Clicca **Delete**
  * Al prompt Delete Confirmation, clicca "Delete"

*Tradotto utilizzando GitHub Copilot e GPT-4o.*
