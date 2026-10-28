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

Enquanto ela ouve, a caixa mostra um cronômetro. Toque no X para parar sem guardar nada. Uma gravação pode ter até 2 minutos; aos 2 minutos ela para sozinha e escreve o que você disse.

O que você disse aparece na caixa, onde estava o seu cursor. Nada é enviado: leia, mude o que quiser e envie.

## Na primeira vez

Na primeira vez que você toca no microfone, sua Machine prepara a voz. Ela baixa o modelo de voz uma vez só, de 150 a 500 MB, e mostra "Preparando a voz…" com o progresso. Isso leva alguns minutos. Sua gravação espera e é escrita assim que tudo estiver pronto.

## Para onde vai a sua voz

Por padrão, sua gravação vira texto na sua própria Machine. Ela nunca sai dela e é apagada assim que o texto volta. O reconhecimento de voz do seu navegador não é usado, porque alguns navegadores mandam a sua voz para o fabricante.

Em **Configurações**, **Geral**, em **Entrada por voz**, você pode escolher:

- **Transcrito**: **Nesta Machine**, ou **Com a OpenAI**. A OpenAI é mais rápida em um servidor pequeno, mas sua gravação vai para a OpenAI, com a sua própria chave. Precisa de uma chave de API da OpenAI no OpenClaw. Um login do ChatGPT não inclui isso.
- **Precisão**: **Mais preciso** funciona melhor para a maioria dos idiomas. **Mais rápido** é mais ágil, mas erra mais palavras. Em um servidor Standard, que tem menos memória, **Mais rápido** é o padrão.
- **Idioma**: **Detectar** funciona para todos os idiomas do app. Escolher o seu é um pouco mais rápido.

## Quando não funciona

- **O microfone está bloqueado**: permita o microfone para este site nas configurações do seu navegador. No app do celular, fica nas permissões do app.
- **Nenhum microfone encontrado**: conecte um e tente de novo.
- **Não consigo acessar sua Machine**: sua gravação fica guardada e é escrita quando sua Machine voltar. Para tentar antes, toque em **Tentar agora**.
- **Não entendi nada**: fale um pouco mais perto do microfone, ou por mais tempo.
