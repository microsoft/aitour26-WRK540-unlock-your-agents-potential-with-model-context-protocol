## Partecipanti all'Evento Microsoft

Le istruzioni in questa pagina presuppongono che tu stia partecipando a un evento e abbia accesso a un ambiente lab preconfigurato. Questo ambiente fornisce una sottoscrizione Azure con tutti gli strumenti e le risorse necessari per completare il workshop.

## Introduzione

Questo workshop è progettato per insegnarti il Servizio Agenti Azure AI e l'[SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} associato. È composto da più lab, ognuno che evidenzia una caratteristica specifica del Servizio Agenti Azure AI. I lab sono pensati per essere completati in ordine, poiché ognuno si basa sulla conoscenza e il lavoro del lab precedente.

## Selezionare il Linguaggio di Programmazione del Workshop

Il workshop è disponibile sia in Python che in C#. Assicurati di selezionare il linguaggio che si adatta alla stanza lab o alla preferenza utilizzando le schede del selettore di linguaggio. Nota, non cambiare linguaggio a metà workshop.

**Seleziona la scheda del linguaggio che corrisponde alla tua stanza lab:**

=== "Python"
    Il linguaggio predefinito per il workshop è impostato su **Python**.

## Autenticazione con Azure

Devi autenticarti con Azure in modo che l'app agent possa accedere al Servizio Agenti Azure AI e ai modelli. Segui questi passaggi:

1. Apri una finestra terminale. L'app terminale è **fissata** alla barra delle applicazioni di Windows 11.

    ![Apri la finestra terminale](../../media/windows-taskbar.png){ width="300" }

2. Esegui il seguente comando per autenticarti con Azure:

    ```powershell
    az login
    ```

    !!! note
        Ti verrà richiesto di aprire un link del browser e accedere al tuo account Azure.

        1. Una finestra del browser si aprirà automaticamente, seleziona **Account di lavoro o scuola** e poi seleziona **Continua**.
        2. Utilizza il **Nome utente** e il **TAP (Temporary Access Pass)** trovati nella **sezione superiore** della scheda **Risorse** nell'ambiente lab.
        3. Seleziona **Sì, tutte le app**
        4. Seleziona **Fatto**

3. Quindi seleziona la sottoscrizione **Predefinita** dalla riga di comando, selezionando **Invio**.

4. Lascia aperta la finestra terminale per i prossimi passaggi.

## Autenticazione con il Servizio DevTunnel

DevTunnel consente al Servizio Agenti Azure AI di accedere al tuo Server MCP locale durante il workshop.

```powershell
devtunnel login
```

!!! note
    Ti verrà richiesto di utilizzare l'account che hai utilizzato per `az login`. Seleziona l'account e continua.

Lascia aperta la finestra terminale per i prossimi passaggi.

## Aprire il Workshop

Segui questi passaggi per aprire il workshop in Visual Studio Code:

=== "Python"

    Il seguente blocco di comandi aggiorna il repository del workshop, attiva l'ambiente virtuale Python e apre il progetto in VS Code.

    Copia e incolla il seguente blocco di comandi nel terminale e premi **Invio**.

    ```powershell
    ; cd $HOME\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol `
    ; git pull `
    ; .\src\python\workshop\.venv\Scripts\activate `
    ; code .vscode\python-workspace.code-workspace
    ```

    !!! warning "Quando il progetto si apre in VS Code, appaiono due notifiche nell'angolo in basso a destra. Clicca ✖ per chiudere entrambe le notifiche."

## Struttura del Progetto

=== "Python"

    Assicurati di familiarizzare con le **sottocartelle** e i **file** chiave con cui lavorerai durante tutto il workshop.

    5. Il file **main.py**: Il punto di ingresso per l'app, contenente la sua logica principale.
    6. Il file **sales_data.py**: La logica di funzione per eseguire query SQL dinamiche contro il database SQLite.
    7. Il file **stream_event_handler.py**: Contiene la logica del gestore di eventi per lo streaming di token.
    8. La cartella **shared/files**: Contiene i file creati dall'app agent.
    9. La cartella **shared/instructions**: Contiene le istruzioni passate all'LLM.

    ![Struttura delle cartelle del lab](../../media/project-structure-self-guided-python.png)

## Suggerimenti Pro

!!! tips
    1. Il **Menu Hamburger** nel pannello destro dell'ambiente lab offre funzionalità aggiuntive, inclusa la **Vista Finestra Divisa** e l'opzione per terminare il lab. La **Vista Finestra Divisa** ti consente di massimizzare l'ambiente lab a schermo intero, ottimizzando lo spazio dello schermo. Le **Istruzioni** del lab e il pannello **Risorse** si apriranno in una finestra separata.
