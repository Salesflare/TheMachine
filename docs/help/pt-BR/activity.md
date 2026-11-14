---
title: Atividade
area: settings
summary: Uma lista de tudo o que The Machine fez por você, o mais recente primeiro: mensagens, documentos, respostas do Fleet, aprendizados, conexões e mais.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
---
## O que mostra

Abra **Configurações**, **Atividade**. Cada linha é algo que The Machine fez, o mais recente primeiro, por dia:

- o que ela fez e como terminou: enviado, recusado, com falha ou desfeito
- quando, a conta ou o app que ela usou e [o que permitiu](activity.md#what-allowed-it)
- um link para a tarefa, quando houver
- para uma IA que você conectou, como ChatGPT ou Claude: o nome dela com **(IA conectada)**, para distinguir da The Machine

Ela lista mensagens e respostas, mudanças em documentos e na agenda, etapas na web, correções que ela mesclou, agentes de código, perguntas e respostas do Fleet, aprendizados enviados à equipe da The Machine, habilidades, importações no Graph, fatos que você pediu para esquecer no chat (com **Desfazer**), conexões adicionadas ou removidas, e cada acesso da nossa equipe pelo [Acesso de suporte](get-support.md#support-access), inclusive os recusados.

## O que permitiu

Cada mensagem, mudança em documento ou agenda, etapa na web e correção mesclada diz o que a deixou sair, como aconteceu:

- **Aprovado na tarefa** ou **Aprovado no Telegram**: o seu toque em Enviar, Confirmar ou Mesclar
- **Aprovado por voz**: o seu sim no Talk
- **“Fazer” tocado**: o seu Fazer na tarefa
- **Pedido no chat**: você pediu com palavras, com o início da sua mensagem entre aspas. Uma citação só aparece enquanto essas palavras continuam na sua própria mensagem.
- **Follow-up que ela enviou sozinha**, **Pequena correção, mesclada sozinha**, **Novo documento privado, criado sozinha** ou **Preparada com antecedência, sozinha**: uma configuração sua ou uma regra própria da The Machine
- **Nenhuma aprovação registrada**: nada foi registrado. Também vai para os nossos [relatórios de erro](error-reports.md), para acharmos o caminho que não registrou.

Etapas na web também lista a execução de uma tarefa que clicou ou digitou numa página, com o que permitiu essa execução.

Linhas mais antigas, de antes deste registro, mantêm as palavras antigas, como **Depois do seu OK**.

## Filtrar

Escolha um tipo na lista no topo, como **Mensagens** ou **Fleet**. **Recusado ou bloqueado** mostra só o que não foi, e por quê. **Mostrar mais** carrega linhas mais antigas.

## Outros lugares

O chat de uma tarefa continua contando a própria história; Atividade leva até ele. Fleet, **Atividade** mostra as mesmas linhas para os seus Fleets e aprendizados, com **Retirar** para um aprendizado. Em Configurações, **Segurança**, **Ver cada acesso em Atividade** abre os acessos da nossa equipe.

Atividade só mostra o que aconteceu. Nunca muda o que The Machine pode fazer.
