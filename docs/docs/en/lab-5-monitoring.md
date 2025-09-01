## Introduction

Monitoring keeps your Azure AI Foundry Agent Service available, performant, and reliable. Azure Monitor collects metrics and logs, provides real‑time insights, and sends alerts. Use dashboards and custom alerts to track key metrics, analyze trends, and respond proactively. Access monitoring via the Azure portal, CLI, REST API, or client libraries.

## Lab Exercise

1. From the VS Code file explorer, open the `resources.txt` file in the `workshop` folder.
1. **Copy** the value for the `AI Project Name` key to the clipboard.
1. Navigate to the [Azure AI Foundry Portal](https://ai.azure.com){:target="_blank"} page.
1. Select your project from the list of foundry projects.

## Open the Monitoring dashboard

1. From the `resources.txt`, copy the value for the `Application Insights Name` to the clipboard.
1. Switch back to the AI Foundry portal, select the **Monitoring** section in the left-hand menu.
1. Paste the copied `Application Insights Name` into the `Application Insights resource name` dropdown list.
1. Select the **Application Insights** resource from the dropdown list.
1. Select **Connect**.

### Explore the Monitoring dashboard

Familiarize yourself with the information available on the `Application analytics` dashboard.

!!!tip "You can select date ranges to filter the data displayed in the monitoring tools."

![The image shows the application monitoring dashboard](../media/monitor_usage.png)

### Monitor Resource Usage

You can dig deeper, select `Resource Usage` to view detailed metrics about your AI Project's resource consumption. Again, you can filter the data by time range.

![The image shows the resource usage monitoring dashboard](../media/monitor_resource_usage.png)
