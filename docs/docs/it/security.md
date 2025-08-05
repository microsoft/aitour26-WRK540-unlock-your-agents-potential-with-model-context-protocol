Questa applicazione workshop è progettata per educazione e adattamento, e non è intesa per uso in produzione out-of-the-box. Tuttavia, dimostra alcune best practice per la sicurezza.

## Attacchi SQL Malevoli

Una preoccupazione comune con SQL generato da LLM è il rischio di injection o query dannose. Questi rischi sono mitigati limitando i permessi del database.

Questa app usa PostgreSQL con privilegi ristretti per l'agente ed esegue in un ambiente sicuro. La Row-Level Security (RLS) garantisce che gli agenti accedano solo ai dati per i loro negozi assegnati.

In contesti aziendali, i dati sono tipicamente estratti in un database o warehouse di sola lettura con schema semplificato. Questo garantisce accesso sicuro, performante e di sola lettura per l'agente.

## Sandboxing

Questo usa il [Code Interpreter del Servizio Agenti Azure AI](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} per creare ed eseguire codice su richiesta. Il codice viene eseguito in un ambiente di esecuzione sandboxed per prevenire che il codice compia azioni che vanno oltre lo scopo dell'agente.

*Tradotto utilizzando GitHub Copilot e GPT-4o.*
