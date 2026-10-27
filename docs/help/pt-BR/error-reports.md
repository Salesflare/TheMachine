---
title: Relatórios de erro
area: security
summary: Quando algo quebra, sua Machine conta para a equipe de The Machine o que falhou e onde no código. Nunca suas mensagens, nomes ou endereços.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html
order: 4
---
## O que é

Quando algo quebra na The Machine, sua Machine envia para a equipe uma assinatura curta do erro, para que a gente corrija antes que alguém precise relatar. Isso vem ativado e precisa da [The Machine Network](/network).

## O que vai

Só isto, para cada tipo de erro:

- o tipo de erro, como `KeyError` ou `TypeError`;
- a mensagem dele sem nada específico: números, ids, texto entre aspas, endereços de e-mail, links, caminhos de arquivo e qualquer coisa que pareça uma chave. Qualquer outra palavra que possa ser um nome também sai;
- onde aconteceu no próprio código da The Machine: arquivo, função e linha, nunca uma pasta do seu computador;
- a versão do app, quantas vezes aconteceu, e quando foi a primeira e a última.

Um real: `IndexError`, `list index out of range`, em `assistant.py:fault_event:7899`, versão `05b17ee6ac79`, 1 vez.

## O que nunca vai

O que dizem suas mensagens, tarefas, rascunhos ou chats. Nomes, endereços de e-mail, números de telefone, links, tokens ou senhas. Sobre qual conta ou pessoa era.

## De onde vêm os erros

- o serviço e as tarefas dele: revisões, preparo de tarefas, chat, conexões e sincronizações;
- o painel no seu navegador;
- trabalhos do Claude Code e do Codex que falham: só a ferramenta e o tipo de falha.

O mesmo erro conta uma vez, com uma contagem. No máximo um lote a cada 10 minutos. A equipe guarda os erros por 30 dias.

## Ritmo

O trabalho em segundo plano espera quando os limites do seu plano de IA estão no fim, para sobrar espaço para os seus chats (veja [Seu modelo de IA](model.md)). Com os relatórios de erro ligados, ela também conta à equipe, uma vez por dia, quantas vezes isso aconteceu: para cada vez, a hora do início, qual limite, quantos minutos durou e quantos trabalhos esperaram. Só contagens e minutos, nada sobre os trabalhos.

## Desativar

Em Configurações, Segurança, desative **Enviar relatórios de erro**. Nada mais é registrado ou enviado, incluindo as contagens de ritmo, e o que estava esperando é excluído. Os erros continuam aparecendo na sua própria Machine, que pode oferecer uma correção.

Veja [Segurança e privacidade](security-and-privacy.md).
