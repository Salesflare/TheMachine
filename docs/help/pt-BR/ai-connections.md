---
title: Conectar outras IAs
area: connections
summary: Deixe Claude, ChatGPT, Cursor, Codex ou GBrain ler suas tarefas e seu Graph. Com **Ler e editar**, também podem fazer alterações que você pode desfazer.
covers: ai-connections, settings:apps
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
translated: 7681c632f712e93c
---
## O que outra IA pode fazer

Claude, ChatGPT, Cursor, Codex, GBrain e outras IAs podem se conectar à sua Machine. Elas podem ler suas tarefas, promessas, briefs da equipe e as pessoas e empresas do seu Graph.

Com **Ler e editar**, elas também podem adicionar uma tarefa ou um rascunho de e-mail e atualizar seu Graph: salvar um fato, corrigir detalhes, campos e tags ou adicionar uma linha ao resumo de uma pessoa.

Cada alteração aparece em **Atividade**, com a opção **Desfazer**. Elas nunca mesclam, excluem nem compartilham registros. O que salvam vem marcado como **AI:** com o nome delas, e sua Machine trata isso como algo que a IA afirma, nunca como uma instrução sua.

Um rascunho fica aguardando até você ler e tocar em Enviar. Uma IA conectada nunca envia nada nem age em seu nome.

## O que ela aprende com você

Quando um chat começa, a IA recebe um breve resumo: quem você é, suas principais regras e o que mudou desde a última vez que ela acessou sua Machine. Ela também pode ler o que está em **Aprendizado**: suas regras, fatos gerais e seu jeito de escrever em cada canal. Assim, ela escreve como você.

Com **Ler e editar**, ela pode salvar o que vocês definirem no chat. Um fato é salvo na hora, e você pode usar **Desfazer** em **Atividade**. Uma regra orienta o trabalho da sua Machine, então fica em **Aprendizado** até você tocar em **Aprovar** ou **Descartar**. Ela nunca muda seu jeito de escrever.

Um rascunho com algo faltando, um arquivo mencionado que a IA não tem ou apenas o seu próprio endereço como destinatário volta para a IA corrigir primeiro. Se uma IA pedir a mesma tarefa ou o mesmo rascunho duas vezes seguidas, você receberá apenas um.

## Conectar uma IA

Abra **Configurações**, **Apps**. Abaixo de **Os apps da The Machine**, você encontra **Adicionar no ChatGPT** e **Adicionar no Claude**. Em **Ou adicione por endereço**, ficam o endereço do app oficial, que é o mesmo para todas as Machines, `https://mcp.themachine.computer/mcp`, e **Seu endereço**, `https://<your name>.mcp.themachine.computer/mcp`, cada um com a opção **Copiar**.

Em uma Machine no seu próprio computador, toque primeiro em **Configurar**, abaixo de **Criar seu endereço**. Uma página da sua conta será aberta: confira se ela mostra o mesmo código, confirme e escolha um nome. Sua Machine será pareada automaticamente, sem precisar reiniciar. As duas formas exigem esse passo.

Depois, sua Machine configura o endereço seguro automaticamente. Isso leva alguns minutos.

