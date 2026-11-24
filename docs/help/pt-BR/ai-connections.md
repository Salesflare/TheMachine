---
title: Conectar outras IAs
area: connections
summary: Deixe Claude, ChatGPT, Cursor, Codex ou GBrain ler suas tarefas e seu Graph. Com **Ler e editar**, elas também podem fazer alterações que você pode desfazer.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: cf0776c294917228
---
## O que outra IA pode fazer

Claude, ChatGPT, Cursor, Codex, GBrain e outras IAs podem se conectar à sua Machine. Elas podem ler suas tarefas, promessas, resumos da equipe e as pessoas e empresas do seu Graph.

Com **Ler e editar**, elas também podem adicionar uma tarefa ou um rascunho de e-mail e atualizar seu Graph: salvar uma informação, corrigir detalhes, campos e tags ou adicionar uma linha ao resumo de uma pessoa.

Cada alteração aparece em **Atividade** com a opção **Desfazer**. Elas nunca mesclam, excluem ou compartilham registros. O que salvam recebe a marca **AI:** com o nome da IA, e sua Machine trata isso como uma afirmação dela, nunca como uma instrução sua.

Um rascunho fica aguardando até você ler e pressionar Enviar. Uma IA conectada nunca envia nada nem age por você.

Um rascunho com algo que falta preencher, um arquivo mencionado que não está anexado ou apenas seu próprio endereço volta para a IA corrigir primeiro. Se uma IA pedir a mesma tarefa ou o mesmo rascunho duas vezes seguidas, você recebe só um.

## Conectar uma IA

Abra **Configurações**, **Apps**. Abaixo de **Os apps da The Machine**, aparecem **Adicionar no ChatGPT** e **Adicionar no Claude**. Em **Ou adicione por endereço**, ficam o endereço oficial do app, `https://mcp.themachine.computer/mcp`, que serve para todas as Machines, e **Seu endereço**, `https://<your name>.mcp.themachine.computer/mcp`, cada um com a opção **Copiar**.

Em uma Machine no seu próprio computador, pressione **Configurar**, em **Criar seu endereço**, primeiro. Uma página da sua conta será aberta: confira se o código é o mesmo, confirme e escolha um nome. Sua Machine faz o pareamento automaticamente, sem reiniciar. As duas formas precisam disso.

Sua Machine configura automaticamente o próprio endereço seguro. Isso leva alguns minutos.

