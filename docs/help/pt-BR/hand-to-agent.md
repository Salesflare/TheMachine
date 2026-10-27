---
title: Passar para o Claude Code ou o Codex
area: cards
summary: Envie uma tarefa de código para o Claude Code ou o Codex. O resultado volta na tarefa.
covers: hand-to-agent
code: agent_jobs.py, agent_remote.py, dashboard.html
site: Connect Codex, Add more any time
order: 5
---
## Passar uma tarefa

1. Na tarefa, abra **Mais** e escolha **Passar para o Codex** ou **Passar para o Claude Code**. A opção aparece quando essa ferramenta está configurada.
2. Confira o resumo e o que ela recebe, adicione uma nota se quiser e clique em **Passar**. **Ver o trabalho completo** mostra as instruções inteiras.

A tarefa então mostra que está em andamento e, quando terminar, o resultado, com **Mostrar mudanças**. **Mudar** pede mudanças. **Passar de novo** começa do zero.

Um trabalho nunca envia nada por você.

## No app do Codex

- **Abrir no Codex** abre a conversa do trabalho no app do Codex. Enquanto o Codex trabalha nela aqui, o app ainda não consegue abri-la. Ela abre quando terminar.
- **Alterar** numa conversa aberta no app do Codex continua nessa mesma conversa lá, e a tarefa acompanha.
- Um trabalho só para se o Codex ficar 30 minutos sem fazer nada, ou depois de 6 horas no total. Reiniciar The Machine não o para.

## Configurar

Em **Configurações**, **Geral**, em **Agentes de código**:

- **Sessão do Claude Code**: o endereço de uma sessão do Claude Code.
- **Ambiente de nuvem do Codex**: o id do ambiente, para a nuvem do Codex.
- **Roda em** e, se quiser, uma **Branch**.

O Claude envia o resultado de volta pelo conector da The Machine. Adicione o conector uma vez no claude.ai, em Settings, Connectors, Add custom connector, com o endereço mostrado ali.

## Onde o Codex roda

Em uma Machine hospedada, escolha na sua página de configuração, em **Adicione mais quando quiser**, **Codex**:

- **No meu computador** (o padrão): o trabalho roda no seu próprio computador, com o Codex conectado lá. Nada do Codex fica no seu servidor, e o trabalho é criptografado só para esse computador: a Network repassa, mas não consegue ler. Instale The Machine nesse computador, pareie na sua página Conta e rode `codex login` lá. Deixe The Machine rodando nele. O trabalho aparece como uma conversa no app do Codex nesse computador, e o resultado volta na tarefa. Quando o computador está desligado, os trabalhos esperam até ele voltar.
- **Nuvem do Codex**: o trabalho roda na nuvem da OpenAI. Clique em **Conectar o Codex**. Ele usa o mesmo plano do ChatGPT que o seu modelo, e a OpenAI pede mais um código, para o Codex. Depois digite o ambiente de nuvem do Codex em Configurações.

Em uma Machine hospedada, Agentes de código aparece quando o GitHub ou o Codex está conectado. Também aparece em configurações que rodam trabalhos em outro lugar. Mais no [guia de agentes](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
