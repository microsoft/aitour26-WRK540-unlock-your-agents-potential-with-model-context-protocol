## Self-Guided Learners

ये निर्देश self-guided learners के लिए हैं जिनके पास पूर्व-कॉन्फ़िगर किए गए लैब वातावरण तक पहुंच नहीं है। अपना वातावरण सेट करने और कार्यशाला शुरू करने के लिए इन चरणों का पालन करें।

## परिचय

यह कार्यशाला आपको Azure AI Agents Service और संबंधित SDK के बारे में सिखाने के लिए डिज़ाइन की गई है। इसमें कई लैब्स हैं, जो Azure AI Agents Service की एक विशिष्ट सुविधा को उजागर करती है। लैब्स को क्रम में पूरा करने के लिए बनाया गया है, क्योंकि प्रत्येक पिछली लैब के ज्ञान और कार्य पर आधारित है।

## आवश्यकताएं

1. Azure subscription तक पहुंच। यदि आपके पास Azure subscription नहीं है, तो शुरू करने से पहले एक [free account](https://azure.microsoft.com/free/){:target="_blank"} बनाएं।
1. आपको GitHub account की आवश्यकता है। यदि आपके पास एक नहीं है, तो [GitHub](https://github.com/join){:target="_blank"} पर इसे बनाएं।

## कार्यशाला प्रोग्रामिंग भाषा का चयन

कार्यशाला Python और C# दोनों में उपलब्ध है। अपनी पसंदीदा भाषा चुनने के लिए भाषा चयनकर्ता टैब का उपयोग करें। नोट करें, कार्यशाला के बीच भाषा न बदलें।

**अपनी पसंदीदा भाषा के लिए टैब का चयन करें:**

=== "Python"
    कार्यशाला के लिए डिफ़ॉल्ट भाषा **Python** सेट है।
=== "C#"
    कार्यशाला के लिए डिफ़ॉल्ट भाषा **C#** सेट है।

## कार्यशाला खोलना

इस कार्यशाला को चलाने का **पसंदीदा** तरीका **GitHub Codespaces** का उपयोग करना है। यह विकल्प कार्यशाला पूरा करने के लिए आवश्यक सभी टूल्स और संसाधनों के साथ एक पूर्व-कॉन्फ़िगर किया गया वातावरण प्रदान करता है। वैकल्पिक रूप से, आप Visual Studio Code Dev Container और Docker का उपयोग करके कार्यशाला को स्थानीय रूप से खोल सकते हैं। दोनों विकल्प नीचे वर्णित हैं।

!!! Note
    **Codespace या Dev Container बनाने में लगभग 5 मिनट लगेंगे। प्रक्रिया शुरू करें और फिर आप इसे बनाते समय निर्देशों को पढ़ना जारी रख सकते हैं।**

=== "GitHub Codespaces"

    GitHub Codespaces में प्रोजेक्ट खोलने के लिए **Open in GitHub Codespaces** का चयन करें।

    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol){:target="_blank"}

=== "VS Code Dev Container"

    <!-- !!! warning "Apple Silicon Users"
        आप जल्द ही चलाने वाली automated deployment script Apple Silicon पर समर्थित नहीं है। कृपया Dev Container के बजाय Codespaces से या macOS से deployment script चलाएं। -->

    वैकल्पिक रूप से, आप Visual Studio Code Dev Container का उपयोग करके प्रोजेक्ट को स्थानीय रूप से खोल सकते हैं, जो [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers){:target="_blank"} का उपयोग करके आपके स्थानीय VS Code development environment में प्रोजेक्ट खोलेगा।

    1. Docker Desktop शुरू करें (यदि पहले से इंस्टॉल नहीं है तो इसे इंस्टॉल करें)
    2. VS Code Dev Container में प्रोजेक्ट खोलने के लिए **Dev Containers Open** का चयन करें।

        [![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol)

*GitHub Copilot और GPT-4o का उपयोग करके अनुवादित।*
