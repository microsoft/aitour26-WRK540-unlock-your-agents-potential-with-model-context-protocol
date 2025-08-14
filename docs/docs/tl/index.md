# I-unlock ang Potensyal ng Iyong Agent gamit ang Model Context Protocol

Maligayang pagdating sa Foundry Agent Service workshop para sa agents, Model Context Protocol (MCP), semantic search, at pagmamasid.

Sa workshop na ito matutuklasan mo kung paano lumikha ng AI agent na may napalawak na kakayahan gamit ang Model Context Protocol.

Gagamitin mo ang Agent API para gumawa ng AI agent na ma-trigger ng isang web application. Gagamitin din natin ang Foundry Workflows para ma-automate ang mga agha at orchestrate ang mga tool. Gagawa rin tayo ng semantic search na Tool para maresolba ang isang tanong tungkol sa isang partikular na dog chew toy na may worm egg pheromones.

Ang workshop na ito ay self-guided upang makapagtrabaho ka sa iyong sariling bilis at interes. Maaari mo ring kunin ang Content Experiment bilang isang karagdagang home exercise: lumikha ng isang tool na nagsasagawa ng mga mungkahi sa, o nag-aayos ng pagbaybay sa, product content para sa mga nagtitinda na gumagamit ng imaginary Zava Retail marketplace. Isang kopya ng agent service code sa Python at C# ay ibinibigay. Maaari mong gamitin ang alinman, o parehong codebase.

Maaari kang magsimula agad sa cloud na bersyon ng mga lab kung mayroon kang Azure subscription.

## Mga Pangunahing Konsepto

1. Foundry Agent Service
2. Model Context Protocol
3. Foundry Dev Home
4. Foundry Monitoring
5. Foundry Observability
6. Observability metrics
7. Observability tracing

![Mga Pangunahing Konsepto](../media/retail-scenario.svg)

## Mga Kinakailangan

Ang mga lab ay tinest laban sa macOS, Ubuntu, at Windows 11 sa WSL gamit ang Ubuntu 22.04. Kung gumagamit ka ng Windows, inirerekomenda namin na gamitin mo ang WSL. Kung gumagamit ka ng Ubuntu, gumamit ng Ubuntu 22.04.

May dalawang paraan para kumpletuhin ang mga lab na ito.

> Importante: Kung gumagawa ka nito sa Live Azure workshop events, mangyaring gawin ang iyong mga labs mula sa Zava Live Workshop jump server na ibinigay sa iyo. Huwag gumawa ng mga resource sa sarili mong Azure subscription.

## 1. Cloud Hosted Workshop Environment

May game day workshop environment kami sa cloud. May kasama itong pag-access sa Azure Foundry service na nagbibigay sa iyo ng access sa Foundry, Foundry Agent Service, at Observability para magamit mo sa mga lab ng workshop. Sinusuportahan nito ang parehong Python at C# na mga bersyon para sa Microsoft AI Tour workshops.

Ang lab environment ay nagbibigay ng ating sariling Tagubilin, Visual Studio Code development environment, at Azure Subscription na naglalaman ng Azure Foundry Service.

## 2. Lokal na Geography

Kung wala kang access sa Foundry services, kumpletohin ang alokasyon gamit ang Service agnostic tool list. Tandaan na ang instruction environment ay hindi bahagi ng lokal na simula.

## Mga Mga Barya

Kung ginagawa mo ang workshop na ito sa isang Live IF (In-Person) event, maaari kang kumita ng mga badge. Tandaan ang tatlong pangunahing badge na nakalista sa ibaba. May iba pang mga badge na nais mong alamin sa iyong facilitator.

1. Retail Starter Ace: I-unlock: Setup
2. Retail Agent Ace: I-unlock: Agent Tools at Observability
3. Retail ZPM Ace at ang Maui code: Sa labas ng scope ng workshop na ito ngunit maaari mong makuha kung maglaan ka ng oras upang gawin ang Content Experiment!

Para sa karagdagang impormasyon, tingnan ang [Retail Scenario Event Guide](https://aka.ms/ai-tour-26-retail-scenario-event-guide){:target="_blank"}.

## Mga Karagdagang Tool

Para sa Python agent code, maaaring gumamit ka ng ilang iba't ibang mga tool para simulan, subukan ang Agent code, at pagsamahin sa Foundry Agent API. Tinutukoy ng mga lab ang pangunahing paggamit ng bawat isa.

1. Agent Service: Gumagamit ng Python Foundry Agent SDK para gumawa ng Agent, Workflow, at i-integrate ang tool code na nagbibigay ng bagong kakayahan sa Foundry agent.
2. Zava Retail Web App: Gumagamit ng Product search tool para magamit ng stored embeddings data sa database.

> Tip: Ginagawa ng Makefile ang pag-install at pag-download ng mga runtime at dependency na medyo mas simple – at binabawasan ang mga potensyal na error na maaaring maranasan.

## Mga Workshop Materyales

Ang code at mga dokumento para sa workshop na ito ay available sa [GitHub](https://github.com/gloveboxes/Unlock-your-agents-potential-with-Model-Context-Protocol-PostgreSQL-Workshop){:target="_blank"}

Ito ang opisyal na paglalarawan ng workshop.

## Licensya at Pagpapaunlad at Pagbabago

Ang workshop na ito ay released sa ilalim ng Open Source MIT license. Nakatuon kami na panatilihing up to date ang materyal na ito. Kung nakakita ka ng isyu o may mungkahi, mangyaring mag-file ng issue o magpadala ng pull request.

> Importante: Tingnan ang mga instructor kung nagsasagawa ka ng mga workshop sa Microsoft AI Tour events upang tama nilang ma-highlight ang iyong mga kontribusyon.

Maaari mong ma-clone at gamitin muli ang workshop code at docs pattern para sa iyong sariling mga workshop at training events.

## Mga Bahagi ng Workshop

Ang workshop ay binubuo ng mga sumusunod na bahagi:

### Core Labs

Ang mga core lab ay nagdagdag ng function onsite, madi-dagdagang kagalingan, content filter, Observability, at Tracing. Ang mga ito ay ang core labup.

1. Getting Started — Paliwanag ng scenario at konteksto ng agent service
2. Lab 1: Agent Overview — Pag-unawa sa Foundry Agent Service (Event Only)
3. Lab 2: Agent Tools — Pagdaragdag ng mga tool sa Foundry agent
4. Lab 3: Semantic Search Tools — Pagdaragdag ng semantic search tool habang gumagawa ng Tool API
5. Lab 4: Observability Monitoring — Pagdaragdag ng mga metrics at logging sa isang hypothetical bakery
6. Lab 5: Continuous Evaluation — Pagdaragdag ng patuloy na pagsusuri sa Foundry Agent at Workflow
7. Lab 6: Observability Tracing — Pagdagdag ng deep tracing sa isang bakery shop
8. Lab 7: Finishing Up — Ano na ang susunod? Tapos ka na!

### Mga Karagdagang Lab

Ang mga karagdagang lab ay nagbibigay ng mga ideya sa pagpapatupad at testing. Ang mga ito ay hindi graded at talagang magandang bagay na magkaroon. Patuloy na babalik upang makita kung may mga idinagdag na karagdagang lab.

Para sa iba pang opsyon, maaaring pumunta ka sa completion suggestion as extended home. Gagawa ka ng bagong tool upang magsagawa ng pag-suggest ng content na gumagawa ng pagbabago o paggamit brand compliance checks sa CONTENT codebase.

*Isinalin gamit ang GitHub Copilot.*
