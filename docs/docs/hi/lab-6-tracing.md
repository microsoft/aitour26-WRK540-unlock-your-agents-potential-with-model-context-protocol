**TBC: यह लेबल उपयोगकर्ता को एजेंट निर्देश फाइल को अपडेट करने के लिए कहेगा ताकि एजेंट अपने प्रतिक्रियाओं में उपयोग करने वाले परेशान करने वाले emojis को हटा दे।**

## परिचय

ट्रेसिंग आपको निष्पादन के दौरान चरणों, इनपुट, और आउटपुट के अनुक्रम को दिखाकर आपके एजेंट के व्यवहार को समझने और डिबग करने में मदद करती है। Azure AI Foundry में, ट्रेसिंग आपको यह देखने देती है कि आपका एजेंट अनुरोधों को कैसे प्रोसेस करता है, टूल्स को कॉल करता है, और प्रतिक्रियाएं जेनरेट करता है। आप Azure AI Foundry portal का उपयोग कर सकते हैं या ट्रेस डेटा एकत्र करने और विश्लेषण करने के लिए OpenTelemetry और Application Insights के साथ एकीकृत कर सकते हैं, जिससे आपके एजेंट को ट्रबलशूट और अनुकूलित करना आसान हो जाता है।

<!-- ## लैब अभ्यास

=== "Python"

      1. `app.py` फाइल खोलें।
      2. ट्रेसिंग सक्षम करने के लिए `AZURE_TELEMETRY_ENABLED` वेरिएबल को `True` में बदलें:

         ```python
         AZURE_TELEMETRY_ENABLED = True
         ```

        !!! info "नोट"
            यह सेटिंग आपके एजेंट के लिए telemetry सक्षम करती है। `app.py` में `initialize` फ़ंक्शन में, telemetry client को Azure Monitor में डेटा भेजने के लिए कॉन्फ़िगर किया गया है।

            ```python
             if AZURE_TELEMETRY_ENABLED:
                 configure_azure_monitor(connection_string=await self.project_client.telemetry.get_connection_string())
            ```         

=== "C#"

      tbd -->

## Agent App चलाना

1. ऐप चलाने के लिए <kbd>F5</kbd> दबाएं।
2. नए एडिटर टैब में एजेंट ऐप खोलने के लिए **Preview in Editor** का चयन करें।

### Agent के साथ बातचीत शुरू करना

बातचीत शुरू करने के लिए एजेंट ऐप में निम्नलिखित prompt को कॉपी और पेस्ट करें:

```plaintext
Write an executive report that analysis the top 5 product categories and compares performance of the online store verses the average for the physical stores.
```

## ट्रेसेस देखना

आप Azure AI Foundry portal में या OpenTelemetry का उपयोग करके अपने एजेंट के निष्पादन के ट्रेसेस देख सकते हैं। ट्रेसेस एजेंट के निष्पादन के दौरान चरणों का अनुक्रम, टूल कॉल्स, और डेटा एक्सचेंज दिखाएंगे। यह जानकारी आपके एजेंट के प्रदर्शन को डिबग करने और अनुकूलित करने के लिए महत्वपूर्ण है।

### Azure AI Foundry Portal का उपयोग

Azure AI Foundry portal में ट्रेसेस देखने के लिए, इन चरणों का पालन करें:

1. **[Azure AI Foundry](https://ai.azure.com/) portal पर नेविगेट करें।
2. अपने प्रोजेक्ट का चयन करें।
3. बाएं हाथ के मेनू में **Tracing** टैब का चयन करें।
4. यहां, आप अपने एजेंट द्वारा जेनरेट किए गए ट्रेसेस देख सकते हैं।

   ![](media/ai-foundry-tracing.png)

### ट्रेसेस में गहराई से जाना

1. आपको नवीनतम ट्रेसेस देखने के लिए **Refresh** बटन पर क्लिक करना पड़ सकता है क्योंकि ट्रेसेस दिखाई देने में कुछ समय लग सकता है।
2. विवरण देखने के लिए `Zava Agent Initialization` नामक ट्रेस का चयन करें।
   ![](media/ai-foundry-trace-agent-init.png)
3. एजेंट निर्माण प्रक्रिया का विवरण देखने के लिए `creare_agent Zava DIY Sales Agent` ट्रेस का चयन करें। `Input & outputs` अनुभाग में, आप Agent instructions देखेंगे।
4. इसके बाद, चैट अनुरोध का विवरण देखने के लिए `Zava Agent Chat Request: Write an executive...` ट्रेस का चयन करें। `Input & outputs` अनुभाग में, आप उपयोगकर्ता इनपुट और एजेंट की प्रतिक्रिया देखेंगे।

<!-- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/continuous-evaluation-agents -->

*GitHub Copilot और GPT-4o का उपयोग करके अनुवादित।*
