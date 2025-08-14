**TBC: यह लेबल उपयोगकर्ता को निर्देश फ़ाइल अपडेट करवाएगा ताकि एजेंट इमोजी कम करे।**

## परिचय

Tracing एजेंट के व्यवहार को समझने और डिबग में मदद करता है। यह चरण, इनपुट, आउटपुट दिखाता है। Azure AI Foundry में आप पोर्टल या OpenTelemetry + Application Insights से ट्रेसेज़ देख सकते हैं।

## एजेंट ऐप चलाएँ

1. <kbd>F5</kbd> दबाएँ।
2. **Preview in Editor** चुनें।

### बातचीत शुरू करें

प्रॉम्प्ट:

```plaintext
Write an executive report that analysis the top 5 product categories and compares performance of the online store verses the average for the physical stores.
```

## ट्रेस देखें

पोर्टल में **Tracing** टैब पर जाएँ।

### Drill Down

1. **Refresh** यदि आवश्यक।
2. `Zava Agent Initialization` ट्रेस देखें।
3. `create_agent Zava DIY Sales Agent` ट्रेस में निर्देश।
4. `Zava Agent Chat Request: Write an executive...` में चैट विवरण।

*GitHub Copilot द्वारा अनुवादित.*
