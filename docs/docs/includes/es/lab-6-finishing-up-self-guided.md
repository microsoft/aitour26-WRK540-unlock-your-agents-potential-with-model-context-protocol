Eso es todo para la parte de laboratorio de este taller. Continúa leyendo para conclusiones clave y recursos adicionales, pero primero limpiemos.

## Limpiar GitHub CodeSpaces

### Guardar tus cambios en GitHub

Puedes guardar cualquier cambio que hayas hecho a archivos durante el taller en tu repositorio personal de GitHub como un fork. Esto hace que sea fácil volver a ejecutar el taller con tus personalizaciones, y el contenido del taller siempre permanecerá disponible en tu cuenta de GitHub.

* En VS Code, haz clic en la herramienta "Source Control" en el panel izquierdo. Es la tercera hacia abajo, o puedes usar el atajo de teclado <kbd>Control-Shift-G</kbd>.
* En el campo bajo "Source Control" ingresa `Agents Lab` y haz clic en **✔️Commit**.
  * Haz clic en **Yes** al prompt "There are no staged changes to commit."
* Haz clic en **Sync Changes**.
  * Haz clic en **OK** al prompt "This action will pull and push commits from and to origin/main".

Ahora tienes tu propia copia del taller con tus personalizaciones en tu cuenta de GitHub.

### Eliminar tu codespace de GitHub

Tu GitHub CodeSpace se cerrará por sí mismo, pero consumirá una pequeña cantidad de tu asignación de cómputo y almacenamiento hasta que sea eliminado. (Puedes ver tu uso en tu [resumen de facturación de GitHub](https://github.com/settings/billing/summary).) Puedes eliminar de forma segura el codespace ahora, de la siguiente manera:

* Visita [github.com/codespaces](https://github.com/codespaces){:target="_blank"}
* En la parte inferior de la página, haz clic en el menú "..." a la derecha de tu codespace activo
* Haz clic en **Delete**
  * En el prompt "Are you sure?", haz clic en **Delete**.

## Eliminar tus recursos de Azure

La mayoría de los recursos que creaste en este laboratorio son recursos de pago por uso, lo que significa que no se te cobrará más por usarlos. Sin embargo, algunos servicios de almacenamiento utilizados por AI Foundry pueden incurrir en pequeños cargos continuos. Para eliminar todos los recursos, sigue estos pasos:

* Visita el [Portal de Azure](https://portal.azure.com){:target="_blank"}
* Haz clic en **Resource groups**
* Haz clic en tu grupo de recursos `rg-agent-workshop-****`
* Haz clic en **Delete Resource group**
* En el campo en la parte inferior "Enter resource group name to confirm deletion" ingresa `rg-agent-workshop-****`
* Haz clic en **Delete**
  * En el prompt de Confirmación de Eliminación, haz clic en "Delete"

*Traducido usando GitHub Copilot y GPT-4o.*
