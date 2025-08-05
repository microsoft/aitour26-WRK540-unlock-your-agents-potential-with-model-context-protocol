Isso é tudo para a parte de laboratório deste workshop. Continue lendo para pontos-chave de aprendizado e recursos adicionais, mas primeiro vamos organizar.

## Limpar GitHub CodeSpaces

### Salvar suas mudanças no GitHub 

Você pode salvar quaisquer mudanças que tenha feito em arquivos durante o workshop em seu repositório pessoal do GitHub como um fork. Isso facilita executar novamente o workshop com suas personalizações, e o conteúdo do workshop permanecerá sempre disponível em sua conta GitHub.

* No VS Code, clique na ferramenta "Source Control" no painel esquerdo. É a terceira opção, ou você pode usar o atalho de teclado <kbd>Control-Shift-G</kbd>.
* No campo sob "Source Control" digite `Agents Lab` e clique em **✔️Commit**.
  * Clique **Yes** no prompt "There are no staged changes to commit."
* Clique **Sync Changes**.
  * Clique **OK** no prompt "This action will pull and push commits from and to origin/main".

Agora você tem sua própria cópia do workshop com suas personalizações em sua conta GitHub.

### Deletar seu GitHub codespace

Seu GitHub CodeSpace será encerrado sozinho, mas consumirá uma pequena quantidade de sua cota de computação e armazenamento até ser deletado. (Você pode ver seu uso em seu [resumo de cobrança do GitHub](https://github.com/settings/billing/summary).) Você pode deletar com segurança o codespace agora, da seguinte forma:

* Visite [github.com/codespaces](https://github.com/codespaces){:target="_blank"}
* Na parte inferior da página, clique no menu "..." à direita do seu codespace ativo
* Clique **Delete**
  * No prompt "Are you sure?", clique **Delete**.

## Deletar seus recursos Azure

A maioria dos recursos que você criou neste laboratório são recursos pague-conforme-usa, significando que você não será cobrado mais por usá-los. No entanto, alguns serviços de armazenamento usados pelo AI Foundry podem incorrer em pequenas taxas contínuas. Para deletar todos os recursos, siga estes passos:

* Visite o [Portal Azure](https://portal.azure.com){:target="_blank"}
* Clique **Resource groups**
* Clique no seu grupo de recursos `rg-agent-workshop-****`
* Clique **Delete Resource group**
* No campo na parte inferior "Enter resource group name to confirm deletion" digite `rg-agent-workshop-****`
* Clique **Delete**
  * No prompt de Confirmação de Delete, clique "Delete"

*Traduzido usando GitHub Copilot e GPT-4o.*
