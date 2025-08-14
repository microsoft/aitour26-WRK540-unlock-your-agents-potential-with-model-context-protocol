**TBC: Ang label na ito ay makakakuha sa user na i-update ang agent instructions file upang tanggalin ang nakakainis na emojis na ginagamit ng agent sa mga responses nito.**

## Introduction

Tumutulong ang tracing na maintindihan at i-debug ang behavior ng inyong agent sa pamamagitan ng pagpapakita ng sequence ng steps, inputs, at outputs sa panahon ng execution. Sa Azure AI Foundry, nagbibigay-daan ang tracing na ma-observe ninyo kung paano pinoproseso ng inyong agent ang mga requests, tumatawag sa tools, at gumagawa ng responses. Maaari ninyong gamitin ang Azure AI Foundry portal o mag-integrate sa OpenTelemetry at Application Insights upang makuha at mag-analyze ng trace data, na ginagawang mas madaling mag-troubleshoot at mag-optimize ng inyong agent.

<!-- ## Lab Exercise

=== "Python"

      1. Open the `app.py` file.
      2. Change the `AZURE_TELEMETRY_ENABLED` variable to `True` to enable tracing:

         ```python
         AZURE_TELEMETRY_ENABLED = True
         ```

        !!! info "Note"
            This setting enables telemetry for your agent. In the `initialize` function in `app.py`, the telemetry client is configured to send data to Azure Monitor.

            ```python
             if AZURE_TELEMETRY_ENABLED:
                 configure_azure_monitor(connection_string=await self.project_client.telemetry.get_connection_string())
            ```         

=== "C#"

      tbd -->

## Patakbuhin ang Agent App

1. Pindutin ang <kbd>F5</kbd> upang patakbuhin ang app.
2. Piliin ang **Preview in Editor** upang buksan ang agent app sa bagong editor tab.

### Simulan ang Conversation sa Agent

I-copy at paste ang sumusunod na prompt sa agent app upang simulan ang conversation:

```plaintext
Write an executive report that analysis the top 5 product categories and compares performance of the online store verses the average for the physical stores.
```

## Tingnan ang Traces

Maaari ninyong tingnan ang traces ng execution ng inyong agent sa Azure AI Foundry portal o sa pamamagitan ng paggamit ng OpenTelemetry. Ipapakita ng traces ang sequence ng steps, tool calls, at data na na-exchange sa panahon ng execution ng agent. Ang information na ito ay mahalaga para sa debugging at pag-optimize ng performance ng inyong agent.

### Gamit ang Azure AI Foundry Portal

Upang tingnan ang traces sa Azure AI Foundry portal, sundin ang mga steps na ito:

1. Pumunta sa **[Azure AI Foundry](https://ai.azure.com/) portal.
2. Piliin ang inyong project.
3. Piliin ang **Tracing** tab sa left-hand menu.
4. Dito, makikita ninyo ang traces na na-generate ng inyong agent.

   ![](media/ai-foundry-tracing.png)

### Mag-drill Down sa Traces

1. Maaaring kailangan ninyong i-click ang **Refresh** button upang makita ang latest traces dahil maaaring tumagal ng ilang sandali ang traces bago lumabas.
2. Piliin ang trace na nagngangalang `Zava Agent Initialization` upang tingnan ang details.
   ![](media/ai-foundry-trace-agent-init.png)
3. Piliin ang `creare_agent Zava DIY Sales Agent` trace upang tingnan ang details ng agent creation process. Sa `Input & outputs` section, makikita ninyo ang Agent instructions.
4. Susunod, piliin ang `Zava Agent Chat Request: Write an executive...` trace upang tingnan ang details ng chat request. Sa `Input & outputs` section, makikita ninyo ang user input at ang response ng agent.

<!-- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/continuous-evaluation-agents -->

*Isinalin gamit ang GitHub Copilot.*
