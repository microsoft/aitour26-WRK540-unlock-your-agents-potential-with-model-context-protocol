## Introducción

El rastreo te ayuda a entender y depurar el comportamiento de tu agente mostrando la secuencia de pasos, entradas y salidas durante la ejecución. En Azure AI Foundry, el rastreo te permite observar cómo tu agente procesa solicitudes, llama herramientas y genera respuestas. Puedes usar el portal de Azure AI Foundry o integrarte con OpenTelemetry y Application Insights para recopilar y analizar datos de rastreo, facilitando la solución de problemas y optimización de tu agente.

<!-- ## Ejercicio del Laboratorio

=== "Python"

      1. Abre el archivo `app.py`.
      2. Cambia la variable `AZURE_TELEMETRY_ENABLED` a `True` para habilitar el rastreo:

         ```python
         AZURE_TELEMETRY_ENABLED = True
         ```

        !!! info "Nota"
            Esta configuración habilita la telemetría para tu agente. En la función `initialize` en `app.py`, el cliente de telemetría se configura para enviar datos a Azure Monitor.

            ```python
             if AZURE_TELEMETRY_ENABLED:
                 configure_azure_monitor(connection_string=await self.project_client.telemetry.get_connection_string())
            ```         

=== "C#"

      por definir -->

<!-- ## Ejecutar la Aplicación del Agente

1. Presiona <kbd>F5</kbd> para ejecutar la aplicación.
2. Selecciona **Preview in Editor** para abrir la aplicación del agente en una nueva pestaña del editor.

### Iniciar una Conversación con el Agente

Copia y pega el siguiente prompt en la aplicación del agente para iniciar una conversación:

```plaintext
Write an executive report that analysis the top 5 product categories and compares performance of the online store verses the average for the physical stores.
``` -->

## Ver Rastros

Puedes ver los rastros de la ejecución de tu agente en el portal de Azure AI Foundry o usando OpenTelemetry. Los rastros mostrarán la secuencia de pasos, llamadas de herramientas e intercambio de datos durante la ejecución del agente. Esta información es crucial para depurar y optimizar el rendimiento de tu agente.

### Usando el Portal de Azure AI Foundry

Para ver rastros en el portal de Azure AI Foundry, sigue estos pasos:

1. Navega al portal de [Azure AI Foundry](https://ai.azure.com/).
2. Selecciona tu proyecto.
3. Selecciona la pestaña **Tracing** en el menú de la izquierda.
4. Aquí, puedes ver los rastros generados por tu agente.

   ![](media/ai-foundry-tracing.png)

### Profundizando en los Rastros

1. Es posible que necesites hacer clic en el botón **Refresh** para ver los rastros más recientes ya que los rastros pueden tardar unos momentos en aparecer.
2. Selecciona el rastro llamado `Zava Agent Initialization` para ver los detalles.
   ![](media/ai-foundry-trace-agent-init.png)
3. Selecciona el rastro `create_agent Zava DIY Sales Agent` para ver los detalles del proceso de creación del agente. En la sección `Input & outputs`, verás las instrucciones del Agente.
4. A continuación, selecciona el rastro `Zava Agent Chat Request: Write an executive...` para ver los detalles de la solicitud de chat. En la sección `Input & outputs`, verás la entrada del usuario y la respuesta del agente.

<!-- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/continuous-evaluation-agents -->

*Traducido usando GitHub Copilot.*
