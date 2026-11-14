---
title: Graph da equipe
area: fleet
summary: **Experimental**. Compartilhe o trabalho com clientes com seu Fleet de trabalho, como em um CRM. Saiba o que é compartilhado, o que nunca é e como manter algo privado.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
translated: fc842bc761a3ab17
---
Em um Fleet de trabalho, sua Machine pode compartilhar o trabalho com clientes com as Machines dos seus colegas, como em um CRM compartilhado. Esse recurso é **Experimental** e vem desativado.

## Ativar

Um admin ativa **Compartilhar o Graph neste Fleet** em **O que é compartilhado** e confirma que a empresa pode compartilhar esses e-mails e avisou as pessoas. Todos veem se o recurso está ativado.

Exigir o e-mail ou o calendário de trabalho de todos também ativa o recurso. Depois, cada pessoa escolhe o que mais compartilhar em **Suas conexões**. O primeiro compartilhamento de uma pessoa que acabou de entrar na equipe espera uma hora, para que ela possa manter algo privado antes.

## Suas conexões

**Suas conexões** em **O que é compartilhado** lista cada conexão com uma chave. As conexões de trabalho no domínio do Fleet vêm ativadas. As de outro domínio de empresa vêm desativadas e mostram “Outra empresa, não compartilhada”. As conexões pessoais nunca são compartilhadas. Ao desativar uma conexão, o que foi compartilhado por ela deixa de ser compartilhado.

O calendário de outra pessoa que você acessa com sua própria conta aparece com o nome dela, como pessoal.

Mesmo quando uma conexão está ativada, cada conversa é classificada separadamente. O Slack da sua empresa conta apenas como conversa com colegas. Só uma conversa do Slack Connect com outra empresa pode ser trabalho com clientes. Conversas pessoais, só com colegas, confidenciais e automatizadas não são compartilhadas, a menos que você compartilhe uma delas.

## Exigido pelo Fleet

Um admin pode exigir o **E-mail de trabalho** e o **Calendário de trabalho** de todos no domínio do Fleet, em **Exigido pelo Fleet**, depois de confirmar que a empresa avisou as pessoas. O e-mail de trabalho pertence à empresa, como em qualquer CRM. As conexões obrigatórias mostram “Exigido pelo” seu Fleet e não podem ser desativadas. As conversas que você mantém privadas continuam privadas.

## O que é compartilhado com a equipe

