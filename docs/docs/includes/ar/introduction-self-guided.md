## المتعلمون الذاتيون

هذه التعليمات مخصصة للمتعلمين الذاتيين الذين لا يملكون وصولاً إلى بيئة مختبر مُكونة مسبقاً. اتبع هذه الخطوات لإعداد بيئتك وبدء الورشة.

## مقدمة

صُممت هذه الورشة لتعليمك عن خدمة Azure AI Agents Service ومجموعة التطوير المرتبطة بها. تتكون من مختبرات متعددة، كل منها يسلط الضوء على ميزة محددة من خدمة Azure AI Agents Service. المختبرات مُصممة لإكمالها بالترتيب، حيث يبني كل منها على المعرفة والعمل من المختبر السابق.

## المتطلبات الأساسية

1. الوصول إلى اشتراك Azure. إذا لم يكن لديك اشتراك Azure، أنشئ [حساباً مجانياً](https://azure.microsoft.com/free/){:target="_blank"} قبل البدء.
1. تحتاج إلى حساب GitHub. إذا لم يكن لديك واحد، أنشئه في [GitHub](https://github.com/join){:target="_blank"}.

## اختيار لغة البرمجة للورشة

الورشة متاحة بلغتي Python وC#. استخدم علامات تبويب محدد اللغة لاختيار لغتك المفضلة. لاحظ، لا تغير اللغة في منتصف الورشة.

**اختر علامة التبويب للغتك المفضلة:**

=== "Python"
    اللغة الافتراضية للورشة مضبوطة على **Python**.
=== "C#"
    اللغة الافتراضية للورشة مضبوطة على **C#**.

## فتح الورشة

الطريقة **المفضلة** لتشغيل هذه الورشة هي استخدام **GitHub Codespaces**. يوفر هذا الخيار بيئة مُكونة مسبقاً مع جميع الأدوات والموارد المطلوبة لإكمال الورشة. بدلاً من ذلك، يمكنك فتح الورشة محلياً باستخدام Visual Studio Code Dev Container وDocker. كلا الخيارين موصوفان أدناه.

!!! Note
    **سيستغرق بناء Codespace أو Dev Container حوالي 5 دقائق. ابدأ العملية ثم يمكنك متابعة قراءة التعليمات أثناء البناء.**

=== "GitHub Codespaces"

    اختر **Open in GitHub Codespaces** لفتح المشروع في GitHub Codespaces.

    [![فتح في GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol){:target="_blank"}



=== "VS Code Dev Container"

    <!-- !!! warning "مستخدمو Apple Silicon"
        نص النشر الآلي الذي ستشغله قريباً غير مدعوم على Apple Silicon. يرجى تشغيل نص النشر من Codespaces أو من macOS بدلاً من Dev Container. -->

    بدلاً من ذلك، يمكنك فتح المشروع محلياً باستخدام Visual Studio Code Dev Container، والذي سيفتح المشروع في بيئة تطوير VS Code المحلية الخاصة بك باستخدام [امتداد Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers){:target="_blank"}.

    1. ابدأ Docker Desktop (ثبته إذا لم يكن مثبتاً بالفعل)
    2. اختر **Dev Containers Open** لفتح المشروع في VS Code Dev Container.

        [![فتح في Dev Containers](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol)

*Translated using GitHub Copilot and GPT-4o.*
