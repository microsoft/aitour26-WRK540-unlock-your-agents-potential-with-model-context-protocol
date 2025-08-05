## Asistentes de Eventos de Microsoft

Las instrucciones en esta página asumen que estás asistiendo al [Evento de Microsoft 2025](https://build.microsoft.com/){:target="_blank"} y tienes acceso a un entorno de laboratorio preconfigurado. Este entorno proporciona una suscripción de Azure con todas las herramientas y recursos necesarios para completar el taller.

## Introducción

Este taller está diseñado para enseñarte sobre el Servicio de Agentes de IA de Azure y el [SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} asociado. Consiste en múltiples laboratorios, cada uno destacando una característica específica del Servicio de Agentes de IA de Azure. Los laboratorios están diseñados para completarse en orden, ya que cada uno se basa en el conocimiento y trabajo del laboratorio anterior.

## Seleccionar el Lenguaje de Programación del Taller

El taller está disponible tanto en Python como en C#. Por favor asegúrate de seleccionar el lenguaje que se adapte al aula de laboratorio en la que estás, usando las pestañas del selector de lenguaje. Nota, no cambies de lenguaje a mitad del taller.

**Selecciona la pestaña de lenguaje que coincida con tu aula de laboratorio:**

=== "Python"
    El lenguaje predeterminado para el taller está configurado como **Python**.
=== "C#"
    El lenguaje predeterminado para el taller está configurado como **C#**.

## Autenticar con Azure

Necesitas autenticarte con Azure para que la aplicación del agente pueda acceder al Servicio de Agentes de IA de Azure y a los modelos. Sigue estos pasos:

1. Abre una ventana de terminal. La aplicación de terminal está **anclada** a la barra de tareas de Windows 11.

    ![Abrir la ventana de terminal](../media/windows-taskbar.png){ width="300" }

2. Ejecuta el siguiente comando para autenticarte con Azure:

    ```powershell
    az login
    ```

    !!! note
        Se te pedirá que abas un enlace del navegador e inicies sesión en tu cuenta de Azure.

        1. Una ventana del navegador se abrirá automáticamente, selecciona **Cuenta de trabajo o escuela** y haz clic en **Siguiente**.

        1. Usa el **Nombre de usuario** y **Contraseña** que se encuentran en la **sección superior** de la pestaña **Recursos** en el entorno de laboratorio.

        2. Selecciona **OK**, luego **Hecho**.

3. Luego selecciona la suscripción **Predeterminada** desde la línea de comandos, haciendo clic en **Enter**.

4. Una vez que hayas iniciado sesión, ejecuta el siguiente comando para asignar el rol de **usuario** al grupo de recursos:

    ```powershell
    $subId = $(az account show --query id --output tsv) `
    ;$objectId = $(az ad signed-in-user show --query id -o tsv) `
    ; az role assignment create --role "f6c7c914-8db3-469d-8ca1-694a8f32e121" --assignee-object-id $objectId --scope /subscriptions/$subId/resourceGroups/"rg-agent-workshop" --assignee-principal-type 'User'
    ```

5. Deja la ventana de terminal abierta para los siguientes pasos.

## Abrir el Taller

Sigue estos pasos para abrir el taller en Visual Studio Code:

=== "Python"

      1. Desde la ventana de terminal, ejecuta los siguientes comandos para clonar el repositorio del taller, navegar a la carpeta relevante, configurar un entorno virtual, activarlo e instalar los paquetes requeridos:

          ```powershell
          git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git `
          ; cd build-your-first-agent-with-azure-ai-agent-service-workshop `
          ; python -m venv src/python/workshop/.venv `
          ; src\python\workshop\.venv\Scripts\activate `
          ; pip install -r src/python/workshop/requirements.txt `
          ; code --install-extension tomoki1207.pdf
          ```

      2. Abrir en VS Code. Desde la ventana de terminal, ejecuta el siguiente comando:

          ```powershell
          code .vscode\python-workspace.code-workspace
          ```

        !!! warning "Cuando el proyecto se abre en VS Code, aparecen dos notificaciones en la esquina inferior derecha. Haz clic en ✖ para cerrar ambas notificaciones."

=== "C#"

    1. Desde una ventana de terminal, ejecuta los siguientes comandos para clonar el repositorio del taller:

        ```powershell
        git clone https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop.git
        ```

    === "VS Code"

        1. Abre el taller en Visual Studio Code. Desde la ventana de terminal, ejecuta el siguiente comando:

            ```powershell
            code build-your-first-agent-with-azure-ai-agent-service-workshop\.vscode\csharp-workspace.code-workspace
            ```

        !!! note "Cuando el proyecto se abre en VS Code, aparecerá una notificación en la esquina inferior derecha para instalar la extensión de C#. Haz clic en **Instalar** para instalar la extensión de C#, ya que esto proporcionará las características necesarias para el desarrollo de C#."

    === "Visual Studio 2022"

        1. Abre el taller en Visual Studio 2022. Desde la ventana de terminal, ejecuta el siguiente comando:

            ```powershell
            start build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.sln
            ```

            !!! note "Es posible que te pregunten con qué programa abrir la solución. Selecciona **Visual Studio 2022**."

## Endpoint del Proyecto de Azure AI Foundry

A continuación, iniciamos sesión en Azure AI Foundry para recuperar el endpoint del proyecto, que la aplicación del agente usa para conectarse al Servicio de Agentes de IA de Azure.

1. Navega al sitio web de [Azure AI Foundry](https://ai.azure.com){:target="_blank"}.
2. Selecciona **Iniciar sesión** y usa el **Nombre de usuario** y **Contraseña** que se encuentran en la **sección superior** de la pestaña **Recursos** en el entorno de laboratorio. Haz clic en los campos **Nombre de usuario** y **Contraseña** para completar automáticamente los detalles de inicio de sesión.
    ![Credenciales de Azure](../media/azure-credentials.png){:width="500"}
3. Lee la introducción a Azure AI Foundry y haz clic en **Entendido**.
4. Navega a [Todos los Recursos](https://ai.azure.com/AllResources){:target="_blank"} para ver la lista de recursos de IA que han sido pre-aprovisionados para ti.
5. Selecciona el nombre del recurso que comience con **aip-** de tipo **Proyecto**.

    ![Seleccionar proyecto](../media/ai-foundry-project.png){:width="500"}

6. Revisa la guía de introducción y haz clic en **Cerrar**.
7. Desde el menú lateral **Visión general**, localiza la sección **Endpoints y claves** -> **Bibliotecas** -> **Azure AI Foundry**, haz clic en el ícono **Copiar** para copiar el **endpoint del proyecto Azure AI Foundry**.

    ![Copiar cadena de conexión](../media/project-connection-string.png){:width="500"}

=== "Python"

    ## Configurar el Taller

    1. Regresa al taller que abriste en VS Code.
    2. **Renombra** el archivo `.env.sample` a `.env`.

        - Selecciona el archivo **.env.sample** en el panel **Explorador** de VS Code.
        - Haz clic derecho en el archivo y selecciona **Renombrar**, o presiona <kbd>F2</kbd>.
        - Cambia el nombre del archivo a `.env` y presiona <kbd>Enter</kbd>.

    3. Pega el **Endpoint del proyecto** que copiaste de Azure AI Foundry en el archivo `.env`.

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        ```

        Tu archivo `.env` debería verse similar a esto pero con tu endpoint del proyecto.

        ```python
        PROJECT_ENDPOINT="<your_project_endpoint>"
        MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
        DEV_TUNNEL_URL="<your_dev_tunnel_url>"
        ```

    4. Guarda el archivo `.env`.

    ## Estructura del Proyecto

    Asegúrate de familiarizarte con las **subcarpetas** y **archivos** clave con los que trabajarás durante el taller.

    5. El archivo **app.py**: El punto de entrada para la aplicación, conteniendo su lógica principal.
    6. El archivo **sales_data.py**: La lógica de función para ejecutar consultas SQL dinámicas contra la base de datos SQLite.
    7. El archivo **stream_event_handler.py**: Contiene la lógica del manejador de eventos para transmisión de tokens.
    8. La carpeta **shared/files**: Contiene los archivos creados por la aplicación del agente.
    9. La carpeta **shared/instructions**: Contiene las instrucciones pasadas al LLM.

    ![Estructura de carpetas del laboratorio](../media/project-structure-self-guided-python.png)

=== "C#"

    ## Configurar el Taller

    1. Abre una terminal y navega a la carpeta **src/csharp/workshop/AgentWorkshop.Client**.

        ```powershell
        cd build-your-first-agent-with-azure-ai-agent-service-workshop\src\csharp\workshop\AgentWorkshop.Client
        ```

    2. Agrega el **Endpoint del proyecto** que copiaste de Azure AI Foundry a los secretos de usuario.

        ```powershell
        dotnet user-secrets set "ConnectionStrings:AiAgentService" "<your_project_endpoint>"
        ```

    3. Agrega el **Nombre de implementación del modelo** a los secretos de usuario.

        ```powershell
        dotnet user-secrets set "Azure:ModelName" "gpt-4o"
        ```

    4. Agrega el **ID de conexión de Bing** a los secretos de usuario para fundamentación con búsqueda de Bing.

        ```powershell
        $subId = $(az account show --query id --output tsv)
        $rgName = "rg-agent-workshop"
        $aiAccount = "<ai_account_name>" # Reemplaza con el nombre real de la cuenta de IA
        $aiProject = "<ai_project_name>" # Reemplaza con el nombre real del proyecto de IA
        $bingConnectionId = "/subscriptions/$subId/resourceGroups/$rgName/providers/Microsoft.CognitiveServices/accounts/$aiAccount/projects/$aiProject/connections/groundingwithbingsearch"
        dotnet user-secrets set "Azure:BingConnectionId" "$bingConnectionId"
        ```

    ## Estructura del Proyecto

    Asegúrate de familiarizarte con las **subcarpetas** y **archivos** clave con los que trabajarás durante el taller.

    ### La carpeta workshop

    - Los archivos **Lab1.cs, Lab2.cs, Lab3.cs**: El punto de entrada para cada laboratorio, conteniendo su lógica de agente.
    - El archivo **Program.cs**: El punto de entrada para la aplicación, conteniendo su lógica principal.
    - El archivo **SalesData.cs**: La lógica de función para ejecutar consultas SQL dinámicas contra la base de datos SQLite.

    ### La carpeta shared

    - La carpeta **files**: Contiene los archivos creados por la aplicación del agente.
    - La carpeta **fonts**: Contiene las fuentes multilingües utilizadas por el Intérprete de Código.
    - La carpeta **instructions**: Contiene las instrucciones pasadas al LLM.

    ![Estructura de carpetas del laboratorio](../media/project-structure-self-guided-csharp.png)

## Consejos Pro

!!! tips
    1. El **Menú de Hamburguesa** en el panel derecho del entorno de laboratorio ofrece características adicionales, incluyendo la **Vista de Ventana Dividida** y la opción de finalizar el laboratorio. La **Vista de Ventana Dividida** te permite maximizar el entorno de laboratorio a pantalla completa, optimizando el espacio de pantalla. El panel de **Instrucciones** y **Recursos** del laboratorio se abrirá en una ventana separada.
    2. Si las instrucciones del laboratorio son lentas para desplazarse en el entorno de laboratorio, intenta copiar la URL de las instrucciones y abrirla en **el navegador local de tu computadora** para una experiencia más fluida.
    3. Si tienes problemas para ver una imagen, simplemente **haz clic en la imagen para ampliarla**.

*Traducido usando GitHub Copilot y GPT-4o.*
