## Cosa Imparerai

In questo lab, farai:

- Utilizzare DevTunnel per rendere il tuo server MCP locale accessibile ai servizi agent basati su cloud
- Configurare il tuo ambiente per la sperimentazione pratica con il Model Context Protocol

## Introduzione

Il server Model Context Protocol (MCP) è un componente cruciale che gestisce la comunicazione tra i Large Language Models (LLM) e strumenti e fonti di dati esterni. Eseguirai il server MCP sulla tua macchina locale, ma il Servizio Agenti Azure AI Foundry richiede accesso a internet per connettersi ad esso. Per rendere il tuo server MCP locale accessibile da internet, utilizzerai un DevTunnel. Questo consente al Servizio Agenti di comunicare con il tuo server MCP come se stesse funzionando come servizio in Azure.

## Opzioni di interfaccia per MCP

MCP supporta due interfacce principali per collegare gli LLM con gli strumenti:

- **Streamable HTTP Transport**: Per API e servizi basati su web.
- **Stdio Transport**: Per script locali e strumenti a riga di comando.

Questo lab utilizza l'interfaccia Streamable HTTP transport per integrarsi con il Servizio Agenti Azure AI Foundry.

!!! note
    Normalmente, distribuiresti il server MCP in un ambiente di produzione, ma per questo workshop, lo eseguirai localmente nel tuo ambiente di sviluppo. Questo ti consente di testare e interagire con gli strumenti MCP senza necessità di un deployment completo.

### Avviare un DevTunnel per il Server MCP

1. In un nuovo terminale, autentica DevTunnel. Ti verrà richiesto di accedere con il tuo account Azure, utilizza lo stesso account che hai utilizzato per accedere al Servizio Agenti Azure AI Foundry o al Portale Azure. Esegui il seguente comando:

    ```bash
    devtunnel login
    ```

2. Successivamente, nel terminale dove sta funzionando il server MCP, avvia un DevTunnel eseguendo:

    ```bash
    devtunnel host -p 8000 --allow-anonymous
    ```

    Questo produrrà un URL che ti servirà per consentire all'agent di connettersi al server MCP. L'output sarà simile a:

    ```text
    Hosting port: 8000
    Connect via browser: https://<tunnel-id>-8000.aue.devtunnels.ms
    Inspect network activity: https://<tunnel-id>-8000-inspect.aue.devtunnels.ms
    ```

## Aggiornare la Variabile d'Ambiente DevTunnel

1. Copia l'URL **Connect via browser** negli appunti - ti servirà nel prossimo lab per configurare l'agent.
2. Apri il file `.env` nella cartella workshop.
3. Aggiorna la variabile `DEV_TUNNEL_URL` con l'URL copiato.

    ```text
    DEV_TUNNEL_URL=https://<tunnel-id>-8000.aue.devtunnels.ms
    ```

## Avviare l'App Agent

1. Copia il testo sottostante negli appunti:

    ```text
    Debug: Select and Start Debugging
    ```

2. Premi <kbd>F1</kbd> per aprire la Command Palette di VS Code.
3. Incolla il testo nella Command Palette e seleziona **Debug: Select and Start Debugging**.
4. Seleziona **🌎🤖Debug Compound: Agent and MCP (http)** dalla lista. Questo avvierà l'app agent e il client web chat.

## Iniziare una conversazione con l'Agent

Passa alla scheda **Web Chat** nel tuo browser. Dovresti vedere l'app agent in funzione e pronta ad accettare domande.

### Debugging con DevTunnel

Puoi utilizzare DevTunnel per effettuare il debug del server MCP e dell'app agent. Questo ti consente di ispezionare l'attività di rete e risolvere problemi in tempo reale.

1. Seleziona l'URL **Inspect network activity** dall'output DevTunnel.
2. Questo aprirà una nuova scheda nel tuo browser dove potrai vedere l'attività di rete del server MCP e dell'app agent.
3. Puoi utilizzare questo per il debug di qualsiasi problema che sorge durante il workshop.

Puoi anche impostare breakpoint nel codice del server MCP e nel codice dell'app agent per il debug di problemi specifici. Per fare questo:

1. Apri il file `sales_analysis.py` nella cartella `mcp_server`.
2. Imposta un breakpoint cliccando nella grondaia accanto al numero di riga dove vuoi mettere in pausa l'esecuzione.
3. Quando l'esecuzione raggiunge il breakpoint, puoi ispezionare variabili, procedere passo passo nel codice e valutare espressioni nella Debug Console.
