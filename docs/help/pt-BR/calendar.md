---
title: Calendário
area: calendar
summary: A semana em um só lugar: reuniões, tarefas com prazo, tarefas adiadas e promessas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py, calendar_clashes.py
order: 1
---
## O que ele mostra

Seus dias a partir de hoje, com:

- reuniões das agendas que você conectou,
- tarefas que vencem naquele dia, e tarefas adiadas no dia em que voltam,
- acompanhamentos de trabalho que você passou adiante,
- promessas com data.

Uma reunião que está em duas agendas aparece uma vez só. Uma agenda que alguém compartilhou com você mostra os eventos dessa pessoa em tom mais claro, com o primeiro nome dela. Esses eventos nunca viram tarefa. Eventos de dia inteiro e de vários dias aparecem como dia inteiro, em cada dia que cobrem.

Um plano feito em conjunto é uma promessa só, marcada com "Com" e o nome da pessoa. Uma promessa sobre uma reunião naquele dia com a mesma pessoa fica na linha dessa reunião.

**Atrasada** vem primeiro. Uma reunião com uma tarefa em aberto mostra essa tarefa: **Preparação pronta**, **Preparando** ou **Tarefa**. Uma tarefa que parece feita (você já respondeu, ou a execução dela a encontrou feita) não aparece como **Vence**.

## Agenda, semana ou mês

- **Agenda** lista cada dia. Role para baixo para ver os dias seguintes, ou para cima (ou **Mostrar dias anteriores**) para os anteriores. Ela vai até uma semana antes de você conectar sua agenda, e uma linha no topo diz a partir de que dia. Quando o [histórico](history.md) chega, ela volta cerca de um ano.
- **Semana** mostra uma grade, de segunda a domingo. No celular ela mostra três dias.
- **Mês** mostra o mês inteiro. No computador aparecem até três itens por dia; no celular aparecem pontos, e um toque lista aquele dia.

**Hoje**, ‹ e › no topo passam pelas semanas ou meses. A visualização que você escolhe fica salva naquele dispositivo.

Na grade da semana, eventos no mesmo horário ficam lado a lado, e cada um continua legível. Os demais aparecem como **+N**, que abre aquele dia na agenda.

## Abrir algo

Clique em uma linha para abrir o chat da tarefa, a promessa ou a reunião na própria agenda. Em uma reunião, quem o seu Graph conhece, e as organizações e projetos de que ela trata, são links para a página deles. Só olhar não muda nada.

Uma sala de reunião reservada aparece no local, nunca como pessoa nem no seu Graph.

## Notas e transcrição da reunião

Os detalhes de uma reunião têm duas partes. **Notas** é o resumo: decisões e ações. **Transcrição** é o que foi dito, palavra por palavra. Ela começa recolhida, com a duração; **Mostrar** abre.

Se não carregarem (por exemplo, enquanto a sua Machine reinicia), a reunião tenta de novo sozinha por cerca de meio minuto, e de novo quando você volta para a janela. Depois disso ela avisa, com **Tentar de novo**.

Cada uma tem seu próprio **Adicionar notas** ou **Adicionar transcrição**, **Enviar arquivo** para um arquivo Markdown ou de texto, **Editar** e **Remover** (toque duas vezes). O que vai numa fica nela. Numa reunião que você pode mudar, **Notas** embaixo do formulário abre as duas.

Com o [Zoom](zoom.md) ou o [Google Meet](google-meet.md) conectado, as notas dele aparecem em Notas e a transcrição em Transcrição, marcadas **Do Zoom** ou **Do Google Meet**. Eles nunca substituem o que você adicionou: quando os dois existem, os dois aparecem.

As notas também podem vir no próprio evento da agenda, adicionadas depois que ele começou, ou por e-mail do Zoom ou do Gemini. Depois da reunião, The Machine só cria to-dos com elas para próximos passos claros. As mesmas notas chegando de duas formas viram um só to-do, com a reunião como origem: **Notas de** e o nome dela.

Uma reunião com transcrição e sem notas tem **Gerar notas**. A The Machine escreve as notas a partir da transcrição: um resumo curto, as decisões e as ações com quem faz cada uma, no idioma da reunião.

A The Machine mostra **Escrevendo as notas…** e continua se você fechar a reunião; uma longa leva alguns minutos. Ela usa o seu próprio modelo e espera se você atingir seu limite de uso. As notas dizem **Escritas pela The Machine**, nunca substituem as que você adicionou, e os acompanhamentos saem delas como das do Zoom.

A The Machine também pode adicioná-las. Peça numa tarefa, como "adicione esta transcrição à reunião do conselho de hoje". Uma transcrição vai em Transcrição, um resumo em Notas. Uma reunião com elas mostra **Notas** ou **Transcrição** no calendário.

A The Machine lê as duas para os próximos passos da reunião. Elas são Trabalho ou Pessoal como a reunião, e só vão para sua equipe quando a reunião vai.

Uma reunião abre com estes detalhes onde quer que você a encontre: em uma linha do tempo, em uma pesquisa de mensagens ou como fonte de uma tarefa. **Convite original** embaixo mostra o convite como ele chegou.

## Adicionar ou mudar um evento

Quando uma agenda pode ser alterada daqui, **Novo evento** adiciona um (no celular, fica em **+** na barra de cima): escolha a agenda, um título e o horário. Clique em um evento sem convidados nessa agenda para mudá-lo, ou para **Excluir** (toque duas vezes).

**Onde** sugere lugares enquanto você digita: primeiro os que você já usou e suas organizações, depois endereços do [OpenStreetMap](https://www.openstreetmap.org) via Photon, uma busca de mapas gratuita. Sua Machine faz a consulta só com as palavras que você digitou. Escolha uma sugestão ou mantenha seu próprio texto.

**Convidar** adiciona pessoas do seu Graph, ou qualquer endereço de e-mail. Só aparece na sua própria agenda. Quem vai receber convite aparece acima do botão, e o botão diz quantas pessoas: **Adicionar e convidar 2**. O Google envia os convites quando você toca nele, não antes. Sem convidados, ninguém é convidado nem recebe atualização.

Uma tarefa também pode sugerir uma mudança, como adicionar uma busca de alguém. Ela mostra exatamente o que muda, e só o seu **Adicionar**, **Salvar** ou **Excluir** faz a mudança.

Ainda sem reuniões? Sem agenda, **Conecte seu calendário** abre Conexões: conecte o [Google Calendar](google-calendar.md), o [Outlook Calendar](microsoft.md) ou [outro calendário](other-calendars.md).

## Conflitos com sua outra agenda

Quando uma reunião de trabalho se sobrepõe a algo na sua agenda pessoal, ou o contrário, The Machine cria uma tarefa sobre o mais recente dos dois. Ela pode preparar um rascunho curto para remarcar, ou oferecer recusar. Nada sai antes da sua aprovação.

Eventos de dia inteiro, livres ou provisórios nunca contam, e cada conflito aparece uma vez só. Uma tarefa de Trabalho diz só que há um conflito, então sua equipe nunca vê o evento pessoal. Só você vê com o que ele conflita.