Para usar o Claude, toque em **Adicionar no Claude** ou abra [The Machine no diretório do Claude](https://claude.ai/directory/the-machine) e toque em Connect. Nos planos Team e Enterprise, um proprietário precisa adicioná-lo nas configurações da organização.

A habilidade da The Machine informa ao Claude quando usar sua Machine: primeiro, ele recebe o brief, suas regras e seu jeito de escrever, antes de criar qualquer rascunho. Toque em **Baixar**, ao lado de **habilidade do Claude**. Depois, no Claude, abra Customize, Skills e faça o upload.

Para usar um endereço no Claude, em vez disso, abra Customize, Connectors, toque em + Add e depois em Add custom connector. Dê o nome The Machine, cole o endereço, toque em Continue e depois em Add.

Para usar o ChatGPT, toque em **Adicionar no ChatGPT** ou abra [The Machine no ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_6ae74ac637d0819199400cd3750138b4) e toque em Install plugin. Nos planos Business e Enterprise, talvez seja necessário que um administrador permita o uso primeiro.

O app oficial se conecta a uma Machine hospedada e também a uma Machine no seu próprio computador, depois que ela tiver um endereço.

Para usar seu endereço privado ou uma Machine que não esteja na Network, adicione um servidor MCP personalizado no ChatGPT: abra chatgpt.com/plugins, toque em + e depois em Add custom MCP server. Dê o nome The Machine, cole o endereço e escolha OAuth. Confirme o aviso e toque em Create as a plugin. Seu plano ou espaço de trabalho precisa permitir servidores MCP personalizados.

Com o app oficial, a IA pede para você entrar com sua conta da The Machine. Se tiver mais de uma Machine, escolha esta e depois aprove o acesso na página da sua Machine. Com o endereço privado, a IA se conecta diretamente à sua Machine.

IAs em um dispositivo da sua rede privada (Tailscale), como Claude Code ou Cursor, também podem usar o endereço do seu painel seguido de `/mcp`. **Desfazer o pareamento desta Machine**, no fim de **Configurações**, **Conta**, remove da sua conta uma Machine que esteja no seu próprio computador.

Sua Machine mostra qual IA está fazendo a solicitação. Se não conseguir identificá-la, mostra de onde a solicitação veio: conecte apenas se você acabou de iniciar essa ação.

Escolha o que ela pode fazer: **Ler** ou **Ler e editar**. Se você tiver contas de Trabalho e Pessoal, escolha o que ela pode acessar. Depois, escolha por quanto tempo: **1 dia**, **7 dias**, **30 dias** ou **1 ano**. Toque em **Conectar** ou em **Cancelar** para recusar sem permitir o acesso.

## App oficial ou endereço privado

O app oficial é a opção mais simples: um endereço para todo mundo, e sua conta encontra sua Machine. Nosso serviço na nuvem encaminha as solicitações e nunca armazena o conteúdo delas.

Com seu endereço privado, tudo é criptografado até chegar à sua Machine. O serviço na nuvem só encaminha o conteúdo e não consegue lê-lo.

De qualquer forma, quem decide é sua Machine. Só uma IA que você aprovou na página dela consegue entrar, com o acesso que você escolheu. Em **Configurações**, **Apps**, uma IA conectada pelo app oficial aparece como **App oficial**.

## O que ela pode acessar

Uma conexão acessa apenas a área correspondente. Trabalho inclui as tarefas e promessas das suas contas de trabalho, contatos de trabalho, empresas, projetos e o brief da equipe do seu Fleet de Trabalho. Pessoal inclui o restante. O texto das mensagens continua na sua Machine, a menos que você ative **Mensagens**. Sem essa opção, uma IA só vê o remetente, o assunto e a data das mensagens relacionadas a uma tarefa.

Os registros do Graph da equipe dos seus colegas nunca são enviados a uma IA externa.

## Mensagens

**Mensagens** permite que uma IA pesquise e leia seus e-mails, mensagens do Slack, WhatsApp e outros chats. Essa opção fica desativada até você ativá-la, na página de conexão ou depois em **Configurações**, **Apps**. A IA só pode ler: nunca envia nem exclui mensagens, nem as marca.

Ela só lê mensagens da área correspondente. Algumas nunca são compartilhadas: códigos de uso único e links de acesso, mensagens de um quadro ou projeto **Só você**, conversas que a The Machine identificou como confidenciais (negócios, RH, questões jurídicas, saúde e dinheiro), conversas que você manteve privadas e mensagens excluídas.

Cada leitura aparece em **Atividade**, com o número de mensagens e as conversas acessadas, nunca o texto. Sua Machine entrega o texto marcado como dado, para que a IA não siga instruções escritas em uma mensagem.

Enquanto **Mensagens** estiver ativada, as alterações no Graph feitas por uma IA com **Ler e editar** aguardam sua aprovação. Toque em **Aplicar** ou **Descartar** na alteração em **Atividade**.

## Em Configurações

Abra **Configurações**, **Apps** para ver cada IA que se conectou, uma vez, com o acesso, a área, a data de término e o último uso. Você pode ativar ou desativar **Mensagens** nessa mesma tela. Toque em **Mudar** para alterar o acesso, a área ou por quanto tempo ele vale. A próxima solicitação usará as novas configurações. **Atividade** lista todas as solicitações, inclusive as recusadas. **Desativar agora** pausa o acesso: todas as sessões são encerradas, mas o histórico é mantido. **Remover** exclui a IA e o histórico dela.

Quando você entra na mesma IA de novo, a nova aprovação substitui a anterior. Se você já tinha entrado nessa IA, ela continua conectada com o novo nível de acesso. Uma IA que você usa continua conectada até a data de término. Se não for usada por 90 dias, será necessário entrar de novo.

Uma IA que não consegue entrar por conta própria pode usar uma chave. Em **Adicionar uma chave**, dê um nome para ela, escolha o acesso e a duração e toque em **Criar chave**. Copie a chave na hora: ela só será exibida uma vez. A IA a envia como `Authorization: Bearer <key>`.

## Mantenha a segurança

Todas as solicitações são registradas, inclusive as recusadas. Uma conexão expirada ou desativada é recusada até você alterá-la. Sua Machine guarda apenas uma impressão digital de cada acesso, então uma cópia dos dados não dá acesso a nada.
