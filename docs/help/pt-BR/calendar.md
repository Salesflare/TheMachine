---
title: Calendário
area: calendar
summary: A semana que vem em um só lugar: reuniões, tarefas que vencem, tarefas adiadas e promessas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py, meeting_prep.py
order: 1
translated: d85b3eff63ea503d
---
## O que aparece

Seus dias a partir de hoje, com:

- reuniões dos calendários que você conectou,
- tarefas que vencem naquele dia e tarefas adiadas para o dia em que voltam,
- acompanhamentos de trabalhos que você delegou,
- promessas com data,
- [notas](notes.md) com datas, como uma viagem.

Uma reunião que aparece em dois calendários é exibida uma só vez. Um calendário que alguém compartilhou com você mostra os eventos dessa pessoa em tom esmaecido e com o primeiro nome dela. Esses eventos nunca geram uma tarefa. Eventos de dia inteiro e de vários dias aparecem como eventos de dia inteiro em cada dia que ocupam. Uma viagem aparece primeiro em cada um dos dias na Agenda e como uma única faixa ao longo dos dias nas visualizações Semana e Mês, como “Viagem a Lisboa”.

Um plano feito em conjunto é uma única promessa, marcada como “Com” e com o nome da outra pessoa. Uma promessa sobre uma reunião naquele dia com a mesma pessoa aparece na linha da reunião.

**Atrasada** aparece primeiro. Uma reunião com uma tarefa em aberto mostra o status dela: **Preparação pronta**, **Preparando** ou **Tarefa**. Uma tarefa que parece concluída (você já respondeu ou a execução identificou que ela foi concluída) não aparece como **Vence**.

## Agenda, semana ou mês

- **Agenda** mostra cada dia. Role para baixo para ver os próximos dias ou para cima (ou toque em **Mostrar dias anteriores**) para ver os dias anteriores. A visualização volta até uma semana antes de você conectar seu calendário, e uma linha no topo indica a partir de qual dia. Quando o [histórico](history.md) estiver disponível, ela volta cerca de um ano.
- **Semana** mostra uma grade de segunda a domingo. No celular, mostra três dias.
- **Mês** mostra o mês inteiro. No computador, mostra até três itens por dia. No celular, mostra pontos, e tocar em um dia lista os itens dele.

**Hoje**, ‹ e › no topo permitem navegar pelas semanas ou meses. A visualização escolhida fica salva nesse dispositivo.

Na grade semanal, eventos no mesmo horário aparecem lado a lado, sem perder a legibilidade. Os outros aparecem como **+N**. Toque para abrir esse dia na Agenda.

## Abrir um item

Clique em uma linha para abrir o chat da tarefa, a promessa, a nota ou a reunião. Uma reunião que você não pode alterar aqui, como uma reunião de outra pessoa ou com convidados, mostra os detalhes: quando, onde e quem participa. Uma pessoa que o Graph conhece, e as organizações e os projetos relacionados à reunião, têm links para suas páginas. **Abrir no Google Calendar** (ou **Abrir no Outlook**) abre a reunião no respectivo serviço. Só de abrir, nada é alterado.

Uma sala de reunião reservada para uma reunião aparece abaixo de onde, nunca como uma pessoa nem no seu Graph.

O link da reunião aparece com o nome do serviço, como Zoom, Google Meet ou Teams, ou como **Videochamada**. Abra a reunião para entrar.

## Notas e transcrição da reunião

Os detalhes de uma reunião têm duas partes. **Notas** é o resumo: decisões e itens de ação. **Transcrição** registra palavra por palavra o que foi dito. Ela começa recolhida e mostra sua duração. Toque em **Mostrar** para abrir.

Se não carregarem, elas tentam carregar de novo automaticamente por cerca de meio minuto. Depois disso, toque em **Tentar de novo**.

Cada uma tem suas próprias opções **Adicionar notas** ou **Adicionar transcrição**, **Enviar arquivo** para enviar um arquivo Markdown ou de texto, **Editar** e **Remover** (toque duas vezes). O conteúdo de uma não vai para a outra. Em uma reunião que você pode alterar, **Notas**, abaixo do formulário, abre as notas.

Com [Zoom](zoom.md) ou [Google Meet](google-meet.md) conectado, as notas do serviço aparecem em Notas e a transcrição em Transcrição, marcadas como **Do Zoom** ou **Do Google Meet**. Elas nunca substituem o que você adicionou: se ambas estiverem disponíveis, as duas aparecem.

As notas também podem vir do evento da reunião no calendário, ser adicionadas depois que ela começou ou chegar por e-mail do Zoom ou Gemini. Depois que a reunião termina, The Machine cria tarefas a partir delas somente para próximos passos claros. Se as mesmas notas chegarem por dois meios, elas geram uma única tarefa, com a reunião como origem: “Origem: notas da” reunião.

