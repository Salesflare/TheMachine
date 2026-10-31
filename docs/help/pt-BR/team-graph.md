---
title: Graph da equipe
area: fleet
summary: Experimental. Compartilhe o trabalho com clientes com seu Fleet de Trabalho, como um CRM. O que vai, o que nunca vai e como manter algo privado.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
---
Em um Fleet de Trabalho, sua Machine pode compartilhar seu trabalho com clientes com as Machines dos seus colegas, como um CRM compartilhado. É **Experimental**: novo e ainda mudando, por isso começa desligado.

## Ative

Um admin ativa **Compartilhar o Graph neste Fleet** em **O que é compartilhado** e confirma que a empresa pode compartilhar esses e-mails e já avisou as pessoas dela. Todos veem se está ativado. Um Fleet que já compartilhava antes continua ativado. Depois, cada pessoa confere o que iria e toca em **Começar agora**. Nada vai antes disso.

## Suas conexões

**Suas conexões**, em **O que é compartilhado**, lista cada conexão com um botão. As de trabalho no domínio do próprio Fleet começam ligadas. Uma no domínio de outra empresa começa desligada, mesmo sendo uma conta de trabalho: ela diz "Outra empresa, não compartilhada". Você pode ligar. As pessoais nunca vão. Desligar uma conexão retira o que ela compartilhou.

A agenda de outra pessoa que você lê pelo seu próprio login aparece com o nome dela, como uma conexão pessoal.

Dentro de uma conexão ligada, cada conversa ainda é separada. O Slack da sua própria empresa conta como só entre colegas, mensagens diretas também: só uma conversa do Slack Connect com outra empresa pode ser uma conversa com cliente. Conversas pessoais e só entre colegas ficam de fora. E-mails sensíveis e automáticos ficam fora do compartilhamento automático. Suas escolhas explícitas de compartilhamento podem passar por cima dessas classificações.

## Exigido pelo Fleet

Um admin pode exigir o **E-mail de trabalho** e o **Calendário de trabalho** de todos no domínio do próprio Fleet, em **Exigido pelo Fleet**, depois de confirmar que a empresa avisou as pessoas dela. Os e-mails de trabalho pertencem à empresa, como em qualquer CRM. Essas conexões passam a mostrar "Exigido por" seu Fleet e não podem ser desligadas. As conversas que você mantém privadas continuam privadas.

## O que vai para a equipe

- Conversas com clientes: e-mails com pessoas de fora da sua empresa sobre trabalho, com os anexos.
- Pessoas, organizações e projetos de trabalho, com uma linha do tempo curta.
- Em um quadro de Equipe, também as reuniões, as notas do Zoom, as conversas do Intercom e os chats de um projeto, por estarem no quadro. Os sensíveis, como negócios, ficam de fora.

## Fora do compartilhamento automático

- Conversas sensíveis: compra ou venda de uma empresa, investimentos, avaliações, negociações, RH, contratações e recrutadores, jurídico, saúde, dinheiro, segurança. Nem mesmo a existência delas vai.
- E-mails automáticos: recibos, faturas, alertas, newsletters e as contas da sua própria empresa com os fornecedores dela.
- Conversas internas (só entre colegas), e-mails pessoais e qualquer coisa de uma conta pessoal. O que é pessoal nunca vai, nem quando você toca em Equipe.
- Tudo o que você marcou com **Manter privado**, e quadros e projetos definidos como Só você.

Cada conversa é avaliada sozinha, pelo assunto dela. A classificação pode errar: confira o que iria e use Manter privado para corrigir. Sua escolha explícita de Equipe ou um compartilhamento com colegas específicos pode passar por cima de uma classificação sensível. Confira os destinatários antes de compartilhar.

## Compartilhe um quadro com pessoas escolhidas

No menu **⋯** de um quadro, toque em **Compartilhar quadro…** e escolha os colegas. Só eles recebem os projetos do quadro com as linhas do tempo completas: conversas de e-mail, reuniões e as notas do Zoom delas, conversas do Intercom, chats, tarefas e mudanças. Os sensíveis também vão, como negócios.

Conversas pessoais e só entre colegas ficam de fora, assim como pessoas da sua Família ou dos seus Amigos e os e-mails automáticos quando só o quadro é compartilhado. Conexões que você não selecionou também ficam de fora.

