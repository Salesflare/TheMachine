---
title: Notas
area: graph
summary: Uma página fácil de ler para cada assunto, como uma viagem ou sua casa, vinculada às pessoas e aos projetos relacionados.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: a32102a88a8b3856
---
Uma nota é um resumo de um assunto: uma viagem, sua casa, como as faturas são pagas. As notas ficam no Graph, ao lado de Pessoas, Organizações e Projetos. Elas ficam na sua Machine e não são compartilhadas com sua equipe.

## Começar uma nota

Toque em **Nova nota** na parte superior de Notas. Dê um título e toque em **Começar a nota** para abrir a página. **Adicionar uma linha** adiciona o que você quer guardar. Cada linha de texto vira uma linha separada.

## Vincular pessoas, projetos e outras notas

Digite @ e algumas letras de um nome em uma linha. Escolha uma pessoa, organização, projeto ou nota na lista para inserir o nome como link. A página do item vinculado mostra **Vinculado de** com sua nota.

## Notas dentro de outras notas

Uma nota pode ficar dentro de outra, como Eletrodomésticos dentro de Casa. Notas mostra tudo em uma árvore: a seta ao lado de uma nota abre as notas dentro dela. Para mover uma nota, toque em **Editar** e escolha onde ela ficará em **Abaixo**. **Nova nota abaixo desta**, no menu ⋯, cria uma nota ali mesmo.

## Notas que sua Machine mantém

Sua Machine também escreve notas automaticamente com base nas suas mensagens e as mantém atualizadas. Cada linha indica de onde veio, como quem enviou o e-mail. Toque nela para abrir a mensagem. Uma linha de **O que aprendi** mostra **Com base no que aprendi**.

Suas alterações sempre prevalecem. Renomeie uma nota, mova-a, altere as datas ou uma linha, e sua Machine manterá essas mudanças quando atualizar a nota. Se excluir uma linha ou nota, ela não voltará. Notas futuras sobre o mesmo assunto serão adicionadas à primeira nota que você criou.

**Voltar ao original** mostra novamente as palavras da sua Machine. Editar uma linha que veio do que sua Machine aprendeu também altera essa informação em **O que aprendi**, para que haja uma única versão.

## Viagens

Quando uma reserva de voo, hotel, trem, ônibus, balsa ou carro alugado chega ao seu e-mail, sua Machine a adiciona a uma viagem em **Viagens**. As reservas de uma mesma viagem ficam juntas: a ida, o hotel e a volta. A viagem mostra o código da reserva, o assento e a passagem de cada linha, em ordem cronológica, além das datas. Em [Calendário](calendar.md), aparece como uma faixa ao longo desses dias e abre a viagem.

Sua Machine lê os detalhes das reservas que companhias aéreas, hotéis e sites de reservas incluem nos e-mails de confirmação. Um e-mail sem esses dados não cria uma viagem. Se uma reserva for alterada, a linha correspondente será atualizada. Se for cancelada, será removida. Quando todas as reservas de uma viagem forem canceladas, a viagem também será removida.

## Eventos

Quando ingressos para um show, uma partida, um festival ou uma conferência chegam ao seu e-mail, sua Machine adiciona o evento em **Eventos**, com uma nota para cada evento. Uma linha mostra onde será, o código da reserva, o assento e o número de ingressos. Um segundo pedido para o mesmo evento é adicionado à mesma nota. Assim como uma viagem, o evento mostra as datas e aparece como uma faixa em [Calendário](calendar.md), que abre a nota.

- Cada linha indica de quem vieram os ingressos, como **De Example Tickets**, e abre o e-mail.
- Se uma tarefa veio do e-mail dos ingressos, como pagar por eles, **Abrir a tarefa** mostra a tarefa.
- Um evento reservado pelo seu e-mail de trabalho é classificado como Trabalho. Caso contrário, é Pessoal.

Sua Machine lê os detalhes dos ingressos que os vendedores incluem nos e-mails de confirmação, sem usar IA. Um e-mail sem esses dados não cria um evento. Uma reserva cancelada é removida. Quando todos os ingressos de um evento são cancelados, o evento também é removido.

