## Abriendo el Espacio de Trabajo del Lenguaje

Hay dos espacios de trabajo en el taller, uno para Python y otro para C#. El espacio de trabajo contiene el código fuente y todos los archivos necesarios para completar los laboratorios para cada lenguaje. Elige el espacio de trabajo que coincida con el lenguaje con el que quieres trabajar.

=== "Python"

    1. Copia el siguiente comando a tu portapapeles:

        ```text
        File: Open Workspace from File...
        ```
    2. Cambia a Visual Studio Code, presiona <kbd>F1</kbd> para abrir la Paleta de Comandos.
    3. Pega el comando en la Paleta de Comandos y selecciona **Open Workspace from File...**.
    4. Copia y pega la siguiente ruta en el selector de archivos y presiona <kbd>Enter</kbd>:

        ```text
        /workspace/.vscode/python-workspace.code-workspace
        ```

    ## Estructura del Proyecto

    Asegúrate de familiarizarte con las **carpetas** y **archivos** clave con los que trabajarás durante el taller.

    ### La carpeta workshop

    - El archivo **app.py**: El punto de entrada para la aplicación, conteniendo su lógica principal.
  
    Nota la variable **INSTRUCTIONS_FILE**—establece qué archivo de instrucciones usa el agente. Actualizarás esta variable en un laboratorio posterior.

    - El archivo **resources.txt**: Contiene los recursos utilizados por la aplicación del agente.
    - El archivo **.env**: Contiene las variables de entorno utilizadas por la aplicación del agente.

    ### La carpeta mcp_server

    - El archivo **sales_analysis.py**: El Servidor MCP con herramientas para análisis de ventas.

    ### La carpeta shared

    - La carpeta **instructions**: Contiene las instrucciones pasadas al LLM.

    ![Estructura de carpetas del laboratorio](media/project-structure-self-guided-python.png)

=== "C#"

    1. En Visual Studio Code, ve a **File** > **Open Workspace from File**.
    2. Reemplaza la ruta predeterminada con la siguiente:

        ```text
        /workspace/.vscode/csharp-workspace.code-workspace
        ```

    3. Selecciona **OK** para abrir el espacio de trabajo.

    ## Estructura del Proyecto

    Asegúrate de familiarizarte con las **carpetas** y **archivos** clave con los que trabajarás durante el taller.

    ### La carpeta workshop

    - Los archivos **Lab1.cs, Lab2.cs, Lab3.cs**: El punto de entrada para cada laboratorio, conteniendo su lógica de agente.
    - El archivo **Program.cs**: El punto de entrada para la aplicación, conteniendo su lógica principal.
    - El archivo **SalesData.cs**: La lógica de función para ejecutar consultas SQL dinámicas contra la base de datos SQLite.

    ### La carpeta shared

    - La carpeta **files**: Contiene los archivos creados por la aplicación del agente.
    - La carpeta **fonts**: Contiene las fuentes multilingües utilizadas por el Intérprete de Código.
    - La carpeta **instructions**: Contiene las instrucciones pasadas al LLM.

    ![Estructura de carpetas del laboratorio](media/project-structure-self-guided-csharp.png)

*Traducido usando GitHub Copilot y GPT-4o.*
