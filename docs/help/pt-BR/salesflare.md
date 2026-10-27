---
title: Salesflare CRM
area: connections
summary: Contas, contatos e negócios, para ela saber quem importa. Ela lê com sua chave de API.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
---
## O que ela lê

Suas contas, contatos e negócios no Salesflare, e os feeds das contas: e-mails de colegas que não envolvem você e reuniões com notas.

## O que ela pode mudar

Nada, a menos que você defina `join_pipelines` no arquivo de configurações da sua Machine. Aí ela adiciona você sozinha às contas desses pipelines. Por padrão, ele fica vazio.

## Conecte

1. No Salesflare, abra [Configurações, Chaves de API](https://app.salesflare.com/#/settings/apikeys) e crie uma chave.
2. Em uma Machine hospedada: abra sua página de configuração em app.themachine.computer/setup, vá para **Mais fontes**, abra Salesflare CRM, cole a chave e clique em **Conectar**.
3. No seu próprio computador: rode `assistant connect crm`, ou **Conexões**, **+ Adicionar**, Salesflare CRM. Depois de **Conectar**, sua Machine reinicia e abre o cartão do Salesflare, que primeiro diz que está encontrando as contas com e-mails e reuniões recentes, e depois quantas já leu.

## Detalhes da sincronização

O cartão dele em **Conexões**, **Outras fontes** mostra o andamento: quantas contas ela leu nesta rodada e quantas pulou porque o Salesflare demorou demais para responder. Uma rodada que dura horas avisa que pode estar travada.

- **Parar**: nada novo chega até você clicar em **Início**. Ela continua de onde estava.
- **Reiniciar sincronização**: descarta a rodada atual, com os erros dela, e lê a última semana de novo agora. Nada do que ela já trouxe se perde.
- **Chaves de API**: abre a página de chaves de API do Salesflare, para criar uma chave nova.

## Remova

- No painel: **Conexões**, abra Salesflare, **Detalhes** e depois **Desconectar**. O que já foi trazido continua lá.
- Em uma Machine hospedada, você também pode clicar em **Remover** ao lado dele na sua página de configuração.

## Revogue no Salesflare

Exclua a chave de API no Salesflare, em Configurações, Chaves de API.
