---
title: Salesflare CRM
area: connections
summary: Contas, contatos e negócios para ela saber quem é importante. Ela lê os dados usando sua chave de API.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
translated: 3d6041d568843d96
---
## O que ela lê

Suas contas, contatos e negócios no Salesflare, além do feed de cada conta: e-mails de colegas dos quais você não participou e reuniões com anotações.

## O que ela pode alterar

Nada. (No seu próprio computador, a configuração `join_pipelines` pode fazer com que ela adicione você a contas em pipelines escolhidos. Essa opção vem desativada por padrão.)

## Conectar

1. No Salesflare, acesse [Configurações, chaves de API](https://app.salesflare.com/#/settings/apikeys) e crie uma chave.
2. Em uma Machine hospedada: abra sua página de configuração em app.themachine.computer/setup, acesse **Mais fontes**, abra Salesflare CRM, cole a chave e pressione **Conectar**.
3. No painel: **Conexões**, **Clientes**, Salesflare CRM, cole a chave e pressione **Conectar**. O cartão mostra o andamento da sincronização.

## Detalhes da sincronização

Em **Conexões**, **Clientes**, o Salesflare mostra o andamento: quantas contas foram lidas nesta rodada e quantas foram ignoradas porque o Salesflare estava lento demais. Se uma rodada durar horas, isso significa que ela pode ter travado.

Os cartões mostram quantas contas ela conseguiu abrir e quantos e-mails e reuniões importou. Se sua chave de API não permitir abrir nenhuma conta no Salesflare, o cartão mostrará **Precisa da sua ajuda**: use a chave de um usuário que tenha acesso a elas. Se o Salesflare continuar excedendo o tempo limite, mas cada nova tentativa funcionar, o cartão mostrará que o Salesflare **fica lento às vezes**.

Se o Salesflare ainda não tiver ativado o acesso ao feed por chaves de API para sua equipe, o cartão avisará. Nenhum e-mail ou reunião será importado até que o suporte do Salesflare ative o acesso. A Machine verifica novamente a cada 10 minutos no primeiro dia e, depois, a cada hora. Quando tudo estiver funcionando, a sincronização continua automaticamente.

- **Parar**: nada novo será importado até você pressionar **Começar**. A sincronização continua de onde parou.
- **Reiniciar sincronização**: começa de novo e lê os dados da última semana. Nada do que ela já importou será perdido.
- **Chaves de API**: abre a página de chaves de API do Salesflare para você criar uma nova chave.

## Remover

- No painel: acesse **Conexões**, abra Salesflare, selecione **Detalhes** e depois **Desconectar**. O que ela já importou será mantido.
- Em uma Machine hospedada, você também pode pressionar **Remover** ao lado dela na página de configuração.

## Revogar o acesso no Salesflare

Exclua a chave de API no Salesflare, em Configurações, chaves de API.
