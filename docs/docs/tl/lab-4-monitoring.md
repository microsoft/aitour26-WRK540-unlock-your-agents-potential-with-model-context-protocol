## Introduction

Sinisiguro ng monitoring na ang inyong Azure AI Foundry Agent Service ay available, performant, at reliable. Kinokolekta ng Azure Monitor ang metrics at logs, nagbibigay ng real‑time insights, at nagpapadala ng alerts. Gamitin ang dashboards at custom alerts upang subaybayan ang key metrics, mag-analyze ng trends, at tumugon nang proactive. I-access ang monitoring sa pamamagitan ng Azure portal, CLI, REST API, o client libraries.

## Lab Exercise

1. Mula sa VS Code file explorer, buksan ang `resources.txt` file sa `workshop` folder.
1. **I-copy** ang value para sa `AI Project Name` key sa clipboard.
1. Pumunta sa [Azure AI Portal All Resources](https://ai.azure.com/allResources) page.
1. Sa search box, i-paste ang copied `AI Project Name`.
1. Piliin ang **AI Project** mula sa search results.

## Buksan ang Monitoring dashboard

1. Mula sa `resources.txt`, i-copy ang value para sa `Application Insights Name` sa clipboard.
1. Bumalik sa AI Foundry portal, piliin ang **Monitoring** section sa left-hand menu.
1. I-paste ang copied `Application Insights Name` sa `Application Insights resource name` dropdown list.
1. Piliin ang **Application Insights** resource mula sa dropdown list.
1. Piliin ang **Connect**.

### I-explore ang Monitoring dashboard

Pamilyaruhin ang sarili sa information na available sa `Application analytics` dashboard.

!!!tip "Maaari ninyong piliin ang date ranges upang i-filter ang data na pinapakita sa monitoring tools."

![The image shows the application monitoring dashboard](../media/monitor_usage.png)

### I-monitor ang Resource Usage

Maaari ninyong magpatuloy sa mas malalim na pag-alam, piliin ang `Resource Usage` upang makita ang detalyadong metrics tungkol sa resource consumption ng inyong AI Project. Muli, maaari ninyong i-filter ang data by time range.

![The image shows the resource usage monitoring dashboard](../media/monitor_resource_usage.png)

*Isinalin gamit ang GitHub Copilot.*
