---
title: Stripe
area: connections
summary: Pagamentos recusados, contestações, cancelamentos e novas assinaturas de alto valor. A integração só lê dados.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
translated: 85e6e07cca1a8e8d
---
## O que ela lê

Eventos na sua conta do Stripe que podem exigir sua atenção: pagamentos recusados, contestações, cancelamentos e novas assinaturas de alto valor, junto com os clientes relacionados. O e-mail do cliente associa o evento à pessoa e à organização dela no [Graph](graph.md).

Um pagamento recusado informa a que se refere (um primeiro pagamento, uma renovação) e quando o Stripe tentará novamente. Ele não informa por que o cartão foi recusado: o evento do Stripe não inclui esse dado, então abra o evento no Stripe para ver o motivo.

## O que ela pode fazer

Nada no Stripe. Ela nunca faz reembolsos, tenta cobrar novamente nem altera nada. A integração pede apenas acesso de leitura, e o Stripe mostra isso antes da instalação.

## Conectar

Entre com o Stripe, de um jeito fácil:

1. No painel: **Conexões**, **Clientes**, Stripe. Ou, na página de configuração de uma Machine hospedada, em app.themachine.computer/setup: **Mais fontes**, Stripe. No seu próprio computador, primeiro vincule sua Machine à sua conta.
2. Pressione **Entrar com Stripe**. O Stripe pergunta qual conta você quer usar e mostra o que The Machine poderá ler.
3. Pressione **Instalar**. Você voltará à página anterior, e o Stripe estará conectado.

No seu próprio computador, você também pode colar uma chave restrita:

1. No Stripe, crie uma chave restrita com acesso de leitura a Events, Customers e Account, e acesso None a todo o restante.
2. Encontre o ID da sua conta (acct_...) em Settings, Business details.
3. Abra o Stripe como explicado acima (ou execute `assistant connect stripe`), abra **Ou cole uma chave restrita**, cole o ID da conta e a chave e pressione **Conectar**.

No seu próprio computador, se a opção Entrar com Stripe ainda não estiver disponível, Conexões informa isso e abre este formulário diretamente.

## Conectar uma vez para a equipe

Em um Fleet de Trabalho, um proprietário ou administrador conecta o Stripe uma vez e compartilha o acesso com a equipe:

1. Conecte o Stripe à sua Machine (acima). A caixa **Conexões compartilhadas** na guia Fleet também tem a opção **Conectar Stripe**.
2. Na guia Fleet, abra **Compartilhar Stripe**. Todas as pessoas já estarão selecionadas. Desmarque quem não deve ter acesso e pressione **Compartilhar**.

As Machines dos colegas também poderão ler os dados. Em Conexões, você pode ver quem compartilhou o acesso, e somente os administradores do Fleet podem alterá-lo ou interrompê-lo. Sua Machine renova o acesso a cada hora. Enquanto ela estiver desligada, o acesso ao Stripe pelos colegas ficará pausado. Ninguém recebe seus dados de acesso. Saiba mais em [Fleets](fleet.md).

Se um colega também conectar a mesma conta do Stripe por conta própria, os dados serão lidos uma única vez: a conexão compartilhada ficará em espera.

Não é possível compartilhar uma conexão do Stripe feita por um serviço cuja chave também dá acesso a outros aplicativos. Em vez disso, conecte o Stripe diretamente para a equipe.

## Remover

- No painel: abra **Conexões**, selecione Stripe, pressione **Detalhes** e depois **Desconectar**. O que já foi importado continuará disponível.
- Em uma Machine hospedada, a conexão com o Stripe feita por login mostra **Desconectar ↗**, que abre sua página de configuração. Pressione **Remover** ao lado dela.
- Se o acesso for compartilhado com um Fleet, primeiro pressione **Parar de compartilhar** na guia Fleet.

## Revogar o acesso no Stripe

- Se você entrou com o Stripe: no Stripe, abra Settings, Installed apps e remova The Machine.
- Se usou uma chave restrita: no Stripe, abra Developers, API keys e exclua a chave ou gere uma nova.
