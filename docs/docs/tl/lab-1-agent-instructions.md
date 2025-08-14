## Ano ang Matutuhan Ninyo

Sa lab na ito, susuriin at i-update ninyo ang agent instructions upang isama ang rule tungkol sa financial year na nagsisimula sa July 1. Mahalaga ito para sa agent na tama ang interpretation at analysis ng sales data.

## Introduction

Ang layunin ng agent instructions ay tukuyin ang behavior ng agent, kasama kung paano ito nakikipag-ugnayan sa mga users, anong mga tools ang maaari nitong gamitin, at kung paano ito dapat tumugon sa iba't ibang types ng queries. Sa lab na ito, susuriin ninyo ang existing agent instructions at gagawa ng maliit na update upang matiyak na tama ang interpretation ng agent sa financial year.

## Lab Exercise

### Buksan ang Agent Instructions

1. Mula sa VS Code Explorer, pumunta sa `shared/instructions` folder.
2. **Buksan** ang `mcp_server_tools_with_code_interpreter.txt` file.

### Suriin ang Agent Instructions

Suriin kung paano tinutukoy ng mga instructions ang behavior ng agent app:

!!! tip "Sa VS Code, pindutin ang Alt + Z (Windows/Linux) o Option + Z (Mac) upang i-enable ang word wrap mode, na ginagawang mas madaling basahin ang mga instructions."

- **Core Role:** Sales agent para sa Zava (WA DIY retailer) na may professional, friendly tone gamit ang emojis at walang assumptions o unverified content.
- **Database Rules:** Laging kunin muna ang schemas (get_multiple_table_schemas()) na may mandatory LIMIT 20 sa lahat ng SELECT queries gamit ang exact table/column names.
- **Visualizations:** Gumawa ng charts LAMANG kapag explicitly na hiningi gamit ang triggers tulad ng "chart", "graph", "visualize", o "show as [type]" sa PNG format na na-download mula sa sandbox na walang markdown image paths.
- **Responses:** Default sa Markdown tables na may multi-language support at CSV available sa request.
- **Safety:** Manatili sa scope ng Zava sales data lamang na may exact responses para sa out-of-scope/unclear queries at i-redirect ang hostile users sa IT.
- **Key Constraints:** Walang made-up data gamit ang tools lamang na may 20-row limit at PNG images lagi.

### I-update ang Agent Instructions

I-copy ang text sa ibaba at i-paste direkta pagkatapos ng rule tungkol sa hindi pag-generate ng unverified content o pag-gawa ng assumptions:

!!! tip "I-click ang copy icon sa kanan upang i-copy ang text sa clipboard."

```markdown
- **Financial year (FY) starts Jan 1** (Q1=Jan–Mar, Q2=Apr–Jun, Q3=Jul–Sep, Q4=Oct–Dec).
```

Ang updated instructions ay dapat maging ganito:

```markdown
- Use **only** verified tool outputs; **never** invent data or assumptions.
- **Financial year (FY) starts Jan 1** (Q1=Jan–Mar, Q2=Apr–Jun, Q3=Jul–Sep, Q4=Oct–Dec).
```

*Isinalin gamit ang GitHub Copilot.*
