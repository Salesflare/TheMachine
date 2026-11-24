---
title: Atividade
area: settings
summary: Uma lista de tudo que a The Machine fez por você, da atividade mais recente à mais antiga: mensagens, documentos, respostas do Fleet, aprendizados, conexões e muito mais.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
translated: 1ebeba09417a11e9
---
## O que ela mostra

Acesse **Configurações** e **Atividade**. Cada linha mostra uma ação da The Machine, da mais recente à mais antiga, organizada por dia:

- o que ela fez e como terminou: enviada, recusada, falhou ou desfeita; no caso de uma mensagem [agendada para depois](send-later.md), também mostra quando foi agendada, alterada ou cancelada
- quando aconteceu, qual conta ou app ela usou e [o que autorizou a ação](activity.md#what-allowed-it)
- um link para a tarefa correspondente, se houver
- no caso de uma IA que você conectou, como ChatGPT ou Claude: o nome seguido de **(IA conectada)**, para você saber que não é a própria The Machine

A lista inclui mensagens e respostas, alterações em documentos e no calendário, ações na web, correções mescladas, agentes de programação, perguntas e respostas do Fleet, aprendizados enviados à equipe da The Machine, habilidades, importações do Graph, informações que você pediu para o chat esquecer (com **Desfazer**), conexões adicionadas ou removidas e cada acesso feito pela nossa equipe em [Acesso do suporte](get-support.md#support-access), inclusive os recusados.

## O que autorizou a ação

Cada mensagem, alteração em documentos ou no calendário, ação na web e correção mesclada mostra o que a autorizou no momento em que aconteceu:

- **Aprovado na tarefa** ou **Aprovado no Telegram**: você tocou em **Enviar**, **Confirmar** ou **Mesclar**
- **Aprovado por voz**: você disse sim no Talk
- **“Fazer” tocado**: você tocou em **Fazer** na tarefa
- **Pedido no chat**: você pediu por escrito, e o começo da sua mensagem aparece entre aspas. A citação só aparece enquanto essas palavras ainda estiverem na sua mensagem.
- **Follow-up que ela enviou sozinha**, **Pequena correção, mesclada sozinha**, **Novo documento privado, criado por ela mesma** ou **Preparada com antecedência, sozinha**: uma configuração sua ou uma regra da própria The Machine
- **Nenhuma aprovação registrada**: nada foi registrado para essa ação. Ela também aparece nos nossos [relatórios de erro](error-reports.md), para que possamos encontrar o caminho que não funcionou.

A seção de ações na web também mostra as execuções de tarefas que clicaram ou digitaram em uma página, com a autorização de cada execução. O trabalho que continua depois de ser adiado mantém a autorização que tinha antes do adiamento.

As linhas mais antigas, de antes de esse registro existir, mantêm os termos antigos, como **Depois do seu OK**.

## Filtrar a lista

Escolha um tipo na lista no topo, como **Mensagens** ou **Fleet**. **Recusado ou bloqueado** mostra apenas o que não foi feito e o motivo. Toque em **Mostrar mais** para carregar linhas mais antigas.

## Outros lugares

O chat de uma tarefa continua mostrando o que aconteceu nela, e a Atividade tem um link para ele. Em **Atividade** do Fleet, você vê as mesmas linhas dos seus Fleets e aprendizados, com a opção **Retirar** para um aprendizado. Em **Configurações**, acesse **Segurança** e toque em **Ver cada acesso em Atividade** para abrir os acessos feitos pela nossa equipe.

A Atividade só mostra o que aconteceu. Ela nunca altera o que a The Machine pode fazer.
