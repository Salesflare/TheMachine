---
title: Stripe
area: connections
summary: Pagamentos que falharam, disputas, cancelamentos e grandes assinaturas novas. Ele só lê.
covers: connector:stripe
code: connectors/stripe.py, shared_connectors.py
site: Sign in with Stripe, Connect, More sources, Share Stripe, Connect Stripe, Remove
---
## O que ele lê

Eventos na sua conta do Stripe que podem precisar de você: pagamentos que falharam, disputas, cancelamentos e grandes assinaturas novas, com o cliente a que pertencem. O e-mail de um cliente liga o evento a essa pessoa e à organização dela no [Graph](graph.md).

## O que ele pode fazer

Nada no Stripe. Ele nunca escreve, reembolsa ou tenta de novo um pagamento. O app Stripe da The Machine pede ao Stripe só permissões de leitura, e o Stripe mostra essas permissões antes de você instalar.

## Conectar

Entre com o Stripe, o jeito fácil:

1. No painel: **Conexões**, **+ Adicionar**, Stripe. Ou na página de configuração de uma Machine hospedada, em app.themachine.computer/setup: **Mais fontes**, Stripe. No seu próprio computador, pareie-o primeiro com sua conta.
2. Clique em **Entrar com o Stripe**. O Stripe pergunta qual conta e mostra o que The Machine pode ler.
3. Clique em **Instalar**. Você volta para onde começou, e o Stripe está conectado.

Ou cole uma chave restrita:

1. No Stripe, crie uma chave restrita com Read em Events, Customers e Account, e None em todo o resto.
2. Encontre o ID da sua conta (acct_...) em Settings, Business details.
3. Abra Stripe como acima (ou rode `assistant connect stripe`), abra **Ou cole uma chave restrita**, cole o ID da conta e a chave, depois clique em **Conectar**.

No seu próprio computador, se entrar com Stripe ainda não estiver disponível, + Add avisa e abre este formulário na hora.

## Conectar uma vez para sua equipe

Em um Fleet de Trabalho, um proprietário ou admin conecta o Stripe uma vez e compartilha com a equipe:

1. Conecte o Stripe na sua própria Machine (acima). A caixa **Conexões compartilhadas** da aba Fleet também tem **Conectar Stripe**.
2. Na aba Fleet, abra **Compartilhar Stripe**. Todos vêm marcados; desmarque quem não deve receber. Clique em **Compartilhar**.

As Machines dos colegas também leem, só leitura. Em Conexões aparece quem compartilhou, e só os admins do Fleet podem mudar ou parar. Sua Machine renova o acesso deles a cada hora, então enquanto ela fica desligada por mais tempo, o Stripe deles pausa até ela voltar. Ninguém recebe o seu login. Detalhes: [Fleets](fleet.md).

Uma conexão do Stripe que passa por outro serviço, com uma chave só para muitas conexões, não pode ser compartilhada: essa chave abre mais que o Stripe. Conecte o Stripe sozinho para a equipe.

## Remover

- No painel: **Conexões**, abra Stripe, **Detalhes** e depois **Desconectar**. O que ele já trouxe continua.
- Em uma Machine hospedada, você também pode clicar em **Remover** ao lado dele na sua página de configuração.
- Compartilhado com um Fleet: primeiro **Parar de compartilhar** na aba Fleet.

## Revogar no Stripe

- Entrou com o Stripe: no Stripe, abra Settings, Installed apps, e remova The Machine.
- Chave restrita: no Stripe, abra Developers, API keys, e exclua ou troque a chave.
