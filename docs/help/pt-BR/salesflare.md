---
title: Salesflare CRM
area: connections
summary: Contas, contatos e oportunidades para saber quem é importante. Acessa os dados usando sua chave de API.
covers: connector:salesflare
code: assistant.py, onboarding.py
site: More sources, Connect, Remove
translated: 8051c61777603a7e
---
## O que ela lê

Suas contas, seus contatos e suas oportunidades no Salesflare, além do feed de cada conta: e-mails de colegas dos quais você não participou e reuniões com anotações.

## O que ela pode alterar

Nada. (No seu próprio computador, a configuração `join_pipelines` pode adicionar você a contas em pipelines específicos. Ela fica desativada por padrão.)

## Como conectar

1. No Salesflare, acesse [Configurações, Chaves de API](https://app.salesflare.com/#/settings/apikeys) e crie uma chave.
2. Em uma Machine hospedada: abra a página de configuração em app.themachine.computer/setup, acesse **Mais fontes**, abra Salesflare CRM, cole a chave e pressione **Conectar**.
3. No painel: acesse **Conexões**, **Clientes**, Salesflare CRM, cole a chave e pressione **Conectar**. O cartão mostra o andamento da sincronização.

## Detalhes da sincronização

Em **Conexões**, **Clientes**, o cartão do Salesflare mostra o andamento: quantas contas foram verificadas nesta rodada, quantas foram ignoradas porque o Salesflare estava lento e quantas sua chave de API não consegue acessar (**sem acesso**). Se uma rodada levar horas, pode ser que ela esteja travada.

Os indicadores mostram quantas contas foram lidas nesta semana e quantos e-mails e reuniões foram importados.

Não é preciso fazer nada se algumas contas estiverem sem acesso: o restante será importado normalmente. Se sua chave de API não conseguir acessar nenhuma conta, o cartão mostrará **Precisa da sua ajuda**: use a chave de um usuário que tenha acesso a elas. Uma nova chave começa do zero e lê novamente os dados da última semana. Se o Salesflare continuar atingindo o tempo limite, mas cada nova tentativa funcionar, o cartão mostrará que o Salesflare está **lento às vezes**.

Se o Salesflare ainda não tiver ativado o acesso ao feed por chave de API para sua equipe, o cartão avisará. Nenhum e-mail ou reunião será importado até o suporte do Salesflare ativar o acesso. A Machine verificará novamente a cada 10 minutos no primeiro dia e, depois, aproximadamente a cada hora. A sincronização será retomada automaticamente assim que o acesso funcionar.

- **Parar**: nada novo será importado até você pressionar **Começar**. A sincronização continuará de onde parou.
- **Reiniciar sincronização**: recomeça e lê novamente os dados da última semana. Nada do que já foi importado será perdido.
- **Chaves de API**: abre a página de chaves de API do Salesflare para criar uma nova chave.

## Como remover

- No painel: acesse **Conexões**, abra Salesflare, selecione **Detalhes** e pressione **Desconectar**. Os dados que já foram importados continuam na Machine.
- Em uma Machine hospedada, você também pode pressionar **Remover** ao lado de Salesflare na página de configuração.

## Revogar o acesso no Salesflare

Exclua a chave de API no Salesflare, em Configurações, Chaves de API.
