---
title: Conecte outras IAs
area: connections
summary: Deixe Claude, ChatGPT, Cursor, Codex ou GBrain ler suas tarefas e seu Graph. Com **Ler e editar**, elas também podem fazer mudanças que você pode desfazer.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: acdce4a5793f7c67
---
## O que outra IA pode fazer

Claude, ChatGPT, Cursor, Codex, GBrain e outras IAs podem se conectar à sua Machine. Elas podem ler suas tarefas, promessas, resumos da equipe e as pessoas e empresas do seu Graph.

Com **Ler e editar**, elas também podem adicionar uma tarefa ou um rascunho de e-mail e atualizar seu Graph: salvar um fato, corrigir detalhes, campos e tags ou adicionar uma linha ao resumo de alguém.

Cada mudança aparece em **Atividade**, com a opção **Desfazer**. Elas nunca mesclam, excluem nem compartilham registros. O que salvam fica marcado como **IA:** com o nome delas, e sua Machine trata isso como uma afirmação da IA, nunca como uma instrução sua.

Um rascunho fica aguardando até você ler e pressionar Enviar. Uma IA conectada nunca envia nada nem age por você.

Um rascunho que tenha algo para preencher, mencione um arquivo que a IA não tem ou contenha apenas seu próprio endereço é enviado de volta à IA para ser corrigido primeiro. Se uma IA pedir a mesma tarefa ou o mesmo rascunho duas vezes seguidas, você recebe apenas um.

## Conecte uma IA

Abra **Configurações** e **Apps**. Em **Os apps da The Machine**, você encontra **Adicionar no ChatGPT** e **Adicionar no Claude**. Em **Ou adicione por endereço**, ficam o endereço único do app oficial para todas as Machines, `https://mcp.themachine.computer/mcp`, e **Seu endereço**, `https://<your name>.mcp.themachine.computer/mcp`, cada um com a opção **Copiar**.

Em uma Machine no seu próprio computador, pressione **Configurar**, em **Criar seu endereço**, primeiro. Uma página da sua conta será aberta. Confira se o código exibido é o mesmo, confirme e escolha um nome. Sua Machine será pareada automaticamente, sem precisar reiniciar. Isso é necessário das duas formas.

Sua Machine configura automaticamente o endereço seguro. Isso leva alguns minutos.

