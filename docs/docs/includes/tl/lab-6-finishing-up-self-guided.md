Iyan na ang lahat para sa lab portion ng workshop na ito. Magpatuloy sa pagbabasa para sa key takeaways at additional resources, pero muna natin ayusin.

## I-clean up ang GitHub CodeSpaces

### I-save ang inyong mga changes sa GitHub 

Maaari ninyong i-save ang anumang mga changes na ginawa ninyo sa mga files sa panahon ng workshop sa inyong personal GitHub repository bilang fork. Ginagawa nitong madali na muling patakbuhin ang workshop na may inyong customizations, at ang workshop content ay laging magiging available sa inyong GitHub account.

* Sa VS Code, i-click ang "Source Control" tool sa left pane. Ito ang pangatlong nasa ibaba, o maaari ninyong gamitin ang keyboard shortcut na <kbd>Control-Shift-G</kbd>.
* Sa field sa ilalim ng "Source Control" ilagay ang `Agents Lab` at i-click ang **✔️Commit**.
  * I-click ang **Yes** sa prompt na "There are no staged changes to commit."
* I-click ang **Sync Changes**.
  * I-click ang **OK** sa prompt na "This action will pull and push commits from and to origin/main".

Mayroon na kayong sariling copy ng workshop na may inyong customizations sa inyong GitHub account.

### I-delete ang inyong GitHub codespace

Awtomatikong magsasara ang inyong GitHub CodeSpace, pero kakain ito ng maliit na bahagi ng inyong compute at storage allotment hanggang sa ma-delete ito. (Maaari ninyong tingnan ang inyong usage sa inyong [GitHub Billing summary](https://github.com/settings/billing/summary).) Maaari ninyong ligtas na i-delete ang codespace ngayon, tulad ng sumusunod:

* Bisitahin ang [github.com/codespaces](https://github.com/codespaces){:target="_blank"}
* Sa bottom ng page, i-click ang "..." menu sa kanan ng inyong active codespace
* I-click ang **Delete**
  * Sa "Are you sure?" prompt, i-click ang **Delete**.

## I-delete ang inyong Azure resources

Karamihan sa mga resources na ginawa ninyo sa lab na ito ay pay-as-you-go resources, ibig sabihin hindi na kayo singilan pa para sa paggamit sa mga ito. Gayunpaman, maaaring magkaroon ng maliit na ongoing charges ang ilang storage services na ginagamit ng AI Foundry. Upang i-delete ang lahat ng resources, sundin ang mga steps na ito:

* Bisitahin ang [Azure Portal](https://portal.azure.com){:target="_blank"}
* I-click ang **Resource groups**
* I-click ang inyong resource group na `rg-agent-workshop-****`
* I-click ang **Delete Resource group**
* Sa field sa bottom na "Enter resource group name to confirm deletion" ilagay ang `rg-agent-workshop-****`
* I-click ang **Delete**
  * Sa Delete Confirmation prompt, i-click ang "Delete"

*Isinalin gamit ang GitHub Copilot.*
