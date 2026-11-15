---
title: Notas
area: graph
summary: Uma página fácil de consultar para cada assunto, como uma viagem ou sua casa, vinculada às pessoas e aos projetos relacionados.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: b88647412222409d
---
Uma nota é um resumo de um assunto: uma viagem, sua casa, como as faturas são pagas. As notas ficam no Graph, junto de Pessoas, Organizações e Projetos. Elas ficam na sua Machine e não são compartilhadas com sua equipe.

## Começar uma nota

**Nova nota** no topo de Notas. Dê um título e toque em **Começar a nota** para abrir a página. **Adicionar uma linha** adiciona o que você quer guardar. Cada linha de texto vira uma linha separada.

## Vincular pessoas, projetos e outras notas

Digite @ e algumas letras de um nome em uma linha. Escolha uma pessoa, organização, projeto ou nota da lista para inserir o nome como link. Na página do item vinculado, aparece **Vinculado de** com sua nota.

## Notas dentro de outras notas

Uma nota pode ficar dentro de outra, como Eletrodomésticos dentro de Casa. Notas mostra tudo em árvore: toque na seta ao lado de uma nota para abrir as notas dentro dela. Para mover uma nota, toque em **Editar** e escolha onde ela fica em **Abaixo**. **Nova nota abaixo desta**, no menu ⋯, cria uma nota ali mesmo.

## Notas que sua Machine mantém

Sua Machine também escreve notas por conta própria, com base nas suas mensagens, e as mantém atualizadas. Cada linha indica de onde veio, como quem enviou o e-mail: toque nela para abrir a mensagem. Uma linha de **O que aprendi** mostra **Com base no que aprendi**.

Suas alterações sempre prevalecem. Renomeie uma nota, mova-a, altere as datas ou uma linha, e sua Machine mantém essas mudanças quando atualiza a nota. Se você excluir uma linha ou nota, ela não volta. Notas adicionadas depois sobre o mesmo assunto vão para onde você colocou a primeira.

**Voltar ao original** mostra novamente as palavras da sua Machine. Editar uma linha que veio do que sua Machine aprendeu também altera essa informação em **O que aprendi**, para que ela tenha uma só versão.

## Viagens

Quando uma reserva de voo, hotel, trem, ônibus, balsa ou carro alugado chega ao seu e-mail, sua Machine a adiciona a uma viagem em **Viagens**. As reservas de uma mesma jornada ficam em uma viagem: o trecho de ida, o hotel e o trecho de volta. A viagem mostra o código da reserva, o assento e a passagem de cada linha, em ordem cronológica, além das datas. Em [Agenda](calendar.md), ela aparece como uma faixa ao longo desses dias e abre a viagem.

Sua Machine lê os detalhes da reserva que companhias aéreas, hotéis e sites de reservas incluem no e-mail de confirmação. Um e-mail sem esses detalhes não cria uma viagem. E-mails de reservas anteriores, dentro do ano de [histórico](history.md) que sua Machine mantém, são lidos em segundo plano assim que esse histórico fica disponível. Se uma reserva for alterada, a linha correspondente é atualizada. Se for cancelada, ela é removida. Quando todas as reservas de uma viagem são canceladas, a viagem também é removida.

## Eventos

Quando ingressos para um show, uma partida, um festival ou uma conferência chegam ao seu e-mail, sua Machine adiciona o evento em **Eventos**, com uma nota para cada evento. Uma linha informa o local, o código da reserva, o assento e o número de ingressos. Se você fizer outro pedido para o mesmo evento, ele será adicionado à mesma nota. Assim como uma viagem, o evento mostra as datas e aparece como uma faixa em [Agenda](calendar.md) que abre a nota.

- Cada linha informa de quem vieram os ingressos, como **De Example Tickets**, e abre o e-mail.
- Se uma tarefa tiver sido criada com base no e-mail dos ingressos, como pagar por eles, **Abrir a tarefa** mostra essa tarefa.
- Um evento reservado pelo seu e-mail de trabalho é Trabalho. Caso contrário, é Pessoal.

Sua Machine lê os detalhes dos ingressos que os vendedores incluem no e-mail de confirmação, sem usar IA. Um e-mail sem esses detalhes não cria um evento. Uma reserva cancelada é removida. Se todos os ingressos de um evento forem cancelados, o evento também é removido.

