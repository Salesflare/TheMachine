---
title: Intercom
area: connections
summary: Conversas com clientes no seu espaço de trabalho do Intercom. Ela só responde depois que você envia, como se fosse você.
covers: connector:intercom
code: connectors/intercom.py, onboarding.py
site: Sign in with Intercom, More sources, Remove
translated: 5a6938dd6c220a43
---
## O que ela lê

As conversas com clientes no seu espaço de trabalho do Intercom: as dos últimos 7 dias quando você conecta a conta e, depois, as novas que chegam. Ela também lê a qual espaço de trabalho e colega de equipe o login pertence.

## O que ela pode fazer

Com seu próprio **Entrar com Intercom**, ela pode responder a uma conversa como se fosse você, mas só depois que você clicar em **Enviar** para aquele texto exato. Ela nunca atribui, encerra ou marca conversas, nem escreve notas. Uma conexão do Intercom compartilhada com você pelo seu Fleet só permite leitura.

## Tarefas do Intercom

Uma tarefa do Intercom mostra o cliente, e **Ler mensagem** abre a conversa com um link para ela no Intercom. Cada mensagem aparece abaixo do nome de quem escreveu: o cliente de um lado, sua equipe e o bot dela do outro, inclusive quando um colega de equipe ou uma campanha iniciou a conversa. A resposta é enviada nessa conversa, a menos que você peça para enviá-la por e-mail.

Só viram tarefas as conversas atribuídas a você ou ainda sem responsável. Quando um colega de equipe assume uma conversa no Intercom, a tarefa correspondente é encerrada automaticamente, com a opção **Desfazer**. Em uma conexão do Intercom compartilhada com você, suas conversas são as atribuídas ao colega de equipe em cujo nome você escreve.

Uma tarefa do Intercom também é encerrada automaticamente quando alguém da equipe encerra a conversa no Intercom ou responde e o cliente não escreve mais, caso a tarefa pedisse apenas uma resposta. Isso também vale quando você respondeu pouco antes de a tarefa chegar, antes que a The Machine lesse sua resposta. Uma nota, um adiamento ou uma resposta do bot nunca contam.

Quando sua Machine não pode responder no Intercom (porque a conexão compartilhada só permite leitura, as respostas não estão ativadas ou a conta não está conectada), o rascunho é enviado por e-mail. A tarefa explica o motivo e pergunta **Enviar por e-mail em vez disso?** Para responder no Intercom, toque em **Conecte seu próprio Intercom** na tarefa e faça login. A tarefa é então criada novamente como uma resposta no Intercom. Nada é enviado antes de você confirmar.

Sua conexão própria do Intercom e uma conexão compartilhada com você para o mesmo espaço de trabalho não leem as conversas ao mesmo tempo: a compartilhada fica inativa, e as conversas dela passam para a sua, uma única vez cada.

## Conectar

1. No painel: **Conexões**, **Clientes**, Intercom. Ou, na página de configuração de uma Machine hospedada, em app.themachine.computer/setup: **Mais fontes**, Intercom. No seu próprio computador, primeiro emparelhe a Machine com sua conta.
2. Clique em **Entrar com Intercom**.
3. Autorize The Machine (criada pela Salesflare) no Intercom. Você voltará ao ponto de partida.

Ao fazer login em outro espaço de trabalho, você adiciona uma segunda conta do Intercom.

O Intercom sempre é considerado trabalho, para a empresa indicada pelo nome do espaço de trabalho.

## Remover

- No painel: **Conexões**, abra o Intercom, **Detalhes** e clique em **Desconectar**. Ela para de ler as conversas. O que já foi importado continua disponível.
- Em uma Machine hospedada, você também pode clicar em **Remover** ao lado do Intercom na página de configuração.

## Desinstalar no Intercom

No Intercom, abra **Configurações**, **Apps**, **Aplicativos instalados** e remova The Machine.
