## Aguarde a Conclusão da Construção do Codespace

Antes de prosseguir, certifique-se de que seu Codespace ou Dev Container esteja totalmente construído e pronto. Isso pode levar vários minutos, dependendo da sua conexão com a internet e dos recursos sendo baixados.

## Autenticar com Azure

Autentique com Azure para permitir que a aplicação do agente acesse o Serviço de Agentes Azure AI e modelos. Siga estes passos:

1. Confirme que o ambiente do workshop está pronto e aberto no VS Code.
2. Do VS Code, abra um terminal via **Terminal** > **New Terminal** no VS Code, depois execute:

    ```shell
    az login --use-device-code
    ```

    !!! note
        Será solicitado que você abra um navegador e faça login no Azure. Copie o código de autenticação e:

        1. Escolha seu tipo de conta e clique em **Next**.
        2. Faça login com suas credenciais Azure.
        3. Cole o código.
        4. Clique em **OK**, depois **Done**.

    !!! warning
        Se você tem múltiplos tenants Azure, especifique o correto usando:

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

3. Em seguida, selecione a assinatura apropriada da linha de comando.
4. Deixe a janela do terminal aberta para os próximos passos.

## Implantar os Recursos Azure

Esta implantação cria os seguintes recursos em sua assinatura Azure sob o grupo de recursos **rg-zava-agent-wks-nnnn**:

- Um **hub Azure AI Foundry** chamado **fdy-zava-agent-wks-nnnn**
- Um **projeto Azure AI Foundry** chamado **prj-zava-agent-wks-nnnn**
- Dois modelos são implantados: **gpt-4o-mini** e **text-embedding-3-small**. [Veja preços.](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}

!!! warning "Certifique-se de ter pelo menos cota de 120K TPM para o SKU Global Standard gpt-4o-mini, pois o agente faz chamadas frequentes ao modelo. Verifique sua cota no [Centro de Gerenciamento AI Foundry](https://ai.azure.com/managementCenter/quota){:target="_blank"}."

Fornecemos um script bash para automatizar a implantação dos recursos necessários para o workshop.

### Implantação Automatizada

O script `deploy.sh` implanta recursos na região `westus` por padrão. Para executar o script:

```bash
cd infra && ./deploy.sh
```

<!-- !!! note "No Windows, execute `deploy.ps1` em vez de `deploy.sh`" -->

### Configuração do Workshop

=== "Python"

    #### Configuração de Recursos Azure

    O script de implantação gera o arquivo **.env**, que contém os endpoints do projeto e modelo, nomes de implantação de modelo e string de conexão do Application Insights. O arquivo .env será automaticamente salvo na pasta `src/python/workshop`. 
    
    Seu arquivo **.env** será similar ao seguinte, atualizado com seus valores:

    ```python
    PROJECT_ENDPOINT="<your_project_endpoint>"
    GPT_MODEL_DEPLOYMENT_NAME="<your_model_deployment_name>"
    EMBEDDING_MODEL_DEPLOYMENT_NAME="<your_embedding_model_deployment_name>"
    APPLICATIONINSIGHTS_CONNECTION_STRING="<your_application_insights_connection_string>"
    DEV_TUNNEL_URL="<your_dev_tunnel_url>"
    AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED="true"
    AZURE_OPENAI_ENDPOINT="<your_azure_openai_endpoint>"
    ```

    #### Nomes de Recursos Azure

    Você também encontrará um arquivo chamado `resources.txt` na pasta `workshop`. Este arquivo contém os nomes dos recursos Azure criados durante a implantação. 

    Será similar ao seguinte:

    ```plaintext
    Azure AI Foundry Resources:
    - Resource Group Name: rg-zava-agent-wks-nnnn
    - AI Project Name: prj-zava-agent-wks-nnnn
    - Foundry Resource Name: fdy-zava-agent-wks-nnnn
    - Application Insights Name: appi-zava-agent-wks-nnnn
    ```


=== "C#"

    O script armazena com segurança variáveis do projeto usando o Secret Manager para [segredos de desenvolvimento ASP.NET Core](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}.

    Você pode visualizar os segredos executando o seguinte comando após ter aberto o workspace C# no VS Code:

    ```bash
    dotnet user-secrets list
    ```

*Traduzido usando GitHub Copilot e GPT-4o.*
