---
title: Conectar outras IAs
area: connections
summary: Deixe Claude, ChatGPT, Cursor, Codex ou GBrain lerem suas tarefas e seu Graph por MCP, cada uma com seu acesso e prazo.
covers: ai-connections, settings:ai
code: ai_access.py, ai_app.py, pairing.py, ai_reach.py
keywords: MCP, Claude, ChatGPT, Cursor, Codex, GBrain, connector, AI, OAuth
order: 95
---
## O que outra IA pode fazer

Outras IAs podem se conectar à sua Machine por MCP: Claude, ChatGPT, Cursor, Codex, GBrain e outras. Elas podem ler suas tarefas, promessas, resumos da equipe e as pessoas e empresas do seu Graph.

Com **Ler e editar** elas também podem adicionar uma tarefa, ou uma tarefa com um rascunho de e-mail, e mudar seu Graph: salvar um fato sobre uma pessoa ou empresa, corrigir detalhes, campos e tags, ou adicionar uma linha ao resumo de uma pessoa.

Cada mudança aparece em **Atividade** com **Desfazer**. Elas nunca mesclam, excluem nem compartilham registros. O que elas salvam mostra **IA:** e o nome delas, na área delas. Você pode editar ou remover, e The Machine pode reescrever uma linha do resumo depois. Sua Machine trata isso como afirmação delas, nunca como instrução sua.

Um rascunho espera na sua Machine até você ler e tocar em **Enviar**. Uma IA conectada nunca envia nada e nunca age por você. O Do it e os agentes da sua Machine não fazem parte disso.

## Conectar uma

Abra **Configurações**, **IAs**. Há dois jeitos de entrar. Primeiro vem **App oficial**: um endereço para todas as Machines, `https://mcp.themachine.computer/mcp`, com **Copiar**. Abaixo fica seu **Endereço privado (ponta a ponta)**, `https://<seu nome>.mcp.themachine.computer/mcp`.

Numa Machine no seu próprio computador, toque antes em **Obter seu endereço**. Abre uma página da sua conta: confira se ela mostra o mesmo código, confirme e escolha um nome. Sua Machine se pareia sozinha, sem reiniciar. Os dois jeitos precisam disso.

Depois ela obtém o próprio certificado para o endereço. Leva alguns minutos e precisa do pacote `cryptography` para Python.

No ChatGPT, abra chatgpt.com/plugins, toque em + e depois em Add custom MCP server. Chame de The Machine, cole o endereço e escolha OAuth. Confirme o aviso e toque em Create as a plugin. Seu plano ou workspace precisa permitir servidores MCP personalizados.

No Claude, abra Customize, Connectors, toque em + Add e depois em Add custom connector. Chame de The Machine, cole o endereço, toque em Continue e depois em Add. No Team e no Enterprise, um proprietário adiciona em Organization settings.

Com o app oficial, a IA pede que você entre com sua conta The Machine. Escolha esta Machine se tiver mais de uma e depois aprove a IA na página da sua Machine. Com o endereço privado, a IA vai direto para sua Machine.

IAs num dispositivo da sua tailnet, como Claude Code ou Cursor, também podem usar o endereço do seu painel seguido de `/mcp`. **Desfazer pareamento** tira da sua conta uma Machine no seu próprio computador.

Sua Machine mostra qual IA é. Uma IA que ela não reconhece mostra o endereço de onde vem: conecte só se você acabou de iniciar isso.

Escolha o que ela pode fazer, **Ler** ou **Ler e editar**. Com contas de trabalho e pessoais, escolha também o que ela pode ver. Depois escolha por quanto tempo: **1 dia**, **7 dias**, **30 dias** ou **1 ano**. Toque em **Conectar**, ou em **Cancelar** para devolvê-la sem nada.

## App oficial ou endereço privado

O app oficial é o jeito fácil: um endereço para todos, e sua conta encontra sua Machine. A nuvem encaminha as solicitações no caminho, mas não guarda nada.

Com seu endereço privado, tudo é criptografado até sua Machine. A nuvem só repassa e não consegue ler.

De qualquer jeito, quem decide é sua Machine. Só entra uma IA que você aprovou na página dela, com o acesso que você escolheu. Em **Configurações**, **IAs**, uma IA que veio pelo app oficial mostra **App oficial**.

## O que ela vê

Uma conexão só vê a sua área. Trabalho cobre as tarefas e promessas das suas contas de trabalho, contatos de trabalho, empresas, projetos e o resumo da equipe da sua Work Fleet. Pessoal cobre o resto. O texto das mensagens fica na sua Machine, a não ser que você ative **Mensagens**: sem isso, uma IA vê as fontes de uma tarefa só por remetente, assunto e data.

Os dados do Team Graph dos seus colegas nunca vão para uma IA de fora.

## Mensagens

**Mensagens** deixa uma IA buscar e ler seu e-mail, Slack, WhatsApp e outros chats. Fica desativado até você ativar, na página onde você a conecta ou depois em **Configurações**, **IAs**. Ela só lê: nunca envia, apaga ou marca nada.

Ela só lê mensagens da sua área. Algumas nunca saem: códigos de uso único e links de login, mensagens de um quadro ou projeto **Só você**, conversas que The Machine considerou sensíveis (negócios, RH, jurídico, saúde, dinheiro), conversas que você manteve privadas e mensagens apagadas.

Cada leitura aparece na **Atividade** dela, com quantas mensagens e quais conversas, nunca o texto. Sua Machine entrega o texto marcado como dados, para que a IA não siga instruções escritas em uma mensagem.

Enquanto Mensagens estiver ativado, as mudanças no Graph de uma IA com **Ler e editar** esperam seu OK. Toque em **Aplicar** ou **Dispensar** na mudança em **Atividade**.

## Em Configurações

Abra **Configurações**, **IAs** para ver cada IA conectada, com o último uso e quantas chamadas fez. Mude ali o acesso, a área ou a duração. A próxima chamada já usa isso. **Desativar agora** encerra todos os logins dela de uma vez. **Atividade** lista cada chamada, as recusadas também. **Remover** tira a IA.

Uma IA que não consegue entrar sozinha pode usar uma chave. Em **Adicionar uma chave**, dê um nome, escolha o acesso e a duração e toque em **Criar chave**. Copie a chave na hora: ela aparece só uma vez. A IA envia como `Authorization: Bearer <key>`.

## Segurança

Cada chamada fica registrada, as recusadas também. Uma conexão expirada ou desativada é recusada até você mudá-la. O login usa OAuth com PKCE. Sua Machine guarda só uma impressão digital de cada token, então uma cópia dos dados dela não abre nada.
