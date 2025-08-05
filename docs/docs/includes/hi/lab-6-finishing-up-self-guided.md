इस कार्यशाला के लैब भाग के लिए बस इतना ही। मुख्य takeaways और अतिरिक्त संसाधनों के लिए आगे पढ़ें, लेकिन पहले आइए साफ-सफाई करते हैं।

## GitHub CodeSpaces की सफाई

### GitHub में अपने परिवर्तन सेव करें

आप कार्यशाला के दौरान फाइलों में किए गए किसी भी परिवर्तन को fork के रूप में अपनी व्यक्तिगत GitHub repository में सेव कर सकते हैं। यह आपके customizations के साथ कार्यशाला को फिर से चलाना आसान बनाता है, और कार्यशाला सामग्री हमेशा आपके GitHub account में उपलब्ध रहेगी।

* VS Code में, बाएं pane में "Source Control" tool पर क्लिक करें। यह तीसरा है, या आप keyboard shortcut <kbd>Control-Shift-G</kbd> का उपयोग कर सकते हैं।
* "Source Control" के नीचे field में `Agents Lab` दर्ज करें और **✔️Commit** पर क्लिक करें।
  * Prompt "There are no staged changes to commit." के लिए **Yes** पर क्लिक करें।
* **Sync Changes** पर क्लिक करें।
  * Prompt "This action will pull and push commits from and to origin/main" के लिए **OK** पर क्लिक करें।

अब आपके पास अपने GitHub account में अपने customizations के साथ कार्यशाला की अपनी copy है।

### अपना GitHub codespace delete करें

आपका GitHub CodeSpace अपने आप बंद हो जाएगा, लेकिन यह delete होने तक आपके compute और storage allotment की एक छोटी मात्रा का उपभोग करेगा। (आप अपने [GitHub Billing summary](https://github.com/settings/billing/summary) में अपना usage देख सकते हैं।) आप अब codespace को safely delete कर सकते हैं, निम्नलिखित तरीके से:

* [github.com/codespaces](https://github.com/codespaces){:target="_blank"} पर जाएं
* Page के नीचे, अपने active codespace के दाईं ओर "..." menu पर क्लिक करें
* **Delete** पर क्लिक करें
  * "Are you sure?" prompt पर, **Delete** पर क्लिक करें।

## अपने Azure resources delete करें

इस लैब में आपने जो अधिकांश resources बनाए हैं वे pay-as-you-go resources हैं, मतलब उनका उपयोग करने के लिए आपसे और कोई शुल्क नहीं लिया जाएगा। हालांकि, AI Foundry द्वारा उपयोग की जाने वाली कुछ storage services में छोटे ongoing charges हो सकते हैं। सभी resources delete करने के लिए, इन चरणों का पालन करें:

* [Azure Portal](https://portal.azure.com){:target="_blank"} पर जाएं
* **Resource groups** पर क्लिक करें
* अपने resource group `rg-agent-workshop-****` पर क्लिक करें
* **Delete Resource group** पर क्लिक करें
* नीचे field में "Enter resource group name to confirm deletion" में `rg-agent-workshop-****` दर्ज करें
* **Delete** पर क्लिक करें
  * Delete Confirmation prompt पर, "Delete" पर क्लिक करें

*GitHub Copilot और GPT-4o का उपयोग करके अनुवादित।*
