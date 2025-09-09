## Introducción

!!! note "El rastreo con el Panel de Aspire solo está soportado en la versión C# del taller."

Hasta ahora para nuestro rastreo, nos hemos enfocado en cómo visualizar esto a través de los paneles de Azure AI Foundry, lo que puede ser una interrupción en el flujo de trabajo al desarrollar localmente. Además de eso, podemos aprovechar el Panel de Aspire para visualizar los rastros generados por nuestra aplicación en tiempo real, y cómo una acción se extiende a través de múltiples recursos dentro de nuestro sistema.

## Ejecutar la Aplicación del Agente

Lanza la aplicación presionando <kbd>F5</kbd> y espera a que el Panel de Aspire aparezca en tu navegador. Esto mostrará una lista completa de los recursos en el taller.

![Panel de Aspire](../media/lab-7-dashboard.png)

Como en pasos de laboratorio anteriores, abre el **Workshop Frontend** e ingresa un prompt en el chat, como:

```plaintext
Write an executive report that analysis the top 5 product categories and compares performance of the online store verses the average for the physical stores.
```

## Ver Rastros

Para ver los rastros generados por tu aplicación, navega a la pestaña **Traces** en el Panel de Aspire. Aquí, puedes ver una lista de todos los rastros que han sido capturados, comenzando con su originador.

![Vista general de rastros](../media/lab-7-trace-overview.png)

La entrada final en la captura de pantalla anterior muestra el evento del **dotnet-front-end** realizando un `GET` a `/chat/stream`. La columna **Span** luego muestra los recursos que este rastro abarca, `dotnet-front-end`, `dotnet-agent-app`, `ai-foundry`, `dotnet-mcp-server`, y `pg`.

Cada recurso tiene un número asociado con él, que es el número de _spans_ que ocurrieron para ese recurso. También podemos notar un indicador de error en los recursos `dotnet-mcp-server` y `pg`, lo que indicaría que ocurrió un error en esos recursos.

Hacer clic en el rastro te mostrará una vista detallada de la línea de tiempo del rastro:

![Línea de tiempo del rastro](../media/lab-7-trace-timeline.png)

Desde aquí, podemos ver los spans individuales, el orden en que ocurrieron, su duración, y cómo los eventos sucedieron a través de recursos dentro de nuestra aplicación.

Hacer clic en un span individual te mostrará más detalles sobre ese span específico:

![Detalles del span](../media/lab-7-span-details.png)

Intenta experimentar con diferentes prompts y simular errores, para observar cómo cambian los rastros en el Panel de Aspire.

## Lectura Adicional

- [Documentación de Aspire](https://aka.ms/aspire-docs)
- [Documentación de Telemetría de Aspire](https://learn.microsoft.com/dotnet/aspire/fundamentals/telemetry)

*Traducido usando GitHub Copilot.*
