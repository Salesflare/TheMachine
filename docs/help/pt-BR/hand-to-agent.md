---
title: Passar para o Claude Code ou o Codex
area: cards
summary: Envie uma tarefa de código para o Claude Code ou o Codex. O resultado volta na tarefa.
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time, On your Machine, Other ways, On my computer
order: 5
translated: 333d553e80aea529
---
## Passar uma tarefa

1. Na tarefa, abra **…**, depois **Passar…**, e escolha **Codex** ou **Claude Code**. Só aparecem as ferramentas que você configurou.
2. Confira o resumo e o que ela recebe, adicione uma nota se quiser e clique em **Passar**. **Ver o trabalho completo** mostra as instruções inteiras.

A tarefa então mostra que está em andamento e, quando terminar, o resultado, com **O que fez** e **Mostrar mudanças**. **Pedir mudanças** diz o que mudar. **Passar…** em **…** começa do zero. **Ocultar** guarda o resultado. Uma tarefa **Travada** que você passa mostra **Processando…** enquanto o trabalho roda.

Um trabalho nunca envia nada por você. Quando ele deixa uma etapa de publicar ou fazer deploy para você, **Fazer** na tarefa executa essa etapa. Uma resposta que ele escreveu continua como rascunho que você mesmo envia.

## No app do Codex

- **Abrir no Codex** abre a conversa do trabalho no app do Codex, depois que o trabalho termina.
- **Pedir mudanças** continua nessa mesma conversa do Codex, e a tarefa acompanha.
- Um trabalho para depois de 30 minutos sem progresso ou de 6 horas no total. Uma reinicialização não o interrompe.

## Configurar

Em **Configurações**, **Modelo**, em **Codex e Claude Code**:

- **Codex**: onde ele roda. Na sua Machine ou no seu computador, não precisa de mais nada aqui; **Mudar** abre a sua página de configuração.
- **Codex cloud**: o ID do ambiente, do Codex, e, se quiser, uma **Branch** de onde começar.
- **Claude Code**: o link de uma sessão do Claude Code.

O Claude envia o resultado de volta pelo conector da The Machine. Adicione o conector uma vez no claude.ai, em Settings, Connectors, Add custom connector, com o endereço mostrado abaixo da sessão.

## Onde o Codex roda

Em uma Machine hospedada, escolha na sua página de configuração, em **Adicionar mais quando quiser**, **Codex**:

- **Na sua Machine** (o padrão): clique em **Conectar Codex** e digite na OpenAI o código que aparece. Ele usa o mesmo plano do ChatGPT que o seu modelo, e os trabalhos rodam na sua Machine. Sem terminal.
- **Outras formas**, **No meu computador**: o trabalho roda no seu próprio computador, com o Codex conectado lá. O trabalho viaja criptografado, só para esse computador. Instale a The Machine nesse computador, pareie na sua página Conta, rode `codex login` e deixe a The Machine rodando. O resultado volta na tarefa. Quando o computador está desligado, os trabalhos esperam.
- **Outras formas**, **Codex cloud**: o trabalho roda na nuvem da OpenAI. Clique em **Conectar Codex**. Ele usa o mesmo plano do ChatGPT que o seu modelo, e a OpenAI pede mais um código, para o Codex. Depois digite o ambiente de nuvem do Codex em Configurações.

Ou entre pelo painel: **Conexões**, **Projetos e código**, **Codex**, **Receber um código**. Uma Machine auto-hospedada faz esse mesmo login sozinha.

Em uma Machine hospedada, **Codex e Claude Code** aparece em Configurações quando o GitHub ou o Codex está conectado. Para desenvolvedores: o [guia de agentes](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
