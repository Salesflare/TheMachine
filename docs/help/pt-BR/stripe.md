---
title: Stripe
area: connections
summary: Pagamentos recusados, contestações, cancelamentos e novas assinaturas de alto valor. A integração só faz leitura.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
translated: 6e7ca235dc502297
---
## O que ela lê

Eventos na sua conta Stripe que podem precisar da sua atenção: pagamentos recusados, contestações, cancelamentos e novas assinaturas de alto valor, com o cliente relacionado a cada um. O e-mail do cliente conecta o evento à pessoa e à organização dela no [Graph](graph.md).

## O que ela pode fazer

Nada no Stripe. Ela nunca reembolsa, tenta cobrar de novo nem altera nada. Ela solicita apenas acesso de leitura, e o Stripe mostra isso antes de você instalar.

## Conectar

Entre com sua conta Stripe, do jeito mais fácil:

1. No painel: **Conexões**, **Clientes**, Stripe. Ou, na página de configuração de uma Machine hospedada, em app.themachine.computer/setup: **Mais fontes**, Stripe. No seu próprio computador, primeiro pareie a Machine com a sua conta.
2. Pressione **Entrar com o Stripe**. O Stripe pergunta qual conta você quer usar e mostra o que The Machine pode ler.
3. Pressione **Instalar**. Você volta para onde estava, e o Stripe fica conectado.

No seu próprio computador, você também pode colar uma chave restrita:

1. No Stripe, crie uma chave restrita com permissão de leitura para Events, Customers e Account, e sem permissões para todo o resto.
2. Encontre o ID da sua conta (acct_...) em Configurações, Business details.
3. Abra o Stripe como acima (ou execute `assistant connect stripe`), abra **Ou cole uma chave restrita**, cole o ID da conta e a chave e pressione **Conectar**.

No seu próprio computador, se a opção Entrar com o Stripe ainda não estiver disponível, Conexões avisa você e abre este formulário diretamente.

## Conectar uma vez para sua equipe

Em um Fleet de Trabalho, um proprietário ou administrador conecta o Stripe uma vez e compartilha com a equipe:

1. Conecte o Stripe na sua própria Machine (acima). A caixa **Conexões compartilhadas** da aba Fleet também tem a opção **Conectar Stripe**.
2. Na aba Fleet, abra **Compartilhar Stripe**. Todos já vêm selecionados; desmarque quem não deve ter acesso. Pressione **Compartilhar**.

As Machines dos colegas também poderão ler os dados. Em Conexões, você vê quem compartilhou o acesso, e somente os administradores do Fleet podem alterá-lo ou interrompê-lo. Sua Machine renova o acesso deles a cada hora. Enquanto ela estiver desligada, o acesso ao Stripe fica pausado. Ninguém recebe seus dados de login. Saiba mais: [Fleets](fleet.md).

Se um colega também conectar essa mesma conta Stripe por conta própria, os dados serão lidos apenas uma vez: a conexão compartilhada fica inativa.

Não é possível compartilhar uma conexão do Stripe feita por um serviço cuja chave também dá acesso a outros aplicativos. Em vez disso, conecte o Stripe diretamente para a equipe.

## Remover a conexão

- No painel: **Conexões**, abra Stripe, **Detalhes** e depois **Desconectar**. Os dados que já foram importados continuam lá.
- Em uma Machine hospedada, o Stripe conectado por login mostra **Desconectar ↗**, que abre sua página de configuração. Pressione **Remover** ao lado dele.
- Se a conexão foi compartilhada com um Fleet, primeiro selecione **Parar de compartilhar** na aba Fleet.

## Revogar o acesso no Stripe

- Se você entrou com o Stripe: no Stripe, abra Configurações, Installed apps e remova The Machine.
- Se usou uma chave restrita: no Stripe, abra Developers, API keys e exclua ou substitua a chave.
