## Azure AI Foundry Project

## Modellen vereist voor Zava DIY

## Synthetische Gegevensgeneratie voor Zava DIY

Zava DIY is een tool die is ontworpen om ontwikkelaars te helpen bij het maken van synthetische gegevens voor test- en ontwikkelingsdoeleinden. Het stelt gebruikers in staat om realistische datasets te genereren die kunnen worden gebruikt in verschillende applicaties, waarbij ervoor wordt gezorgd dat de gegevens voldoen aan specifieke vereisten zonder privacy of beveiliging in gevaar te brengen.

De database omvat:

- **8 winkels** verspreid over Washington State, elk met unieke voorraad- en verkoopgegevens
- **50.000+ klantrecords** verspreid over Washington State en online
- **400+ DIY-producten** inclusief gereedschap, buitenuitrusting en woningverbeteringsbenodigdheden
- **400+ productafbeeldingen** gekoppeld aan de database voor op afbeeldingen gebaseerde zoekopdrachten
- **200.000+ besteltransacties** met gedetailleerde verkoopgeschiedenis
- **3000+ voorraadartikelen** verspreid over meerdere winkels
- **Afbeeldingsembeddings** voor productafbeeldingen die AI-gestuurde gelijkenis zoekopdrachten mogelijk maken (gecodeerd met [openai/clip-vit-base-patch32](https://huggingface.co/openai/clip-vit-base-patch32/blob/main/README.md){:target="_blank"})
- **Tekst embeddings** voor productbeschrijvingen die zoek- en aanbevelingsmogelijkheden verbeteren [openai/text-embedding-3-small](https://ai.azure.com/catalog/models/text-embedding-3-small){:target="_blank"}

De database ondersteunt complexe queries en analyses, waardoor efficiënte toegang tot verkoop-, voorraad- en klantgegevens mogelijk is. PostgreSQL Row Level Security (RLS) beperkt agents tot alleen de gegevens van hun toegewezen winkels, waardoor beveiliging en privacy worden gewaarborgd.

*Vertaald met behulp van GitHub Copilot.*
