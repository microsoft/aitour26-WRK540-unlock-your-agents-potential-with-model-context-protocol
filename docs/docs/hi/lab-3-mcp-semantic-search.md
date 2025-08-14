## आप क्या सीखेंगे

इस लैब में आप Azure AI एजेंट में Model Context Protocol (MCP) और PostgreSQL (pgvector सक्षम) का उपयोग करते हुए सेमान्टिक सर्च सक्षम करेंगे।

## परिचय

उत्पाद नाम और विवरण OpenAI embedding मॉडल (text-embedding-3-small) से वेक्टर में बदले गए और डेटाबेस में संग्रहित हैं। यह एजेंट को उपयोगकर्ता इरादे को बेहतर समझने में मदद करता है।

## लैब अभ्यास

पहले एजेंट केवल सटीक मिलान पर उत्तर देता था। अब आप सेमान्टिक सर्च जोड़कर अधिक लचीले प्रश्न सक्षम करेंगे।

1. वेब चैट में प्रश्न पेस्ट करें:

    ```text
    What 18 amp circuit breakers do we sell?
    ```

    संभावित उत्तर: "मैं कोई विशेष 18 amp सर्किट ब्रेकर नहीं खोज पाया..." आदि।

## एजेंट ऐप रोकें

VS Code से <kbd>Shift</kbd> + <kbd>F5</kbd>।

## सेमान्टिक सर्च लागू करें

1. <kbd>F1</kbd> → **File: Open File...**
2. पथ पेस्ट:

    ```text
    /workspace/src/python/mcp_server/sales_analysis/sales_analysis.py
    ```
3. ~लाइन 100 पर `semantic_search_products` विधि देखें।
4. `@mcp.tool()` डेकोरेटर अनकमेंट करें:

    ```python
    # @mcp.tool()
    async def semantic_search_products(...
    ```
5. `app.py` पर जाएँ।
6. लाइन ~30: `# INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"` अनकमेंट करें।

    ```python
    INSTRUCTIONS_FILE = "instructions/mcp_server_tools_with_semantic_search.txt"
    ```

## निर्देश समीक्षा

`/workspace/src/shared/instructions/mcp_server_tools_with_semantic_search.txt` खोलें।

## एजेंट ऐप पुनः शुरू करें

1. <kbd>F5</kbd>।
2. वेब चैट में पुनः प्रश्न:

    ```text
    What 18 amp circuit breakers do we sell?
    ```

    अब एजेंट सेमान्टिक अर्थ समझेगा।

!!! info "नोट"
    चरण:
    1. प्रश्न को उसी embedding मॉडल से वेक्टर में बदला जाता है।
    2. वेक्टर समानता खोज pgvector के माध्यम से।
    3. परिणामों पर उत्तर निर्मित।

## एग्जीक्यूटिव रिपोर्ट लिखें

```plaintext
Write an executive report on the sales performance of different stores for these circuit breakers.
```

## एजेंट ऐप चालू रखें

अगली लैब के लिए।

*GitHub Copilot द्वारा अनुवादित.*
