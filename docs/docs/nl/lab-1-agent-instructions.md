## Wat Je Gaat Leren

In deze lab bekijk en werk je de agent instructies bij om een regel toe te voegen over het financiële jaar dat begint op 1 juli. Dit is belangrijk zodat de agent verkoopgegevens correct kan interpreteren en analyseren.

## Introductie

Het doel van agent instructies is om het gedrag van de agent te definiëren, inclusief hoe deze met gebruikers interacteert, welke tools het kan gebruiken en hoe het moet reageren op verschillende soorten vragen. In deze lab bekijk je de bestaande agent instructies en maak je een kleine update om ervoor te zorgen dat de agent het financiële jaar correct interpreteert.

## Lab Oefening

### De Agent Instructies Openen

1. Navigeer vanuit de VS Code Explorer naar de `shared/instructions` map.
2. **Open** het `mcp_server_tools_with_code_interpreter.txt` bestand.

### De Agent Instructies Bekijken

Bekijk hoe de instructies het gedrag van de agent app definiëren:

!!! tip "In VS Code, druk op Alt + Z (Windows/Linux) of Option + Z (Mac) om de woordomslag modus in te schakelen, waardoor de instructies gemakkelijker te lezen zijn."

- **Kernrol:** Verkoopagent voor Zava (WA DIY retailer) met professionele, vriendelijke toon met emoji's en geen aannames of niet-geverifieerde inhoud.
- **Database Regels:** Altijd eerst schema's ophalen (get_multiple_table_schemas()) met verplichte LIMIT 20 op alle SELECT queries met exacte tabel/kolomnamen.
- **Visualisaties:** Grafieken ALLEEN maken wanneer expliciet gevraagd met triggers zoals "grafiek", "diagram", "visualiseer", of "toon als [type]" in PNG formaat gedownload van sandbox zonder markdown beeldpaden.
- **Antwoorden:** Standaard naar Markdown tabellen met meertalige ondersteuning en CSV beschikbaar op verzoek.
- **Veiligheid:** Blijf binnen het bereik van alleen Zava verkoopgegevens met exacte antwoorden voor buiten-bereik/onduidelijke vragen en verwijs vijandige gebruikers naar IT.
- **Belangrijke Beperkingen:** Geen verzonnen gegevens met alleen tools met 20-rij limiet en altijd PNG afbeeldingen.

### De Agent Instructies Bijwerken

Kopieer de tekst hieronder en plak deze direct na de regel over het niet genereren van niet-geverifieerde inhoud of het maken van aannames:

!!! tip "Klik op het kopieer icoon rechts om de tekst naar het klembord te kopiëren."

```markdown
- Het financiële jaar voor Zava begint op 1 januari.
```

De bijgewerkte instructies zouden er zo uit moeten zien:

```markdown
- Genereer **geen niet-geverifieerde inhoud** of maak geen aannames.
- Het financiële jaar voor Zava begint op 1 januari.
```

*Vertaald met behulp van GitHub Copilot.*
