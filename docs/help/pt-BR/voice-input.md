---
title: Entrada por voz
area: cards
summary: Fale em vez de digitar. O que você diz aparece na caixa de mensagem para você conferir. Nada é enviado.
covers: voice-input
code: voice_input.py, voice_worker.py, dashboard.html
order: 7
keywords: voice, dictate, dictation, speak, talk, microphone, mic, speech, transcribe
---
## Fale em vez de digitar

Toque no microfone em uma caixa de mensagem: o chat de uma tarefa, **Nova tarefa**, **Ajuda**, ou a caixa para mudar um rascunho. Fale e depois toque no sinal de confirmação. Ou segure o microfone enquanto fala e solte quando terminar.

Enquanto ela ouve, a caixa mostra um cronômetro. Toque no X para parar sem guardar nada. Uma gravação pode ter até 2 minutos; aos 2 minutos ela para sozinha e escreve o que você disse. O que ela já ouviu aparece na barra enquanto você fala, então o texto fica pronto logo depois que você para.

O que você disse aparece na caixa, onde estava o seu cursor. Nada é enviado: leia, mude o que quiser e envie.

## Para onde vai a sua voz

Em **Configurações**, **Geral**, em **Entrada por voz**, uma linha curta diz qual está em uso.

- **Automático** (o padrão): quando a OpenAI está configurada no OpenClaw, sua gravação é transcrita pela OpenAI. Isso é uma chave de API, ou um login do ChatGPT quando seu plano permite áudio. Sem a OpenAI, ela é transcrita na sua própria Machine e nunca sai dela.
- **Nesta Machine**: sempre na sua Machine, mesmo com a OpenAI configurada.
- **Com a OpenAI**: sempre a OpenAI.

Uma gravação é apagada assim que o texto volta.

## Preparação

Para transcrever a fala sozinha, sua Machine precisa de um modelo de voz de 150 a 500 MB. Ela o baixa em segundo plano, com baixa prioridade, depois de configurada, quando a primeira revisão termina e ela fica tranquila por um tempo. Enquanto isso, as configurações mostram **Preparando (em segundo plano)**. Ela nunca faz isso quando a OpenAI está em uso.

Até ficar pronta, **Automático** usa o reconhecimento de voz do seu navegador, se ele tiver um, e avisa embaixo da caixa. Alguns navegadores enviam isso ao fabricante. Com **Nesta Machine** escolhido, sua gravação espera e a caixa mostra "Preparando a voz…" com o tempo restante.

## Configurações

- **Transcrito**: **Automático**, **Nesta Machine** ou **Com a OpenAI**.
- **Precisão** (só na sua Machine): **Mais preciso** funciona melhor para a maioria dos idiomas. **Mais rápido** é mais ágil, mas erra mais palavras. Em uma Machine Standard, que tem menos memória, **Mais rápido** é o padrão.
- **Idioma**: **Detectar** funciona para todos os idiomas do app. Escolher o seu é um pouco mais rápido.

Para conversar em voz alta com a The Machine, veja [Falar ao vivo](talk-live.md).

## Quando não funciona

- **O microfone está bloqueado**: permita o microfone para este site nas configurações do seu navegador. No app do celular, fica nas permissões do app.
- **Nenhum microfone encontrado**: conecte um e tente de novo.
- **Não consigo acessar sua Machine**: sua gravação fica guardada e é escrita quando sua Machine voltar. Para tentar antes, toque em **Tentar agora**.
- **Não entendi nada**: fale um pouco mais perto do microfone, ou por mais tempo.
