---
title: Atividade
area: settings
summary: Uma lista de tudo o que sua Machine fez por você, da atividade mais recente à mais antiga: mensagens, documentos, respostas do Fleet, aprendizados, conexões e muito mais.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
translated: ebb6a4cf0474a020
---
## O que ela mostra

Acesse **Configurações** e **Atividade**. Cada linha mostra uma coisa que a sua Machine fez, da mais recente à mais antiga, por dia:

- o que ela fez e como terminou: enviada, recusada, com erro ou desfeita
- quando aconteceu, a conta ou o app que ela usou e [o que permitiu a ação](activity.md#what-allowed-it)
- um link para a tarefa, se houver
- no caso de uma IA conectada por você, como ChatGPT ou Claude: o nome seguido de **(IA conectada)**, para você não confundi-la com a própria The Machine

A lista inclui mensagens e respostas, alterações em documentos e no calendário, ações na web, correções que ela mesclou, agentes de programação, perguntas e respostas do Fleet, aprendizados enviados à equipe da The Machine, habilidades, importações do Graph, informações que você pediu no chat para esquecer (com **Desfazer**), conexões adicionadas ou removidas e cada acesso da nossa equipe em [Acesso do suporte](get-support.md#support-access), inclusive os recusados.

## O que permitiu a ação

Cada mensagem, alteração em documento ou no calendário, ação na web e correção mesclada informa o que permitiu a ação, no momento em que aconteceu:

- **Aprovado na tarefa** ou **Aprovado no Telegram**: você tocou em Enviar, Confirmar ou Mesclar
- **Aprovado por voz**: você disse sim no Talk
- **“Fazer” tocado**: você tocou em Fazer na tarefa
- **Pedido no chat**: você pediu em palavras, e o início da sua mensagem aparece entre aspas. A citação só aparece enquanto essas palavras ainda estiverem na sua mensagem.
- **Follow-up que ela enviou sozinha**, **Pequena correção, mesclada sozinha**, **Novo documento privado, criado sozinha** ou **Preparada com antecedência, sozinha**: a ação foi permitida por uma configuração sua ou por uma regra da própria The Machine
- **Nenhuma aprovação registrada**: nada foi registrado para essa ação. Ela também aparece nos nossos [relatórios de erro](error-reports.md), para podermos encontrar o caminho que não foi registrado.

As ações na web também mostram a execução de uma tarefa que clicou ou digitou em uma página, junto com o que permitiu essa execução. O trabalho que continua depois de ser adiado mantém a permissão que tinha antes do adiamento.

Linhas mais antigas, de antes desse registro, mantêm os termos anteriores, como **Depois do seu OK**.

## Filtrar

Escolha um tipo na lista no topo, como **Mensagens** ou **Fleet**. **Recusado ou bloqueado** mostra apenas o que não foi feito e o motivo. Toque em **Mostrar mais** para carregar linhas mais antigas.

## Outros lugares

O chat de uma tarefa continua mostrando o que aconteceu nela; a Atividade tem um link para esse chat. Em Fleet, **Atividade** mostra as mesmas linhas dos seus Fleets e aprendizados, com a opção **Retirar** para um aprendizado. Em Configurações, **Segurança**, toque em **Ver cada acesso em Atividade** para abrir os acessos da nossa equipe.

A Atividade mostra apenas o que aconteceu. Ela nunca muda o que a The Machine pode fazer.
