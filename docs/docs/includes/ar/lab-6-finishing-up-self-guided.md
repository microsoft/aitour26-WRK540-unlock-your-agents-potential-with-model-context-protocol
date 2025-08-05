هذا كل شيء بالنسبة لجزء المختبر من هذه الورشة. تابع القراءة للحصول على النقاط الرئيسية المستفادة والموارد الإضافية، ولكن أولاً دعنا نرتب الأمور.

## تنظيف GitHub CodeSpaces

### حفظ تغييراتك في GitHub

يمكنك حفظ أي تغييرات أجريتها على الملفات أثناء الورشة في مستودع GitHub الشخصي الخاص بك كفرع. يسهل هذا إعادة تشغيل الورشة مع تخصيصاتك، وستبقى محتوى الورشة متاحاً دائماً في حساب GitHub الخاص بك.

* في VS Code، انقر على أداة "Source Control" في الجزء الأيسر. إنها الثالثة من الأعلى، أو يمكنك استخدام اختصار لوحة المفاتيح <kbd>Control-Shift-G</kbd>.
* في الحقل تحت "Source Control" أدخل `Agents Lab` وانقر **✔️Commit**.
  * انقر **Yes** على التنبيه "There are no staged changes to commit."
* انقر **Sync Changes**.
  * انقر **OK** على التنبيه "This action will pull and push commits from and to origin/main".

لديك الآن نسختك الخاصة من الورشة مع تخصيصاتك في حساب GitHub الخاص بك.

### حذف GitHub codespace الخاص بك

سيتم إيقاف GitHub CodeSpace الخاص بك تلقائياً، لكنه سيستهلك كمية صغيرة من حصة الحوسبة والتخزين الخاصة بك حتى يتم حذفه. (يمكنك رؤية استخدامك في [ملخص فوترة GitHub](https://github.com/settings/billing/summary).) يمكنك حذف codespace بأمان الآن، كما يلي:

* قم بزيارة [github.com/codespaces](https://github.com/codespaces){:target="_blank"}
* في أسفل الصفحة، انقر على قائمة "..." على يمين codespace النشط الخاص بك
* انقر **Delete**
  * في التنبيه "Are you sure?"، انقر **Delete**.

## حذف موارد Azure الخاصة بك

معظم الموارد التي أنشأتها في هذا المختبر هي موارد الدفع حسب الاستخدام، مما يعني أنك لن تُحاسب أكثر على استخدامها. ومع ذلك، قد تتسبب بعض خدمات التخزين المستخدمة بواسطة AI Foundry في رسوم صغيرة مستمرة. لحذف جميع الموارد، اتبع هذه الخطوات:

* قم بزيارة [بوابة Azure](https://portal.azure.com){:target="_blank"}
* انقر **Resource groups**
* انقر على مجموعة الموارد الخاصة بك `rg-agent-workshop-****`
* انقر **Delete Resource group**
* في الحقل في الأسفل "Enter resource group name to confirm deletion" أدخل `rg-agent-workshop-****`
* انقر **Delete**
  * في تنبيه تأكيد الحذف، انقر "Delete"

*Translated using GitHub Copilot and GPT-4o.*
