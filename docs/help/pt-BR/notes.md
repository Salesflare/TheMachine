---
title: Notas
area: graph
summary: Uma página fácil de ler para cada assunto, como uma viagem ou sua casa, com links para as pessoas e os projetos relacionados.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, dashboard/graph-notes.js
order: 8
translated: 59dd4e1951e7cc7d
---
Uma nota reúne as informações sobre um assunto: uma viagem, sua casa, como as faturas são pagas. As notas ficam no Graph, junto com Pessoas, Organizações e Projetos. Elas ficam na sua Machine e não são compartilhadas com sua equipe.

## Começar uma nota

Selecione **Nova nota** na parte superior de Notas. Dê um título e selecione **Começar a nota** para abrir a página. **Adicionar uma linha** acrescenta o que você quiser guardar. Cada linha de texto vira uma linha própria.

## Links para pessoas, projetos e outras notas

Digite @ e algumas letras de um nome em uma linha. Escolha uma pessoa, organização, projeto ou nota na lista para inserir o nome como link. Na página do item vinculado, aparece **Vinculado de** com sua nota.

## Notas dentro de notas

Uma nota pode ficar dentro de outra, como Eletrodomésticos dentro de Casa. Notas mostra esses itens em uma árvore: a seta ao lado de uma nota abre as notas que ficam dentro dela. Para mover uma nota, selecione **Editar** e escolha onde ela fica em **Abaixo**. **Nova nota abaixo desta**, no menu ⋯, cria uma nota nesse local.

## Notas que sua Machine mantém

Sua Machine também escreve notas automaticamente com base nas suas mensagens e as mantém atualizadas. Cada linha indica de onde veio, como quem enviou o e-mail. Toque nela para abrir a mensagem. Uma linha de **O que aprendi** mostra **Com base no que aprendi**.

Suas alterações são sempre mantidas. Renomeie uma nota, mova-a, altere as datas ou uma linha, e sua Machine mantém essas mudanças quando atualiza a nota. Se você excluir uma linha ou nota, ela não volta. Notas futuras sobre o mesmo assunto serão adicionadas onde você colocou a primeira.

**Voltar ao original** mostra novamente o texto que sua Machine escreveu. Se você editar uma linha que veio do que sua Machine aprendeu, ela também será alterada em **O que aprendi**, para que haja uma única versão.

## Viagens

Quando uma reserva de voo, hotel, trem, ônibus, balsa ou carro alugado chega por e-mail, sua Machine a adiciona a uma viagem em **Viagens**. As reservas de uma mesma jornada ficam em uma única viagem: a ida, o hotel e a volta. A viagem reúne o código da reserva, o assento e o bilhete de cada item, em ordem cronológica, e mostra as datas. Na [Agenda](calendar.md), ela aparece como uma faixa que cobre esses dias e abre a viagem.

Sua Machine lê os detalhes de reserva que companhias aéreas, hotéis e sites de reservas incluem nos e-mails de confirmação. Um e-mail sem esses detalhes não cria uma viagem. Se uma reserva mudar, o item correspondente será atualizado. Se for cancelada, será removido. Quando todas as reservas de uma viagem forem canceladas, a viagem também será removida.

## Casa

Em **Casa**, sua Machine mantém o que sabe sobre sua casa: **Contas e assinaturas**, **Eletrodomésticos**, **Reparos e manutenção** e **A Casa**. Uma seção aparece quando tem pelo menos duas linhas.

- Uma conta recorrente, como a de energia ou água, ganha uma linha com a frequência e a data da última cobrança. **Abrir a tarefa** mostra a conta; o valor e os dados de pagamento ficam lá.
- Uma assinatura que você manteve ganha uma linha que abre a tarefa de **Assinaturas**. Assinaturas canceladas não aparecem na lista.
- O que sua Machine aprendeu sobre sua casa, como a marca da lava-louças, também aparece em uma linha. Se você editar essa informação, ela também será alterada em **O que aprendi**.
- Se você mantiver uma nota própria em uma seção, como uma nota sobre sua lava-louças em **Eletrodomésticos**, as informações sobre ela ficam nessa nota. Sua Machine não cria esse tipo de nota por conta própria.

São usadas apenas contas e assinaturas Pessoais, e as notas de Casa são sempre Pessoais. Sua Machine consulta a IA uma vez sobre cada conta, assinatura ou informação nova que aprende para identificar se é sobre sua casa. No caso de uma conta, ela envia o nome do emissor, nunca o valor.

## Saúde

Em **Saúde**, sua Machine mantém o que sabe sobre sua saúde: **Consultas**, **Médicos e cuidados**, **Medicamentos**, **Alergias e condições** e **Contas e plano de saúde**. Uma seção aparece quando tem pelo menos duas linhas.

- Uma consulta na sua agenda da qual só você participa, como uma ida ao dentista, ganha uma linha com a próxima data ou a data mais recente. **Da sua agenda** abre o evento.
- Uma conta de médico, dentista ou farmácia ganha uma linha que abre a tarefa correspondente. O valor fica lá.
- O que sua Machine aprendeu sobre sua saúde, como uma alergia, também aparece em uma linha. Se você editar essa informação, ela também será alterada em **O que aprendi**.
- Uma nota sua em uma seção, como uma nota sobre seu fisioterapeuta em **Consultas**, reúne as informações sobre esse assunto.

As notas de Saúde são sempre Pessoais, mesmo quando uma conta chega no seu endereço de trabalho. Sua Machine consulta a IA uma vez sobre cada consulta, conta ou informação nova que aprende para identificar se é sobre sua saúde. Ela envia o nome da consulta, nunca as anotações nem os nomes de outras pessoas convidadas.

## Mesclar, excluir e desfazer

**Mesclar em…**, no menu ⋯, move as linhas de uma nota e as notas dentro dela para outra nota. A partir daí, sua Machine adiciona novas informações a essa nota. **Excluir** remove uma nota. Depois de cada uma dessas ações, aparece **Desfazer** por um momento. O mesmo acontece quando você remove uma linha.

## Diferente das notas de reunião

As notas de reunião e as notas sobre uma pessoa ou organização continuam onde estavam. As notas daqui são páginas próprias.