## Casa

Em **Casa**, sua Machine guarda o que sabe sobre sua casa: **Contas e assinaturas**, **Eletrodomésticos**, **Reparos e manutenção** e **A Casa**. Uma seção aparece quando tem pelo menos duas linhas.

- Uma conta recorrente, como a de energia ou água, ganha uma linha que informa com que frequência ela chega e a data da última conta. **Abrir a tarefa** mostra a conta. O valor e os detalhes de pagamento ficam nela.
- Uma assinatura que você manteve ganha uma linha que abre a tarefa de **Assinaturas**. Uma assinatura cancelada não aparece na lista.
- O que sua Machine aprendeu sobre sua casa, como a marca da lava-louças, também vira uma linha. Ao editá-la, você também altera essa informação em **O que aprendi**.
- Se você tiver uma nota própria em uma seção, como uma nota sobre sua lava-louças em **Eletrodomésticos**, as informações sobre ela ficam nessa nota. Sua Machine não cria notas desse tipo por conta própria.

Só são usadas contas e assinaturas Pessoais, e as notas de Casa são sempre Pessoais. Sua Machine pergunta uma vez à IA sobre cada conta, assinatura ou informação nova que aprendeu, para descobrir se diz respeito à sua casa. No caso de uma conta, ela informa quem a enviou, nunca o valor.

## Saúde

Em **Saúde**, sua Machine guarda o que sabe sobre sua saúde: **Consultas**, **Médicos e cuidados**, **Medicamentos**, **Alergias e condições** e **Contas e plano de saúde**. Uma seção aparece quando tem pelo menos duas linhas.

- Uma consulta na sua agenda à qual só você vai, como uma consulta no dentista, ganha uma linha com a próxima data ou, se não houver, a última. **Da sua agenda** abre o evento.
- Uma conta de médico, dentista ou farmácia ganha uma linha que abre a tarefa correspondente. O valor fica nela.
- O que sua Machine aprendeu sobre sua saúde, como uma alergia, também vira uma linha. Ao editá-la, você também altera essa informação em **O que aprendi**.
- Uma nota própria em uma seção, como uma nota sobre seu fisioterapeuta em **Consultas**, reúne as informações sobre esse assunto.

As notas de Saúde são sempre Pessoais, mesmo quando uma conta chega ao seu e-mail de trabalho. Sua Machine pergunta uma vez à IA sobre cada nova consulta, conta ou informação que aprendeu, para descobrir se diz respeito à sua saúde. Ela envia o nome da consulta, nunca as anotações nem os nomes de outras pessoas convidadas.

## Filhos

Em **Filhos**, sua Machine guarda o que sabe sobre seus filhos: **Escola**, **Atividades**, **Médicos e cuidados** e **Contas e taxas**. Uma seção aparece quando tem pelo menos duas linhas.

- O que sua Machine aprendeu sobre seu filho, como o nome do professor ou o dia da aula de natação, vira uma linha vinculada à página dele. Ela considera alguém seu filho quando em **Para você** consta essa relação, como filha ou filho.
- Um evento na sua agenda ao qual só você vai, como uma reunião de pais, ganha uma linha com a próxima data ou, se não houver, a última. **Da sua agenda** abre o evento.
- Uma conta da escola, de um clube ou de uma creche ganha uma linha que abre a tarefa correspondente. O valor fica nela.
- Uma nota própria para um dos seus filhos em uma seção, como uma nota para Isla em **Escola**, reúne as informações sobre essa criança.

As notas de Filhos são sempre Pessoais, mesmo quando a escola escreve para o seu e-mail de trabalho. Sua Machine pergunta uma vez à IA sobre cada informação nova, para descobrir se diz respeito aos seus filhos.

## Mesclar, excluir e desfazer

**Mesclar em…**, no menu ⋯, move as linhas e as notas dentro de uma nota para outra nota. A partir daí, sua Machine adiciona novas informações a essa outra nota. **Excluir** remove uma nota. As duas ações mostram **Desfazer** por alguns instantes. O mesmo acontece quando você remove uma linha.

## Diferentes das notas de reunião

As notas de reunião e as notas sobre uma pessoa ou organização continuam onde estavam. As notas daqui são páginas próprias.
