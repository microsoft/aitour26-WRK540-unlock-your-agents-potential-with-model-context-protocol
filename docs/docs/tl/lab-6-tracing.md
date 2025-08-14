**TBC: Ang label na ito ay magpapagawa sa user na i-update ang agent instructions file upang alisin ang nakakainis na emojis na ginagamit ng agent sa mga tugon nito.**

## Panimula

Tumutulong ang tracing na maunawaan at ma-debug mo ang pag-uugali ng agent sa pamamagitan ng pagpapakita ng sunod-sunod na mga hakbang, input, at output sa oras ng execution. Sa Azure AI Foundry, pinapahintulutan ka ng tracing na obserbahan kung paano pinoproseso ng agent ang mga request, tumatawag ng mga tool, at bumubuo ng mga tugon. Maaari mong gamitin ang Azure AI Foundry portal o mag-integrate sa OpenTelemetry at Application Insights upang kolektahin at suriin ang trace data, na nagpapadali sa pag-troubleshoot at pag-optimize ng performance ng agent.

## Patakbuhin ang Agent App

1. Pindutin ang <kbd>F5</kbd> upang patakbuhin ang app.
2. Piliin ang **Preview in Editor** upang buksan ang agent app sa bagong editor tab.

### Mag-umpisa ng Usapan sa Agent

Kopyahin at i-paste ang sumusunod na prompt sa agent app upang magsimula ng usapan:

```plaintext
Write an executive report that analysis the top 5 product categories and compares performance of the online store verses the average for the physical stores.
```

## Tingnan ang Traces

Maaari mong tingnan ang traces ng execution ng agent sa Azure AI Foundry portal o gamit ang OpenTelemetry. Ipinapakita ng traces ang sunud-sunod na mga hakbang, tool calls, at datos na ipinasa sa panahon ng execution. Napakahalaga ng impormasyong ito para sa pag-debug at pag-optimize ng performance ng agent.

### Gamit ang Azure AI Foundry Portal

Upang tingnan ang traces sa Azure AI Foundry portal, sundin ang mga hakbang na ito:

1. Mag-navigate sa **[Azure AI Foundry](https://ai.azure.com/)** portal.
2. Piliin ang iyong project.
3. Piliin ang **Tracing** tab sa kaliwang menu.
4. Dito, makikita mo ang mga trace na nabuo ng iyong agent.

   ![](media/ai-foundry-tracing.png)

### Pag-drill Down sa Traces

1. Maaaring kailanganin mong i-click ang **Refresh** button upang makita ang pinakabagong traces dahil maaaring ilang sandali bago lumabas ang mga ito.
2. Piliin ang trace na pinangalanang `Zava Agent Initialization` upang makita ang mga detalye.
   ![](media/ai-foundry-trace-agent-init.png)
3. Piliin ang `creare_agent Zava DIY Sales Agent` trace upang makita ang detalye ng proseso ng paglikha ng agent. Sa `Input & outputs` section, makikita mo ang Agent instructions.
4. Susunod, piliin ang `Zava Agent Chat Request: Write an executive...` trace upang makita ang detalye ng chat request. Sa `Input & outputs` section, makikita mo ang user input at ang tugon ng agent.

*Isinalin gamit ang GitHub Copilot.*
