## Progetto Azure AI Foundry

## Modelli richiesti per Zava DIY

## Generazione di Dati Sintetici per Zava DIY

Zava DIY è uno strumento progettato per aiutare gli sviluppatori a creare dati sintetici per scopi di test e sviluppo. Consente agli utenti di generare dataset realistici che possono essere utilizzati in varie applicazioni, garantendo che i dati soddisfino requisiti specifici senza compromettere la privacy o la sicurezza.

Il database include:

- **8 negozi** in tutto lo Stato di Washington, ognuno con inventario e dati di vendita unici
- **50.000+ record clienti** in tutto lo Stato di Washington e online
- **400+ prodotti DIY** inclusi strumenti, attrezzature per esterni e forniture per il miglioramento della casa
- **400+ immagini prodotto** collegate al database per ricerche basate su immagini
- **200.000+ transazioni di ordini** con cronologia dettagliata delle vendite
- **3000+ articoli di inventario** distribuiti in più negozi
- **Embedding di immagini** per le immagini dei prodotti che abilitano ricerche di similarità basate su AI (codificate usando [openai/clip-vit-base-patch32](https://huggingface.co/openai/clip-vit-base-patch32/blob/main/README.md){:target="_blank"})
- **Embedding di testo** per le descrizioni dei prodotti che migliorano le capacità di ricerca e raccomandazione [openai/text-embedding-3-small](https://ai.azure.com/catalog/models/text-embedding-3-small){:target="_blank"}

Il database supporta query complesse e analitiche, consentendo un accesso efficiente ai dati di vendite, inventario e clienti. PostgreSQL Row Level Security (RLS) limita gli agenti solo ai dati per i loro negozi assegnati, garantendo sicurezza e privacy.

*Tradotto utilizzando GitHub Copilot e GPT-4o.*
