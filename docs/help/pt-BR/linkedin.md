---
title: LinkedIn
area: connections
summary: Suas mensagens do LinkedIn, lidas no navegador da sua Machine com sessão iniciada na sua conta. Respostas só depois da sua aprovação.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py, linkedin_connections.py
site: Connect, More sources, Remove
translated: 850b91f79b9e23fc
---
## O que ela lê

Suas mensagens do LinkedIn. Ela as lê de vez em quando, durante o dia, no navegador da sua Machine, com sessão iniciada na sua conta. Ela não marca nenhuma como lida. Também chegam mensagens de conversas que você arquivou e solicitações de mensagem. Spam fica de fora.

## Cargos e empresas

Ela também mantém atualizados os cargos e as empresas das suas conexões do LinkedIn que já estão no seu Graph, usando sua lista de Conexões. Ela não abre os perfis dessas pessoas nem adiciona ninguém. Quando o cargo ou a empresa de alguém muda, isso aparece na linha do tempo, por exemplo: "Agora Head of Sales na Acme, antes Sales Lead na Acme".

O cargo vem do título do perfil, como "Head of Sales at Acme" ou "VP Sales and Strategy", nunca de um slogan. Ela encontra a pessoa pelo link do perfil ou pelo nome e pela empresa. Se não houver uma empresa para comparar, basta que o nome completo pertença a uma única pessoa no seu Graph. A página dessa pessoa também mostra há quanto tempo vocês estão conectados.

Ela lê bem devagar: uma página por vez, com intervalos de alguns minutos, algumas dezenas de páginas por dia e só durante o dia. Cerca de 3.000 conexões levam uns quatro dias. Se o LinkedIn bloquear o acesso, ela para até o dia seguinte.

## O que ela pode enviar

Uma resposta a uma mensagem ou uma nova mensagem para um perfil que você indicar, e só depois que você aprovar a tarefa. Até lá, ela só cria rascunhos.

O LinkedIn não oferece uma maneira oficial de fazer isso. Ler mensagens e enviar ocasionalmente uma mensagem aprovada por você dificilmente causará problemas. O envio em massa ou automatizado pode bloquear uma conta.

## Conectar

Em uma Machine hospedada:

1. Abra sua página de configuração em app.themachine.computer/setup e acesse **Mais fontes**.
2. Abra o LinkedIn, entre na sua conta do LinkedIn no navegador da sua Machine quando solicitado e pressione **Conectar**.

No seu próprio computador:

1. No painel, abra **Conexões**, depois **Chat** e escolha LinkedIn.
2. Escolha **Trabalho** (com a empresa) ou **Pessoal** e pressione **Conectar**.
3. Pressione **Entrar no LinkedIn** e entre no navegador da sua Machine. A conexão será feita automaticamente quando você entrar.

Ou execute `assistant connect linkedin`.

Uma segunda conta do LinkedIn terá um navegador próprio. Se o LinkedIn desconectar sua Machine, consulte [Saiu de um site](signed-out.md).

## Se o LinkedIn pedir um código

Na primeira vez que sua Machine entrar, o LinkedIn costuma enviar um código por e-mail. Digite-o na janela de entrada, em **Código**, e pressione **Entrar**. A página não muda enquanto você digita.

Se o LinkedIn voltar ao início ou nada acontecer por dois minutos, espere um minuto e pressione **Tentar de novo**. Se o LinkedIn mostrar uma verificação de robô, conclua-a no navegador da sua Machine.

## Remover

- No painel: abra **Conexões**, selecione LinkedIn, escolha **Detalhes** e depois **Desconectar**. Ela para de ler as mensagens. O que já importou continua lá.
- Em uma Machine hospedada, você também pode pressionar **Remover** ao lado do LinkedIn na página de configuração.

## Sair da conta no LinkedIn

No LinkedIn, abra Configurações, Entrar e segurança, Onde você está conectado e encerre a sessão do navegador da sua Machine.
