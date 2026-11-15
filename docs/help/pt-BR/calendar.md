---
title: Calendário
area: calendar
summary: Veja a semana que vem em um só lugar: reuniões, tarefas que vencem, tarefas adiadas e promessas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
translated: 9da7909bce253806
---
## O que aparece

Seus dias a partir de hoje, com:

- reuniões dos calendários que você conectou,
- tarefas que vencem naquele dia e tarefas adiadas para o dia em que voltam,
- acompanhamentos de trabalhos que você delegou,
- promessas com data.

Uma reunião que aparece em dois calendários é exibida uma só vez. Um calendário compartilhado com você mostra os eventos da outra pessoa em tom mais claro, com o primeiro nome dela. Esses eventos nunca geram uma tarefa. Eventos de dia inteiro e de vários dias aparecem como eventos de dia inteiro em cada dia que abrangem.

Um plano feito em conjunto é uma só promessa, marcada com "Com" e o nome da outra pessoa. Uma promessa sobre uma reunião naquele dia com a mesma pessoa aparece na linha da reunião.

**Atrasada** aparece primeiro. Uma reunião com uma tarefa em aberto mostra o status dela: **Preparação pronta**, **Preparando** ou **Tarefa**. Uma tarefa que parece concluída, porque você já respondeu ou porque a execução identificou que ela foi concluída, não aparece como **Vence**.

## Agenda, semana ou mês

- **Agenda** lista cada dia. Role para baixo para ver os próximos dias ou para cima (ou toque em **Mostrar dias anteriores**) para ver os anteriores. A visualização volta até uma semana antes de você conectar seu calendário, e uma linha no topo indica a partir de qual dia. Depois que o [histórico](history.md) for carregado, ela volta cerca de um ano.
- **Semana** mostra uma grade de segunda a domingo. No celular, mostra três dias.
- **Mês** mostra o mês inteiro. No computador, mostra até três itens por dia. No celular, mostra pontos; toque em um dia para ver a lista.

**Hoje**, ‹ e › no topo permitem navegar pelas semanas ou pelos meses. A visualização escolhida fica salva nesse dispositivo.

Na grade semanal, eventos no mesmo horário aparecem lado a lado, sem perder a legibilidade. Os demais aparecem como **+N**. Toque para abrir esse dia na agenda.

## Abrir um item

Clique em uma linha para abrir o chat da tarefa, a promessa ou a reunião. Uma reunião que você não pode alterar aqui, como a de outra pessoa ou uma com convidados, mostra os detalhes: quando, onde e quem. As pessoas que a Graph reconhece, além das organizações e dos projetos relacionados à reunião, têm links para suas páginas. **Abrir no Google Calendar** (ou **Abrir no Outlook**) abaixo abre a reunião no calendário correspondente. Só visualizar não altera nada.

Uma sala de reunião reservada para uma reunião aparece em Onde, nunca como uma pessoa ou na sua Graph.

O link de uma reunião aparece com o nome do serviço, como Zoom, Google Meet ou Teams, ou como **Videochamada**. Abra a reunião para participar.

## Notas e transcrição da reunião

Os detalhes de uma reunião têm duas partes. **Notas** é o resumo, com decisões e itens de ação. **Transcrição** mostra o que foi dito, palavra por palavra. Ela começa recolhida e mostra sua duração. Toque em **Mostrar** para abrir.

Se não carregar, o sistema tenta novamente por conta própria durante cerca de meio minuto. Depois disso, toque em **Tentar de novo**.

Cada parte tem seus próprios campos **Adicionar notas** ou **Adicionar transcrição**, além de **Enviar arquivo** para arquivos Markdown ou de texto, **Editar** e **Remover** (toque duas vezes). O conteúdo de uma parte fica só nela. Em uma reunião que você pode alterar, **Notas**, abaixo do formulário, abre as notas.

Quando [Zoom](zoom.md) ou [Google Meet](google-meet.md) está conectado, as notas do serviço aparecem em Notas e a transcrição em Transcrição, marcadas como **Do Zoom** ou **Do Google Meet**. Elas nunca substituem o que você adicionou: se as duas versões estiverem disponíveis, ambas aparecem.

As notas também podem vir do evento da reunião no calendário, adicionadas depois que ela começa, ou de um e-mail do Zoom ou Gemini. Depois que a reunião termina, The Machine só cria tarefas com base nelas quando há próximos passos claros. Se as mesmas notas chegarem por dois meios, elas geram uma única tarefa, com a reunião como origem: "Origem: notas da" reunião.

