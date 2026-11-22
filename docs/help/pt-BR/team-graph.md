---
title: Graph da equipe
area: fleet
summary: Experimental. Compartilhe o trabalho com clientes com seu Fleet de Trabalho, como em um CRM. Saiba o que é compartilhado, o que nunca é e como manter algo privado.
covers: team-graph
code: shared_graph.py, fleet_trust.py, dashboard.html
order: 2
translated: 9788be6d2d5e3fa6
---
Em um Fleet de Trabalho, sua Machine pode compartilhar o trabalho com clientes com as Machines dos seus colegas, como em um CRM compartilhado. Esse recurso é **Experimental** e vem desativado.

## Ativar

Um administrador ativa **Compartilhar o Graph neste Fleet** em **O que é compartilhado** e confirma que a empresa pode compartilhar esse e-mail e já informou as pessoas. Todo mundo vê se o recurso está ativado.

Exigir o e-mail de trabalho ou o calendário de trabalho de todos também ativa o recurso. Depois, cada pessoa escolhe o que mais compartilhar em **Suas conexões**. O primeiro compartilhamento de uma pessoa que acabou de entrar na equipe fica aguardando uma hora, para que ela possa manter algo privado antes.

## Suas conexões

**Suas conexões** em **O que é compartilhado** mostra cada conexão com uma chave. As conexões de trabalho no domínio do seu Fleet vêm ativadas. As de outro domínio empresarial vêm desativadas e mostram “Outra empresa, não compartilhada”. As conexões pessoais nunca são compartilhadas. Ao desativar uma conexão, você desfaz o que foi compartilhado por ela.

O calendário de outra pessoa que você acessa com seu próprio login aparece com o nome dele, como pessoal.

Mesmo dentro de uma conexão ativada, cada conversa é classificada. O Slack da sua empresa conta apenas como conversa entre colegas. Só uma conversa do Slack Connect com outra empresa pode ser trabalho com clientes. Conversas pessoais, apenas entre colegas, confidenciais e automatizadas ficam de fora, a menos que você compartilhe alguma delas.

## Exigido pelo Fleet

Em **Exigido pelo Fleet**, um administrador pode exigir o **E-mail de trabalho** e o **Calendário de trabalho** de todos no domínio do Fleet, depois de confirmar que a empresa já informou as pessoas. O e-mail de trabalho pertence à empresa, como em qualquer CRM. As conexões exigidas mostram “Exigido pelo” seu Fleet e não podem ser desativadas. As conversas que você mantiver privadas continuam privadas.

## O que é compartilhado com a equipe

