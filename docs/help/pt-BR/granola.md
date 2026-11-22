---
title: Granola
area: connections
summary: Notas e transcrições das reuniões que você teve no Granola. A integração só lê.
covers: connector:granola
code: connectors/granola.py, meeting_notes.py, onboarding.py
site: Connect, More sources, Remove
translated: fb6244142af7800d
---
## O que ela lê

As notas e transcrições das reuniões em que você participou no Granola: os últimos 7 dias quando você conecta a integração e, depois, as novas notas conforme são adicionadas. Notas ainda em edição são importadas quando Granola termina de escrevê-las.

Cada nota é vinculada à reunião correspondente no seu calendário: a que Granola identifica ou, se não houver, a reunião no mesmo horário. As notas do Granola ficam em Notas, e a transcrição, em Transcrição, marcadas como **Do Granola**. O que você adicionou continua lá.

Depois da reunião, a Machine lê as notas e transcrições para identificar o que foi prometido, decidido ou ainda está pendente, como "Vou enviar a apresentação", e cria tarefas apenas para próximos passos claros. As pessoas da reunião são vinculadas ao seu [Graph](graph.md) pelo endereço de e-mail.

## O que ela pode fazer

Nada no Granola. A integração só lê, e nunca altera, compartilha ou exclui uma nota.

## O que ela solicita

Uma chave de API pessoal do Granola. O Granola oferece chaves de API nos planos Business e Enterprise. A chave permite ler suas próprias notas e as que compartilharam com você, da mesma forma que aparecem no Granola.

## Conectar

1. No app para computador do Granola: **Configurações**, Connectors, API keys. Crie uma chave com acesso a Personal notes e copie-a.
2. No painel: **Conexões**, **Reuniões**, Granola. Ou, na página de configuração de uma Machine hospedada em app.themachine.computer/setup: **Mais fontes**, Granola. No seu próprio computador, `assistant connect granola` também solicita a chave.
3. Cole a chave, escolha **Trabalho** ou **Pessoal** e pressione **Conectar**.

A chave é verificada na hora. Se o Granola deixar de aceitá-la, Granola em **Conexões** solicitará uma nova chave.

## Remover

- No painel: **Conexões**, abra Granola, selecione **Detalhes** e depois **Desconectar**. O conteúdo que já foi importado continua lá.
- Em uma Machine hospedada, você também pode pressionar **Remover** ao lado de Granola na página de configuração.

## Revogar a chave no Granola

No app para computador do Granola: **Configurações**, Connectors, API keys. Depois, exclua a chave.
