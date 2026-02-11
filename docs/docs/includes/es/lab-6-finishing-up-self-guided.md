Eso es todo para la parte de laboratorio de este taller. Continúa leyendo para conocer los puntos clave y recursos adicionales, pero primero vamos a limpiar.

## Limpiar GitHub CodeSpaces

### Guardar tus cambios en GitHub 

Puedes guardar cualquier cambio que hayas hecho a los archivos durante el taller en tu repositorio personal de GitHub como un fork. Esto facilita volver a ejecutar el taller con tus personalizaciones, y el contenido del taller siempre permanecerá disponible en tu cuenta de GitHub.

* En VS Code, haz clic en la herramienta "Control de Código Fuente" en el panel izquierdo. Es la tercera hacia abajo, o puedes usar el atajo de teclado <kbd>Control-Shift-G</kbd>.
* En el campo bajo "Control de Código Fuente" ingresa `Laboratorio de Agentes` y haz clic en **✔️Confirmar**.
  * Haz clic en **Sí** al aviso "No hay cambios en etapa para confirmar."
* Haz clic en **Sincronizar Cambios**.
  * Haz clic en **OK** al aviso "Esta acción extraerá y enviará confirmaciones desde y hacia origin/main".

Ahora tienes tu propia copia del taller con tus personalizaciones en tu cuenta de GitHub.

### Eliminar tu codespace de GitHub

Tu GitHub CodeSpace se cerrará por sí mismo, pero consumirá una pequeña cantidad de tu asignación de cómputo y almacenamiento hasta que sea eliminado. (Puedes ver tu uso en tu [resumen de facturación de GitHub](https://github.com/settings/billing/summary).) Puedes eliminar el codespace de forma segura ahora, como sigue:

* Visita [github.com/codespaces](https://github.com/codespaces){:target="_blank"}
* En la parte inferior de la página, haz clic en el menú "..." a la derecha de tu codespace activo
* Haz clic en **Eliminar**
  * En el aviso "¿Estás seguro?", haz clic en **Eliminar**.

## Eliminar tus recursos de Azure

La mayoría de los recursos que creaste en este laboratorio son recursos de pago por uso, lo que significa que no se te cobrará más por usarlos. Sin embargo, algunos servicios de almacenamiento utilizados por AI Foundry pueden incurrir en pequeños cargos continuos. Para eliminar todos los recursos, sigue estos pasos:

* Visita el [Portal de Azure](https://portal.azure.com){:target="_blank"}
* Haz clic en **Grupos de recursos**
* Haz clic en tu grupo de recursos `rg-zava-agent-wks-****`
* Haz clic en **Eliminar grupo de recursos**
* En el campo en la parte inferior "Ingresa el nombre del grupo de recursos para confirmar la eliminación" ingresa `rg-zava-agent-wks-****`
* Haz clic en **Eliminar**
  * En el aviso de Confirmación de Eliminación, haz clic en "Eliminar"

*Traducido usando GitHub Copilot.*