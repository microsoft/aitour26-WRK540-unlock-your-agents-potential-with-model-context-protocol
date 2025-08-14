## Ano ang Iyong Matututuhan

Sa lab na ito, gagawin mo ang sumusunod:

- Gumamit ng DevTunnel upang ma-access ng cloud-based agent services ang lokal mong MCP server
- Isaayos ang iyong environment para sa hands-on na eksperimento sa Model Context Protocol

## Panimula

Ang Model Context Protocol (MCP) server ay isang mahalagang bahagi na humahawak sa komunikasyon sa pagitan ng Large Language Models (LLMs) at panlabas na mga tool at pinagkukunan ng datos. Patatakbuhin mo ang MCP server sa iyong lokal na makina, ngunit nangangailangan ang Azure AI Foundry Agent Service ng internet access upang kumonekta rito. Upang gawing accessible mula sa internet ang lokal mong MCP server, gagamit ka ng DevTunnel. Pinapayagan nitong makipag-usap ang Agent Service sa iyong MCP server na para bang tumatakbo ito bilang isang serbisyo sa Azure.

## Mga Opsyon sa Interface para sa MCP

Sinusuportahan ng MCP ang dalawang pangunahing interface para ikonekta ang LLMs sa mga tool:

- **Streamable HTTP Transport**: Para sa mga web-based API at serbisyo.
- **Stdio Transport**: Para sa lokal na mga script at command-line na mga tool.

Gumagamit ang lab na ito ng Streamable HTTP transport interface upang mag-integrate sa Azure AI Foundry Agent Service.

!!! note
    Karaniwan, ide-deploy mo ang MCP server sa isang production environment, ngunit para sa workshop na ito, patatakbuhin mo ito nang lokal sa iyong development environment. Pinapahintulutan kang subukan at makipag-interact sa MCP tools nang hindi kailangan ng full deployment.

### Mag-start ng DevTunnel para sa MCP Server

1. Sa isang bagong terminal, i-authenticate ang DevTunnel. Ma-pi-prompt kang mag-log in gamit ang iyong Azure account; gamitin ang parehong account na ginamit mo para mag-log in sa Azure AI Foundry Agent Service o Azure Portal. Patakbuhin ang sumusunod na command:

    ```bash
    devtunnel login
    ```

1. Susunod, sa terminal kung saan tumatakbo ang MCP server, simulan ang DevTunnel sa pamamagitan ng pagpapatakbo ng:

    ```bash
    devtunnel host -p 8000 --allow-anonymous
    ```

    Maglalabas ito ng isang URL na kakailanganin mo para makakonekta ang agent sa MCP server. Ang output ay magiging katulad ng:

    ```text
    Hosting port: 8000
    Connect via browser: https://<tunnel-id>-8000.aue.devtunnels.ms
    Inspect network activity: https://<tunnel-id>-8000-inspect.aue.devtunnels.ms
    ```

## I-update ang DevTunnel Environment Variable

1. Kopyahin ang **Connect via browser** URL sa clipboard - kakailanganin mo ito sa susunod na lab para i-configure ang agent.
2. Buksan ang `.env` file sa workshop folder.
3. I-update ang `DEV_TUNNEL_URL` variable gamit ang kinopyang URL.

    ```text
    DEV_TUNNEL_URL=https://<tunnel-id>-8000.aue.devtunnels.ms
    ```

## I-start ang Agent App

1. Kopyahin ang text sa ibaba sa clipboard:

    ```text
    Debug: Select and Start Debugging
    ```

2. Pindutin ang <kbd>F1</kbd> upang buksan ang VS Code Command Palette.
3. I-paste ang text sa Command Palette at piliin ang **Debug: Select and Start Debugging**.
4. Piliin ang **🌎🤖Debug Compound: Agent and MCP (http)** mula sa listahan. Ia-start nito ang agent app at ang web chat client.

## Mag-umpisa ng usapan sa Agent

Lumipat sa **Web Chat** tab sa iyong browser. Dapat mong makita ang agent app na tumatakbo at handang tumanggap ng mga tanong.

### Pagde-debug gamit ang DevTunnel

Maaari mong gamitin ang DevTunnel upang i-debug ang MCP server at ang agent app. Pinapayagan kang i-inspect ang network activity at i-troubleshoot ang mga isyu sa real-time.

1. Piliin ang **Inspect network activity** URL mula sa DevTunnel output.
2. Bubukas ito ng bagong tab sa iyong browser kung saan makikita mo ang network activity ng MCP server at ng agent app.
3. Maaari mo itong gamitin upang i-debug ang anumang isyu na lilitaw sa panahon ng workshop.

Maaari ka ring mag-set ng breakpoints sa MCP server code at agent app code upang i-debug ang partikular na mga isyu. Upang gawin ito:

1. Buksan ang `sales_analysis.py` file sa `mcp_server` folder.
2. Mag-set ng breakpoint sa pamamagitan ng pag-click sa gutter sa tabi ng line number kung saan mo gustong i-pause ang execution.
3. Kapag naabot ng execution ang breakpoint, maaari mong i-inspect ang mga variable, mag-step sa code, at mag-evaluate ng mga expression sa Debug Console.

*Isinalin gamit ang GitHub Copilot.*
