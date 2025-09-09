## Asistentes a Evento de Microsoft

Las instrucciones de esta página asumen que estás asistiendo a un evento y tienes acceso a un entorno de laboratorio preconfigurado. Este entorno proporciona una suscripción de Azure con todas las herramientas y recursos necesarios para completar el taller.

## Introducción

Este taller está diseñado para enseñarte sobre el Servicio de Agentes de IA de Azure y el [SDK](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme?context=%2Fazure%2Fai-services%2Fagents%2Fcontext%2Fcontext){:target="_blank"} asociado. Consta de múltiples laboratorios, cada uno destacando una característica específica del Servicio de Agentes de IA de Azure. Los laboratorios están diseñados para completarse en orden, ya que cada uno se basa en el conocimiento y trabajo del laboratorio anterior.

## Recursos en la Nube del Taller

Los siguientes recursos están aprovisionados previamente en tu suscripción de Azure del laboratorio:

- Un grupo de recursos llamado **rg-zava-agent-wks-nnnnnnnn**
- Un **hub de Azure AI Foundry** llamado **fdy-zava-agent-wks-nnnnnnnn**
- Un **proyecto de Azure AI Foundry** llamado **prj-zava-agent-wks-nnnnnnnn**
- Dos modelos están desplegados: **gpt-4o-mini** y **text-embedding-3-small**. [Ver precios.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="\_blank"}
- Base de datos de Azure Database para PostgreSQL Flexible Server (B1ms Burstable 32GB) llamada **pg-zava-agent-wks-nnnnnnnn**. [Ver precios](https://azure.microsoft.com/pricing/details/postgresql/flexible-server){:target="\_blank"}
- Recurso de Application Insights llamado **appi-zava-agent-wks-nnnnnnnn**. [Ver precios](https://azure.microsoft.com/pricing/calculator/?service=monitor){:target="\_blank"}

## Seleccionar Lenguaje de Programación del Taller

El taller está disponible tanto en Python como en C#. Por favor, asegúrate de seleccionar el lenguaje que se ajuste al aula de laboratorio o preferencia usando las pestañas de selector de lenguaje. Nota, no cambies de lenguaje a mitad del taller.

**Selecciona la pestaña de lenguaje que coincida con tu aula de laboratorio:**

=== "Python"
    El lenguaje predeterminado para el taller está configurado como **Python**.
=== "C#"
    El lenguaje predeterminado para el taller está configurado como **C#**.

    !!! warning "La versión C#/.NET de este taller está en beta y tiene problemas de estabilidad conocidos."

    Asegúrate de leer la sección de [guía de solución de problemas](../../es/dotnet-troubleshooting.md) **ANTES** de comenzar el taller. De lo contrario, selecciona la versión **Python** del taller.

## Autenticarse con Azure

Necesitas autenticarte con Azure para que la aplicación del agente pueda acceder al Servicio de Agentes de IA de Azure y los modelos. Sigue estos pasos:

1. Abre una ventana de terminal. La aplicación de terminal está **anclada** a la barra de tareas de Windows 11.

    ![Abrir la ventana de terminal](../../media/windows-taskbar.png){ width="300" }

2. Ejecuta el siguiente comando para autenticarte con Azure:

    ```powershell
    az login
    ```

    !!! note
        Se te pedirá que abras un enlace del navegador e inicies sesión en tu cuenta de Azure.

        1. Una ventana del navegador se abrirá automáticamente, selecciona **Cuenta de trabajo o escuela** y luego selecciona **Continuar**.
        1. Usa el **Nombre de usuario** y **TAP (Pase de Acceso Temporal)** que se encuentran en la **sección superior** de la pestaña **Recursos** en el entorno de laboratorio.
        1. Selecciona **Sí, todas las aplicaciones**
        1. Selecciona **Terminado**

3. Luego selecciona la suscripción **Predeterminada** desde la línea de comandos, seleccionando **Enter**.

4. Deja la ventana de terminal abierta para los siguientes pasos.

## Autenticarse con el Servicio DevTunnel

DevTunnel permite al Servicio de Agentes de IA de Azure acceder a tu Servidor MCP local durante el taller.

```powershell
devtunnel login
```

!!! note
    Se te pedirá que uses la cuenta que usaste para `az login`. Selecciona la cuenta y continúa.

Deja la ventana de terminal abierta para los siguientes pasos.

## Abrir el Taller

Sigue estos pasos para abrir el taller en Visual Studio Code:

=== "Python"

    El siguiente bloque de comandos actualiza el repositorio del taller, activa el entorno virtual de Python, y abre el proyecto en VS Code.

    Copia y pega el siguiente bloque de comandos en la terminal y presiona **Enter**.

    ```powershell
    ; cd $HOME\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol `
    ; git pull `
    ; .\src\python\workshop\.venv\Scripts\activate `
    ; code .vscode\python-workspace.code-workspace
    ```

    !!! warning "Cuando el proyecto se abra en VS Code, aparecen dos notificaciones en la esquina inferior derecha. Haz clic en ✖ para cerrar ambas notificaciones."

=== "C#"

    === "VS Code"

        1. Abre el taller en Visual Studio Code. Desde la ventana de terminal, ejecuta el siguiente comando:

            ```powershell
            ; cd $HOME\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol `
            ; git pull `
            ;code .vscode\csharp-workspace.code-workspace
            ```

        !!! note "Cuando el proyecto se abra en VS Code, aparecerá una notificación en la esquina inferior derecha para instalar la extensión C#. Haz clic en **Instalar** para instalar la extensión C#, ya que esto proporcionará las características necesarias para el desarrollo en C#."

    === "Visual Studio 2022"

        2. Abre el taller en Visual Studio 2022. Desde la ventana de terminal, ejecuta el siguiente comando:

            ```powershell
            ; git pull `
            ;cd $HOME; start .\aitour26-WRK540-unlock-your-agents-potential-with-model-context-protocol\src\csharp\McpAgentWorkshop.slnx
            ```

            !!! note "Se te puede preguntar con qué programa abrir la solución. Selecciona **Visual Studio 2022**."

## Estructura del Proyecto

=== "Python"

    Asegúrate de familiarizarte con las **subcarpetas** y **archivos** clave con los que trabajarás durante el taller.

    5. El archivo **main.py**: El punto de entrada para la aplicación, conteniendo su lógica principal.
    6. El archivo **sales_data.py**: La lógica de función para ejecutar consultas SQL dinámicas contra la base de datos SQLite.
    7. El archivo **stream_event_handler.py**: Contiene la lógica del manejador de eventos para el streaming de tokens.
    8. La carpeta **shared/files**: Contiene los archivos creados por la aplicación del agente.
    9. La carpeta **shared/instructions**: Contiene las instrucciones pasadas al LLM.

    ![Estructura de carpetas del laboratorio](../../media/project-structure-self-guided-python.png)

=== "C#"

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

## Consejos Pro

!!! tips
    1. El **Menú Hamburguesa** en el panel derecho del entorno de laboratorio ofrece características adicionales, incluyendo la **Vista de Ventana Dividida** y la opción de finalizar el laboratorio. La **Vista de Ventana Dividida** te permite maximizar el entorno de laboratorio a pantalla completa, optimizando el espacio de pantalla. El panel de **Instrucciones** y **Recursos** del laboratorio se abrirá en una ventana separada.