Para Claude, pressione **Adicionar no Claude** ou abra [The Machine no diretório do Claude](https://claude.ai/directory/the-machine) e pressione Connect. Nos planos Team e Enterprise, alguém com perfil de proprietário precisa adicionar o app nas configurações da organização.

Para usar um endereço no Claude, em vez disso, abra Customize, Connectors, pressione + Add e depois Add custom connector. Dê o nome The Machine, cole o endereço, pressione Continue e depois Add.

Para ChatGPT, pressione **Adicionar no ChatGPT** ou abra [The Machine no ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) e pressione Install plugin. Nos planos Business e Enterprise, talvez um administrador precise permitir o app primeiro.

O app oficial se conecta a uma Machine hospedada e, depois que ela tem um endereço, também a uma Machine no seu próprio computador.

Para usar seu endereço privado ou uma Machine que não esteja na Network, adicione um servidor MCP personalizado no ChatGPT: abra chatgpt.com/plugins, pressione + e depois Add custom MCP server. Dê o nome The Machine, cole o endereço e escolha OAuth. Confirme o aviso e pressione Create as a plugin. Seu plano ou espaço de trabalho precisa permitir servidores MCP personalizados.

Com o app oficial, a IA pede que você entre com sua conta da The Machine. Se tiver mais de uma Machine, escolha esta e aprove o acesso na página da sua Machine. Com o endereço privado, a IA se conecta diretamente à sua Machine.

IAs em um dispositivo da sua rede privada (Tailscale), como Claude Code ou Cursor, também podem usar o endereço do seu painel seguido de `/mcp`. A opção **Desfazer o pareamento desta Machine**, na parte inferior de **Configurações**, em **Conta**, remove do seu pareamento uma Machine no seu próprio computador.

Sua Machine mostra qual IA está fazendo a solicitação. Se não conseguir identificá-la, mostra de onde veio a solicitação. Conecte-se apenas se você acabou de iniciar esse processo.

Escolha o que ela pode fazer: **Ler** ou **Ler e editar**. Se você tiver contas de Trabalho e Pessoal, escolha o que ela pode acessar. Depois, escolha por quanto tempo: **1 dia**, **7 dias**, **30 dias** ou **1 ano**. Pressione **Conectar** ou **Cancelar** para recusar a solicitação sem conceder acesso.

## App oficial ou endereço privado

O app oficial é a opção mais simples: um único endereço para todos, e sua conta encontra sua Machine. Nossa nuvem encaminha as solicitações e nunca armazena o conteúdo delas.

Com seu endereço privado, tudo é criptografado até chegar à sua Machine. A nuvem apenas encaminha as solicitações e não consegue lê-las.

De qualquer forma, quem decide é sua Machine. Só uma IA que você aprovou na página dela consegue entrar, com o acesso que você escolheu. Em **Configurações**, **Apps**, uma IA conectada pelo app oficial aparece com o rótulo **App oficial**.

## O que ela vê

Uma conexão só acessa a área dela. Trabalho inclui as tarefas e promessas das suas contas de trabalho, as pessoas, empresas e projetos de trabalho, além do resumo da equipe do seu Fleet de Trabalho. Pessoal inclui o restante. O conteúdo das mensagens fica na sua Machine, a menos que você ative **Mensagens**. Sem essa opção, uma IA só vê o remetente, o assunto e a data das mensagens relacionadas a uma tarefa.

Os registros do Graph da equipe dos seus colegas nunca são enviados a uma IA externa.

## Mensagens

**Mensagens** permite que uma IA pesquise e leia seus e-mails, mensagens do Slack, WhatsApp e outros chats. Essa opção fica desativada até você ativá-la na página de conexão ou depois em **Configurações**, **Apps**. Ela só lê: nunca envia, exclui nem marca nada.

Ela só lê mensagens da área dela. Alguns tipos de mensagem nunca são enviados: códigos de uso único e links de acesso, mensagens de um quadro ou projeto **Só você**, conversas que a The Machine identificou como sensíveis (negócios, RH, jurídico, saúde, dinheiro), conversas que você manteve privadas e mensagens excluídas.

Cada leitura aparece em **Atividade**, com a quantidade de mensagens e as conversas acessadas, mas sem o conteúdo. Sua Machine entrega o conteúdo marcado como dado, para que a IA não siga instruções escritas em uma mensagem.

Enquanto Mensagens estiver ativado, as mudanças no Graph feitas por uma IA com **Ler e editar** ficam aguardando sua aprovação. Pressione **Aplicar** ou **Descartar** na mudança em **Atividade**.

## Nas Configurações

Abra **Configurações** e **Apps** para ver cada IA que se conectou, uma única vez, com o acesso, a área, a data de término e o último uso. Você pode ativar ou desativar **Mensagens** nessa mesma tela. Pressione **Mudar** para alterar o acesso, a área ou o período de validade. A próxima chamada usará as novas configurações. **Atividade** mostra todas as chamadas, inclusive as recusadas. **Desativar agora** interrompe o acesso: todas as sessões são encerradas, mas o histórico é mantido. **Remover** revoga o acesso e apaga o histórico.

Quando você entra novamente na mesma IA, a nova aprovação substitui a anterior. Se essa IA já estava conectada em algum lugar, ela continua conectada com o novo acesso. Uma IA que você usa permanece conectada até a data de término. Se ficar sem uso por 90 dias, ela pedirá que você entre novamente.

Uma IA que não consegue entrar sozinha pode usar uma chave. Em **Adicionar uma chave**, dê um nome, escolha o acesso e o período de validade e pressione **Criar chave**. Copie a chave na hora: ela só aparece uma vez. A IA a envia como `Authorization: Bearer <key>`.

## Mantenha tudo seguro

Todas as chamadas são registradas, inclusive as recusadas. Uma conexão expirada ou desativada é recusada até você alterá-la. Sua Machine guarda apenas uma impressão digital de cada sessão, então uma cópia dos dados não permite acessar nada.
