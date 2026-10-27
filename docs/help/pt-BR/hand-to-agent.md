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

## Configurar

Em **Configurações**, **Geral**, em **Agentes de código**:

- **Sessão do Claude Code**: o endereço de uma sessão do Claude Code.
- **Ambiente de nuvem do Codex**: o id do ambiente.
- **Roda em** e, se quiser, uma **Branch**.

O Claude envia o resultado de volta pelo conector da The Machine. Adicione o conector uma vez no claude.ai, em Settings, Connectors, Add custom connector, com o endereço mostrado ali. Para o Codex em uma Machine hospedada, clique primeiro em **Conectar o Codex** na sua página de configuração, em **Adicione mais quando quiser**. Ele usa o mesmo plano do ChatGPT que o seu modelo, e a OpenAI pede mais um código, para o Codex.

Em uma Machine hospedada, Agentes de código aparece quando o GitHub ou o Codex está conectado. Também aparece em configurações que rodam trabalhos em outro lugar. Mais no [guia de agentes](https://github.com/Salesflare/TheMachine/blob/main/docs/agents.md).
