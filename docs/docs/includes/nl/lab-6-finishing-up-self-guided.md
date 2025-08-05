Dat is alles voor het lab gedeelte van deze workshop. Lees verder voor belangrijke aandachtspunten en aanvullende resources, maar laten we eerst opruimen.

## GitHub CodeSpaces Opruimen

### Sla je wijzigingen op in GitHub

Je kunt alle wijzigingen die je hebt gemaakt aan bestanden tijdens de workshop opslaan in je persoonlijke GitHub repository als een fork. Dit maakt het gemakkelijk om de workshop opnieuw uit te voeren met je aanpassingen, en de workshop inhoud blijft altijd beschikbaar in je GitHub account.

* Klik in VS Code op de "Source Control" tool in het linkerpaneel. Het is de derde van boven, of je kunt de toetsencombinatie <kbd>Control-Shift-G</kbd> gebruiken.
* Voer in het veld onder "Source Control" `Agents Lab` in en klik **✔️Commit**.
  * Klik **Ja** op de prompt "There are no staged changes to commit."
* Klik **Sync Changes**.
  * Klik **OK** op de prompt "This action will pull and push commits from and to origin/main".

Je hebt nu je eigen kopie van de workshop met je aanpassingen in je GitHub account.

### Verwijder je GitHub codespace

Je GitHub CodeSpace zal vanzelf afsluiten, maar het zal een kleine hoeveelheid van je compute en storage toewijzing verbruiken totdat het wordt verwijderd. (Je kunt je gebruik zien in je [GitHub Billing summary](https://github.com/settings/billing/summary).) Je kunt de codespace nu veilig verwijderen, als volgt:

* Bezoek [github.com/codespaces](https://github.com/codespaces){:target="_blank"}
* Klik onderaan de pagina op het "..." menu rechts van je actieve codespace
* Klik **Delete**
  * Klik bij de "Are you sure?" prompt op **Delete**.

## Verwijder je Azure resources

De meeste resources die je hebt gemaakt in deze lab zijn pay-as-you-go resources, wat betekent dat je niet meer wordt gefactureerd voor het gebruik ervan. Echter, sommige storage services die door AI Foundry worden gebruikt kunnen kleine doorlopende kosten met zich meebrengen. Om alle resources te verwijderen, volg deze stappen:

* Bezoek de [Azure Portal](https://portal.azure.com){:target="_blank"}
* Klik **Resource groups**
* Klik op je resource groep `rg-agent-workshop-****`
* Klik **Delete Resource group**
* Voer in het veld onderaan "Enter resource group name to confirm deletion" `rg-agent-workshop-****` in
* Klik **Delete**
  * Klik bij de Delete Confirmation prompt op "Delete"

*Vertaald met behulp van GitHub Copilot.*
