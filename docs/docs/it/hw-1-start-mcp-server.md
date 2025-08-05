## Cosa Imparerai

In questo lab, tu:

- Userai DevTunnel per rendere il tuo server MCP locale accessibile ai servizi agente basati su cloud
- Configurerai il tuo ambiente per sperimentazione pratica con il Model Context Protocol

## Introduzione

Il server Model Context Protocol (MCP) è un componente cruciale che gestisce la comunicazione tra Large Language Models (LLM) e strumenti esterni e fonti di dati. Eseguirai il server MCP sulla tua macchina locale, ma il Servizio Agente Azure AI Foundry richiede accesso internet per connettersi ad esso. Per rendere il tuo server MCP locale accessibile da internet, userai un DevTunnel. Questo permette al Servizio Agente di comunicare con il tuo server MCP come se stesse funzionando come un servizio in Azure.

## Opzioni di interfaccia per MCP

MCP supporta due interfacce principali per connettere LLM con strumenti:

- **Streamable HTTP Transport**: Per API e servizi basati su web.
- **Stdio Transport**: Per script locali e strumenti da riga di comando.

Questo lab usa l'interfaccia Streamable HTTP transport per integrarsi con il Servizio Agente Azure AI Foundry.

!!! note
    Normalmente, distribuiresti il server MCP in un ambiente di produzione, ma per questo workshop, lo eseguirai localmente nel tuo ambiente di sviluppo. Questo ti permette di testare e interagire con gli strumenti MCP senza bisogno di una distribuzione completa.

### Avvia un DevTunnel per il Server MCP

1. In un nuovo terminale, autentica DevTunnel. Ti verrà chiesto di accedere con il tuo account Azure, usa lo stesso account che hai usato per accedere al Servizio Agente Azure AI Foundry o al Portale Azure. Esegui il seguente comando:

    ```bash
    devtunnel login
    ```

1. Successivamente, nel terminale dove il server MCP è in esecuzione, avvia un DevTunnel eseguendo:

    ```bash
    devtunnel host -p 8000 --allow-anonymous
    ```

    Questo produrrà un URL di cui avrai bisogno affinché l'agente si connetta al server MCP. L'output sarà simile a:

    ```text
    Hosting port: 8000
    Connect via browser: https://<tunnel-id>-8000.aue.devtunnels.ms
    Inspect network activity: https://<tunnel-id>-8000-inspect.aue.devtunnels.ms
    ```

## Aggiorna la Variabile d'Ambiente DevTunnel

1. Copia l'URL **Connect via browser** negli appunti - ne avrai bisogno nel prossimo lab per configurare l'agente.
2. Apri il file `.env` nella cartella workshop.
3. Aggiorna la variabile `DEV_TUNNEL_URL` con l'URL copiato.

    ```text
    DEV_TUNNEL_URL=https://<tunnel-id>-8000.aue.devtunnels.ms
    ```

## Avvia l'App Agente

1. Copia il testo qui sotto negli appunti:

    ```text
    Debug: Select and Start Debugging
    ```

2. Premi <kbd>F1</kbd> per aprire la Command Palette di VS Code.
3. Incolla il testo nella Command Palette e seleziona **Debug: Select and Start Debugging**.
4. Seleziona **🌎🤖Debug Compound: Agent and MCP (http)** dalla lista. Questo avvierà l'app agente e il client di chat web.

## Avvia una conversazione con l'Agente

Passa alla scheda **Web Chat** nel tuo browser. Dovresti vedere l'app agente in esecuzione e pronta ad accettare domande.

### Debug con DevTunnel

Puoi usare DevTunnel per fare debug del server MCP e dell'app agente. Questo ti permette di ispezionare l'attività di rete e risolvere problemi in tempo reale.

1. Seleziona l'URL **Inspect network activity** dall'output DevTunnel.
2. Questo aprirà una nuova scheda nel tuo browser dove puoi vedere l'attività di rete del server MCP e dell'app agente.
3. Puoi usare questo per fare debug di qualsiasi problema che sorga durante il workshop.

Puoi anche impostare breakpoint nel codice del server MCP e nel codice dell'app agente per fare debug di problemi specifici. Per farlo:

1. Apri il file `sales_analysis.py` nella cartella `mcp_server`.
2. Imposta un breakpoint cliccando nella grondaia accanto al numero di riga dove vuoi mettere in pausa l'esecuzione.
3. Quando l'esecuzione raggiunge il breakpoint, puoi ispezionare variabili, procedere attraverso il codice e valutare espressioni nella Console di Debug.

*Tradotto utilizzando GitHub Copilot e GPT-4o.*
