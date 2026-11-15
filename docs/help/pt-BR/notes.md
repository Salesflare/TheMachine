---
title: Notas
area: graph
summary: Uma página fácil de consultar para cada assunto, como uma viagem ou sua casa, com links para as pessoas e os projetos relacionados.
covers: notes
code: note_pages.py, note_pages_app.py, trip_notes.py, event_notes.py, bookings.py, section_notes.py, home_notes.py, health_notes.py, kids_notes.py, dashboard/graph-notes.js
order: 8
translated: 336e0f0dad44f19a
---
Uma nota reúne as informações sobre um assunto: uma viagem, sua casa, como as faturas são pagas. As notas ficam no Graph, junto de Pessoas, Organizações e Projetos. Elas ficam na sua Machine e não são compartilhadas com sua equipe.

## Começar uma nota

**Nova nota** na parte superior de Notas. Dê um título e toque em **Começar a nota** para abrir a página. **Adicionar uma linha** adiciona o que você quer guardar. Cada linha de texto vira uma linha separada.

## Vincular pessoas, projetos e outras notas

Digite @ e algumas letras de um nome em uma linha. Escolha uma pessoa, organização, projeto ou nota na lista. O nome será inserido como link. A página do item vinculado mostra **Vinculado de** com sua nota.

## Notas dentro de outras notas

Uma nota pode ficar dentro de outra, como Eletrodomésticos dentro de Casa. Notas mostra tudo em uma árvore: a seta ao lado de uma nota abre as notas que ficam dentro dela. Para mover uma nota, toque em **Editar** e escolha onde ela ficará em **Abaixo**. **Nova nota abaixo desta**, no menu ⋯, cria uma nota ali mesmo.

Na parte superior da página de uma nota, você vê onde ela fica, como **Notas › Filhos**. Toque em qualquer parte para ir até ela. No celular, as notas intermediárias ficam ocultas no menu ⋯.

## Notas que sua Machine mantém

Sua Machine também cria notas com base nas suas mensagens e mantém tudo atualizado. Cada linha indica de onde veio, como quem enviou o email. Toque nela para abrir a mensagem. Uma linha baseada no **O que aprendi** mostra **Com base no que aprendi**. Uma reunião ou consulta na sua agenda nunca aparece como uma linha independente: ela fica no [Calendário](calendar.md).

**Casa**, **Saúde** e **Filhos** só aparecem quando sua Machine tem pelo menos duas informações concretas para incluir, como uma conta ou algo que aprendeu. Até lá, elas não aparecem na lista. Se ficarem sem informações novamente, desaparecem.

Suas alterações são sempre mantidas. Renomeie uma nota, mova-a, altere as datas ou uma linha, e sua Machine manterá essas mudanças quando atualizar a nota. Se você excluir uma linha ou uma nota, ela não volta. As notas criadas depois sobre o mesmo assunto ficam onde você colocou a primeira.

**Voltar ao original** mostra novamente o texto original da sua Machine. Se você editar uma linha baseada no que sua Machine aprendeu, ela também será alterada em **O que aprendi**, para que haja uma única versão.

## Viagens

Quando uma reserva de voo, hotel, trem, ônibus, balsa ou carro alugado chega ao seu email, sua Machine a adiciona a uma viagem em **Viagens**. As reservas da mesma jornada ficam em uma só viagem: ida, hotel e volta. A viagem mostra o código da reserva, o assento e o bilhete de cada linha, em ordem cronológica, além das datas. No [Calendário](calendar.md), ela aparece como uma faixa que cobre esses dias e abre a viagem.

Sua Machine lê os detalhes da reserva que companhias aéreas, hotéis e sites de reservas incluem nos emails de confirmação. Um email sem esses detalhes não cria uma viagem. Emails de reservas anteriores, dentro do ano de [histórico](history.md) que sua Machine mantém, são lidos em segundo plano depois que esse histórico é importado, começando pelas suas caixas de email Pessoais. Se uma confirmação antiga for lida mais tarde, ela será adicionada à viagem que já existe.

Uma reserva alterada atualiza a linha correspondente, e uma cancelada é removida. Quando todas as reservas de uma viagem são canceladas, a viagem também é removida.

## Eventos

Quando ingressos para um show, jogo, festival ou conferência chegam ao seu email, sua Machine adiciona o evento em **Eventos**, com uma nota para cada evento. Uma linha mostra o local, o código da reserva, o assento e o número de ingressos. Um segundo pedido para o mesmo evento fica na mesma nota. Assim como uma viagem, o evento mostra as datas e aparece como uma faixa no [Calendário](calendar.md), que abre a nota.

- Cada linha indica de quem vieram os ingressos, como **De Example Tickets**, e abre esse email.
- Se uma tarefa veio do email dos ingressos, como pagar por eles, **Abrir a tarefa** mostra a tarefa.
- Um evento reservado pela sua caixa de email de trabalho é de Trabalho. Caso contrário, é Pessoal.

Sua Machine lê os detalhes dos ingressos que os vendedores incluem nos emails de confirmação, sem usar IA. Um email sem esses detalhes não cria um evento. Uma reserva cancelada é removida. Quando todos os ingressos de um evento são cancelados, o evento também é removido.

## Casa

