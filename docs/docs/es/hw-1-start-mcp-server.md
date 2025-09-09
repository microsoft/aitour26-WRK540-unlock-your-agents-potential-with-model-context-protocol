## Lo que Aprenderás

En este laboratorio, harás lo siguiente:

- Usar DevTunnel para hacer tu servidor MCP local accesible a servicios de agente basados en la nube
- Configurar tu entorno para experimentación práctica con el Protocolo de Contexto de Modelo

## Introducción

El servidor del Protocolo de Contexto de Modelo (MCP) es un componente crucial que maneja la comunicación entre Modelos de Lenguaje Grandes (LLMs) y herramientas y fuentes de datos externas. Ejecutarás el servidor MCP en tu máquina local, pero el Servicio de Agentes de Azure AI Foundry requiere acceso a internet para conectarse a él. Para hacer tu servidor MCP local accesible desde internet, usarás un DevTunnel. Esto permite al Servicio de Agentes comunicarse con tu servidor MCP como si estuviera ejecutándose como un servicio en Azure.

## Opciones de interfaz para MCP

MCP soporta dos interfaces principales para conectar LLMs con herramientas:

- **Transporte HTTP Transmisible**: Para APIs y servicios basados en web.
- **Transporte Stdio**: Para scripts locales y herramientas de línea de comandos.

Este laboratorio usa la interfaz de transporte HTTP Transmisible para integrarse con el Servicio de Agentes de Azure AI Foundry.

!!! note
    Normalmente, desplegarías el servidor MCP en un entorno de producción, pero para este taller, lo ejecutarás localmente en tu entorno de desarrollo. Esto te permite probar e interactuar con las herramientas MCP sin necesidad de un despliegue completo.

### Iniciar un DevTunnel para el Servidor MCP

1. En un nuevo terminal, autentica DevTunnel. Se te pedirá que inicies sesión con tu cuenta de Azure, usa la misma cuenta que usaste para iniciar sesión en el Servicio de Agentes de Azure AI Foundry o el Portal de Azure. Ejecuta el siguiente comando:

    ```bash
    devtunnel login
    ```

2. A continuación, en el terminal donde se ejecuta el servidor MCP, inicia un DevTunnel ejecutando:

    ```bash
    devtunnel host -p 8000 --allow-anonymous
    ```

    Esto generará una URL que necesitarás para que el agente se conecte al servidor MCP. La salida será similar a:

    ```text
    Hosting port: 8000
    Connect via browser: https://<tunnel-id>-8000.aue.devtunnels.ms
    Inspect network activity: https://<tunnel-id>-8000-inspect.aue.devtunnels.ms
    ```

## Actualizar la Variable de Entorno DevTunnel

1. Copia la URL **Connect via browser** al portapapeles - la necesitarás en el próximo laboratorio para configurar el agente.
2. Abre el archivo `.env` en la carpeta workshop.
3. Actualiza la variable `DEV_TUNNEL_URL` con la URL copiada.

    ```text
    DEV_TUNNEL_URL=https://<tunnel-id>-8000.aue.devtunnels.ms
    ```

## Iniciar la Aplicación del Agente

1. Copia el texto de abajo al portapapeles:

    ```text
    Debug: Select and Start Debugging
    ```

2. Presiona <kbd>F1</kbd> para abrir la Paleta de Comandos de VS Code.
3. Pega el texto en la Paleta de Comandos y selecciona **Debug: Select and Start Debugging**.
4. Selecciona **🌎🤖Debug Compound: Agent and MCP (http)** de la lista. Esto iniciará la aplicación del agente y el cliente de chat web.

## Iniciar una conversación con el Agente

Cambia a la pestaña **Web Chat** en tu navegador. Deberías ver la aplicación del agente ejecutándose y lista para aceptar preguntas.

### Depuración con DevTunnel

Puedes usar DevTunnel para depurar el servidor MCP y la aplicación del agente. Esto te permite inspeccionar la actividad de la red y solucionar problemas en tiempo real.

1. Selecciona la URL **Inspect network activity** de la salida de DevTunnel.
2. Esto abrirá una nueva pestaña en tu navegador donde puedes ver la actividad de red del servidor MCP y la aplicación del agente.
3. Puedes usar esto para depurar cualquier problema que surja durante el taller.

También puedes establecer puntos de interrupción en el código del servidor MCP y el código de la aplicación del agente para depurar problemas específicos. Para hacer esto:

1. Abre el archivo `sales_analysis.py` en la carpeta `mcp_server`.
2. Establece un punto de interrupción haciendo clic en el margen junto al número de línea donde quieres pausar la ejecución.
3. Cuando la ejecución llegue al punto de interrupción, puedes inspeccionar variables, recorrer el código y evaluar expresiones en la Consola de Depuración.

*Traducido usando GitHub Copilot.*
