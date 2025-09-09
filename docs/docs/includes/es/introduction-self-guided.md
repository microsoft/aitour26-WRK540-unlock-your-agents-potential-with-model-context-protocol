## Estudiantes Autoguiados

Estas instrucciones son para estudiantes autoguiados que no tienen acceso a un entorno de laboratorio preconfigurado. Sigue estos pasos para configurar tu entorno y comenzar el taller.

## Introducción

Este taller está diseñado para enseñarte sobre el Servicio de Agentes de IA de Azure y el SDK asociado. Consta de múltiples laboratorios, cada uno destacando una característica específica del Servicio de Agentes de IA de Azure. Los laboratorios están diseñados para completarse en orden, ya que cada uno se basa en el conocimiento y trabajo del laboratorio anterior.

## Prerrequisitos

1. Acceso a una suscripción de Azure. Si no tienes una suscripción de Azure, crea una [cuenta gratuita](https://azure.microsoft.com/free/){:target="_blank"} antes de comenzar.
1. Necesitas una cuenta de GitHub. Si no tienes una, créala en [GitHub](https://github.com/join){:target="_blank"}.

## Seleccionar Lenguaje de Programación del Taller

El taller está disponible tanto en Python como en C#. Usa las pestañas de selector de lenguaje para elegir tu lenguaje preferido. Nota, no cambies de lenguaje a mitad del taller.

**Selecciona la pestaña para tu lenguaje preferido:**

=== "Python"
    El lenguaje predeterminado para el taller está configurado como **Python**.
=== "C#"
    El lenguaje predeterminado para el taller está configurado como **C#**.

    !!! warning "La versión C#/.NET de este taller está en beta y tiene problemas de estabilidad conocidos."

    Asegúrate de leer la sección de [guía de solución de problemas](../../es/dotnet-troubleshooting.md) **ANTES** de comenzar el taller. De lo contrario, selecciona la versión **Python** del taller.

## Abrir el Taller

Preferido: **GitHub Codespaces**, que proporciona un entorno preconfigurado con todas las herramientas requeridas. Alternativamente, ejecuta localmente con un **Dev Container** de Visual Studio Code y **Docker**. Usa las pestañas abajo para elegir.

!!! Tip
    Las construcciones de Codespaces o Dev Container toman alrededor de 5 minutos. Inicia la construcción, luego **continúa leyendo** mientras se completa.

=== "GitHub Codespaces"

    Selecciona **Abrir en GitHub Codespaces** para abrir el proyecto en GitHub Codespaces.

    [![Abrir en GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol){:target="_blank"}

=== "VS Code Dev Container"

    1. Asegúrate de tener lo siguiente instalado en tu máquina local:

        - [Docker](https://docs.docker.com/get-docker/){:target="\_blank"}
        - [Visual Studio Code](https://code.visualstudio.com/download){:target="\_blank"}
        - La [extensión Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers){:target="\_blank"}
    1. Clona el repositorio a tu máquina local:

        ```bash
        git clone https://github.com/microsoft/aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol.git
        ```

    1. Abre el repositorio clonado en Visual Studio Code.
    1. Cuando se te solicite, selecciona **Reabrir en Contenedor** para abrir el proyecto en un Dev Container.

---

## Autenticar Servicios de Azure

!!! danger
Antes de continuar, asegúrate de que tu Codespace o Dev Container esté completamente construido y listo.

### Autenticarse con DevTunnel

DevTunnel proporciona un servicio de reenvío de puertos que se utilizará en el taller para permitir que el Servicio de Agentes de IA de Azure acceda al Servidor MCP que estarás ejecutando en tu entorno de desarrollo local. Sigue estos pasos para autenticarte:

1. Desde VS Code, **presiona** <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>`</kbd> para abrir una nueva ventana de terminal. Luego ejecuta el siguiente comando:
1. **Ejecuta el siguiente comando** para autenticarte con DevTunnel:

   ```shell
   devtunnel login
   ```

1. Sigue estos pasos para autenticarte:

   1. Copia el **Código de Autenticación** al portapapeles.
   2. **Mantén presionada** la tecla <kbd>ctrl</kbd> o <kbd>cmd</kbd>.
   3. **Selecciona** la URL de autenticación para abrirla en tu navegador.
   4. **Pega** el código y haz clic en **Siguiente**.
   5. **Elige una cuenta** e inicia sesión.
   6. Selecciona **Continuar**
   7. **Regresa** a la ventana de terminal en VS Code.

1. Deja la ventana de terminal **abierta** para los siguientes pasos.

### Autenticarse con Azure

Autentica con Azure para permitir que la aplicación del agente acceda al Servicio de Agentes de IA de Azure y los modelos. Sigue estos pasos:

1. Luego ejecuta el siguiente comando:

    ```shell
    az login --use-device-code
    ```

    !!! warning
    Si tienes múltiples inquilinos de Azure, especifica el correcto usando:

    ```shell
    az login --use-device-code --tenant <tenant_id>
    ```

2. Sigue estos pasos para autenticarte:

    1. **Copia** el **Código de Autenticación** al portapapeles.
    2. **Mantén presionada** la tecla <kbd>ctrl</kbd> o <kbd>cmd</kbd>.
    3. **Selecciona** la URL de autenticación para abrirla en tu navegador.
    4. **Pega** el código y haz clic en **Siguiente**.
    5. **Elige una cuenta** e inicia sesión.
    6. Selecciona **Continuar**
    7. **Regresa** a la ventana de terminal en VS Code.
    8. Si se te solicita, **selecciona** una suscripción.

3. Deja la ventana de terminal abierta para los siguientes pasos.

---

## Desplegar los Recursos de Azure

Este despliegue crea los siguientes recursos en tu suscripción de Azure.

- Un grupo de recursos llamado **rg-zava-agent-wks-nnnnnnnn**
- Un **hub de Azure AI Foundry** llamado **fdy-zava-agent-wks-nnnnnnnn**
- Un **proyecto de Azure AI Foundry** llamado **prj-zava-agent-wks-nnnnnnnn**
- Dos modelos están desplegados: **gpt-4o-mini** y **text-embedding-3-small**. [Ver precios.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="\_blank"}
- Recurso de Application Insights llamado **appi-zava-agent-wks-nnnnnnnn**. [Ver precios](https://azure.microsoft.com/pricing/calculator/?service=monitor){:target="\_blank"}
- Para mantener los costos del taller bajos, PostgreSQL se ejecuta en un contenedor local dentro de tu Codespace o Dev Container en lugar de como un servicio en la nube. Ve [Azure Database para PostgreSQL Flexible Server](https://azure.microsoft.com/es-es/products/postgresql){:target="\_blank"} para aprender sobre las opciones para un servicio PostgreSQL gestionado.

!!! warning "Asegúrate de tener al menos las siguientes cuotas de modelo" - 120K TPM de cuota para el SKU Global Standard de gpt-4o-mini, ya que el agente hace llamadas frecuentes al modelo. - 50K TPM para el modelo text-embedding-3-small SKU Global Standard. - Verifica tu cuota en el [Centro de Gestión de AI Foundry](https://ai.azure.com/managementCenter/quota){:target="\_blank"}."

### Despliegue Automatizado

Ejecuta el siguiente script bash para automatizar el despliegue de los recursos requeridos para el taller. El script `deploy.sh` despliega recursos en la región `westus` por defecto. Para ejecutar el script:

```bash
cd infra && ./deploy.sh
```

### Configuración del Taller

=== "Python"

    #### Configuración de Recursos de Azure

    El script de despliegue genera el archivo **.env**, que contiene los endpoints del proyecto y modelo, nombres de despliegue de modelo, y cadena de conexión de Application Insights. El archivo .env se guardará automáticamente en la carpeta `src/python/workshop`.

    Tu archivo **.env** se verá similar a lo siguiente, actualizado con tus valores:

    ```python
    PROJECT_ENDPOINT="<tu_endpoint_de_proyecto>"
    GPT_MODEL_DEPLOYMENT_NAME="<tu_nombre_de_despliegue_de_modelo>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<tu_nombre_de_despliegue_de_modelo_embedding>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<tu_cadena_de_conexion_application_insights>"
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
    AZURE_OPENAI_ENDPOINT="<tu_endpoint_azure_openai>"
    ```

    #### Nombres de Recursos de Azure

    También encontrarás un archivo llamado `resources.txt` en la carpeta `workshop`. Este archivo contiene los nombres de los recursos de Azure creados durante el despliegue.

    Se verá similar a lo siguiente:

    ```plaintext
    Recursos de Azure AI Foundry:
    - Nombre del Grupo de Recursos: rg-zava-agent-wks-nnnnnnnn
    - Nombre del Proyecto AI: prj-zava-agent-wks-nnnnnnnn
    - Nombre del Recurso Foundry: fdy-zava-agent-wks-nnnnnnnn
    - Nombre de Application Insights: appi-zava-agent-wks-nnnnnnnn
    ```

=== "C#"

    El script almacena variables de proyecto de manera segura usando el Secret Manager para [secretos de desarrollo de ASP.NET Core](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}.

    Puedes ver los secretos ejecutando el siguiente comando después de haber abierto el espacio de trabajo de C# en VS Code:

    ```bash
    dotnet user-secrets list
    ```

---

## Abrir el Espacio de Trabajo de VS Code

Hay dos espacios de trabajo de VS Code en el taller, uno para Python y uno para C#. El espacio de trabajo contiene el código fuente y todos los archivos necesarios para completar los laboratorios para cada lenguaje. Elige el espacio de trabajo que coincida con el lenguaje con el que quieres trabajar.

=== "Python"

    1. **Copia** la siguiente ruta al portapapeles:

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```
    1. Desde el menú de VS Code, selecciona **Archivo** luego **Abrir Espacio de Trabajo desde Archivo**.
    3. Reemplaza y **pega** el nombre de ruta copiado y selecciona **OK**.


    ## Estructura del Proyecto

    Familiarízate con las **carpetas** y **archivos** clave en el espacio de trabajo con los que trabajarás durante el taller.

    ### La carpeta "workshop"

    - El archivo **app.py**: El punto de entrada para la aplicación, conteniendo su lógica principal.

    Nota la variable **INSTRUCTIONS_FILE**—establece qué archivo de instrucciones usa el agente. Actualizarás esta variable en un laboratorio posterior.

    - El archivo **resources.txt**: Contiene los recursos utilizados por la aplicación del agente.
    - El archivo **.env**: Contiene las variables de entorno utilizadas por la aplicación del agente.

    ### La carpeta "mcp_server"

    - El archivo **sales_analysis.py**: El Servidor MCP con herramientas para análisis de ventas.

    ### La carpeta "shared/instructions"

    - La carpeta **instructions**: Contiene las instrucciones pasadas al LLM.

    ![Estructura de carpetas del laboratorio](../../media/project-structure-self-guided-python.png)

=== "C#"

    1. En Visual Studio Code, ve a **Archivo** > **Abrir Espacio de Trabajo desde Archivo**.
    2. Reemplaza la ruta predeterminada con la siguiente:

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. Selecciona **OK** para abrir el espacio de trabajo.

    ## Estructura del Proyecto

    El proyecto usa [Aspire](http://aka.ms/dotnet-aspire) para simplificar la construcción de la aplicación del agente, gestionar el servidor MCP, y orquestar todas las dependencias externas. La solución está compuesta por cuatro proyectos, todos con el prefijo `McpAgentWorkshop`:

    * `AppHost`: El orquestador de Aspire, y proyecto de lanzamiento para el taller.
    * `McpServer`: El proyecto del servidor MCP.
    * `ServiceDefaults`: Configuración predeterminada para servicios, como logging y telemetría.
    * `WorkshopApi`: La API del Agente para el taller. La lógica central de la aplicación está en la clase `AgentService`.

    Además de los proyectos .NET en la solución, hay una carpeta `shared` (visible como una Carpeta de Solución, y a través del explorador de archivos), que contiene:

    * `instructions`: Las instrucciones pasadas al LLM.
    * `scripts`: Scripts de shell auxiliares para varias tareas, estos serán referenciados cuando sea necesario.
    * `webapp`: La aplicación cliente front-end. Nota: Esta es una aplicación Python, que Aspire gestionará el ciclo de vida.

    ![Estructura de carpetas del laboratorio](../../media/project-structure-self-guided-csharp.png)