Uma reunião com transcrição e sem notas tem a opção **Gerar notas**. The Machine cria notas com base na transcrição: um resumo curto, decisões e itens de ação com os responsáveis, no idioma da reunião.

A opção **Escrevendo as notas…** aparece, e o processo continua mesmo que você feche a reunião. Uma reunião longa pode levar alguns minutos, usando seu próprio modelo. As notas indicam **Escrito por The Machine** e nunca substituem as notas que você adicionou.

The Machine também pode adicioná-las. Peça isso em uma tarefa, por exemplo: “adicione esta transcrição à reunião de hoje do quadro”. A transcrição vai para Transcrição e o resumo, para Notas. No Calendário, uma reunião com notas ou transcrição mostra **Notas** ou **Transcrição**.

The Machine lê as duas para identificar os acompanhamentos da reunião. Eles são classificados como Trabalho ou Pessoal, assim como a reunião, e só vão para sua equipe quando a reunião também for de equipe.

Os detalhes da reunião são os mesmos onde quer que você a encontre: na linha do tempo, em uma busca de mensagens ou como origem de uma tarefa. **Convite original**, na parte inferior, mostra o convite como foi recebido.

## Adicionar ou alterar um evento

Você pode alterar seu próprio calendário do Google por aqui. O Outlook e os outros calendários são somente para visualização. **Novo evento** adiciona um evento (no celular, fica em **+** na barra superior): escolha o calendário, o título e o horário. Clique em um evento sem convidados nesse calendário para alterá-lo ou em **Excluir** para removê-lo (toque duas vezes).

**Onde** sugere lugares enquanto você digita: primeiro, os que você já usou e suas organizações; depois, endereços do [OpenStreetMap](https://www.openstreetmap.org), um mapa gratuito. Só as palavras que você digitar são enviadas para a busca. Escolha uma sugestão ou mantenha seu próprio texto.

**Convidar** adiciona pessoas do seu Graph ou qualquer endereço de e-mail. Essa opção só aparece no seu próprio calendário. Os convidados aparecem acima do botão, que mostra quantas pessoas serão convidadas: **Adicionar e convidar 2**. O Google envia os convites quando você toca no botão, não antes. Se não houver convidados, ninguém recebe convite ou atualização.

Uma tarefa também pode sugerir uma alteração, como adicionar uma retirada. Ela mostra exatamente o que vai mudar, e a alteração só acontece quando você toca em **Adicionar**, **Salvar** ou **Excluir**.

Ainda não tem reuniões? Se você não tiver um calendário conectado, **Conecte seu calendário** abre Conexões: conecte o [Google Calendar](google-calendar.md), o [Outlook Calendar](microsoft.md) ou [outro calendário](other-calendars.md).

## Conflitos com seu outro calendário

Quando uma reunião de trabalho se sobrepõe a algo no seu calendário pessoal, ou vice-versa, The Machine cria uma tarefa sobre o evento mais recente. Ela pode preparar uma mensagem curta para remarcar ou oferecer a opção de recusar. Nada é enviado até você aprovar.

Eventos de dia inteiro, marcados como disponível ou provisórios nunca são considerados, e cada conflito aparece uma única vez. Uma tarefa de Trabalho só informa que há um conflito, então sua equipe nunca vê o evento pessoal. Só você vê o evento com o qual ele conflita.

## Preparação para suas reuniões

Antes de uma reunião com pessoas de fora da sua empresa, The Machine cria uma tarefa: **Preparar-se para** a reunião. É um resumo breve:

- **Quem:** quem são, de acordo com seu Graph.
- **Último contato:** sua última conversa com elas. Essa mensagem é a origem da tarefa depois da reunião.
- **Promessas em aberto:** o que você ou elas ainda precisam cumprir.
- **Perguntas em aberto:** o que ainda não foi respondido.
- **Decidir ou levar:** o que resolver ou levar.

Ela chega na manhã de um dia útil: no próprio dia da reunião, se ela acontecer à tarde; caso contrário, no dia útil anterior. Ela só usa o que já está na sua Machine. Serve apenas para consulta: toque em **Feito** depois de ler. Uma promessa ou pergunta que exija uma ação tem sua própria tarefa.

Se não houver histórico útil, nenhuma tarefa é criada. Reuniões recorrentes, internas, pessoais ou recusadas não geram tarefas. Se uma reunião mudar de horário, a mesma tarefa é mantida no novo horário. Uma tarefa descartada não volta, e a tarefa de uma reunião cancelada é encerrada automaticamente.

Os detalhes da reunião mostram a tarefa abaixo de **Tarefa**, a um toque do chat dela.
