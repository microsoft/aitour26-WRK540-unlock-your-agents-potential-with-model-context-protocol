## Cosa Imparerai

In questo lab, rivedi e aggiorni le istruzioni dell'agente per includere una regola sull'anno finanziario che inizia il 1° luglio. Questo è importante affinché l'agente interpreti e analizzi correttamente i dati di vendita.

## Introduzione

Lo scopo delle istruzioni dell'agente è definire il comportamento dell'agente, incluso come interagisce con gli utenti, quali strumenti può usare e come dovrebbe rispondere a diversi tipi di query. In questo lab, rivederai le istruzioni esistenti dell'agente e farai un piccolo aggiornamento per garantire che l'agente interpreti correttamente l'anno finanziario.

## Esercizio del Lab

### Apri le Istruzioni dell'Agente

1. Dall'Esploratore di VS Code, naviga alla cartella `shared/instructions`.
2. **Apri** il file `mcp_server_tools_with_code_interpreter.txt`.

### Rivedi le Istruzioni dell'Agente

Rivedi come le istruzioni definiscono il comportamento dell'app agente:

!!! tip "In VS Code, premi Alt + Z (Windows/Linux) o Option + Z (Mac) per abilitare la modalità word wrap, rendendo le istruzioni più facili da leggere."

- **Ruolo Principale:** Agente di vendite per Zava (rivenditore DIY WA) con tono professionale e amichevole usando emoji e nessuna assunzione o contenuto non verificato.
- **Regole Database:** Ottieni sempre prima gli schemi (get_multiple_table_schemas()) con LIMIT 20 obbligatorio su tutte le query SELECT usando nomi esatti di tabelle/colonne.
- **Visualizzazioni:** Crea grafici SOLO quando esplicitamente richiesto usando trigger come "chart", "graph", "visualize", o "show as [type]" in formato PNG scaricato dalla sandbox senza percorsi immagine markdown.
- **Risposte:** Default a tabelle Markdown con supporto multi-lingua e CSV disponibile su richiesta.
- **Sicurezza:** Rimani nell'ambito solo dei dati di vendita Zava con risposte esatte per query fuori ambito/poco chiare e reindirizza utenti ostili all'IT.
- **Vincoli Chiave:** Nessun dato inventato usando solo strumenti con limite di 20 righe e sempre immagini PNG.

### Aggiorna le Istruzioni dell'Agente

Copia il testo qui sotto e incolla direttamente dopo la regola sul non generare contenuto non verificato o fare assunzioni:

!!! tip "Clicca l'icona copia a destra per copiare il testo negli appunti."

```markdown
- L'anno finanziario per Zava inizia il 1° gennaio.
```

Le istruzioni aggiornate dovrebbero apparire così:

```markdown
- **Non generare contenuto non verificato** o fare assunzioni.
- L'anno finanziario per Zava inizia il 1° gennaio.
```

*Tradotto utilizzando GitHub Copilot e GPT-4o.*