- Um projeto adicionado ao quadro depois também vai. Um que sai do quadro é retirado.
- Tire alguém, ou não escolha ninguém, e tudo é retirado da Machine dessa pessoa.
- Uma única conversa também pode ir para pessoas escolhidas: toque no rótulo dela e depois em **Compartilhar com…**. Essa escolha explícita pode incluir e-mails de trabalho sensíveis ou automáticos. Conversas pessoais e só entre colegas não podem ser compartilhadas.

## Na dúvida, ela espera

Quando sua Machine não tem certeza, ela não compartilha. Essas conversas esperam em **Compartilhar estes?**, agrupadas pelo que são (como "Trocas com parceiros e listagens"), cada grupo com uma escolha sugerida:

- **Compartilhar com a equipe** vai para todos na Fleet.
- **Compartilhar com…** vai só para quem você escolher, por exemplo um membro do conselho para conversas com investidores. O resto da equipe não recebe.
- **Manter privado** deixa com você.

Um toque decide o grupo inteiro. Abra um grupo para ver as conversas e desmarque as que quiser decidir separadamente.

Conversas sobre comprar, vender ou investir em uma empresa e assuntos do conselho contam como sensíveis, então não esperam aqui. Listagens, integrações e o resto do trabalho do dia a dia com uma empresa parceira são trabalho de cliente.

## Antes do primeiro compartilhamento

Abra **Fleet** e depois **O que é compartilhado**. Ali aparecem as conversas com clientes que iriam, por organização. Toque em **Manter privado** em qualquer uma delas e depois em **Começar agora**.

Até você começar, sua Machine lembra você a cada poucos dias, durante seu horário de trabalho. Os admins veem quem ainda não começou.

## O que é compartilhado

**Fleet** › **O que é compartilhado** mostra tudo em um só lugar: totais por tipo, cada conversa compartilhada com o motivo, as que esperam em **Compartilhar estes?** e o que você mantém privado. **Configurações** tem um atalho, e o rótulo de cada conversa também. Toque no assunto de uma conversa para ler.

Uma nova conversa com cliente espera uma hora antes de ir, para dar tempo de você mudar de ideia.

## Pare de compartilhar algo

Toque no rótulo **Equipe** de uma conversa e depois em **Parar de compartilhar**. Sua Machine avisa a Machine de cada colega, e cada uma exclui a conversa, os anexos e as linhas dela na linha do tempo. Uma Machine que estava desligada faz isso quando volta. Alguém pode já ter lido.

**Manter privado** em uma pessoa, organização ou projeto para de compartilhar tudo dele do mesmo jeito.

Mantenha privadas duas conversas com a mesma empresa e sua Machine pergunta uma vez: manter sempre privadas as conversas dessa empresa?

## Quem vê

Só as Machines dos seus colegas. Tudo é criptografado de ponta a ponta, selado para a Machine de cada colega. The Machine Network só repassa e não consegue ler.

## Entrada e novos dispositivos

Um admin deixa cada pessoa entrar no Fleet uma vez. Depois disso, compartilhar com ela não precisa de mais nenhum OK. O pedido aparece em **Sugestões** para cada admin, e a primeira resposta vale para a equipe toda. Membros nunca recebem.

Uma nova Machine de alguém que já está no Fleet recebe o Graph da equipe depois de 24 horas. Enquanto isso, os admins veem essa Machine e podem tocar em **Não é dessa pessoa** para deixá-la de fora.

## Quando alguém sai

A pessoa não recebe mais nada a partir desse momento. O que ela compartilhou fica com a equipe. Um admin também pode usar **Retirar** com alguém e **Compartilhar de novo** depois.

## Desative para todos

Um admin pode desativar **Compartilhar o Graph neste Fleet** em **O que é compartilhado**. Todos veem se está ativado. Quando está desativado, nada novo vai.

**Desativar** mantém o que já foi para as Machines dos colegas. **Desativar e remover os dados compartilhados** faz cada Machine excluir o que recebeu. Quando o compartilhamento volta, cada pessoa confere tudo de novo antes.

## Pare de compartilhar seu próprio trabalho

Desligue suas conexões em **Suas conexões**, a menos que o Fleet exija. O que elas compartilharam é retirado.

Veja também [Fleets](fleet.md) e [Segurança e privacidade](security-and-privacy.md).
