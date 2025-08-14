## Ano ang Iyong Matututuhan

Sa lab na ito, rerepasuhin at ia-update mo ang agent instructions upang isama ang isang tuntunin tungkol sa financial year na nagsisimula sa Hulyo 1. Mahalaga ito para tama ang interpretasyon at pagsusuri ng agent sa sales data.

## Panimula

Ang layunin ng agent instructions ay tukuyin ang pag-uugali ng agent, kabilang kung paano ito nakikipag-interact sa mga user, anong mga tool ang maaari nitong gamitin, at kung paano ito tutugon sa iba’t ibang uri ng query. Sa lab na ito, rerepasuhin mo ang umiiral na agent instructions at gagawa ng maliit na update upang matiyak na tama nitong mai-interpret ang financial year.

## Lab Exercise

### Buksan ang Agent Instructions

1. Mula sa VS Code Explorer, mag-navigate sa `shared/instructions` folder.
2. **Buksan** ang `mcp_server_tools_with_code_interpreter.txt` file.

### Repasuhin ang Agent Instructions

Repasuhin kung paano tinutukoy ng instructions ang pag-uugali ng agent app:

!!! tip "Sa VS Code, pindutin ang Alt + Z (Windows/Linux) o Option + Z (Mac) upang paganahin ang word wrap mode para mas madaling basahin ang instructions."

- **Core Role:** Sales agent para sa Zava (WA DIY retailer) na may propesyonal, magiliw na tono gamit ang emoji at walang anumang haka-haka o unverified na nilalaman.
- **Database Rules:** Laging kunin muna ang schemas (get_multiple_table_schemas()) na may mandatory LIMIT 20 sa lahat ng SELECT queries gamit ang eksaktong table/column names.
- **Visualizations:** Gumawa lamang ng charts kapag hayagang hiniling gamit ang mga trigger tulad ng "chart", "graph", "visualize", o "show as [type]" sa PNG format na dina-download mula sa sandbox at walang markdown image paths.
- **Responses:** Default sa Markdown tables na may multi-language support at CSV na available kung hihilingin.
- **Safety:** Manatili sa saklaw ng Zava sales data lamang na may eksaktong tugon para sa out-of-scope/unclear queries at i-redirect ang hostile users sa IT.
- **Key Constraints:** Walang imbentong data, gamit lang ang tools na may 20-row limit at laging PNG ang images.

### I-update ang Agent Instructions

Kopyahin ang text sa ibaba at i-paste kaagad pagkatapos ng tuntunin tungkol sa hindi pagbuo ng unverified content o paggawa ng assumptions:

!!! tip "I-click ang copy icon sa kanan upang kopyahin ang text sa clipboard."

```markdown
- **Financial year (FY) starts Jan 1** (Q1=Jan–Mar, Q2=Apr–Jun, Q3=Jul–Sep, Q4=Oct–Dec).
```

Ang na-update na instructions ay dapat ganito ang itsura:

```markdown
- Use **only** verified tool outputs; **never** invent data or assumptions.
- **Financial year (FY) starts Jan 1** (Q1=Jan–Mar, Q2=Apr–Jun, Q3=Jul–Sep, Q4=Oct–Dec).
```

*Isinalin gamit ang GitHub Copilot.*
