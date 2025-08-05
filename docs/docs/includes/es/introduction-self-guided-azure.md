## Esperar a que se Complete la Construcción del Codespace

Antes de proceder, asegúrate de que tu Codespace o Dev Container esté completamente construido y listo. Esto puede tomar varios minutos, dependiendo de tu conexión a internet y los recursos que se estén descargando.

## Autenticar con Azure

Autentica con Azure para permitir que la aplicación del agente acceda al Servicio de Agentes de IA de Azure y a los modelos. Sigue estos pasos:

1. Confirma que el entorno del taller esté listo y abierto en VS Code.
2. Desde VS Code, abre una terminal a través de **Terminal** > **New Terminal** en VS Code, luego ejecuta:

    ```shell
    az login --use-device-code
    ```

    !!! note
        Se te pedirá que abras un navegador e inicies sesión en Azure. Copia el código de autenticación y:

        1. Elige tu tipo de cuenta y haz clic en **Siguiente**.
        2. Inicia sesión con tus credenciales de Azure.
        3. Pega el código.
        4. Haz clic en **OK**, luego **Hecho**.

    !!! warning
        Si tienes múltiples inquilinos de Azure, especifica el correcto usando:

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

3. A continuación, selecciona la suscripción apropiada desde la línea de comandos.
4. Deja la ventana de terminal abierta para los siguientes pasos.

## Desplegar los Recursos de Azure

Este despliegue crea los siguientes recursos en tu suscripción de Azure bajo el grupo de recursos **rg-zava-agent-wks-nnnn**:

- Un **hub de Azure AI Foundry** llamado **fdy-zava-agent-wks-nnnn**
- Un **proyecto de Azure AI Foundry** llamado **prj-zava-agent-wks-nnnn**
- Se despliegan dos modelos: **gpt-4o-mini** y **text-embedding-3-small**. [Ver precios.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}

!!! warning "Asegúrate de tener al menos 120K TPM de cuota para el SKU Global Standard gpt-4o-mini, ya que el agente hace llamadas frecuentes al modelo. Verifica tu cuota en el [Centro de Gestión de AI Foundry](https://ai.azure.com/managementCenter/quota){:target="_blank"}."

Hemos proporcionado un script bash para automatizar el despliegue de los recursos requeridos para el taller.

### Despliegue Automatizado

El script `deploy.sh` despliega recursos a la región `westus` por defecto. Para ejecutar el script:

```bash
cd infra && ./deploy.sh
```

<!-- !!! note "En Windows, ejecuta `deploy.ps1` en lugar de `deploy.sh`" -->

### Configuración del Taller

=== "Python"

    #### Configuración de Recursos de Azure

    El script de despliegue genera el archivo **.env**, que contiene los endpoints del proyecto y modelo, nombres de despliegue de modelo y cadena de conexión de Application Insights. El archivo .env se guardará automáticamente en la carpeta `src/python/workshop`.
    
    Tu archivo **.env** se verá similar al siguiente, actualizado con tus valores:

    ```python
    PROJECT_ENDPOINT="<your_project_endpoint>"
    GPT_MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<your_embedding_model_deployment_name>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<your_application_insights_connection_string>"
    DEV_TUNNEL_URL="<your_dev_tunnel_url>"
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
    AZURE_OPENAI_ENDPOINT="<your_azure_openai_endpoint>"
    ```

    #### Nombres de Recursos de Azure

    También encontrarás un archivo llamado `resources.txt` en la carpeta `workshop`. Este archivo contiene los nombres de los recursos de Azure creados durante el despliegue.

    Se verá similar al siguiente:

    ```plaintext
    Recursos de Azure AI Foundry:
    - Nombre del Grupo de Recursos: rg-zava-agent-wks-nnnn
    - Nombre del Proyecto de IA: prj-zava-agent-wks-nnnn
    - Nombre del Recurso de Foundry: fdy-zava-agent-wks-nnnn
    - Nombre de Application Insights: appi-zava-agent-wks-nnnn
    ```

=== "C#"

    El script almacena de forma segura las variables del proyecto usando el Administrador de Secretos para [secretos de desarrollo de ASP.NET Core](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}.

    Puedes ver los secretos ejecutando el siguiente comando después de haber abierto el espacio de trabajo de C# en VS Code:

    ```bash
    dotnet user-secrets list
    ```

*Traducido usando GitHub Copilot y GPT-4o.*
