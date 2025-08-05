**NTB: Deze label zorgt ervoor dat de gebruiker het agent instructiebestand bijwerkt om de vervelende emoji's te verwijderen die de agent gebruikt in zijn antwoorden.**

## Introductie

Tracing helpt je het gedrag van je agent te begrijpen en te debuggen door de volgorde van stappen, inputs en outputs tijdens uitvoering te tonen. In Azure AI Foundry stelt tracing je in staat om te observeren hoe je agent verzoeken verwerkt, tools aanroept en antwoorden genereert. Je kunt de Azure AI Foundry portal gebruiken of integreren met OpenTelemetry en Application Insights om trace-gegevens te verzamelen en analyseren, waardoor het gemakkelijker wordt om je agent te troubleshooten en optimaliseren.

<!-- ## Lab Oefening

=== "Python"

      1. Open het `app.py` bestand.
      2. Verander de `AZURE_TELEMETRY_ENABLED` variabele naar `True` om tracing in te schakelen:

         ```python
         AZURE_TELEMETRY_ENABLED = True
         ```

        !!! info "Opmerking"
            Deze instelling schakelt telemetrie in voor je agent. In de `initialize` functie in `app.py` wordt de telemetrie client geconfigureerd om gegevens naar Azure Monitor te sturen.

            ```python
             if AZURE_TELEMETRY_ENABLED:
                 configure_azure_monitor(connection_string=await self.project_client.telemetry.get_connection_string())
            ```         

=== "C#"

      tbd -->

## De Agent App Uitvoeren

1. Druk op <kbd>F5</kbd> om de app uit te voeren.
2. Selecteer **Preview in Editor** om de agent app in een nieuw editor tabblad te openen.

### Een Gesprek Starten met de Agent

Kopieer en plak de volgende prompt in de agent app om een gesprek te starten:

```plaintext
Schrijf een executive rapport dat de top 5 productcategorieën analyseert en de prestaties van de online winkel vergelijkt met het gemiddelde van de fysieke winkels.
```

## Traces Bekijken

Je kunt de traces van de uitvoering van je agent bekijken in de Azure AI Foundry portal of door OpenTelemetry te gebruiken. De traces tonen de volgorde van stappen, tool-aanroepen en gegevens die worden uitgewisseld tijdens de uitvoering van de agent. Deze informatie is cruciaal voor het debuggen en optimaliseren van de prestaties van je agent.

### Azure AI Foundry Portal Gebruiken

Om traces te bekijken in de Azure AI Foundry portal, volg deze stappen:

1. Navigeer naar de **[Azure AI Foundry](https://ai.azure.com/) portal.
2. Selecteer je project.
3. Selecteer het **Tracing** tabblad in het linkermenu.
4. Hier kun je de traces zien die door je agent zijn gegenereerd.

   ![](media/ai-foundry-tracing.png)

### Inzoomen op Traces

1. Je moet mogelijk op de **Refresh** knop klikken om de nieuwste traces te zien omdat traces enkele momenten kunnen duren om te verschijnen.
2. Selecteer de trace genaamd `Zava Agent Initialization` om de details te bekijken.
   ![](media/ai-foundry-trace-agent-init.png)
3. Selecteer de `creare_agent Zava DIY Sales Agent` trace om de details van het agent aanmaakproces te bekijken. In de `Input & outputs` sectie zie je de Agent instructies.
4. Selecteer vervolgens de `Zava Agent Chat Request: Write an executive...` trace om de details van het chat verzoek te bekijken. In de `Input & outputs` sectie zie je de gebruikersinput en het antwoord van de agent.

<!-- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/continuous-evaluation-agents -->

*Vertaald met behulp van GitHub Copilot.*
