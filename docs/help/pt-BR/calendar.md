---
title: Calendário
area: calendar
summary: A semana em um só lugar: reuniões, tarefas com prazo, tarefas adiadas e promessas.
covers: tab:calendar
code: dashboard.html, meeting_notes.py, meeting_writer.py
order: 1
---
## O que ele mostra

Os próximos 7 dias, com:

- reuniões das agendas que você conectou,
- tarefas que vencem naquele dia, e tarefas adiadas no dia em que voltam,
- acompanhamentos de trabalho que você passou adiante,
- promessas com data.

Uma reunião que está em duas agendas aparece uma vez só. Uma agenda que alguém compartilhou com você mostra os eventos dessa pessoa em tom mais claro, com o primeiro nome dela. Esses eventos nunca viram tarefa. Eventos de dia inteiro e de vários dias aparecem como dia inteiro, em cada dia que cobrem.

Um plano feito em conjunto é uma promessa só, marcada com "Com" e o nome da pessoa. Uma promessa sobre uma reunião naquele dia com a mesma pessoa fica na linha dessa reunião.

**Atrasada** vem primeiro. Uma reunião com uma tarefa em aberto mostra essa tarefa: **Preparação pronta**, **Preparando** ou **Tarefa**.

## Agenda ou semana

**Agenda** lista cada dia. No computador, **Semana** mostra uma grade. Sua escolha fica salva naquele dispositivo.

Na grade, eventos no mesmo horário ficam lado a lado, e cada um continua legível. Os demais aparecem como **+N**, que abre aquele dia na agenda.

## Abrir algo

Clique em uma linha para abrir o chat da tarefa, a promessa ou a reunião na própria agenda. Em uma reunião, quem o seu Graph conhece, e as organizações e projetos de que ela trata, são links para a página deles. Só olhar não muda nada.

Uma sala de reunião reservada aparece no local, nunca como pessoa nem no seu Graph.

## Notas e transcrição da reunião

Os detalhes de uma reunião têm duas partes. **Notas** é o resumo: decisões e ações. **Transcrição** é o que foi dito, palavra por palavra. Ela começa recolhida, com a duração; **Mostrar** abre.

Cada uma tem seu próprio **Adicionar notas** ou **Adicionar transcrição**, **Enviar arquivo** para um arquivo Markdown ou de texto, **Editar** e **Remover** (toque duas vezes). O que vai numa fica nela. Numa reunião que você pode mudar, **Notas** embaixo do formulário abre as duas.

Com o [Zoom](zoom.md) ou o [Google Meet](google-meet.md) conectado, as notas dele aparecem em Notas e a transcrição em Transcrição, marcadas **Do Zoom** ou **Do Google Meet**. Eles nunca substituem o que você adicionou: quando os dois existem, os dois aparecem.

Uma reunião com transcrição e sem notas tem **Gerar notas**. A The Machine escreve as notas a partir da transcrição: um resumo curto, as decisões e as ações com quem faz cada uma, no idioma da reunião.

A The Machine mostra **Escrevendo as notas…** e continua se você fechar a reunião; uma longa leva alguns minutos. Ela usa o seu próprio modelo e espera se você atingir seu limite de uso. As notas dizem **Escritas pela The Machine**, nunca substituem as que você adicionou, e os acompanhamentos saem delas como das do Zoom.

A The Machine também pode adicioná-las. Peça numa tarefa, como "adicione esta transcrição à reunião do conselho de hoje". Uma transcrição vai em Transcrição, um resumo em Notas. Uma reunião com elas mostra **Notas** ou **Transcrição** no calendário.

A The Machine lê as duas para os próximos passos da reunião. Elas são Trabalho ou Pessoal como a reunião, e só vão para sua equipe quando a reunião vai.

## Adicionar ou mudar um evento

Quando uma agenda pode ser alterada daqui, **Novo evento** adiciona um (no celular, fica em **+** na barra de cima): escolha a agenda, um título e o horário. Clique em um evento sem convidados nessa agenda para mudá-lo, ou para **Excluir** (toque duas vezes).

**Onde** sugere lugares enquanto você digita: primeiro os que você já usou e suas organizações, depois endereços do [OpenStreetMap](https://www.openstreetmap.org) via Photon, uma busca de mapas gratuita. Sua Machine faz a consulta só com as palavras que você digitou. Escolha uma sugestão ou mantenha seu próprio texto.

**Convidar** adiciona pessoas do seu Graph, ou qualquer endereço de e-mail. Só aparece na sua própria agenda. Quem vai receber convite aparece acima do botão, e o botão diz quantas pessoas: **Adicionar e convidar 2**. O Google envia os convites quando você toca nele, não antes. Sem convidados, ninguém é convidado nem recebe atualização.

Uma tarefa também pode sugerir uma mudança, como adicionar uma busca de alguém. Ela mostra exatamente o que muda, e só o seu **Adicionar**, **Salvar** ou **Excluir** faz a mudança.

Ainda sem reuniões? Sem agenda, **Conecte seu calendário** abre Conexões: conecte o [Google Calendar](google-calendar.md) ou o [Outlook Calendar](microsoft.md).