- Conversas com clientes: e-mails de trabalho com pessoas de fora da sua empresa, incluindo anexos.
- Pessoas, organizações e projetos de trabalho, com uma linha do tempo resumida. Na **Linha do tempo** de uma página, **Equipe** mostra cada evento uma vez, no idioma em que a Machine de um colega o registrou, junto com todas as pessoas de quem veio: “via Sam, Kim e Lee”.
- Uma cópia pequena do logotipo de uma organização e da foto de trabalho de uma pessoa, obtidas em uma busca, no Slack, LinkedIn, X, Salesflare ou Microsoft. Nunca são compartilhadas imagens dos contatos do Google, WhatsApp, Telegram ou Facebook, nem imagens que você alterou ou removeu.
- Em um quadro da equipe, as reuniões, notas do Zoom, conversas do Intercom e chats de um projeto. Conversas confidenciais, como negociações, e chats só com colegas não são compartilhados.
- Contagens e datas do [resumo da equipe](fleet.md#brief-requests) de um colega.
- Respostas quando um colega pergunta quem conhece alguém ou quer saber o contexto de uma reunião. Consulte [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).
- [Aprendizados da equipe](fleet.md#team-learnings): como a equipe trabalha, sem nomes nem detalhes de clientes.

## O que não é compartilhado automaticamente

- Conversas confidenciais: compra ou venda de uma empresa, investimentos, negociações, RH e contratação, assuntos jurídicos, saúde, dinheiro e segurança. Nem mesmo o fato de existirem é compartilhado.
- E-mails automatizados: recibos, faturas, alertas, newsletters e cobranças de fornecedores.
- Conversas só com colegas, e-mails pessoais e qualquer coisa de uma conta pessoal. Conteúdo pessoal nunca é compartilhado, nem quando você toca em Equipe.
- Tudo o que você marcou como **Manter privado**, além de quadros e projetos definidos como Apenas você.
- Alguém que é pessoal para você, como sua família ou seus amigos, e os e-mails dessa pessoa. Um projeto em que ela participa ainda é compartilhado com o quadro, mas sem ela.

Cada conversa é avaliada pelo assunto, e a avaliação pode estar errada. Confira o que seria compartilhado e use **Manter privado** para corrigir. Se você compartilhar uma conversa com a equipe ou com pessoas específicas, isso substitui a classificação de confidencial. Confira quem terá acesso.

## Compartilhar um quadro com pessoas específicas

No menu **⋯** de um quadro, toque em **Compartilhar quadro…** e escolha colegas. Só essas pessoas recebem os projetos do quadro com as linhas do tempo completas: e-mails, reuniões e notas do Zoom, conversas do Intercom, chats, tarefas e alterações. Conversas confidenciais, como negociações, também são compartilhadas.

Conversas pessoais e só com colegas continuam privadas. O mesmo vale para sua família e seus amigos, e-mails automatizados e conexões que você não selecionou.

- Um projeto adicionado ao quadro depois também é compartilhado. Se for removido do quadro, deixa de ser compartilhado.
- Se você remover alguém ou não escolher ninguém, o conteúdo deixa de ser compartilhado com essa pessoa e é removido da Machine dela.
- Para compartilhar uma conversa com pessoas específicas, toque no marcador dela e depois em **Compartilhar com…**. Isso pode incluir e-mails de trabalho confidenciais ou automatizados, mas nunca conversas pessoais ou só com colegas.

## Em caso de dúvida, aguarde

Quando sua Machine não tem certeza, ela não compartilha. Essas conversas ficam em **Compartilhar estes?**, agrupadas por tipo, como “Conversas com parceiros e sobre anúncios”, cada uma com uma sugestão:

- **Compartilhar com a equipe**: todas as pessoas no Fleet.
- **Compartilhar com…**: só os colegas que você escolher, como alguém do quadro para conversas com investidores.
- **Manter privado**: o conteúdo continua só com você.

Com um toque, você decide por um grupo inteiro. Abra um grupo para desmarcar as conversas que quiser decidir uma por uma.

Conversas sobre comprar, vender ou investir em uma empresa, e assuntos do conselho, são confidenciais e não aparecem aqui para você decidir. O trabalho cotidiano com uma empresa parceira é trabalho com clientes.

## Antes do primeiro compartilhamento

Sua primeira seleção é compartilhada automaticamente uma hora depois que sua Machine avisa você. Durante essa hora, abra **Fleet** e depois **O que é compartilhado** para ver, por organização, as conversas com clientes que seriam compartilhadas. Toque em **Manter privado** em qualquer uma delas ou em **Compartilhar agora** para compartilhar na hora. Os admins veem quem ainda não compartilhou.

## O que é compartilhado

**Fleet** › **O que é compartilhado** mostra tudo: contagens por tipo, cada conversa compartilhada e o motivo, as conversas em **Compartilhar estes?** e o que você mantém privado. Toque no assunto para ler a conversa. **Configurações** e o marcador de cada conversa também levam a esta página.

Uma nova conversa com um cliente espera uma hora antes de ser compartilhada, para que você tenha tempo de mudar de ideia.

## Parar de compartilhar

Toque no marcador **Equipe** de uma conversa e depois em **Parar de compartilhar**. A Machine de cada colega apaga a conversa, os anexos e as entradas da linha do tempo, assim que voltar a ficar online. Alguém pode já ter lido o conteúdo.

Ao marcar uma pessoa, organização ou projeto como **Manter privado**, tudo o que foi compartilhado deixa de ser compartilhado.

Se você mantiver privadas duas conversas com a mesma empresa, sua Machine perguntará uma vez se você quer sempre manter essa empresa privada.

## Quem pode ver

Somente as Machines dos seus colegas. O conteúdo é criptografado de ponta a ponta. The Machine Network o repassa, mas não consegue lê-lo.

## Entrada de pessoas e novos dispositivos

Um admin autoriza cada pessoa uma vez. O pedido aparece em **Tarefas** para todos os admins, e vale a primeira resposta. Depois disso, não é preciso aprovar o compartilhamento novamente.

Até lá, o Graph e o Fleet da nova pessoa mostram quais admins ainda precisam responder. **Meus** e **Equipe** aparecem alguns segundos depois da aprovação, sem precisar atualizar a página.

Uma nova Machine de alguém que já está na equipe recebe o Graph da equipe após 24 horas. Enquanto isso, admins podem tocar em **Não é dessa pessoa** para impedir o compartilhamento.

## Quando alguém sai

A partir desse momento, a pessoa não recebe mais nada. O que ela compartilhou continua com a equipe. Um admin também pode **Retirar** alguém e **Compartilhar de novo** mais tarde.

## Desativar para todos

Um admin desativa **Compartilhar o Graph neste Fleet** em **O que é compartilhado**. Nada mais é compartilhado.

**Desativar** mantém o que os colegas já receberam. **Desativar e remover os dados compartilhados** faz todas as Machines apagarem esse conteúdo. Quando o compartilhamento for ativado novamente, cada pessoa confere tudo antes.

## Parar de compartilhar seu próprio trabalho

Desative suas conexões em **Suas conexões**, a menos que o Fleet as exija. O que elas compartilharam deixa de ser compartilhado.

Veja também [Fleets](fleet.md) e [Segurança e privacidade](security-and-privacy.md).
