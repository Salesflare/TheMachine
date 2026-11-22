---
title: Passar para Claude Code ou Codex
area: cards
summary: Envie uma tarefa de programação para Claude Code ou Codex. O resultado aparece na tarefa.
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time, On your Machine, Other ways, On my computer
order: 5
translated: 22e1b9b950988a58
---
## Passar uma tarefa

1. Na tarefa, abra **…**, depois **Passar…** e escolha **Codex** ou **Claude Code**. Só aparecem as ferramentas que você configurou.
2. Confira o resumo e o que a ferramenta vai receber, adicione uma observação se quiser e pressione **Passar**. **Ver o trabalho completo** mostra todas as instruções.

A tarefa mostra que está em andamento e, depois, exibe o resultado com **O que fez** e **Mostrar mudanças**. **Pedir mudanças** envia instruções sobre o que mudar. **Passar…** em **…** reinicia o processo. **Ocultar** esconde o resultado. Se você passar uma tarefa travada, ela mostra **Processando…** em vez de **Travada** enquanto o trabalho é executado.

A tarefa nunca envia nada por você. Quando ela chegar a uma etapa de publicação ou implantação que você precisa fazer, **Fazer** na tarefa executa essa etapa. Uma resposta escrita pela ferramenta fica como rascunho para você enviar.

## No app Codex

- **Abrir no Codex** abre a conversa do trabalho no app Codex quando ele termina.
- **Pedir mudanças** continua na mesma conversa do Codex, e a tarefa acompanha essa conversa.
- O trabalho é interrompido após 30 minutos sem progresso ou após 6 horas no total. Uma reinicialização não interrompe o trabalho.

## Configurar

Em **Configurações**, **Modelo**, na seção **Codex e Claude Code**:

- **Codex**: onde ele é executado. Na sua Machine ou no seu computador, não é necessário configurar mais nada aqui. **Mudar** abre a página de configuração.
- **Codex cloud**: o ID do ambiente, disponível no Codex, e, se quiser, uma **Branch** para usar como ponto de partida.
- **Claude Code**: o link de uma sessão do Claude Code.

O Claude envia o resultado de volta pelo conector da The Machine. Adicione-o uma vez em claude.ai, em Settings, Connectors, Add custom connector, usando o endereço mostrado abaixo da sessão.

## Onde o Codex é executado

Em uma Machine hospedada, escolha onde executá-lo na página de configuração, em **Adicionar mais quando quiser**, **Codex**:

- **Na sua Machine** (padrão): pressione **Conectar Codex** e digite o código exibido pela OpenAI. Ele usa o mesmo plano do ChatGPT que seu modelo, e as tarefas são executadas na sua Machine. Não é preciso usar o terminal. Se você estiver conectado à mesma conta do ChatGPT, sua Machine também poderá ver e usar as redefinições do seu limite de uso.
- **Outras opções**, **No meu computador**: a tarefa é executada no seu computador, onde o Codex está conectado. Ela é transmitida de forma criptografada e só funciona nesse computador. Instale a The Machine nele, faça o pareamento na página da sua conta, execute `codex login` e mantenha a The Machine em execução. O resultado aparece na tarefa. Quando o computador estiver desligado, as tarefas ficam aguardando.
- **Outras opções**, **Codex cloud**: a tarefa é executada na nuvem da OpenAI. Pressione **Conectar Codex**. Ele usa o mesmo plano do ChatGPT que seu modelo, e a OpenAI solicita mais um código, para o Codex. Em seguida, informe o ambiente do Codex cloud em Configurações.

Você também pode entrar pelo painel: **Conexões**, **Projetos e código**, **Codex**, **Receber um código**. Uma Machine auto-hospedada faz esse mesmo login por conta própria.

Em uma Machine hospedada, **Codex e Claude Code** aparece em Configurações quando o GitHub ou o Codex está conectado. Para desenvolvedores: [guia de agentes](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
