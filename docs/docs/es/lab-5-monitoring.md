## Introducción

El monitoreo mantiene tu Servicio de Agentes de Azure AI Foundry disponible, eficiente y confiable. Azure Monitor recopila métricas y registros, proporciona información en tiempo real y envía alertas. Usa paneles de control y alertas personalizadas para rastrear métricas clave, analizar tendencias y responder de forma proactiva. Accede al monitoreo a través del portal de Azure, CLI, API REST o bibliotecas de cliente.

## Ejercicio del Laboratorio

1. Desde el explorador de archivos de VS Code, abre el archivo `resources.txt` en la carpeta `workshop`.
2. **Copia** el valor para la clave `AI Project Name` al portapapeles.
3. Navega a la página del [Portal de Azure AI Foundry](https://ai.azure.com){:target="_blank"}.
4. Selecciona tu proyecto de la lista de proyectos foundry.

## Abrir el panel de Monitoreo

1. Desde el `resources.txt`, copia el valor para `Application Insights Name` al portapapeles.
2. Regresa al portal de AI Foundry, selecciona la sección **Monitoring** en el menú de la izquierda.
3. Pega el `Application Insights Name` copiado en la lista desplegable `Application Insights resource name`.
4. Selecciona el recurso **Application Insights** de la lista desplegable.
5. Selecciona **Connect**.

### Explorar el panel de Monitoreo

Familiarízate con la información disponible en el panel de `Application analytics`.

!!!tip "Puedes seleccionar rangos de fechas para filtrar los datos mostrados en las herramientas de monitoreo."

![La imagen muestra el panel de monitoreo de aplicaciones](../media/monitor_usage.png)

### Monitorear el Uso de Recursos

Puedes profundizar más, selecciona `Resource Usage` para ver métricas detalladas sobre el consumo de recursos de tu Proyecto de IA. Nuevamente, puedes filtrar los datos por rango de tiempo.

![La imagen muestra el panel de monitoreo de uso de recursos](../media/monitor_resource_usage.png)

*Traducido usando GitHub Copilot.*
