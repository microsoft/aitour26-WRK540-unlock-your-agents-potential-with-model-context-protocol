## انتظار اكتمال بناء Codespace

قبل المتابعة، تأكد من أن Codespace أو Dev Container الخاص بك مبني بالكامل وجاهز. قد يستغرق هذا عدة دقائق، اعتماداً على اتصال الإنترنت والموارد التي يتم تحميلها.

## المصادقة مع Azure

قم بالمصادقة مع Azure للسماح لتطبيق الوكيل بالوصول إلى خدمة Azure AI Agents Service والنماذج. اتبع هذه الخطوات:

1. تأكد من أن بيئة الورشة جاهزة ومفتوحة في VS Code.
2. من VS Code، افتح محطة عبر **Terminal** > **New Terminal** في VS Code، ثم شغّل:

    ```shell
    az login --use-device-code
    ```

    !!! note
        ستُطلب منك فتح متصفح وتسجيل الدخول إلى Azure. انسخ رمز المصادقة و:

        1. اختر نوع حسابك وانقر **التالي**.
        2. سجل الدخول ببيانات اعتماد Azure الخاصة بك.
        3. الصق الرمز.
        4. انقر **موافق**، ثم **تم**.

    !!! warning
        إذا كان لديك مستأجرون Azure متعددون، حدد الصحيح باستخدام:

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

3. بعد ذلك، اختر الاشتراك المناسب من سطر الأوامر.
4. اترك نافذة المحطة مفتوحة للخطوات التالية.

## نشر موارد Azure

ينشئ هذا النشر الموارد التالية في اشتراك Azure الخاص بك تحت مجموعة الموارد **rg-zava-agent-wks-nnnn**:

- **مركز Azure AI Foundry** يُسمى **fdy-zava-agent-wks-nnnn**
- **مشروع Azure AI Foundry** يُسمى **prj-zava-agent-wks-nnnn**
- يتم نشر نموذجين: **gpt-4o-mini** و**text-embedding-3-small**. [راجع التسعير.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}

!!! warning "تأكد من أن لديك على الأقل 120K TPM حصة لـ gpt-4o-mini Global Standard SKU، حيث يقوم الوكيل بإجراء استدعاءات نموذج متكررة. تحقق من حصتك في [مركز إدارة AI Foundry](https://ai.azure.com/managementCenter/quota){:target="_blank"}."

لقد وفرنا نص bash لأتمتة نشر الموارد المطلوبة للورشة.

### النشر الآلي

ينشر نص `deploy.sh` الموارد إلى منطقة `westus` بشكل افتراضي. لتشغيل النص:

```bash
cd infra && ./deploy.sh
```

<!-- !!! note "في Windows، شغّل `deploy.ps1` بدلاً من `deploy.sh`" -->

### تكوين الورشة

=== "Python"

    #### تكوين موارد Azure

    ينشئ نص النشر ملف **.env**، والذي يحتوي على نقاط نهاية المشروع والنموذج وأسماء نشر النماذج وسلسلة اتصال Application Insights. سيتم حفظ ملف .env تلقائياً في مجلد `src/python/workshop`.
    
    سيبدو ملف **.env** الخاص بك مشابهاً للتالي، محدث بقيمك:

    ```python
    PROJECT_ENDPOINT="<your_project_endpoint>"
    GPT_MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<your_embedding_model_deployment_name>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<your_application_insights_connection_string>"
    DEV_TUNNEL_URL="<your_dev_tunnel_url>"
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
    AZURE_OPENAI_ENDPOINT="<your_azure_openai_endpoint>"
    ```

    #### أسماء موارد Azure

    ستجد أيضاً ملفاً يُسمى `resources.txt` في مجلد `workshop`. يحتوي هذا الملف على أسماء موارد Azure المُنشأة أثناء النشر.

    سيبدو مشابهاً للتالي:

    ```plaintext
    Azure AI Foundry Resources:
    - Resource Group Name: rg-zava-agent-wks-nnnn
    - AI Project Name: prj-zava-agent-wks-nnnn
    - Foundry Resource Name: fdy-zava-agent-wks-nnnn
    - Application Insights Name: appi-zava-agent-wks-nnnn
    ```


=== "C#"

    يحفظ النص متغيرات المشروع بأمان باستخدام Secret Manager لـ [أسرار تطوير ASP.NET Core](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}.

    يمكنك عرض الأسرار بتشغيل الأمر التالي بعد فتح مساحة عمل C# في VS Code:

    ```bash
    dotnet user-secrets list
    ```

*Translated using GitHub Copilot and GPT-4o.*
