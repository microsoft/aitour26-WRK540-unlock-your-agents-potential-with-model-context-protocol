## Ano ang Matutuhan Ninyo

Sa lab na ito, matutuhan ninyo ang:

- Gamitin ang DevTunnel upang maging accessible ang inyong local MCP server sa cloud-based agent services
- I-set up ang inyong environment para sa hands-on experimentation sa Model Context Protocol

## Introduction

Ang Model Context Protocol (MCP) server ay isang mahalagang component na tumutulong sa komunikasyon sa pagitan ng Large Language Models (LLMs) at external tools at data sources. Papatakbuhin ninyo ang MCP server sa inyong local machine, pero kailangan ng Azure AI Foundry Agent Service ng internet access upang makonekta dito. Upang gawing accessible ang inyong local MCP server mula sa internet, gagamitin ninyo ang DevTunnel. Nagbibigay-daan ito sa Agent Service na makipag-usap sa inyong MCP server na parang tumatakbo bilang service sa Azure.

## Interface options para sa MCP

Sumusuporta ang MCP ng dalawang pangunahing interfaces para sa pagkonekta ng mga LLM sa tools:

- **Streamable HTTP Transport**: Para sa web-based APIs at services.
- **Stdio Transport**: Para sa local scripts at command-line tools.

Ginagamit ng lab na ito ang Streamable HTTP transport interface upang maging integrated sa Azure AI Foundry Agent Service.

!!! note
    Normal na iding-deploy ninyo ang MCP server sa production environment, pero para sa workshop na ito, papatakbuhin ninyo ito locally sa inyong development environment. Nagbibigay-daan ito sa inyo na subukan at makipag-ugnayan sa MCP tools nang hindi na kailangan ng full deployment.

### Simulan ang DevTunnel para sa MCP Server

1. Sa bagong terminal, i-authenticate ang DevTunnel. Magiging prompted kayo na mag-log in gamit ang inyong Azure account, gamitin ang parehong account na ginamit ninyo sa pag-log in sa Azure AI Foundry Agent Service o Azure Portal. Patakbuhin ang sumusunod na command:

    ```bash
    devtunnel login
    ```

1. Susunod, sa terminal kung saan tumatakbo ang MCP server, simulan ang DevTunnel sa pamamagitan ng pagpapatakbo ng:

    ```bash
    devtunnel host -p 8000 --allow-anonymous
    ```

    Maglalabas ito ng URL na kakailanganin ninyo para sa agent na makonekta sa MCP server. Ang output ay magiging katulad ng:

    ```text
    Hosting port: 8000
    Connect via browser: https://<tunnel-id>-8000.aue.devtunnels.ms
    Inspect network activity: https://<tunnel-id>-8000-inspect.aue.devtunnels.ms
    ```

## I-update ang DevTunnel Environment Variable

1. I-copy ang **Connect via browser** URL sa clipboard - kakailanganin ninyo ito sa susunod na lab upang i-configure ang agent.
2. Buksan ang `.env` file sa workshop folder.
3. I-update ang `DEV_TUNNEL_URL` variable gamit ang copied URL.

    ```text
    DEV_TUNNEL_URL=https://<tunnel-id>-8000.aue.devtunnels.ms
    ```

## Simulan ang Agent App

1. I-copy ang text sa ibaba sa clipboard:

    ```text
    Debug: Select and Start Debugging
    ```

2. Pindutin ang <kbd>F1</kbd> upang buksan ang VS Code Command Palette.
3. I-paste ang text sa Command Palette at piliin ang **Debug: Select and Start Debugging**.
4. Piliin ang **🌎🤖Debug Compound: Agent and MCP (http)** mula sa listahan. Magsisimula ito ng agent app at ng web chat client.

## Simulan ang conversation sa Agent

Lumipat sa **Web Chat** tab sa inyong browser. Dapat makita ninyo ang agent app na tumatakbo at handa na tanggapin ang mga tanong.

### Debugging gamit ang DevTunnel

Maaari ninyong gamitin ang DevTunnel upang i-debug ang MCP server at ang agent app. Nagbibigay-daan ito sa inyo na suriin ang network activity at mag-troubleshoot ng mga issues nang real-time.

1. Piliin ang **Inspect network activity** URL mula sa DevTunnel output.
2. Magbubukas ito ng bagong tab sa inyong browser kung saan makikita ninyo ang network activity ng MCP server at ng agent app.
3. Maaari ninyo itong gamitin upang i-debug ang anumang mga issueng lumitaw sa workshop.

Maaari rin ninyong mag-set ng mga breakpoints sa MCP server code at sa agent app code upang i-debug ang mga specific issues. Upang gawin ito:

1. Buksan ang `sales_analysis.py` file sa `mcp_server` folder.
2. Mag-set ng breakpoint sa pamamagitan ng pag-click sa gutter sa tabi ng line number kung saan ninyo gustong i-pause ang execution.
3. Kapag naabot ng execution ang breakpoint, maaari ninyong suriin ang mga variables, mag-step through ng code, at mag-evaluate ng mga expressions sa Debug Console.

*Isinalin gamit ang GitHub Copilot.*