Em **Casa**, sua Machine mantém o que sabe sobre sua casa: **Contas e assinaturas**, **Eletrodomésticos**, **Reparos e manutenção** e **A Casa**. Uma seção aparece quando tem pelo menos duas linhas.

- Uma conta recorrente, como a de energia ou água, ganha uma linha com a frequência e a data da última conta. **Abrir a tarefa** mostra a própria conta. O valor e os detalhes do pagamento ficam lá.
- Uma assinatura que você manteve ganha uma linha que abre a tarefa de **Assinaturas**. Uma assinatura cancelada não aparece na lista.
- Quem entra em contato regularmente sobre sua casa, como sua fornecedora de energia, seu provedor de internet ou a prefeitura, ganha uma linha com a frequência dos contatos. Toque nela para abrir o email mais recente.
- O que sua Machine aprendeu sobre sua casa, como a marca da sua lava-louças, também aparece como uma linha. Se você editar essa informação, ela também será alterada em **O que aprendi**.
- Se você mantiver sua própria nota em uma seção, como uma nota sobre sua lava-louças em **Eletrodomésticos**, as informações sobre ela ficam nessa nota. Sua Machine não cria notas desse tipo por conta própria.

Só são usadas contas, assinaturas e emails Pessoais, e as notas de Casa são sempre Pessoais. Sua Machine consulta a IA uma vez para cada conta, assinatura ou informação nova que aprendeu, para saber se é sobre sua casa. Para uma conta, ela envia o nome de quem a enviou, nunca o valor.

Para **Casa**, **Saúde** e **Filhos**, sua Machine também consulta a IA uma vez sobre cada remetente dos seus emails Pessoais. Ela envia o nome do remetente, a quantidade de emails enviados e os assuntos mais recentes, ocultando os números. O email em si nunca é enviado. Um email recebido duas vezes, ou em duas das suas caixas de email, conta uma vez. Uma resposta com o mesmo assunto na conversa também conta uma vez.

Emails em massa nunca são incluídos nessas notas nem enviados à IA: spam, promoções, newsletters e outras mensagens de listas, além de notificações de endereços que não aceitam respostas. Emails em uma conversa à qual você respondeu continuam contando, assim como emails de reservas de **Viagens** e **Eventos**.

Na primeira vez, sua Machine analisa os emails do último ano ao longo de algumas horas, fora do período noturno e somente enquanto houver espaço no seu plano de IA. Depois disso, ela verifica novos remetentes a cada seis horas.

## Saúde

Em **Saúde**, sua Machine mantém o que sabe sobre sua saúde: **Consultas**, **Resultados dos testes**, **Médicos e cuidados**, **Medicamentos**, **Alergias e condições** e **Contas e plano de saúde**. Uma seção aparece quando tem pelo menos duas linhas.

- Uma conta de médico, dentista ou farmácia ganha uma linha que abre a tarefa correspondente. O valor fica lá.
- Cada email do seu consultório, de um hospital, laboratório ou plano de saúde vira uma linha datada com o assunto, para seu histórico crescer com o tempo. Toque nela para abrir o email.
- O que sua Machine aprendeu sobre sua saúde, como uma alergia, também aparece como uma linha. Se você editar essa informação, ela também será alterada em **O que aprendi**.
- As informações sobre o assunto ficam na sua própria nota em uma seção, como uma nota sobre seu fisioterapeuta em **Consultas**.

As notas de Saúde são sempre Pessoais, mesmo quando uma conta chega ao seu endereço de trabalho. Sua Machine consulta a IA uma vez para cada conta ou informação nova que aprendeu, para saber se é sobre sua saúde.

## Filhos

Em **Filhos**, sua Machine mantém o que sabe sobre seus filhos: **Escola**, **Atividades**, **Cuidados infantis**, **Médicos e cuidados** e **Contas e taxas**. Uma babá ou creche fica em Cuidados infantis, nunca em Médicos e cuidados. Uma seção aparece quando tem pelo menos duas linhas.

- O que sua Machine aprendeu sobre seu filho, como o nome do professor ou o dia da aula de natação, aparece como uma linha com um link para a página dele. Sua Machine considera alguém seu filho quando em **Para você** consta esse vínculo, como filha ou filho.
- Uma conta da escola, de um clube ou de cuidados infantis ganha uma linha que abre a tarefa correspondente. O valor fica lá.
- Cada email da escola, de um clube ou de quem cuida dos seus filhos, como um aviso sobre uma excursão ou uma mudança de planos, vira uma linha datada com o assunto. Assim, tudo o que enviam fica em um só lugar. Toque nela para abrir o email.
- As informações sobre uma criança ficam na sua própria nota em uma seção, como uma nota sobre Isla em **Escola**.

As notas de Filhos são sempre Pessoais, mesmo quando a escola escreve para seu endereço de trabalho. Sua Machine consulta a IA uma vez para cada informação nova, para saber se é sobre seus filhos.

## Mesclar, excluir e desfazer

**Mesclar em…**, no menu ⋯, move as linhas de uma nota e as notas dentro dela para outra nota. A partir daí, sua Machine adiciona novas informações a essa nota. **Excluir** remove uma nota. As duas ações mostram **Desfazer** por alguns instantes. O mesmo acontece ao remover uma linha.

## Diferente das notas de reunião

As notas de reunião e as notas sobre pessoas ou organizações continuam onde estavam. As notas daqui são páginas próprias.
