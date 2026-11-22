---
title: LinkedIn
area: connections
summary: Suas mensagens do LinkedIn, lidas no navegador da sua Machine, conectado à sua conta. As respostas só são enviadas depois que você aprova.
covers: connector:linkedin
code: connectors/linkedin.py, integrations/linkedin_inbox.py, linkedin_connections.py
site: Connect, More sources, Remove
translated: bc67fbc21c77a97a
---
## O que ela lê

Suas mensagens do LinkedIn. Ela as lê de vez em quando, enquanto você está acordado, no navegador da sua Machine, conectado à sua conta. Não marca nenhuma mensagem como lida. Mensagens de conversas arquivadas e solicitações de mensagem também são incluídas; spam fica de fora.

## Cargos e empresas

Ela também mantém atualizados os cargos e as empresas das suas conexões do LinkedIn que já estão no seu Graph, usando sua lista de Conexões. Ela não abre os perfis nem adiciona pessoas novas. Quando o cargo ou a empresa de alguém muda, isso aparece na linha do tempo, por exemplo: "Agora é Head of Sales na Acme, antes era Sales Lead na Acme".

O cargo vem do título do perfil, como "Head of Sales na Acme" ou "VP Sales and Strategy", nunca de um slogan. Ela identifica a pessoa pelo link do perfil ou pelo nome e pela empresa. Se não houver uma empresa para comparar, basta que o nome completo pertença a uma única pessoa no seu Graph. A página da pessoa também mostra há quanto tempo vocês estão conectados.

Ela lê bem devagar: uma página por vez, com alguns minutos de intervalo, algumas dezenas de páginas por dia e somente durante o dia. Cerca de 3.000 conexões levam aproximadamente quatro dias. Se o LinkedIn não permitir, ela para até o dia seguinte.

## O que ela pode enviar

Uma resposta a uma mensagem ou uma nova mensagem para um perfil que você indicar, e somente depois que você aprovar na tarefa. Até lá, ela só cria rascunhos.

O LinkedIn não oferece uma forma oficial de fazer isso. Ler mensagens e enviar ocasionalmente uma mensagem que você aprovou dificilmente vai causar problemas; envios em massa ou automatizados podem levar ao bloqueio da conta.

## Conectar

1. No painel, abra **Conexões**, depois **Chat**, e escolha LinkedIn.
2. Escolha **Trabalho** (com a empresa) ou **Pessoal**, depois pressione **Conectar**.
3. Pressione **Entrar no LinkedIn** e entre na sua conta pelo navegador da sua Machine. A conexão é feita automaticamente quando você entra.

Em uma Machine hospedada, você também pode usar a página de configuração em app.themachine.computer/setup: acesse **Mais fontes**, abra o LinkedIn, entre na sua conta quando solicitado e pressione **Conectar**. No seu próprio computador, `assistant connect linkedin` faz o mesmo em um terminal.

Uma segunda conta do LinkedIn tem um navegador próprio. Se o LinkedIn desconectar sua Machine, consulte [Um site desconectou sua Machine](signed-out.md).

## Se o LinkedIn pedir um código

Na primeira vez que sua Machine entra na conta, o LinkedIn costuma enviar um código por e-mail. Digite-o na janela de entrada, em **Código**, e pressione **Entrar**. A página não muda enquanto você digita.

Se o LinkedIn voltar ao início ou nada acontecer por dois minutos, espere um minuto e pressione **Tentar de novo**. Se o LinkedIn mostrar uma verificação de robô, conclua-a no navegador da sua Machine.

## Remover

- No painel: abra **Conexões**, selecione LinkedIn, abra **Detalhes** e pressione **Desconectar**. Ela para de ler as mensagens. O que já foi importado permanece.
- Em uma Machine hospedada, você também pode pressionar **Remover** ao lado do LinkedIn na página de configuração.

## Sair da conta no LinkedIn

No LinkedIn, abra **Configurações**, **Entrar e segurança**, **Onde você está conectado** e encerre a sessão do navegador da sua Machine.
