## مشاركو الأحداث من Microsoft

تفترض التعليمات في هذه الصفحة أنك تحضر [حدث Microsoft 2025](https://build.microsoft.com/){:target="_blank"} ولديك وصول إلى بيئة مختبر مُكونة مسبقاً. توفر هذه البيئة اشتراك Azure مع جميع الأدوات والموارد المطلوبة لإكمال الورشة.

## مقدمة

صُممت هذه الورشة لتعليمك عن خدمة Azure AI Agents Service و[SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} المرتبط بها. تتكون من مختبرات متعددة، كل منها يسلط الضوء على ميزة محددة من خدمة Azure AI Agents Service. المختبرات مُصممة لإكمالها بالترتيب، حيث يبني كل منها على المعرفة والعمل من المختبر السابق.

## اختيار لغة البرمجة للورشة

الورشة متاحة بلغتي Python وC#. يرجى التأكد من اختيار اللغة التي تناسب غرفة المختبر التي أنت فيها، باستخدام علامات تبويب محدد اللغة. لاحظ، لا تغير اللغة في منتصف الورشة.

**اختر علامة تبويب اللغة التي تطابق غرفة المختبر الخاصة بك:**

=== "Python"
    اللغة الافتراضية للورشة مضبوطة على **Python**.
=== "C#"
    اللغة الافتراضية للورشة مضبوطة على **C#**.

## المصادقة مع Azure

تحتاج إلى المصادقة مع Azure حتى يتمكن تطبيق الوكيل من الوصول إلى خدمة Azure AI Agents Service والنماذج. اتبع هذه الخطوات:

1. افتح نافذة محطة. تطبيق المحطة **مثبت** في شريط مهام Windows 11.

    ![فتح نافذة المحطة](../media/windows-taskbar.png){ width="300" }

2. شغّل الأمر التالي للمصادقة مع Azure:

    ```powershell
    az login
    ```

    !!! note
        ستُطلب منك فتح رابط متصفح وتسجيل الدخول إلى حساب Azure الخاص بك.

        1. ستفتح نافذة متصفح تلقائياً، اختر **حساب العمل أو المدرسة** وانقر **التالي**.

        1. استخدم **اسم المستخدم** و**كلمة المرور** الموجودين في **القسم العلوي** من علامة تبويب **الموارد** في بيئة المختبر.

        2. اختر **موافق**، ثم **تم**.

3. ثم اختر اشتراك **الافتراضي** من سطر الأوامر، بالنقر على **Enter**.

4. بمجرد تسجيل الدخول، شغّل الأمر التالي لتعيين دور **المستخدم** إلى مجموعة الموارد:

    ```powershell
    $subId = $(az account show --query id --output tsv) `
    ;$objectId = $(az ad signed-in-user show --query id -o tsv) `
    ; az role assignment create --role "f6c7c914-8db3-469d-8ca1-694a8f32e121" --assignee-object-id $objectId --scope /subscriptions/$subId/resourceGroups/"rg-agent-workshop" --assignee-principal-type 'User'
    ```

5. اترك نافذة المحطة مفتوحة للخطوات التالية.

## فتح الورشة

اتبع هذه الخطوات لفتح الورشة في Visual Studio Code:

=== "Python"

      1. من نافذة المحطة، نفذ الأوامر التالية لاستنساخ مستودع الورشة والانتقال إلى المجلد ذي الصلة وإعداد بيئة افتراضية وتفعيلها وتثبيت الحزم المطلوبة:

          ```powershell
          git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git `
          ; cd build-your-first-agent-with-azure-ai-agent-service-workshop `
          ; python -m venv src/python/workshop/.venv `
          ; src\python\workshop\.venv\Scripts\activate `
          ; pip install -r src/python/workshop/requirements.txt `
          ; code --install-extension tomoki1207.pdf
          ```

      2. فتح في VS Code. من نافذة المحطة، شغّل الأمر التالي:

          ```powershell
          code .vscode\python-workspace.code-workspace
          ```

        !!! warning "عندما يُفتح المشروع في VS Code، تظهر إشعاران في الركن الأيمن السفلي. انقر ✖ لإغلاق كلا الإشعارين."

=== "C#"

    1. من نافذة محطة، نفذ الأوامر التالية لاستنساخ مستودع الورشة:

        ```powershell
        git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git
        ```

    === "VS Code"

        1. افتح الورشة في Visual Studio Code. من نافذة المحطة، شغّل الأمر التالي:

            ```powershell
            code build-your-first-agent-with-azure-ai-agent-service-workshop\.vscode\csharp-workspace.code-workspace
            ```

        !!! note "عندما يُفتح المشروع في VS Code، سيظهر إشعار في الركن الأيمن السفلي لتثبيت امتداد C#. انقر **تثبيت** لتثبيت امتداد C#، حيث سيوفر هذا الميزات اللازمة لتطوير C#."

    === "Visual Studio 2022"

        1. افتح الورشة في Visual Studio 2022. من نافذة المحطة، شغّل الأمر التالي:

            ```powershell
            start build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.sln
            ```

            !!! note "قد يُطلب منك ما البرنامج الذي تريد فتح الحل به. اختر **Visual Studio 2022**."

## نقطة نهاية مشروع Azure AI Foundry

بعد ذلك، نسجل الدخول إلى Azure AI Foundry لاسترداد نقطة نهاية المشروع، والتي يستخدمها تطبيق الوكيل للاتصال بخدمة Azure AI Agents Service.

1. انتقل إلى موقع [Azure AI Foundry](https://ai.azure.com){:target="_blank"}.
2. اختر **تسجيل الدخول** واستخدم **اسم المستخدم** و**كلمة المرور** الموجودين في **القسم العلوي** من علامة تبويب **الموارد** في بيئة المختبر. انقر على حقلي **اسم المستخدم** و**كلمة المرور** لتعبئة تفاصيل تسجيل الدخول تلقائياً.
    ![بيانات اعتماد Azure](../media/azure-credentials.png){:width="500"}
3. اقرأ مقدمة Azure AI Foundry وانقر **فهمت**.
4. انتقل إلى [جميع الموارد](https://ai.azure.com/AllResources){:target="_blank"} لعرض قائمة موارد الذكاء الاصطناعي التي تم توفيرها مسبقاً لك.
5. اختر اسم المورد الذي يبدأ بـ **aip-** من نوع **مشروع**.

    ![اختيار المشروع](../media/ai-foundry-project.png){:width="500"}

6. راجع دليل المقدمة وانقر **إغلاق**.
7. من قائمة **نظرة عامة** الجانبية، حدد موقع **نقاط النهاية والمفاتيح** -> **المكتبات** -> قسم **Azure AI Foundry**، انقر على أيقونة **نسخ** لنسخ **نقطة نهاية مشروع Azure AI Foundry**.

    ![نسخ سلسلة الاتصال](../media/project-connection-string.png){:width="500"}

=== "Python"

    ## تكوين الورشة

    1. ارجع إلى الورشة التي فتحتها في VS Code.
    2. **أعد تسمية** ملف `.env.sample` إلى `.env`.

        - اختر ملف **.env.sample** في لوحة **Explorer** في VS Code.
        - انقر بالزر الأيمن على الملف واختر **إعادة تسمية**، أو اضغط <kbd>F2</kbd>.
        - غيّر اسم الملف إلى `.env` واضغط <kbd>Enter</kbd>.

    3. الصق **نقطة نهاية المشروع** التي نسختها من Azure AI Foundry في ملف `.env`.

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        ```

        يجب أن يبدو ملف `.env` الخاص بك مشابهاً لهذا ولكن مع نقطة نهاية مشروعك.

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
        DEV_TUNNEL_URL="<your_dev_tunnel_url>"
        ```

    4. احفظ ملف `.env`.

    ## هيكل المشروع

    تأكد من التعرف على **المجلدات الفرعية** و**الملفات** الرئيسية التي ستعمل معها طوال الورشة.

    5. ملف **app.py**: نقطة الدخول للتطبيق، يحتوي على المنطق الرئيسي.
    6. ملف **sales_data.py**: منطق الدالة لتنفيذ استعلامات SQL الديناميكية مقابل قاعدة بيانات SQLite.
    7. ملف **stream_event_handler.py**: يحتوي على منطق معالج الأحداث لتدفق الرموز المميزة.
    8. مجلد **shared/files**: يحتوي على الملفات المُنشأة بواسطة تطبيق الوكيل.
    9. مجلد **shared/instructions**: يحتوي على التعليمات المُمررة إلى النموذج اللغوي الكبير.

    ![هيكل مجلد المختبر](../media/project-structure-self-guided-python.png)

=== "C#"

    ## تكوين الورشة

    1. افتح محطة وانتقل إلى مجلد **src/csharp/workshop/AgentWorkshop.Client**.

        ```powershell
        cd build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.Client
        ```

    2. أضف **نقطة نهاية المشروع** التي نسختها من Azure AI Foundry إلى أسرار المستخدم.

        ```powershell
        dotnet user-secrets set "ConnectionStrings:AiAgentService" "<your_project_endpoint>"
        ```

    3. أضف **اسم نشر النموذج** إلى أسرار المستخدم.

        ```powershell
        dotnet user-secrets set "Azure:ModelName" "gpt-4o"
        ```

    4. أضف **معرف اتصال Bing** إلى أسرار المستخدم للتأسيس مع بحث Bing.

        ```powershell
        $subId = $(az account show --query id --output tsv)
        $rgName = "rg-agent-workshop"
        $aiAccount = "<ai_account_name>" # استبدل باسم حساب الذكاء الاصطناعي الفعلي
        $aiProject = "<ai_project_name>" # استبدل باسم مشروع الذكاء الاصطناعي الفعلي
        $bingConnectionId = "/subscriptions/$subId/resourceGroups/$rgName/providers/Microsoft.CognitiveServices/accounts/$aiAccount/projects/$aiProject/connections/groundingwithbingsearch"
        dotnet user-secrets set "Azure:BingConnectionId" "$bingConnectionId"
        ```

    ## هيكل المشروع

    تأكد من التعرف على **المجلدات الفرعية** و**الملفات** الرئيسية التي ستعمل معها طوال الورشة.

*Translated using GitHub Copilot and GPT-4o.*
