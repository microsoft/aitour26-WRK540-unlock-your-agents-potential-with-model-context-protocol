## स्व-निर्देशित शिक्षार्थी

ये निर्देश उन स्व-निर्देशित शिक्षार्थियों के लिए हैं जिनके पास pre-configured lab environment तक पहुंच नहीं है। अपना environment set up करने और workshop शुरू करने के लिए इन steps को follow करें।

## परिचय

यह workshop आपको Azure AI Agents Service और संबंधित SDK के बारे में सिखाने के लिए डिज़ाइन किया गया है। इसमें multiple labs हैं, प्रत्येक Azure AI Agents Service की specific feature को highlight करती है। Labs को order में पूरा करना है, क्योंकि प्रत्येक previous lab के knowledge और work पर build करती है।

## Prerequisites

1. Azure subscription तक पहुंच। यदि आपके पास Azure subscription नहीं है, तो शुरू करने से पहले [free account](https://azure.microsoft.com/free/){:target="_blank"} बनाएं।
1. आपको GitHub account की आवश्यकता है। यदि आपके पास नहीं है, तो [GitHub](https://github.com/join){:target="_blank"} पर बनाएं।

## Workshop Programming Language सेलेक्ट करना

Workshop Python और C# दोनों में उपलब्ध है। अपनी preferred language चुनने के लिए language selector tabs का उपयोग करें। नोट करें, workshop के बीच में languages switch न करें।

**अपनी preferred language के लिए tab सेलेक्ट करें:**

=== "Python"
    Workshop के लिए default language **Python** पर set है।
=== "C#"
    Workshop के लिए default language **C#** पर set है।

## Workshop खोलना

इस workshop को चलाने का **preferred** तरीका **GitHub Codespaces** का उपयोग करना है। यह option एक pre-configured environment प्रदान करता है जिसमें workshop पूरा करने के लिए आवश्यक सभी tools और resources हैं। वैकल्पिक रूप से, आप Visual Studio Code Dev Container और Docker का उपयोग करके workshop को locally खोल सकते हैं। दोनों options नीचे describe किए गए हैं।

!!! Note
    **Codespace या Dev Container को build करने में लगभग 5 minutes लगेंगे। Process शुरू करें और फिर आप build होते समय instructions पढ़ना जारी रख सकते हैं।**

=== "GitHub Codespaces"

    Project को GitHub Codespaces में खोलने के लिए **Open in GitHub Codespaces** सेलेक्ट करें।

    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol){:target="_blank"}

=== "VS Code Dev Container"

    <!-- !!! warning "Apple Silicon Users"
        जो automated deployment script आप जल्द ही चलाएंगे वो Apple Silicon पर supported नहीं है। कृपया Dev Container के बजाय Codespaces से या macOS से deployment script चलाएं। -->

    वैकल्पिक रूप से, आप Visual Studio Code Dev Container का उपयोग करके project को locally खोल सकते हैं, जो [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers){:target="_blank"} का उपयोग करके आपके local VS Code development environment में project खोलेगा।

    1. Docker Desktop शुरू करें (यदि पहले से installed नहीं है तो install करें)
    2. Project को VS Code Dev Container में खोलने के लिए **Dev Containers Open** सेलेक्ट करें।

        [![Open in Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol)

*GitHub Copilot का उपयोग करके अनुवादित।*
