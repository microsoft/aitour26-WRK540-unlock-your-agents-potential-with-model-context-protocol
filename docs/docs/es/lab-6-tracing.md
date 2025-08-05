**POR COMPLETAR: Esta etiqueta llevará al usuario a actualizar el archivo de instrucciones del agente para remover los emojis molestos que el agente usa en sus respuestas.**

## Introducción

El trazado te ayuda a entender y depurar el comportamiento de tu agente mostrando la secuencia de pasos, entradas y salidas durante la ejecución. En Azure AI Foundry, el trazado te permite observar cómo tu agente procesa solicitudes, llama herramientas y genera respuestas. Puedes usar el portal de Azure AI Foundry o integrarte con OpenTelemetry y Application Insights para recolectar y analizar datos de trazado, haciendo más fácil solucionar problemas y optimizar tu agente.

<!-- ## Ejercicio de Laboratorio

=== "Python"

      1. Abre el archivo `app.py`.
      2. Cambia la variable `AZURE_TELEMETRY_ENABLED` a `True` para habilitar el trazado:

         ```python
         AZURE_TELEMETRY_ENABLED = True
         ```

        !!! info "Nota"
            Esta configuración habilita la telemetría para tu agente. In la función `initialize` en `app.py`, el cliente de telemetría se configura para enviar datos a Azure Monitor.

            ```python
             if AZURE_TELEMETRY_ENABLED:
                 configure_azure_monitor(connection_string=await self.project_client.telemetry.get_connection_string())
            ```         

=== "C#"

      por determinar -->

## Ejecutar la Aplicación del Agente

1. Presiona <kbd>F5</kbd> para ejecutar la aplicación.
2. Selecciona **Preview in Editor** para abrir la aplicación del agente en una nueva pestaña del editor.

### Iniciar una Conversación con el Agente

Copia y pega el siguiente prompt en la aplicación del agente para iniciar una conversación:

```plaintext
Escribe un reporte ejecutivo que analice las 5 categorías de productos principales y compare el rendimiento de la tienda en línea versus el promedio para las tiendas físicas.
```

## Ver Trazados

Puedes ver los trazados de la ejecución de tu agente en el portal de Azure AI Foundry o usando OpenTelemetry. Los trazados mostrarán la secuencia de pasos, llamadas de herramientas y datos intercambiados durante la ejecución del agente. Esta información es crucial para depurar y optimizar el rendimiento de tu agente.

### Usando el Portal de Azure AI Foundry

Para ver trazados en el portal de Azure AI Foundry, sigue estos pasos:

1. Navega al portal de **[Azure AI Foundry](https://ai.azure.com/)**.
2. Selecciona tu proyecto.
3. Selecciona la pestaña **Tracing** en el menú de la izquierda.
4. Aquí, puedes ver los trazados generados por tu agente.

   ![](media/ai-foundry-tracing.png)

### Profundizando en los Trazados

1. Puede que necesites hacer clic en el botón **Refresh** para ver los últimos trazados ya que los trazados pueden tomar unos momentos en aparecer.
2. Selecciona el trazado llamado `Zava Agent Initialization` para ver los detalles.
   ![](media/ai-foundry-trace-agent-init.png)
3. Selecciona el trazado `create_agent Zava DIY Sales Agent` para ver los detalles del proceso de creación del agente. En la sección `Input & outputs`, verás las instrucciones del Agente.
4. A continuación, selecciona el trazado `Zava Agent Chat Request: Write an executive...` para ver los detalles de la solicitud de chat. En la sección `Input & outputs`, verás la entrada del usuario y la respuesta del agente.

<!-- https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/continuous-evaluation-agents -->

*Traducido usando GitHub Copilot y GPT-4o.*
