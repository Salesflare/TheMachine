---
title: Salesflare CRM
area: connections
summary: Contas, contatos e negócios, para ela saber quem importa. Ela lê com sua chave de API.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
translated: 697e6d60b69bb1cd
---
## O que ela lê

Suas contas, contatos e negócios no Salesflare, e os feeds das contas: e-mails de colegas que não envolvem você e reuniões com notas.

## O que ela pode mudar

Nada, a menos que você defina `join_pipelines` no arquivo de configurações da sua Machine. Aí ela adiciona você sozinha às contas desses pipelines. Por padrão, ele fica vazio.

## Conecte

1. No Salesflare, abra [Configurações, Chaves de API](https://app.salesflare.com/#/settings/apikeys) e crie uma chave.
2. Em uma Machine hospedada: abra sua página de configuração em app.themachine.computer/setup, vá para **Mais fontes**, abra Salesflare CRM, cole a chave e clique em **Conectar**.
3. No seu próprio computador: rode `assistant connect crm`, ou **Conexões**, **Clientes**, Salesflare CRM. Depois de **Conectar**, sua Machine reinicia e abre o cartão do Salesflare, que primeiro diz que está encontrando as contas com e-mails e reuniões recentes, e depois quantas já leu.

## Detalhes da sincronização

O cartão dele em **Conexões**, **Outras fontes** mostra o andamento: quantas contas ela leu nesta rodada e quantas pulou porque o Salesflare demorou demais para responder. Uma rodada que dura horas avisa que pode estar travada.

Os blocos contam as contas que ela conseguiu abrir e os e-mails e reuniões que trouxe. Se o Salesflare não deixa sua chave de API abrir nenhuma conta, o cartão diz **Precisa da sua ajuda**: use a chave de um usuário que consiga vê-las. Se o Salesflare demora demais com frequência, mas cada nova tentativa funciona, ele diz que o Salesflare **às vezes fica lento**.

Se o Salesflare não ativou o acesso ao feed com chaves de API para a sua equipe, o cartão diz isso: não chegam e-mails nem reuniões até o suporte do Salesflare ativar. Ela verifica de novo a cada 10 minutos no primeiro dia, depois mais ou menos a cada hora, e continua sozinha assim que funcionar.

- **Parar**: nada novo chega até você clicar em **Início**. Ela continua de onde estava.
- **Reiniciar sincronização**: descarta a rodada atual, com os erros dela, e lê a última semana de novo agora. Nada do que ela já trouxe se perde.
- **Chaves de API**: abre a página de chaves de API do Salesflare, para criar uma chave nova.

## Remova

- No painel: **Conexões**, abra Salesflare, **Detalhes** e depois **Desconectar**. O que já foi trazido continua lá.
- Em uma Machine hospedada, você também pode clicar em **Remover** ao lado dele na sua página de configuração.

## Revogue no Salesflare

Exclua a chave de API no Salesflare, em Configurações, Chaves de API.
