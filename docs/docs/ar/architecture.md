## بنية الحل

في هذه الورشة، ستقوم بإنشاء وكيل مبيعات Zava: وكيل محادثة مصمم للإجابة على الأسئلة حول بيانات المبيعات وتوليد الرسوم البيانية لأعمال Zava التجارية في مجال DIY.

## مكونات تطبيق الوكيل

1. **خدمات Microsoft Azure**

    هذا الوكيل مبني على خدمات Microsoft Azure.

      - **نموذج الذكاء الاصطناعي التوليدي**: النموذج اللغوي الكبير الأساسي الذي يدعم هذا التطبيق هو [Azure OpenAI gpt-4o-mini](https://learn.microsoft.com/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#how-do-i-access-the-gpt-4o-and-gpt-4o-mini-models){:target="_blank"}.

      - **مستوى التحكم**: يتم إدارة التطبيق ومكوناته المعمارية ومراقبتها باستخدام بوابة [Azure AI Foundry](https://ai.azure.com){:target="_blank"}، والتي يمكن الوصول إليها عبر المتصفح.

2. **Azure AI Foundry (SDK)**

    تُقدم الورشة بلغة [Python](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?view=azure-python-preview&context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} باستخدام Azure AI Foundry SDK. تدعم مجموعة التطوير الميزات الرئيسية لخدمة Azure AI Agents، بما في ذلك [مفسر الكود](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?view=azure-python-preview&tabs=python&pivots=overview){:target="_blank"} وتكامل [بروتوكول سياق النموذج (MCP)](https://modelcontextprotocol.io/){:target="_blank"}.

3. **قاعدة البيانات**

    يتم تشغيل التطبيق بواسطة قاعدة بيانات مبيعات Zava، وهي [Azure Database for PostgreSQL flexible server](https://www.postgresql.org/){:target="_blank"} مع امتداد pgvector تحتوي على بيانات مبيعات شاملة لعمليات Zava التجارية في مجال DIY.

    تدعم قاعدة البيانات الاستعلامات المعقدة لبيانات المبيعات والمخزون والعملاء. يضمن أمان المستوى الصفي (RLS) وصول الوكلاء فقط إلى المتاجر المخصصة لهم.

4. **خادم MCP**

    خادم بروتوكول سياق النموذج (MCP) هو خدمة Python مخصصة تعمل كجسر بين الوكيل وقاعدة بيانات PostgreSQL. يتولى:

     - **اكتشاف مخطط قاعدة البيانات**: يسترد تلقائياً مخططات قاعدة البيانات لمساعدة الوكيل في فهم البيانات المتاحة.
     - **توليد الاستعلامات**: يحول طلبات اللغة الطبيعية إلى استعلامات SQL.
     - **تنفيذ الأدوات**: ينفذ استعلامات SQL ويعيد النتائج بتنسيق يمكن للوكيل استخدامه.
     - **خدمات الوقت**: يوفر بيانات متعلقة بالوقت لتوليد تقارير حساسة للوقت.

## توسيع حل الورشة

يمكن تكييف الورشة بسهولة مع حالات الاستخدام مثل دعم العملاء من خلال تحديث قاعدة البيانات وتخصيص تعليمات خدمة Foundry Agent Service.

## أفضل الممارسات المُوضحة في التطبيق

يُظهر التطبيق أيضاً بعض أفضل الممارسات للكفاءة وتجربة المستخدم.

- **واجهات برمجة التطبيقات غير المتزامنة**:
  في عينة الورشة، تستخدم كل من خدمة Foundry Agent Service وPostgreSQL واجهات برمجة تطبيقات غير متزامنة، مما يحسن كفاءة الموارد وقابلية التوسع. يصبح هذا الاختيار التصميمي مفيداً خاصة عند نشر التطبيق مع إطارات الويب غير المتزامنة مثل FastAPI أو ASP.NET أو Streamlit.

- **تدفق الرموز المميزة**:
  يتم تنفيذ تدفق الرموز المميزة لتحسين تجربة المستخدم من خلال تقليل أوقات الاستجابة المُدركة لتطبيق الوكيل المدعوم بالنموذج اللغوي الكبير.

- **إمكانية المراقبة**:
  يتضمن التطبيق [تتبعاً](https://learn.microsoft.com/azure/ai-foundry/agents/concepts/tracing){:target="_blank"} و[مقاييس](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/metrics){:target="_blank"} مدمجين لمراقبة أداء الوكيل وأنماط الاستخدام والكمون. يمكّنك هذا من تحديد المشاكل وتحسين الوكيل مع مرور الوقت.

*Translated using GitHub Copilot and GPT-4o.*
