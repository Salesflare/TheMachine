---
title: Notas
area: graph
summary: Uma página fácil de consultar para cada assunto, como uma viagem ou sua casa, vinculada às pessoas e aos projetos relacionados.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 8e27b2c69f77196d
---
Uma nota reúne as informações sobre um assunto: uma viagem, sua casa, como as faturas são pagas. As notas ficam no Graph, junto com Pessoas, Organizações e Projetos. Elas ficam na sua Machine e não são compartilhadas com sua equipe.

## Começar uma nota

Toque em **Nova nota** na parte superior de Notas. Dê um título e toque em **Começar a nota** para abrir a página. **Adicionar uma linha** inclui o que você quer guardar. Cada linha de texto vira uma linha separada.

## Vincular pessoas, projetos e outras notas

Digite @ e algumas letras de um nome em uma linha. Escolha uma pessoa, organização, projeto ou nota na lista. O nome será inserido como um link. Na página do item vinculado, sua nota aparece em **Vinculado de**.

## Notas abaixo de outras notas

Uma nota pode ficar abaixo de outra, como Eletrodomésticos abaixo de Casa. Em Notas, elas aparecem em forma de árvore: toque na seta ao lado de uma nota para ver as que estão abaixo dela. Para mover uma nota, toque em **Editar** e escolha onde ela ficará em **Abaixo**. **Nova nota abaixo desta**, no menu ⋯, cria uma nota ali mesmo.

Na parte superior da página, você vê onde a nota fica, como **Notas › Filhos**. Toque em qualquer parte para ir até ela. No celular, as notas intermediárias ficam recolhidas no menu ⋯.

## Notas que sua Machine mantém

Sua Machine também cria notas com base nas suas mensagens e as mantém atualizadas. Cada linha indica de onde veio, como quem enviou o e-mail. Toque nela para abrir a mensagem. Uma linha baseada em **O que aprendi** mostra **Com base no que aprendi**. Reuniões e consultas do seu calendário nunca aparecem como linhas separadas: elas ficam na [Agenda](calendar.md).

**Casa**, **Saúde** e **Filhos** só aparecem quando sua Machine tem pelo menos duas informações relevantes para mostrar, como uma conta ou algo que aprendeu. Até lá, elas não aparecem na lista. Se voltarem a ficar sem conteúdo, desaparecem.

Suas alterações são sempre mantidas. Renomeie uma nota, mova-a ou altere as datas ou uma linha, e sua Machine manterá essas mudanças ao atualizar a nota. Se excluir uma linha ou nota, ela não volta. Notas criadas depois sobre o mesmo assunto ficam onde você colocou a primeira.

**Voltar ao original** mostra novamente o texto escrito pela sua Machine. Se você editar uma linha baseada no que sua Machine aprendeu, ela também será alterada em **O que aprendi**, para manter uma única versão.

## Viagens

Quando uma reserva de voo, hotel, trem, ônibus, balsa ou carro alugado chega ao seu e-mail, sua Machine a adiciona a uma viagem em **Viagens**. As reservas da mesma jornada ficam em uma viagem: a ida, o hotel e a volta. A viagem mostra o código da reserva, o assento e a passagem de cada linha, em ordem cronológica, além das datas. Na [Agenda](calendar.md), aparece como uma faixa ao longo desses dias. Toque nela para abrir a viagem.

Sua Machine lê os detalhes que companhias aéreas, hotéis e sites de reservas incluem nos e-mails de confirmação. Um e-mail sem esses detalhes não cria uma viagem. E-mails de reserva recebidos antes, dentro do ano de [histórico](history.md) que sua Machine mantém, são lidos em segundo plano assim que esse histórico estiver disponível. Primeiro, ela lê as caixas de e-mail pessoais.

Se uma reserva mudar, a linha correspondente será atualizada. Se for cancelada, ela será removida. Quando todas as reservas de uma viagem forem canceladas, a viagem também será removida.

## Eventos

Quando ingressos para um show, jogo, festival ou conferência chegam ao seu e-mail, sua Machine adiciona o evento em **Eventos**, em uma nota própria. Uma linha informa o local, o código da reserva, o assento e a quantidade de ingressos. Se você fizer outro pedido para o mesmo evento, ele será adicionado à mesma nota. Assim como uma viagem, o evento mostra as datas e aparece como uma faixa na [Agenda](calendar.md). Toque nela para abrir a nota.

- Cada linha indica de quem vieram os ingressos, como **De Example Tickets**, e abre o e-mail.
- Se o e-mail dos ingressos tiver criado uma tarefa, como pagar pelos ingressos, **Abrir a tarefa** mostra essa tarefa.
- Um evento reservado pelo seu e-mail de trabalho é classificado como Trabalho. Nos outros casos, é Pessoal.

Sua Machine lê os detalhes dos ingressos incluídos pelos vendedores nos e-mails de confirmação, sem usar IA. Um e-mail sem esses detalhes não cria um evento. Uma reserva cancelada é removida. Quando todos os ingressos de um evento forem cancelados, o evento também será removido.

## Casa

