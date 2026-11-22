---
title: Conectar outras IAs
area: connections
summary: Deixe Claude, ChatGPT, Cursor, Codex ou GBrain ler suas tarefas e seu Graph. Com **Ler e editar**, elas também podem fazer alterações que você pode desfazer.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: a8637260c99df309
---
## O que outra IA pode fazer

Claude, ChatGPT, Cursor, Codex, GBrain e outras IAs podem se conectar à sua Machine. Elas podem ler suas tarefas, promessas, resumos da equipe e as pessoas e empresas do seu Graph.

Com **Ler e editar**, elas também podem adicionar uma tarefa ou um rascunho de e-mail e atualizar seu Graph: salvar um fato, corrigir detalhes, campos e tags ou adicionar uma linha ao resumo de alguém.

Cada alteração aparece em **Atividade**, com a opção **Desfazer**. Elas nunca mesclam, excluem ou compartilham registros. O que salvam vem marcado com **AI:** e o nome delas. Sua Machine trata isso como uma informação fornecida pela IA, nunca como uma instrução sua.

Um rascunho fica aguardando até você ler e pressionar Enviar. Uma IA conectada nunca envia nada nem age em seu nome.

## Conectar uma

Abra **Configurações** e **Apps**. Abaixo de **Os apps da The Machine**, ficam **Adicionar no ChatGPT** e **Adicionar no Claude**. Em **Ou adicione por endereço**, estão o endereço único do app oficial para cada Machine, `https://mcp.themachine.computer/mcp`, e **Seu endereço**, `https://<your name>.mcp.themachine.computer/mcp`, cada um com a opção **Copiar**.

Se a Machine estiver no seu próprio computador, pressione **Configurar** em **Criar seu endereço** primeiro. Uma página da sua conta será aberta. Confira se ela mostra o mesmo código, confirme e escolha um nome. O pareamento da sua Machine acontece automaticamente, sem reiniciar. As duas opções precisam disso.

Sua Machine configura o endereço seguro automaticamente. Isso leva alguns minutos.

