## Cosa Imparerai

In questo lab, rivedi e aggiorna le istruzioni dell'agente per includere una regola sull'anno finanziario che inizia il 1° luglio. Questo è importante perché l'agente interpreti e analizzi correttamente i dati di vendita.

## Introduzione

Lo scopo delle istruzioni dell'agente è definire il comportamento dell'agente, incluso come interagisce con gli utenti, quali strumenti può usare e come dovrebbe rispondere a diversi tipi di query. In questo lab, rivederai le istruzioni esistenti dell'agente e farai un piccolo aggiornamento per assicurarti che l'agente interpreti correttamente l'anno finanziario.

## Esercizio del Lab

### Apri le Istruzioni dell'Agente

1. Dall'Explorer di VS Code, naviga nella cartella `shared/instructions`.
2. **Apri** il file `mcp_server_tools_with_code_interpreter.txt`.

### Rivedi le Istruzioni dell'Agente

Rivedi come le istruzioni definiscono il comportamento dell'app dell'agente:

!!! tip "In VS Code, premi Alt + Z (Windows/Linux) o Option + Z (Mac) per abilitare la modalità a capo automatico, rendendo le istruzioni più facili da leggere."

- **Ruolo Principale:** Agente vendite per Zava (rivenditore DIY WA) con tono professionale e amichevole usando emoji e nessuna assunzione o contenuto non verificato.
- **Regole Database:** Ottieni sempre prima gli schemi (get_multiple_table_schemas()) con LIMIT 20 obbligatorio su tutte le query SELECT usando nomi esatti di tabelle/colonne.
- **Visualizzazioni:** Crea grafici SOLO quando esplicitamente richiesto usando trigger come "grafico", "chart", "visualizza", o "mostra come [tipo]" in formato PNG scaricato da sandbox senza percorsi immagini markdown.
- **Risposte:** Default a tabelle Markdown con supporto multi-lingua e CSV disponibile su richiesta.
- **Sicurezza:** Rimani nell'ambito dei soli dati di vendita Zava con risposte esatte per query fuori ambito/non chiare e reindirizza utenti ostili all'IT.
- **Vincoli Chiave:** Nessun dato inventato usando strumenti solo con limite 20-righe e sempre immagini PNG.

### Aggiorna le Istruzioni dell'Agente

Copia il testo sottostante e incollalo direttamente dopo la regola sul non generare contenuto non verificato o fare assunzioni:

!!! tip "Clicca l'icona di copia a destra per copiare il testo negli appunti."

```markdown
- **L'anno finanziario (AF) inizia il 1° lug** (Q1=lug–set, Q2=ott–dic, Q3=gen–mar, Q4=apr–giu).
```

Le istruzioni aggiornate dovrebbero apparire così:

```markdown
- Usa **solo** output di strumenti verificati; **mai** inventare dati o assunzioni.
- **L'anno finanziario (AF) inizia il 1° lug** (Q1=lug–set, Q2=ott–dic, Q3=gen–mar, Q4=apr–giu).
```

*Tradotto usando GitHub Copilot.*
