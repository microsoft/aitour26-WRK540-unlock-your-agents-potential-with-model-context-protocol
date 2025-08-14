## आप क्या सीखेंगे

इस लैब में आप एजेंट निर्देश की समीक्षा करेंगे और वित्तीय वर्ष 1 जनवरी से शुरू होने का नियम जोड़ेंगे ताकि एजेंट बिक्री डेटा को सही अर्थ दे सके।

## परिचय

एजेंट निर्देश एजेंट का व्यवहार परिभाषित करते हैं: उपयोगकर्ताओं से कैसे संवाद, कौन से टूल उपयोग, किस प्रकार प्रतिक्रिया। आप मौजूदा निर्देश की समीक्षा कर एक छोटा अपडेट करेंगे।

## लैब अभ्यास

### एजेंट निर्देश खोलें

1. VS Code Explorer से `shared/instructions` पर जाएँ।
2. `mcp_server_tools_with_code_interpreter.txt` खोलें।

### समीक्षा करें

!!! tip "VS Code में Mac पर Option + Z दबाएँ वर्ड रैप के लिए।"

- **Core Role:** Zava का सेल्स एजेंट (WA DIY रिटेलर) प्रोफेशनल, मित्रवत टोन, इमोजी सहित, कोई अनुमान नहीं।
- **Database Rules:** हमेशा स्कीमा पहले (get_multiple_table_schemas()) और सभी SELECT पर अनिवार्य LIMIT 20।
- **Visualizations:** केवल स्पष्ट अनुरोध पर चार्ट ("chart", "graph", "visualize", "show as") PNG आउटपुट, कोई मार्कडाउन इमेज पाथ नहीं।
- **Responses:** डिफ़ॉल्ट Markdown तालिकाएँ, मल्टीलैंग्वेज सपोर्ट, CSV अनुरोध पर।
- **Safety:** केवल Zava बिक्री दायरे में रहें, असंगत/हमलावर क्वेरी पर सही उत्तर।
- **Key Constraints:** कोई मनगढ़ंत डेटा नहीं, केवल टूल, 20‑row सीमा, PNG इमेज।

### एजेंट निर्देश अपडेट करें

नीचे का पाठ कॉपी करें और "मनगढ़ंत डेटा नहीं" नियम के बाद पेस्ट करें:

```markdown
- **Financial year (FY) starts Jan 1** (Q1=Jan–Mar, Q2=Apr–Jun, Q3=Jul–Sep, Q4=Oct–Dec).
```

अपडेटेड भाग इस प्रकार दिखना चाहिए:

```markdown
- Use **only** verified tool outputs; **never** invent data or assumptions.
- **Financial year (FY) starts Jan 1** (Q1=Jan–Mar, Q2=Apr–Jun, Q3=Jul–Sep, Q4=Oct–Dec).
```

*GitHub Copilot द्वारा अनुवादित.*