Para usar Claude, pressione **Adicionar no Claude** ou abra [The Machine no diretório do Claude](https://claude.ai/directory/the-machine) e pressione Conectar. Nos planos Team e Enterprise, um proprietário precisa adicioná-lo nas configurações da organização.

Para usar um endereço no Claude, abra Customize, Connectors, pressione + Add e depois Add custom connector. Dê o nome The Machine, cole o endereço, pressione Continue e depois Add.

Para usar ChatGPT, pressione **Adicionar no ChatGPT** ou abra [The Machine no ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) e pressione Install plugin. Nos planos Business e Enterprise, talvez um administrador precise permitir o app primeiro.

O app oficial se conecta a uma Machine hospedada e também a uma Machine no seu próprio computador, depois que ela tiver um endereço.

Para usar seu endereço privado ou uma Machine que não esteja na Network, adicione um servidor MCP personalizado no ChatGPT: abra chatgpt.com/plugins, pressione + e depois Add custom MCP server. Dê o nome The Machine, cole o endereço e escolha OAuth. Confirme o aviso e pressione Create as a plugin. Seu plano ou espaço de trabalho precisa permitir servidores MCP personalizados.

Com o app oficial, a IA pede para você entrar com sua conta da The Machine. Se você tiver mais de uma Machine, escolha uma e aprove o acesso na página da própria Machine. Com o endereço privado, a IA se conecta diretamente à sua Machine.

IAs em um dispositivo da sua rede privada (Tailscale), como Claude Code ou Cursor, também podem usar o endereço do seu painel seguido de `/mcp`. A opção **Desfazer o pareamento desta Machine**, na parte inferior de **Configurações**, em **Conta**, remove do seu acesso uma Machine que esteja no seu próprio computador.

Sua Machine mostra qual IA está fazendo a solicitação. Se não conseguir identificá-la, mostra de onde veio a solicitação. Só se conecte se você tiver acabado de iniciar essa ação.

Escolha o que ela pode fazer: **Ler** ou **Ler e editar**. Se você tiver contas de Trabalho e Pessoal, escolha o que ela pode acessar. Depois, escolha por quanto tempo: **1 dia**, **7 dias**, **30 dias** ou **1 ano**. Pressione **Conectar** ou **Cancelar** para recusar a solicitação.

## App oficial ou endereço privado

O app oficial é a opção mais fácil: um único endereço para todo mundo, e sua conta encontra sua Machine. Nosso serviço na nuvem encaminha as solicitações sem armazenar o conteúdo delas.

Com seu endereço privado, tudo é criptografado até chegar à sua Machine. O serviço na nuvem apenas encaminha as solicitações e não consegue ler o conteúdo.

De qualquer forma, quem decide é sua Machine. Só uma IA que você aprovou na página dela consegue entrar, com o acesso que você escolheu. Em **Configurações**, em **Apps**, uma IA conectada pelo app oficial aparece como **App oficial**.

## O que ela vê

Uma conexão só acessa a área correspondente. Trabalho inclui tarefas e promessas das suas contas de trabalho, pessoas, empresas e projetos do trabalho, além do resumo da equipe da sua Fleet de Trabalho. Pessoal inclui o restante. O texto das mensagens continua na sua Machine, a menos que você ative **Mensagens**. Sem essa opção, uma IA só vê o remetente, o assunto e a data das mensagens relacionadas a uma tarefa.

Os registros do Graph da equipe dos seus colegas nunca são enviados para uma IA externa.

## Mensagens

**Mensagens** permite que uma IA pesquise e leia seus e-mails, mensagens do Slack, WhatsApp e outros chats. A opção fica desativada até você ativá-la na página de conexão ou depois em **Configurações**, em **Apps**. A IA só lê: nunca envia, exclui ou marca nada.

Ela só lê as mensagens da área correspondente. Algumas mensagens nunca são enviadas: códigos de uso único e links para entrar, mensagens de um quadro ou projeto **Só você**, conversas que a The Machine identificou como sensíveis (negócios, RH, assuntos jurídicos, saúde e dinheiro), conversas que você manteve privadas e mensagens excluídas.

Cada leitura aparece em **Atividade**, com a quantidade de mensagens e as conversas acessadas, nunca com o texto. Sua Machine entrega o texto marcado como dado, então a IA não deve seguir instruções escritas em uma mensagem.

Enquanto Mensagens estiver ativada, as alterações no Graph feitas por uma IA com **Ler e editar** aguardam sua aprovação. Pressione **Aplicar** ou **Descartar** na alteração em **Atividade**.

## Nas Configurações

Abra **Configurações** e **Apps** para ver cada IA que se conectou, com o tipo de acesso, a área, a data de término e o último uso. Você pode ativar ou desativar **Mensagens** ali mesmo. Pressione **Mudar** para alterar o acesso, a área ou por quanto tempo ele dura. A próxima solicitação usará as novas configurações. **Atividade** mostra todas as solicitações, inclusive as recusadas. **Desativar agora** interrompe o acesso e encerra todas as sessões, mas mantém o histórico. **Remover** exclui a IA e o histórico dela.

Quando você entrar na mesma IA novamente, a nova aprovação substituirá a anterior.

Uma IA que não consegue entrar sozinha pode usar uma chave. Em **Adicionar uma chave**, dê um nome à chave, escolha o acesso e a duração e pressione **Criar chave**. Copie a chave na hora: ela só aparece uma vez. A IA envia a chave como `Authorization: Bearer <key>`.

## Mantenha tudo seguro

Todas as solicitações são registradas, inclusive as recusadas. Uma conexão expirada ou desativada é recusada até você alterar as configurações. Sua Machine guarda apenas uma impressão digital de cada sessão, então uma cópia dos dados dela não dá acesso a nada.
