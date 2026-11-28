---
title: Conectar outras IAs
area: connections
summary: Deixe Claude, ChatGPT, Cursor, Codex ou GBrain ler suas tarefas e seu Graph. Com **Ler e editar**, elas também podem fazer alterações que você pode desfazer.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: 3a7200b2a076c274
---
## O que outra IA pode fazer

Claude, ChatGPT, Cursor, Codex, GBrain e outras IAs podem se conectar à sua Machine. Elas podem ler suas tarefas, promessas, resumos da equipe e as pessoas e empresas do seu Graph.

Com **Ler e editar**, elas também podem adicionar uma tarefa ou um rascunho de e-mail e atualizar seu Graph: salvar um fato, corrigir detalhes, campos e tags ou adicionar uma linha ao resumo de alguém.

Cada alteração aparece em **Atividade**, com a opção **Desfazer**. Elas nunca mesclam, excluem ou compartilham registros. O que salvam fica marcado como **AI:**, com o nome da IA, e sua Machine trata isso como uma afirmação dela, nunca como uma instrução sua.

Um rascunho fica aguardando até você ler e pressionar Enviar por conta própria. Uma IA conectada nunca envia nada nem age em seu nome.

## O que ela aprende com você

Quando um chat começa, a IA recebe um resumo curto: quem você é, suas principais regras e o que mudou desde a última visita. Ela também pode ler o conteúdo de **Aprendizado**: suas regras, fatos gerais e como você escreve em cada canal. Assim, ela escreve como você.

Com **Ler e editar**, ela pode salvar o que vocês definirem no chat. Um fato é salvo na hora, e você pode usar **Desfazer** em **Atividade**. Uma regra orienta o trabalho da sua Machine, então fica em **Aprendizado** até você pressionar **Aprovar** ou **Descartar**. Ela nunca altera seu jeito de escrever.

Um rascunho com algo para preencher, um arquivo mencionado que a IA não tem ou apenas seu próprio endereço como destinatário volta para a IA corrigir primeiro. Se uma IA pedir a mesma tarefa ou o mesmo rascunho duas vezes seguidas, você recebe só um.

## Conectar uma IA

Abra **Configurações**, **Apps**. Abaixo de **Os apps da The Machine**, aparecem **Adicionar no ChatGPT** e **Adicionar no Claude**. Em **Ou adicione por endereço**, você encontra o endereço oficial do app, `https://mcp.themachine.computer/mcp`, válido para todas as Machines, e **Seu endereço**, `https://<your name>.mcp.themachine.computer/mcp`, cada um com a opção **Copiar**.

Se sua Machine estiver no seu próprio computador, primeiro pressione **Configurar**, em **Criar seu endereço**. Uma página da sua conta será aberta: confira se o código exibido é o mesmo, confirme e escolha um nome. Sua Machine será pareada automaticamente, sem reiniciar. Essa etapa é necessária nos dois casos.

Sua Machine configura o endereço seguro automaticamente. Isso leva alguns minutos.

