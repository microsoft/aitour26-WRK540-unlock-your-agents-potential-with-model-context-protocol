**TBC: यह लेबल user को agent instructions फाइल को अपडेट करने के लिए कहेगा ताकि agent अपनी प्रतिक्रियाओं में उपयोग करने वाले annoying emojis को हटा दे।**

## परिचय

Tracing आपके agent के व्यवहार को समझने और debug करने में मदद करती है execution के दौरान steps, inputs, और outputs के sequence को दिखाकर। Azure AI Foundry में, tracing आपको observe करने देती है कि आपका agent कैसे requests को process करता है, tools को call करता है, और responses जेनरेट करता है। आप trace data को collect और analyze करने के लिए Azure AI Foundry portal का उपयोग कर सकते हैं या OpenTelemetry और Application Insights के साथ integrate कर सकते हैं, जिससे आपके agent को troubleshoot और optimize करना आसान हो जाता है।

<!-- ## लैब एक्सरसाइज़

=== "Python"

      1. `app.py` फाइल खोलें।
      2. tracing को सक्षम करने के लिए `AZURE_TELEMETRY_ENABLED` variable को `True` में बदलें:

         ```python
         AZURE_TELEMETRY_ENABLED = True
         ```

        !!! info "नोट"
            यह setting आपके agent के लिए telemetry को सक्षम करती है। `app.py` में `initialize` function में, telemetry client को Azure Monitor को data भेजने के लिए configured किया गया है।

            ```python
             if AZURE_TELEMETRY_ENABLED:
                 configure_azure_monitor(connection_string=await self.project_client.telemetry.get_connection_string())
            ```         

=== "C#"

      tbd -->

## Agent App चलाना

1. app चलाने के लिए <kbd>F5</kbd> दबाएं।
2. agent app को नए editor tab में खोलने के लिए **Preview in Editor** सेलेक्ट करें।

### Agent के साथ बातचीत शुरू करना

बातचीत शुरू करने के लिए निम्नलिखित prompt को agent app में copy और paste करें:

```plaintext
एक executive report लिखें जो top 5 product categories का विश्लेषण करती है और online store के प्रदर्शन की तुलना physical stores के average से करती है।
```

## Traces देखना

आप अपने agent के execution के traces को Azure AI Foundry portal में या OpenTelemetry का उपयोग करके देख सकते हैं। Traces agent के execution के दौरान steps, tool calls, और data exchange के sequence को दिखाएंगे। यह जानकारी आपके agent के प्रदर्शन को debug और optimize करने के लिए महत्वपूर्ण है।

### Azure AI Foundry Portal का उपयोग करना

Azure AI Foundry portal में traces देखने के लिए, इन steps का पालन करें:

1. **[Azure AI Foundry](https://ai.azure.com/)** portal पर navigate करें।
2. अपना project सेलेक्ट करें।
3. बाएं हाथ के menu में **Tracing** tab सेलेक्ट करें।
4. यहां, आप अपने agent द्वारा जेनरेट किए गए traces देख सकते हैं।

   ![](media/ai-foundry-tracing.png)

### Traces में Drilling Down करना

1. latest traces देखने के लिए आपको **Refresh** button पर click करना पड़ सकता है क्योंकि traces को appear होने में कुछ moments लग सकते हैं।
2. details देखने के लिए `Zava Agent Initialization` नाम वाला trace सेलेक्ट करें।
   ![](media/ai-foundry-trace-agent-init.png)
3. agent creation process के details देखने के लिए `creare_agent Zava DIY Sales Agent` trace सेलेक्ट करें। `Input & outputs` section में, आपको Agent instructions दिखेंगे।
4. इसके बाद, chat request के details देखने के लिए `Zava Agent Chat Request: Write an executive...` trace सेलेक्ट करें। `Input & outputs` section में, आपको user input और agent की response दिखेगी।

<!-- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/continuous-evaluation-agents -->

*GitHub Copilot का उपयोग करके अनुवादित।*
