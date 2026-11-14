---
title: Entrada por voz
area: cards
summary: Fale em vez de digitar. O que você disser aparece na caixa de mensagem para você conferir, e nada é enviado.
covers: voice-input
code: voice_input.py, voice_worker.py, dashboard.html
order: 7
keywords: voice, dictate, dictation, speak, talk, microphone, mic, speech, transcribe
translated: f311b21bb4996eb4
---
## Fale em vez de digitar

Toque no microfone em uma caixa de mensagem: no chat de uma tarefa, em **Nova tarefa**, **Ajuda** ou na caixa usada para editar um rascunho. Fale e toque na marca de seleção. Ou mantenha o microfone pressionado enquanto fala e solte quando terminar.

Enquanto o microfone estiver ouvindo, a caixa mostra um cronômetro e o que ele captou até o momento. Toque no X para parar sem guardar nada. A gravação para automaticamente após 2 minutos.

O texto aparece na caixa, onde estava o cursor. Nada é enviado: leia, altere o que quiser e envie você mesmo.

## Para onde vai sua voz

Escolha em **Configurações**, **Geral**, na opção **Entrada por voz**. Uma linha curta informa qual opção está em uso.

- **Automático** (padrão): a OpenAI transcreve o áudio quando sua Machine usa OpenAI (uma chave da OpenAI ou um plano do ChatGPT que permite usar áudio). Caso contrário, sua Machine faz a transcrição e a gravação nunca sai dela.
- **Nesta Machine**: sempre na sua Machine, mesmo quando a OpenAI está configurada.
- **Com a OpenAI**: sempre pela OpenAI.

A gravação é apagada assim que o texto fica pronto.

## Preparação

Para transcrever a fala, sua Machine primeiro baixa um modelo de reconhecimento de fala (150 a 500 MB) em segundo plano, quando está ociosa. Enquanto isso, **Preparando (em segundo plano)** aparece em Configurações. Esse download não acontece quando a OpenAI está em uso.

Até lá, **Automático** usa o reconhecimento de fala do próprio navegador, se ele tiver esse recurso, e informa isso abaixo da caixa. Alguns navegadores enviam o áudio ao fabricante. Se **Nesta Machine** estiver selecionado, sua gravação fica aguardando, e a caixa mostra “Preparando a entrada por voz…” com o tempo restante.

## Configurações

- **Transcrito**: **Automático**, **Nesta Machine** ou **Com a OpenAI**.
- **Precisão** (somente na sua Machine): **Mais preciso** funciona melhor para a maioria dos idiomas. **Mais rápido** é mais ágil, mas comete mais erros, e é a opção padrão em uma Machine padrão.
- **Idioma**: **Detectar** funciona com todos os idiomas do app. Escolher o seu idioma é um pouco mais rápido.

Para conversar com The Machine em voz alta, veja [Converse ao vivo](talk-live.md).

## Quando não funciona

- **O microfone está bloqueado**: permita o acesso ao microfone para este site nas configurações do navegador. No app para celular, essa opção fica nas permissões do app.
- **Nenhum microfone encontrado**: conecte um e tente novamente.
- **Não foi possível conectar à sua Machine**: sua gravação será mantida e transcrita quando sua Machine voltar a ficar disponível. Para tentar antes, toque em **Tentar agora**.
- **Não consegui captar nada**: fale mais perto do microfone ou por um pouco mais de tempo.
