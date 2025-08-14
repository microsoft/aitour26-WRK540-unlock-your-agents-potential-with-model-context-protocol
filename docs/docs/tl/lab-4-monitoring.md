## Panimula

Pinapanatiling available, performant, at reliable ng monitoring ang iyong Azure AI Foundry Agent Service. Kinokolekta ng Azure Monitor ang metrics at logs, nagbibigay ng real‑time insights, at nagpapadala ng alerts. Gumamit ng dashboards at custom alerts upang subaybayan ang mahahalagang metrics, magsuri ng mga trend, at kumilos nang maagap. Maaaring i-access ang monitoring sa pamamagitan ng Azure portal, CLI, REST API, o client libraries.

## Lab Exercise

1. Mula sa VS Code file explorer, buksan ang `resources.txt` file sa `workshop` folder.
1. **Kopyahin** ang value para sa `AI Project Name` key sa clipboard.
1. Mag-navigate sa [Azure AI Portal All Resources](https://ai.azure.com/allResources) page.
1. Sa search box, i-paste ang kinopyang `AI Project Name`.
1. Piliin ang **AI Project** mula sa search results.

## Buksan ang Monitoring dashboard

1. Mula sa `resources.txt`, kopyahin ang value para sa `Application Insights Name` sa clipboard.
1. Lumipat pabalik sa AI Foundry portal, piliin ang **Monitoring** section sa kaliwang menu.
1. I-paste ang kinopyang `Application Insights Name` sa `Application Insights resource name` dropdown list.
1. Piliin ang **Application Insights** resource mula sa dropdown list.
1. Piliin ang **Connect**.

### Galugarin ang Monitoring dashboard

Pamilyarhin ang iyong sarili sa impormasyon na makikita sa `Application analytics` dashboard.

!!!tip "Maaari kang pumili ng date ranges upang i-filter ang datos na ipinapakita sa monitoring tools."

![The image shows the application monitoring dashboard](../media/monitor_usage.png)

### Subaybayan ang Resource Usage

Maaari kang maghukay nang mas malalim, piliin ang `Resource Usage` upang makita ang detalyadong metrics tungkol sa resource consumption ng iyong AI Project. Muli, maaari mong i-filter ang datos ayon sa time range.

![The image shows the resource usage monitoring dashboard](../media/monitor_resource_usage.png)

*Isinalin gamit ang GitHub Copilot.*