Para Claude, pressione **Adicionar no Claude** ou abra [The Machine no diretório do Claude](https://claude.ai/directory/the-machine) e pressione Connect. Nos planos Team e Enterprise, alguém com perfil de proprietário precisa adicioná-la nas configurações da organização.

Para usar um endereço no Claude, em vez disso, abra Customize, Connectors, pressione + Add e depois Add custom connector. Dê o nome The Machine, cole o endereço, pressione Continue e depois Add.

Para ChatGPT, pressione **Adicionar no ChatGPT** ou abra [The Machine no ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4), depois pressione Install plugin. Nos planos Business e Enterprise, talvez um administrador precise permitir o acesso primeiro.

O app oficial se conecta a uma Machine hospedada e também a uma Machine no seu próprio computador, depois que ela tiver um endereço.

Para usar seu endereço privado ou uma Machine fora da Network, adicione um servidor MCP personalizado no ChatGPT: abra chatgpt.com/plugins, pressione + e depois Add custom MCP server. Dê o nome The Machine, cole o endereço e escolha OAuth. Confirme o aviso e pressione Create as a plugin. Seu plano ou espaço de trabalho precisa permitir servidores MCP personalizados.

Com o app oficial, a IA pede para você entrar com sua conta da The Machine. Se você tiver mais de uma Machine, escolha esta e aprove o acesso na página da própria Machine. Com o endereço privado, a IA se conecta diretamente à sua Machine.

IAs em um dispositivo da sua rede privada (Tailscale), como Claude Code ou Cursor, também podem usar o endereço do seu painel seguido de `/mcp`. **Desfazer o pareamento desta Machine**, no fim de **Configurações**, **Conta**, remove uma Machine do seu próprio computador da sua conta.

Sua Machine mostra qual IA está fazendo a solicitação. Se não conseguir identificá-la, mostra a origem da solicitação: conecte apenas se tiver acabado de iniciar esse processo.

Escolha o que ela pode fazer: **Ler** ou **Ler e editar**. Se você tiver contas Work e Personal, escolha o que ela pode ver. Depois, escolha por quanto tempo: **1 dia**, **7 dias**, **30 dias** ou **1 ano**. Pressione **Conectar** ou **Cancelar** para encerrar sem conectar.

## App oficial ou endereço privado

O app oficial é o jeito mais fácil: um endereço para todos, e sua conta encontra sua Machine. Nossa nuvem encaminha as solicitações e nunca armazena o conteúdo delas.

Com seu endereço privado, tudo é criptografado até chegar à sua Machine. A nuvem apenas encaminha o conteúdo e não consegue lê-lo.

De qualquer forma, quem decide é sua Machine. Só uma IA que você aprovou na página dela consegue entrar, com o acesso que você escolheu. Em **Configurações**, **Apps**, uma IA conectada pelo app oficial aparece como **App oficial**.

## O que ela vê

Uma conexão só vê a área autorizada. Work inclui as tarefas e promessas das suas contas de trabalho, pessoas, empresas e projetos de trabalho, além do resumo da equipe do seu Fleet de Trabalho. Personal inclui o restante. O texto das mensagens fica na sua Machine, a menos que você ative **Mensagens**. Sem essa opção, uma IA vê as fontes de uma tarefa apenas pelo remetente, assunto e data.

Os registros do Team Graph dos seus colegas nunca são enviados para uma IA externa.

## Mensagens

**Mensagens** permite que uma IA pesquise e leia seus e-mails, mensagens do Slack e do WhatsApp e outras conversas. A opção fica desativada até você ativá-la na página de conexão ou, mais tarde, em **Configurações**, **Apps**. A IA só pode ler: nunca envia, exclui nem marca nada.

Ela só lê mensagens da área autorizada. Algumas mensagens nunca são enviadas: códigos de uso único e links de acesso, mensagens de um quadro ou projeto **Só você**, conversas que a The Machine identificou como confidenciais (negócios, RH, assuntos jurídicos, saúde e dinheiro), conversas que você manteve privadas e mensagens excluídas.

Cada leitura aparece em **Atividade** com a quantidade de mensagens e as conversas consultadas, nunca com o texto. Sua Machine entrega o texto identificado como dado, para que a IA não siga instruções escritas em uma mensagem.

Enquanto **Mensagens** estiver ativada, as alterações no Graph feitas por uma IA com **Ler e editar** aguardam sua aprovação. Pressione **Aplicar** ou **Descartar** na alteração em **Atividade**.

## Nas Configurações

Abra **Configurações**, **Apps** para ver cada IA que se conectou, uma vez, com o nível de acesso, a área, a data de término e o último uso. **Mensagens** pode ser ativada e desativada ali mesmo. Pressione **Mudar** para alterar o acesso, a área ou o período. A próxima solicitação usará as novas opções. **Atividade** mostra todas as solicitações, inclusive as recusadas. **Desativar agora** pausa o acesso: todos os logins são encerrados, mas o histórico continua disponível. **Remover** exclui a conexão e o histórico dela.

Quando você entrar na mesma IA outra vez, a nova aprovação substituirá a anterior.

Uma IA que não consegue entrar sozinha pode usar uma chave. Em **Adicionar uma chave**, dê um nome à chave, escolha o nível de acesso e a duração e pressione **Criar chave**. Copie a chave na hora: ela só aparece uma vez. A IA a envia como `Authorization: Bearer <key>`.

## Mantenha sua conta segura

Todas as solicitações são registradas, inclusive as recusadas. Uma conexão expirada ou desativada é recusada até você alterá-la. Sua Machine guarda apenas uma impressão digital de cada login, então uma cópia desses dados não dá acesso a nada.
