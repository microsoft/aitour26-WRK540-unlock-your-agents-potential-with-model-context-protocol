इस workshop के lab portion के लिए बस इतना ही। Key takeaways और additional resources के लिए आगे पढ़ें, लेकिन पहले आइए साफ-सफाई करते हैं।

## GitHub CodeSpaces को Clean up करना

### GitHub में अपने changes save करना

आप workshop के दौरान files में किए गए किसी भी changes को अपनी personal GitHub repository में fork के रूप में save कर सकते हैं। यह आपकी customizations के साथ workshop को re-run करना आसान बनाता है, और workshop content हमेशा आपके GitHub account में उपलब्ध रहेगी।

* VS Code में, left pane में "Source Control" tool पर click करें। यह तीसरा है, या आप keyboard shortcut <kbd>Control-Shift-G</kbd> का उपयोग कर सकते हैं।
* "Source Control" के under field में `Agents Lab` enter करें और **✔️Commit** पर click करें।
  * "There are no staged changes to commit." prompt के लिए **Yes** पर click करें।
* **Sync Changes** पर click करें।
  * "This action will pull and push commits from and to origin/main" prompt के लिए **OK** पर click करें।

अब आपके GitHub account में आपकी customizations के साथ workshop की अपनी copy है।

### अपना GitHub codespace delete करना

आपका GitHub CodeSpace अपने आप shut down हो जाएगा, लेकिन यह तब तक आपके compute और storage allotment की थोड़ी मात्रा consume करेगा जब तक यह delete नहीं हो जाता। (आप अपना usage अपनी [GitHub Billing summary](https://github.com/settings/billing/summary) में देख सकते हैं।) आप अब codespace को safely delete कर सकते हैं, निम्नलिखित तरीके से:

* [github.com/codespaces](https://github.com/codespaces){:target="_blank"} पर जाएं
* Page के bottom में, अपने active codespace के दाईं ओर "..." menu पर click करें
* **Delete** पर click करें
  * "Are you sure?" prompt पर, **Delete** पर click करें।

## अपने Azure resources delete करना

इस lab में आपने जो अधिकांश resources create किए हैं वे pay-as-you-go resources हैं, मतलब उनका उपयोग करने के लिए आपसे अब और कुछ charge नहीं किया जाएगा। हालांकि, AI Foundry द्वारा उपयोग की जाने वाली कुछ storage services में छोटे ongoing charges हो सकते हैं। सभी resources delete करने के लिए, इन steps को follow करें:

* [Azure Portal](https://portal.azure.com){:target="_blank"} पर जाएं
* **Resource groups** पर click करें
* अपने resource group `rg-agent-workshop-****` पर click करें
* **Delete Resource group** पर click करें
* Bottom में "Enter resource group name to confirm deletion" field में `rg-agent-workshop-****` enter करें
* **Delete** पर click करें
  * Delete Confirmation prompt पर, "Delete" पर click करें

*GitHub Copilot का उपयोग करके अनुवादित।*
