---
title: Conexões
area: connections
summary: Suas fontes em um só lugar: como cada uma está, adicionar uma nova ou desconectar uma.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
---
## Como elas estão

A aba **Conexões** agrupa suas fontes em **E-mail e agenda**, **Chat** e **Outras fontes**. Cada uma diz como está: Conectada, Aguardando a primeira sincronização, Reconectando automaticamente ou Precisa da sua ajuda. Abra **Detalhes** para ver **Sincronizações recentes**, onde a sincronização aparece em palavras simples (como "Em dia" ou "Primeira leitura"), e o que fazer.

Seus números mostram o que ela trouxe, o que chegou nas últimas 24 h e o que ainda não foi verificado. Uma agenda conta eventos: todos, os dos próximos 7 dias e os das últimas 24 h.

Abaixo do status, cada fonte diz em uma linha o que traz e, quando pode agir, que só faz isso depois que você toca em **Enviar** ou dá o seu OK.

## Adicionar uma

Abra **+ Adicionar** e escolha uma fonte. Ela pede o que precisa, uma pergunta por vez. **Cancelar** para de adicionar a fonte. Saiu antes de terminar? Abra **Conexões** de novo, em qualquer dispositivo, e continua no mesmo passo. Depois de conectada, sua Machine reinicia para começar a ler a fonte e abre o novo cartão, que mostra como vai a primeira sincronização. Em uma Machine hospedada, Google, Microsoft, Microsoft OneDrive, Zoom, Stripe e Intercom entram por aqui: escolha **Trabalho** ou **Pessoal**, entre e você volta para este formulário, que mostra como a conexão está indo. O GitHub, o WhatsApp, o Codex, os Chats do Telegram e seu celular Android mostram o código direto neste formulário.

Uma fonte que você já conectou mostra isso na lista, com a conta. Escolha-a para adicionar outra ao lado: o formulário avisa e leva até a que você já tem.

A lista é agrupada (**E-mail e agenda**, **Chat**, **Reuniões**, **Documentos e arquivos**, **Clientes**, **Projetos e código**, **Outras**), de A a Z em cada grupo.

**Sugerido para você** aparece no topo quando sua Machine vê um motivo para uma fonte, com esse motivo em uma linha: e-mails da Stripe, reuniões no Zoom na sua agenda, mensagens com link para o Google Docs ou uma configuração que não terminou. Ela conta isso na sua Machine; nada sai dela. Sem motivo, sem seção. Uma fonte conectada nunca é sugerida.

**Reconectar** em uma fonte e em **Precisa de você** abre o mesmo formulário. No seu próprio computador, `assistant connect` faz o mesmo em um terminal.

## Trabalho ou pessoal

Cada fonte conta como trabalho (para uma empresa que você informa) ou pessoal. Mude isso em **Detalhes**. Ela só diz **Palpite** quando sua Machine escolheu pelo endereço. Depois que você escolhe, a escolha é sua. Tarefas de trabalho esperam pelos seus dias de trabalho.

E-mail e agendas do Google e da Microsoft seguem o endereço quando ele é claro: um provedor como Gmail ou Outlook.com é Pessoal, o domínio da sua equipe é Trabalho. Se não, ela pergunta uma vez, logo depois de entrar. **Mudar** deixa você escolher. Se depois o e-mail disser o contrário, a tarefa **Aproveite mais a The Machine** pergunta uma vez se você quer mudar.

## Habilidades

Uma fonte pode trazer sinais (o que chega vira to-dos), fazer coisas para seus to-dos (ler um documento quando um precisa, ou enviar, responder ou mudar algo depois do seu OK), ou ambos. Com ambos, **Detalhes** tem uma chave para cada um: **Traz sinais** e **Pode fazer coisas**. Uma fica ligada. Para parar ambas, desconecte a fonte. As respostas de um chat respondem ao que ele traz, então um chat só tem **Pode fazer coisas**.

Com **Traz sinais** desligado, ela não sincroniza e seu cartão não mostra números. Com **Pode fazer coisas** desligado, sua Machine nunca lê nada sob demanda, não redige nem muda nada com ela. Fontes de antes têm ambas ligadas.

## Remover uma

Abra a fonte, **Detalhes** e depois **Desconectar**. Ela para de ler. O que ela já trouxe continua. Em uma Machine hospedada, Google, Microsoft, Microsoft OneDrive, Zoom e Stripe mostram **Desconectar ↗**, que abre sua página de configuração.

**Desconectado recentemente** lista os logins do Google, da Microsoft e do Zoom que você removeu. **Removido, confirmado** quer dizer que o Google confirmou a saída, ou, no caso da Microsoft e do Zoom, que não sobrou nenhuma cópia. **Pendente** diz o motivo, e sua Machine continua tentando.

## Logins salvos

Sites que o navegador da sua Machine usa, como LinkedIn ou X, podem guardar um login salvo: marque **Salvar para a próxima vez** quando entrar. Depois, **Logins** mostra a lista. Quando um site desconecta sua Machine, ela entra de novo com um toque. As senhas ficam criptografadas na sua Machine. **Esquecer** remove um login.

## Verificações

**Verificações** mostra como sua Machine está lendo o que chega: execuções recentes e o que cada uma encontrou. Veja [Nenhuma tarefa nova](reviews-paused.md).

Cada conexão tem seu próprio artigo nesta seção, com o que ela lê e o que pode enviar.