Uma reunião com transcrição, mas sem notas, tem a opção **Gerar notas**. The Machine cria as notas com base na transcrição: um resumo curto, decisões e itens de ação com as pessoas responsáveis, no idioma da reunião.

A mensagem **Escrevendo as notas…** aparece, e a criação continua mesmo que você feche a reunião. Uma reunião longa pode levar alguns minutos e usa seu próprio modelo. As notas dizem **Escrito por The Machine** e nunca substituem as notas que você adicionou.

The Machine também pode adicioná-las. Peça em uma tarefa, por exemplo: "adicione esta transcrição à reunião de hoje do quadro". A transcrição vai para Transcrição e o resumo, para Notas. No Calendário, uma reunião com esses dados mostra **Notas** ou **Transcrição**.

The Machine lê os dois para identificar os acompanhamentos da reunião. Eles são de Trabalho ou Pessoais, conforme a reunião, e só vão para sua equipe se a reunião também for para ela.

A reunião abre com esses detalhes de qualquer lugar em que você a encontre: na linha do tempo, em uma busca de mensagens ou como origem de uma tarefa. **Convite original**, na parte inferior, mostra o convite como foi recebido.

## Adicionar ou alterar um evento

Você pode alterar seu próprio calendário do Google por aqui. O Outlook e outros calendários só permitem visualizar. **Novo evento** adiciona um evento (no celular, fica em **+** na barra superior): escolha o calendário, um título e o horário. Clique em um evento sem convidados nesse calendário para alterá-lo ou **Excluir** (toque duas vezes).

**Onde** sugere lugares enquanto você digita: primeiro, os que você já usou e suas organizações; depois, endereços do [OpenStreetMap](https://www.openstreetmap.org), um mapa gratuito. Só as palavras que você digitar são enviadas para a busca. Escolha uma sugestão ou mantenha o texto que escreveu.

**Convidar** adiciona pessoas da sua Graph ou qualquer endereço de e-mail. Essa opção só aparece no seu próprio calendário. As pessoas que receberão um convite aparecem acima do botão, que indica quantas são: **Adicionar e convidar 2**. O Google envia os convites quando você toca no botão, não antes. Sem convidados, ninguém recebe um convite ou uma atualização.

Uma tarefa também pode sugerir uma alteração, como adicionar uma retirada. Ela mostra exatamente o que vai mudar, e só **Adicionar**, **Salvar** ou **Excluir** confirma a alteração.

Ainda não tem reuniões? Se você não tiver um calendário conectado, **Conecte seu calendário** abre Conexões, onde você pode conectar o [Google Calendar](google-calendar.md), o [Outlook Calendar](microsoft.md) ou [outro calendário](other-calendars.md).

## Conflitos com seu outro calendário

Quando uma reunião de trabalho coincide com algo no seu calendário pessoal, ou vice-versa, The Machine cria uma tarefa sobre o evento mais recente. Ela pode criar um rascunho de mensagem curta para remarcar o evento ou oferecer a opção de recusá-lo. Nada é enviado até você aprovar.

Eventos de dia inteiro, livres ou provisórios nunca contam, e cada conflito aparece uma só vez. Uma tarefa de Trabalho só informa que há um conflito, então sua equipe nunca vê o evento pessoal. Só você vê com o que ele coincide.

## Prepare-se para suas reuniões

Antes de uma reunião com pessoas de fora da sua empresa, The Machine cria uma tarefa: **Preparar-se para** a reunião. É um resumo rápido:

- **Quem:** quem são, de acordo com sua Graph.
- **Último contato:** sua última conversa com elas. Essa mensagem é a origem da tarefa após a reunião.
- **Promessas em aberto:** o que você ou elas ainda precisam fazer.
- **Perguntas em aberto:** o que ainda não foi respondido.
- **Decidir ou levar:** o que precisa ser decidido ou levado.

A tarefa aparece na manhã de um dia útil: no próprio dia da reunião se ela for à tarde; caso contrário, no dia útil anterior. Ela usa apenas o que já está na sua Machine. Serve apenas para consulta: marque **Feito** depois de ler. Uma promessa ou pergunta que exija uma ação tem sua própria tarefa.

Sem um histórico útil, não há tarefa. Reuniões recorrentes, internas, pessoais ou recusadas não geram tarefas. Se uma reunião mudar de horário, ela mantém a mesma tarefa, no novo horário. Uma tarefa descartada não volta, e a tarefa de uma reunião cancelada é fechada automaticamente.

Nos detalhes da reunião, a tarefa aparece em **Tarefa**, a um toque do chat.
