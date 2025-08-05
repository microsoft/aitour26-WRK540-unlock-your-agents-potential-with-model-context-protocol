**TBC: ستحصل هذه التسمية على المستخدم لتحديث ملف تعليمات الوكيل لإزالة الرموز التعبيرية المزعجة التي يستخدمها الوكيل في استجاباته.**

## مقدمة

التتبع يساعدك على فهم وتصحيح سلوك الوكيل الخاص بك من خلال إظهار تسلسل الخطوات والمدخلات والمخرجات أثناء التنفيذ. في Azure AI Foundry، يتيح لك التتبع مراقبة كيفية معالجة الوكيل للطلبات واستدعاء الأدوات وتوليد الاستجابات. يمكنك استخدام بوابة Azure AI Foundry أو التكامل مع OpenTelemetry وApplication Insights لجمع وتحليل بيانات التتبع، مما يجعل من الأسهل استكشاف الأخطاء وإصلاحها وتحسين الوكيل الخاص بك.

<!-- ## تمرين المختبر

=== "Python"

      1. افتح ملف `app.py`.
      2. غيّر متغير `AZURE_TELEMETRY_ENABLED` إلى `True` لتمكين التتبع:

         ```python
         AZURE_TELEMETRY_ENABLED = True
         ```

        !!! info "ملاحظة"
            يمكن هذا الإعداد تتبع المقاييس لوكيلك. في دالة `initialize` في `app.py`, يتم تكوين عميل تتبع المقاييس لإرسال البيانات إلى Azure Monitor.

            ```python
             if AZURE_TELEMETRY_ENABLED:
                 configure_azure_monitor(connection_string=await self.project_client.telemetry.get_connection_string())
            ```         

=== "C#"

      tbd -->

## تشغيل تطبيق الوكيل

1. اضغط <kbd>F5</kbd> لتشغيل التطبيق.
2. اختر **Preview in Editor** لفتح تطبيق الوكيل في علامة تبويب محرر جديدة.

### بدء محادثة مع الوكيل

انسخ والصق الاستدعاء التالي في تطبيق الوكيل لبدء محادثة:

```plaintext
اكتب تقريراً تنفيذياً يحلل أفضل 5 فئات منتجات ويقارن أداء المتجر الإلكتروني مقابل المتوسط للمتاجر الفيزيائية.
```

## عرض التتبعات

يمكنك عرض تتبعات تنفيذ الوكيل الخاص بك في بوابة Azure AI Foundry أو باستخدام OpenTelemetry. ستظهر التتبعات تسلسل الخطوات واستدعاءات الأدوات والبيانات المتبادلة أثناء تنفيذ الوكيل. هذه المعلومات بالغة الأهمية لتصحيح وتحسين أداء الوكيل الخاص بك.

### استخدام بوابة Azure AI Foundry

لعرض التتبعات في بوابة Azure AI Foundry، اتبع هذه الخطوات:

1. انتقل إلى بوابة **[Azure AI Foundry](https://ai.azure.com/)**.
2. اختر مشروعك.
3. اختر علامة تبويب **Tracing** في القائمة اليسرى.
4. هنا، يمكنك رؤية التتبعات المُولدة بواسطة الوكيل الخاص بك.

   ![](media/ai-foundry-tracing.png)

### التعمق في التتبعات

1. قد تحتاج إلى النقر على زر **Refresh** لرؤية أحدث التتبعات حيث قد تستغرق التتبعات بضع لحظات للظهور.
2. اختر التتبع المسمى `Zava Agent Initialization` لعرض التفاصيل.
   ![](media/ai-foundry-trace-agent-init.png)
3. اختر تتبع `creare_agent Zava DIY Sales Agent` لعرض تفاصيل عملية إنشاء الوكيل. في قسم `Input & outputs`، ستشاهد تعليمات الوكيل.
4. بعد ذلك، اختر تتبع `Zava Agent Chat Request: Write an executive...` لعرض تفاصيل طلب المحادثة. في قسم `Input & outputs`، ستشاهد مدخلات المستخدم واستجابة الوكيل.

<!-- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/continuous-evaluation-agents -->

*Translated using GitHub Copilot and GPT-4o.*
