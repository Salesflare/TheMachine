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

Cada mudança aparece em **Atividade** com **Desfazer**. Elas nunca mesclam, excluem nem compartilham registros. Um rascunho espera na sua Machine até você ler e tocar em **Enviar**. Uma IA conectada nunca envia nada e nunca age por você. O Do it e os agentes da sua Machine não fazem parte disso.

## Conectar uma

Abra **Configurações**, **IAs**. No topo fica o endereço da sua Machine para IAs, `https://<seu nome>.mcp.themachine.computer/mcp`, com **Copiar**. Numa Machine no seu próprio computador, toque antes em **Obter seu endereço**. Abre uma página da sua conta: confira se ela mostra o mesmo código, confirme e escolha um nome. Sua Machine se pareia sozinha, sem reiniciar.

Depois ela obtém o próprio certificado para o endereço. Leva alguns minutos e precisa do pacote `cryptography` para Python.

No ChatGPT, abra chatgpt.com/plugins, toque em + e depois em Add custom MCP server. Chame de The Machine, cole o endereço e escolha OAuth. Confirme o aviso e toque em Create as a plugin. Seu plano ou workspace precisa permitir servidores MCP personalizados.

No Claude, abra Customize, Connectors, toque em + Add e depois em Add custom connector. Chame de The Machine, cole o endereço, toque em Continue e depois em Add. No Team e no Enterprise, um proprietário adiciona em Organization settings.

IAs num dispositivo da sua tailnet, como Claude Code ou Cursor, também podem usar o endereço do seu painel seguido de `/mcp`. **Desfazer pareamento** tira da sua conta uma Machine no seu próprio computador.

A IA leva você à sua Machine para entrar. Sua Machine mostra qual IA é. Uma IA que ela não reconhece mostra o endereço de onde vem: conecte só se você acabou de iniciar isso.

Escolha o que ela pode fazer, **Ler** ou **Ler e editar**. Com contas de trabalho e pessoais, escolha também o que ela pode ver. Depois escolha por quanto tempo: **1 dia**, **7 dias**, **30 dias** ou **1 ano**. Toque em **Conectar**, ou em **Cancelar** para devolvê-la sem nada.

## O que ela vê

Uma conexão só vê a sua área. Trabalho cobre as tarefas e promessas das suas contas de trabalho, contatos de trabalho, empresas, projetos e o resumo da equipe da sua Work Fleet. Pessoal cobre o resto. O texto das mensagens fica na sua Machine: uma IA vê as fontes de uma tarefa só por remetente, assunto e data.

Os dados do Team Graph dos seus colegas nunca vão para uma IA de fora.

## Em Configurações

Abra **Configurações**, **IAs** para ver cada IA conectada, com o último uso e quantas chamadas fez. Mude ali o acesso, a área ou a duração. A próxima chamada já usa isso. **Desativar agora** encerra todos os logins dela de uma vez. **Atividade** lista cada chamada, as recusadas também. **Remover** tira a IA.

Uma IA que não consegue entrar sozinha pode usar uma chave. Em **Adicionar uma chave**, dê um nome, escolha o acesso e a duração e toque em **Criar chave**. Copie a chave na hora: ela aparece só uma vez. A IA envia como `Authorization: Bearer <key>`.

## Segurança

Cada chamada fica registrada, as recusadas também. Uma conexão expirada ou desativada é recusada até você mudá-la. O login usa OAuth com PKCE. Sua Machine guarda só uma impressão digital de cada token, então uma cópia dos dados dela não abre nada.
