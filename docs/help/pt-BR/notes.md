---
title: Notas
area: graph
summary: Uma página fácil de ler para cada assunto, como uma viagem ou sua casa, com links para as pessoas e os projetos envolvidos.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, bookings.py, home_notes.py, dashboard/graph-notes.js
order: 8
translated: 4a6b4d56a8d9b93f
---
Uma nota é um resumo de um assunto: uma viagem, sua casa, como as faturas são pagas. As notas ficam no Graph, junto de Pessoas, Organizações e Projetos. Elas ficam na sua Machine e não são compartilhadas com sua equipe.

## Começar uma nota

Toque em **Nova nota** no topo de Notas. Dê um título e toque em **Começar a nota** para abrir a página. **Adicionar uma linha** adiciona o que você quer guardar. Cada linha de texto vira uma linha separada.

## Vincular pessoas, projetos e outras notas

Digite @ e algumas letras de um nome em uma linha. Escolha uma pessoa, organização, projeto ou nota na lista para inserir o nome como link. Na página do item vinculado, sua nota aparece em **Vinculado de**.

## Notas dentro de notas

Uma nota pode ficar dentro de outra, como Eletrodomésticos dentro de Casa. Notas mostra essas notas em uma árvore: toque na seta ao lado de uma nota para abrir as notas dentro dela. Para mover uma nota, toque em **Editar** e escolha onde ela ficará em **Abaixo**. **Nova nota abaixo desta**, no menu ⋯, cria uma nota dentro dela.

## Notas que sua Machine mantém

Sua Machine também cria notas automaticamente com base nas suas mensagens e as mantém atualizadas. Cada linha indica de onde veio, como quem enviou o e-mail: toque nela para abrir a mensagem. Uma linha de **O que aprendi** mostra **Com base no que aprendi**.

Suas alterações são sempre mantidas. Renomeie uma nota, mova-a, altere as datas ou uma linha, e sua Machine mantém essas mudanças quando atualiza a nota. Se você excluir uma linha ou uma nota, ela não volta. Notas futuras sobre o mesmo assunto vão para o lugar que você escolheu para a primeira.

**Voltar ao original** mostra novamente o texto original da sua Machine. Se você editar uma linha que veio do que sua Machine aprendeu, ela também será alterada em **O que aprendi**, para que haja uma só versão.

## Viagens

Quando uma reserva de voo, hotel, trem, ônibus, balsa ou carro alugado chega ao seu e-mail, sua Machine a adiciona a uma viagem em **Viagens**. As reservas de uma mesma jornada ficam em uma única viagem: a ida, o hotel e a volta. A viagem mostra o código da reserva, o assento e o bilhete de cada linha, em ordem cronológica, além das datas. Em [Calendário](calendar.md), ela aparece como uma faixa ao longo desses dias. Toque nela para abrir a viagem.

Sua Machine lê os detalhes da reserva que companhias aéreas, hotéis e sites de reservas incluem nos e-mails de confirmação. Um e-mail sem esses detalhes não cria uma viagem. Se uma reserva mudar, a linha correspondente será atualizada. Se for cancelada, a linha será removida. Quando todas as reservas de uma viagem forem canceladas, a viagem também será removida.

## Casa

Em **Casa**, sua Machine mantém o que sabe sobre sua casa: **Contas e assinaturas**, **Eletrodomésticos**, **Reparos e manutenção** e **A Casa**. Uma seção aparece quando tem pelo menos duas linhas.

- Uma conta recorrente, como a de energia ou água, ganha uma linha com a frequência e a data da última cobrança. **Abrir a tarefa** mostra a conta. O valor e os detalhes do pagamento continuam lá.
- Uma assinatura que você mantém ganha uma linha que abre a tarefa de **Assinaturas**. As assinaturas canceladas não aparecem na lista.
- O que sua Machine aprendeu sobre sua casa, como a marca da lava-louças, também aparece em uma linha. Se você editar essa informação, ela também será alterada em **O que aprendi**.
- Se você mantiver uma nota própria em uma seção, como uma nota sobre sua lava-louças em **Eletrodomésticos**, as informações sobre ela vão para essa nota. Sua Machine não cria esse tipo de nota por conta própria.

Só são usadas contas e assinaturas Pessoais, e as notas de Casa são sempre Pessoais. Sua Machine consulta a IA uma vez para cada conta, assinatura ou informação nova que aprender, para saber se tem a ver com sua casa. Para uma conta, ela informa quem a enviou, nunca o valor.

## Mesclar, excluir e desfazer

**Mesclar em…**, no menu ⋯, move as linhas de uma nota e as notas dentro dela para outra nota. A partir daí, sua Machine adiciona informações a essa nota. **Excluir** remove uma nota. Por um momento, as duas ações mostram **Desfazer**. O mesmo acontece quando você remove uma linha.

## Diferentes das notas de reunião

As notas de reunião e as notas sobre uma pessoa ou organização continuam onde estavam. As notas daqui são páginas próprias.