- Conversas com clientes: e-mails de trabalho com pessoas de fora da sua empresa, incluindo anexos.
- Pessoas, organizações e projetos de trabalho, com uma linha do tempo resumida. Na **Linha do tempo** de uma página, **Equipe** mostra cada evento uma vez, no seu idioma quando a Machine de um colega o registrou assim, com todas as pessoas de quem veio: “via Sam, Kim e Lee”.
- Uma cópia pequena do logotipo de uma organização e da foto de trabalho de uma pessoa: obtida por uma busca, pelo Slack, LinkedIn, X, Salesflare ou Microsoft. Nunca uma foto dos contatos do Google, WhatsApp, Telegram ou Facebook, nem uma foto que você alterou ou removeu.
- Em um quadro da Equipe, reuniões de projetos, notas do Zoom, conversas do Intercom e chats. Conversas confidenciais, como negociações, e chats apenas entre colegas ficam de fora.
- Contagens e datas do [resumo da equipe](fleet.md#brief-requests) de um colega.
- Respostas quando um colega pergunta quem conhece alguém ou quer contexto sobre uma reunião. Consulte [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).
- [Aprendizados da equipe](fleet.md#team-learnings): como a equipe trabalha, sem nomes nem detalhes de clientes.

## O que fica de fora do compartilhamento automático

- Conversas confidenciais: compra ou venda de empresas, investimentos, negociações, RH e contratação, assuntos jurídicos, saúde, dinheiro e segurança. Nem mesmo o fato de existirem é compartilhado.
- E-mails automatizados: recibos, faturas, alertas, newsletters e cobranças de fornecedores.
- Conversas apenas entre colegas, e-mails pessoais e qualquer coisa de uma conta pessoal. O que é pessoal nunca é compartilhado, nem mesmo quando você toca em Equipe.
- Tudo o que você marcou como **Manter privado**, além de quadros e projetos definidos como visíveis só para você.
- Pessoas que são pessoais para você, como sua Família ou seus Amigos, e os e-mails delas. Um projeto em que elas participam ainda é compartilhado com o quadro, mas sem elas.

Cada conversa é classificada de acordo com o assunto, e a classificação pode estar errada. Confira o que seria compartilhado e use Manter privado para corrigir. Se você compartilhar uma conversa com a equipe ou com pessoas específicas, isso substitui uma classificação como confidencial. Confira quem terá acesso.

## Compartilhar um quadro com pessoas específicas

No menu **⋯** de um quadro, toque em **Compartilhar quadro…** e escolha colegas. Só essas pessoas recebem os projetos do quadro com as linhas do tempo completas: e-mails, reuniões e notas do Zoom, conversas do Intercom, chats, tarefas e movimentações. Conversas confidenciais, como negociações, também são compartilhadas.

Conversas pessoais e apenas entre colegas ficam de fora, assim como sua Família e seus Amigos, e-mails automatizados e conexões que você não selecionou.

- Um projeto adicionado ao quadro depois também será compartilhado. Se for movido para fora do quadro, o compartilhamento será desfeito.
- Remova alguém ou não escolha ninguém, e o conteúdo será removido da Machine dessa pessoa.
- Para compartilhar uma conversa com pessoas específicas, toque no rótulo dela e depois em **Compartilhar com…**. Isso pode incluir e-mails de trabalho confidenciais ou automatizados, mas nunca conversas pessoais ou apenas entre colegas.

## Em dúvida? Aguarde

Quando sua Machine não tem certeza, ela não compartilha. Essas conversas ficam em **Compartilhar estes?**, agrupadas por tipo, como “Trocas com parceiros e anúncios”, e cada grupo inclui uma sugestão:

- **Compartilhar com a equipe**: todo mundo no Fleet.
- **Compartilhar com…**: só os colegas que você escolher, como alguém do quadro para conversas sobre investidores.
- **Manter privado**: o conteúdo fica só com você.

Uma única ação decide o grupo inteiro. Abra um grupo para desmarcar as conversas que você quer decidir uma por uma.

Conversas sobre comprar, vender ou investir em uma empresa, além de assuntos do conselho, são confidenciais e não ficam aguardando aqui. O trabalho cotidiano com uma empresa parceira é trabalho com clientes.

## Antes do primeiro compartilhamento

Sua Machine faz o primeiro compartilhamento automaticamente, uma hora depois de avisar você. Durante esse período, abra **Fleet** e depois **O que é compartilhado** para ver, por organização, as conversas com clientes que seriam compartilhadas. Toque em **Manter privado** em qualquer uma delas ou em **Compartilhar agora** para compartilhar na hora. Os administradores veem quem ainda não compartilhou.

## O que é compartilhado

**Fleet** › **O que é compartilhado** mostra tudo: contagens por tipo, cada conversa compartilhada e o motivo, as conversas em **Compartilhar estes?** e o que você mantém privado. Toque em um assunto para ler. **Configurações** e o rótulo de cada conversa também levam a esta página.

Uma nova conversa com clientes aguarda uma hora antes de ser compartilhada, para que você tenha tempo de mudar de ideia. Depois, ela é compartilhada em até meia hora. O compartilhamento desfeito e a ação **Manter privado** chegam à equipe em até 5 minutos.

## Parar de compartilhar

Toque no rótulo **Equipe** de uma conversa e depois em **Parar de compartilhar**. A Machine de cada colega exclui a conversa, os anexos e os itens da linha do tempo, ou faz isso quando voltar a ficar on-line. Alguém pode já ter lido o conteúdo.

Ao marcar uma pessoa, organização ou projeto como **Manter privado**, você desfaz o compartilhamento de todo o conteúdo relacionado.

Mantenha privadas duas conversas com a mesma empresa e sua Machine perguntará uma vez se você quer sempre manter essa empresa privada.

## Quem pode ver

Somente as Machines dos seus colegas. O conteúdo é criptografado de ponta a ponta. A The Machine Network transmite o conteúdo, mas não consegue lê-lo.

## Entrar e usar novos dispositivos

Um administrador permite a entrada de cada pessoa uma vez. O pedido aparece em **Tarefas** para todos os administradores, e vale a primeira resposta. Depois disso, o compartilhamento não precisa de novas aprovações.

Até lá, o Graph e o Fleet da pessoa nova mostram quais administradores ainda precisam aprovar a entrada. **Meus** e **Equipe** aparecem alguns segundos depois da aprovação, sem precisar atualizar a página.

Uma Machine nova de alguém que já faz parte da equipe recebe o Graph da equipe após 24 horas. Enquanto isso, os administradores podem tocar em **Não é dessa pessoa** para impedir o compartilhamento.

## Quando alguém sai

A pessoa deixa de receber conteúdo novo a partir desse momento. O que ela compartilhou continua com a equipe. Um administrador também pode **Retirar** alguém e **Compartilhar de novo** depois.

## Desativar para todo mundo

Um administrador desativa **Compartilhar o Graph neste Fleet** em **O que é compartilhado**. Nada mais será compartilhado.

**Desativar** mantém o que os colegas já têm. **Desativar e remover os dados compartilhados** faz com que todas as Machines excluam esse conteúdo. Quando o compartilhamento for ativado novamente, cada pessoa confere tudo mais uma vez antes.

## Parar de compartilhar seu próprio trabalho

Desative suas conexões em **Suas conexões**, a menos que o Fleet as exija. O conteúdo compartilhado por elas será removido.

Veja também [Fleets](fleet.md) e [Segurança e privacidade](security-and-privacy.md).