Para usar com Claude, pressione **Adicionar no Claude** ou abra [The Machine no diretório do Claude](https://claude.ai/directory/the-machine) e pressione Connect. Nos planos Team e Enterprise, um proprietário precisa adicioná-lo nas configurações da organização.

A habilidade da The Machine informa ao Claude quando usar sua Machine: primeiro, o resumo; depois, suas regras e seu jeito de escrever, antes de criar qualquer rascunho. Pressione **Baixar**, ao lado de **habilidade do Claude**. No Claude, abra Customize, Skills e faça o upload.

Para usar um endereço no Claude, em vez disso, abra Customize, Connectors, pressione + Add e depois Add custom connector. Dê o nome The Machine, cole o endereço, pressione Continue e depois Add.

Para usar com ChatGPT, pressione **Adicionar no ChatGPT** ou abra [The Machine no ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) e pressione Install plugin. Nos planos Business e Enterprise, talvez um administrador precise permitir o acesso primeiro.

O app oficial se conecta a uma Machine hospedada e também a uma Machine no seu próprio computador, depois que ela tiver um endereço.

Para usar seu endereço privado ou uma Machine que não esteja na Network, adicione um servidor MCP personalizado no ChatGPT: acesse chatgpt.com/plugins, pressione + e depois Add custom MCP server. Dê o nome The Machine, cole o endereço e escolha OAuth. Confirme o aviso e pressione Create as a plugin. Seu plano ou espaço de trabalho precisa permitir servidores MCP personalizados.

No app oficial, a IA pede que você entre com sua conta da The Machine. Se tiver mais de uma Machine, escolha esta e depois aprove o acesso na página da sua Machine. Com o endereço privado, a IA se conecta diretamente à sua Machine.

IAs em um dispositivo da sua rede privada (Tailscale), como Claude Code ou Cursor, também podem usar o endereço do seu painel seguido de `/mcp`. A opção **Desfazer o pareamento desta Machine**, no fim de **Configurações**, **Conta**, desvincula da sua conta uma Machine que esteja no seu próprio computador.

Sua Machine mostra qual IA está fazendo a solicitação. Se não conseguir identificá-la, mostra de onde veio a solicitação. Conecte-se apenas se você acabou de iniciar essa ação.

Escolha o que ela pode fazer: **Ler** ou **Ler e editar**. Se você tiver contas de Trabalho e Pessoal, escolha o que ela pode acessar. Depois, escolha por quanto tempo: **1 dia**, **7 dias**, **30 dias** ou **1 ano**. Pressione **Conectar** ou **Cancelar** para recusar sem conceder acesso.

## App oficial ou endereço privado

O app oficial é a opção mais simples: um endereço para todo mundo, e sua conta encontra sua Machine. Nosso serviço na nuvem encaminha as solicitações e nunca armazena o conteúdo delas.

Com seu endereço privado, tudo é criptografado até chegar à sua Machine. O serviço na nuvem só encaminha as solicitações e não consegue lê-las.

De qualquer forma, quem decide é sua Machine. Só uma IA aprovada na página dela consegue entrar, com o acesso que você escolheu. Em **Configurações**, **Apps**, uma IA conectada pelo app oficial aparece como **App oficial**.

## O que ela pode ver

Uma conexão só acessa a área dela. Trabalho inclui as tarefas e promessas das suas contas de trabalho, pessoas, empresas e projetos de trabalho, além do resumo da equipe da sua Fleet de Trabalho. Pessoal inclui todo o resto. O texto das mensagens fica na sua Machine, a menos que você ative **Mensagens**. Sem essa opção, uma IA só vê o remetente, o assunto e a data das mensagens relacionadas a uma tarefa.

Os registros do Team Graph dos seus colegas nunca são enviados a uma IA externa.

## Mensagens

**Mensagens** permite que uma IA pesquise e leia seus e-mails, mensagens do Slack e WhatsApp e outros chats. A opção fica desativada até você ativá-la, na página de conexão ou depois em **Configurações**, **Apps**. A IA só lê: nunca envia, exclui nem marca nada.

Ela só lê mensagens da área dela. Algumas mensagens nunca são compartilhadas: códigos de uso único e links de acesso, mensagens de um quadro ou projeto **Só você**, conversas que a The Machine identificou como sensíveis (negócios, RH, jurídico, saúde, dinheiro), conversas que você manteve privadas e mensagens excluídas.

Cada leitura aparece em **Atividade**, com a quantidade de mensagens e as conversas acessadas, nunca o texto. Sua Machine entrega o texto identificado como dado, para que a IA não siga instruções escritas em uma mensagem.

Enquanto **Mensagens** estiver ativada, as alterações no Graph feitas por uma IA com **Ler e editar** aguardam sua aprovação. Pressione **Aplicar** ou **Descartar** na alteração em **Atividade**.

## Eventos

**Eventos** permite que uma IA, como o ChatGPT, comece a agir sozinha quando algo acontece: uma nova tarefa, um resumo de reunião para amanhã ou uma promessa que vence amanhã. Cada evento fica desativado até você ativá-lo em **Mudar**. Então, a IA recebe o título e uma breve explicação do motivo, nada que já não pudesse ler, e nunca informações anteriores ao evento.

Ela ainda não pode enviar nada, e as alterações aparecem em **Atividade**, com a opção **Desfazer**. Desativar um evento ou a IA interrompe a execução na hora.

## Nas Configurações

Abra **Configurações**, **Apps** para ver cada IA que se conectou, com o acesso, a área, a data de término e o último uso. Você pode ativar ou desativar **Mensagens** ali mesmo. Pressione **Mudar** para alterar o acesso, a área ou o período de validade. A próxima solicitação usará as novas configurações. **Atividade** mostra todas as solicitações, inclusive as recusadas. **Desativar agora** pausa a IA: todas as sessões são encerradas, mas o histórico é mantido. **Remover** exclui a IA e o histórico dela.

Quando você entra novamente na mesma IA, a nova aprovação substitui a anterior. Se essa IA já tiver uma sessão aberta, ela continua conectada com o novo acesso. Uma IA que você usa continua conectada até a data de término. Se ficar 90 dias sem uso, ela pede que você entre novamente.

Uma IA que não consegue entrar sozinha pode usar uma chave. Em **Adicionar uma chave**, dê um nome, escolha o acesso e o período de validade e pressione **Criar chave**. Copie a chave na hora: ela só aparece uma vez. A IA a envia como `Authorization: Bearer <key>`.

## Mantenha tudo seguro

Todas as solicitações são registradas, inclusive as recusadas. Uma conexão expirada ou desativada é recusada até você alterar as configurações. Sua Machine guarda apenas uma impressão digital de cada sessão, então uma cópia dos dados não permite acessar nada.