Em **Casa**, sua Machine mantém o que sabe sobre sua casa: **Contas e assinaturas**, **Eletrodomésticos**, **Reparos e manutenção** e **A Casa**. Uma categoria aparece quando tem pelo menos duas linhas.

- Uma conta recorrente, como a de energia ou água, ganha uma linha que informa a frequência e a data da última conta. **Abrir a tarefa** mostra a conta. O valor e os dados de pagamento ficam nela.
- Uma assinatura que você manteve ganha uma linha que abre a tarefa **Assinaturas**. As assinaturas canceladas não aparecem.
- Pessoas ou empresas que entram em contato regularmente sobre sua casa, como a fornecedora de energia, a operadora de internet ou a prefeitura, ganham uma linha que informa a frequência dos contatos. Toque nela para abrir o e-mail mais recente.
- O que sua Machine aprendeu sobre sua casa, como a marca da lava-louças, também ganha uma linha. Se você editar a informação, ela também será alterada em **O que aprendi**.
- Se você criar uma nota em uma categoria, como uma nota sobre sua lava-louças em **Eletrodomésticos**, as informações sobre ela ficarão nessa nota. Sua Machine não cria notas desse tipo por conta própria.

Só são usadas contas, assinaturas e mensagens pessoais. As notas de Casa são sempre pessoais. Para identificar se uma conta, assinatura ou informação nova que aprendeu diz respeito à sua casa, sua Machine pergunta uma vez à IA. No caso de uma conta, ela envia o nome de quem a enviou, nunca o valor.

Para **Casa**, **Saúde** e **Filhos**, sua Machine também pergunta uma vez à IA sobre cada remetente dos seus e-mails pessoais. Ela envia o nome do remetente, quantos e-mails ele enviou e os assuntos mais recentes, com os números ocultos. Nunca envia o conteúdo dos e-mails.

Na primeira vez, sua Machine analisa os e-mails do último ano em algumas horas, fora do período noturno e somente quando há espaço no seu plano de IA. Depois disso, ela verifica novos remetentes a cada seis horas.

## Saúde

Em **Saúde**, sua Machine mantém o que sabe sobre sua saúde: **Consultas**, **Resultados dos testes**, **Médicos e cuidados**, **Medicamentos**, **Alergias e condições** e **Contas e plano de saúde**. Uma categoria aparece quando tem pelo menos duas linhas.

- Uma conta de médico, dentista ou farmácia ganha uma linha que abre a tarefa correspondente. O valor fica nela.
- Cada e-mail do seu consultório, hospital, laboratório ou plano de saúde vira uma linha com a data e o assunto, para que seu histórico vá se formando com o tempo. Toque nela para abrir o e-mail.
- O que sua Machine aprendeu sobre sua saúde, como uma alergia, também ganha uma linha. Se você editar a informação, ela também será alterada em **O que aprendi**.
- Se você criar uma nota em uma categoria, como uma nota sobre seu fisioterapeuta em **Consultas**, as informações sobre ele ficarão nessa nota.

As notas de Saúde são sempre pessoais, mesmo quando uma conta chega ao seu endereço de trabalho. Sua Machine pergunta uma vez à IA sobre cada nova conta ou informação que aprendeu para identificar se diz respeito à sua saúde.

## Filhos

Em **Filhos**, sua Machine mantém o que sabe sobre seus filhos: **Escola**, **Atividades**, **Cuidados infantis**, **Médicos e cuidados** e **Contas e taxas**. Babás e creches ficam em Cuidados infantis, nunca em Médicos e cuidados. Uma categoria aparece quando tem pelo menos duas linhas.

- O que sua Machine aprendeu sobre seu filho, como o nome do professor da turma ou o dia da natação, vira uma linha vinculada à página dele. Sua Machine identifica alguém como seu filho quando em **Para você** consta uma relação como filha ou filho.
- Uma conta da escola, de um clube ou de uma creche ganha uma linha que abre a tarefa correspondente. O valor fica nela.
- Cada e-mail da escola, de um clube ou de uma creche, como o boletim semanal ou um aviso sobre uma excursão, vira uma linha com a data e o assunto. Assim, tudo o que envia fica em um só lugar. Toque na linha para abrir o e-mail.
- Se você criar uma nota para um filho em uma categoria, como uma nota sobre Isla em **Escola**, as informações sobre ela ficarão nessa nota.

As notas de Filhos são sempre pessoais, mesmo quando a escola escreve para seu endereço de trabalho. Sua Machine pergunta uma vez à IA sobre cada informação nova para identificar se diz respeito aos seus filhos.

## Mesclar, excluir e desfazer

**Mesclar em…**, no menu ⋯, move as linhas de uma nota e as notas abaixo dela para outra nota. A partir daí, sua Machine adiciona novas informações a essa nota. **Excluir** remove uma nota. As duas ações mostram **Desfazer** por alguns instantes. O mesmo acontece ao remover uma linha.

## Diferentes das notas de reunião

As notas de reunião e as notas sobre uma pessoa ou organização continuam onde estavam. As notas daqui são páginas próprias.