## Casa

Em **Casa**, sua Machine guarda o que sabe sobre sua casa: **Contas e assinaturas**, **Eletrodomésticos**, **Reparos e manutenção** e **A Casa**. Uma seção aparece quando tem pelo menos duas linhas.

- Uma conta recorrente, como energia ou água, ganha uma linha com a frequência e a data da última cobrança. **Abrir a tarefa** mostra a própria conta. O valor e os dados de pagamento ficam lá.
- Uma assinatura que você manteve ganha uma linha que abre a tarefa de **Assinaturas**. Uma assinatura cancelada não aparece na lista.
- O que sua Machine aprendeu sobre sua casa, como a marca da lava-louças, também aparece em uma linha. Editar essa informação também altera **O que aprendi**.
- Se você mantiver sua própria nota em uma seção, como uma nota sobre sua lava-louças em **Eletrodomésticos**, as informações sobre ela ficarão na sua nota. Sua Machine não cria notas desse tipo por conta própria.

Só são usadas contas e assinaturas Pessoais, e as notas de Casa são sempre Pessoais. Sua Machine consulta a IA uma vez sobre cada conta, assinatura ou informação nova que aprendeu para saber se tem relação com sua casa. No caso de uma conta, ela informa quem a enviou, nunca o valor.

## Saúde

Em **Saúde**, sua Machine guarda o que sabe sobre sua saúde: **Consultas**, **Médicos e cuidados**, **Medicamentos**, **Alergias e condições** e **Contas e plano de saúde**. Uma seção aparece quando tem pelo menos duas linhas.

- Uma consulta na sua agenda à qual só você vai, como uma ida ao dentista, ganha uma linha com a próxima data ou a última. **Da sua agenda** abre o evento.
- Uma conta de médico, dentista ou farmácia ganha uma linha que abre a tarefa. O valor fica lá.
- O que sua Machine aprendeu sobre sua saúde, como uma alergia, também aparece em uma linha. Editar essa informação também altera **O que aprendi**.
- Sua própria nota em uma seção, como uma nota sobre seu fisioterapeuta em **Consultas**, reúne as informações relacionadas.

As notas de Saúde são sempre Pessoais, mesmo quando uma conta chega ao seu endereço de trabalho. Sua Machine consulta a IA uma vez sobre cada consulta, conta ou informação nova que aprendeu para saber se tem relação com sua saúde. Ela envia o nome da consulta, nunca as anotações ou os nomes de outras pessoas convidadas.

## Filhos

Em **Filhos**, sua Machine guarda o que sabe sobre seus filhos: **Escola**, **Atividades**, **Médicos e cuidados** e **Contas e taxas**. Uma seção aparece quando tem pelo menos duas linhas.

- O que sua Machine aprendeu sobre seu filho, como o nome do professor ou o dia da aula de natação, aparece em uma linha vinculada à página dele. Ela considera alguém seu filho quando a relação em **Para você** indica isso, como filha ou filho.
- Um evento na sua agenda ao qual só você vai, como uma reunião de pais, ganha uma linha com a próxima data ou a última. **Da sua agenda** abre o evento.
- Uma conta da escola, de um clube ou de uma creche ganha uma linha que abre a tarefa. O valor fica lá.
- Sua própria nota sobre um filho em uma seção, como uma nota sobre Isla em **Escola**, reúne as informações relacionadas a ele.

As notas de Filhos são sempre Pessoais, mesmo quando a escola escreve para o seu endereço de trabalho. Sua Machine consulta a IA uma vez sobre cada informação nova para saber se tem relação com seus filhos.

## Mesclar, excluir e desfazer

**Mesclar em…**, no menu ⋯, move as linhas de uma nota e as notas dentro dela para outra nota. A partir daí, sua Machine adiciona novas informações a essa nota. **Excluir** remove uma nota. As duas ações mostram **Desfazer** por um instante. O mesmo acontece quando você remove uma linha.

## Diferente das notas de reunião

As notas de reunião e as notas sobre uma pessoa ou organização continuam onde estavam. As notas daqui são páginas próprias.
