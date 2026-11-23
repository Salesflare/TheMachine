---
title: Fazer e o que é enviado
area: cards
summary: Fazer prepara o trabalho. Nada é enviado, pago ou alterado até você aprovar essa etapa.
covers: do-it
code: dashboard.html, next_actions.py, assistant.py
order: 2
translated: f6078d1de97851ae
---
## O que Fazer faz

**Fazer** pede para sua Machine preparar a tarefa: escrever uma resposta, pesquisar, preencher um formulário. Ela usa suas próprias contas e o próprio navegador, como você faria.

Enquanto trabalha no navegador, a tarefa e o chat mostram a página ao vivo, inclusive entre as etapas, até o trabalho terminar. Clique na imagem para abrir o navegador. Na tarefa, ela abre ampliada, com **Parar**: um toque encerra a execução na hora.

Antes de fazer um follow-up ou repasse, ela verifica se há respostas mais recentes, inclusive de alguém da equipe. Se a tarefa já tiver sido resolvida, ela avisa. Quando altera um documento ou uma página, a tarefa inclui um link para ele.

Quando sua Machine conclui uma tarefa difícil em um site ou fluxo de trabalho, ela guarda as etapas como uma habilidade, sem dados de ninguém. Tarefas futuras nesse site usam essas etapas como orientação, nunca como autorização: enviar ou pagar ainda depende de você. Elas aparecem em **Configurações > Habilidades** como **Aprendido em uma tarefa**.

Se as etapas de uma habilidade dessas deixarem de funcionar em três tarefas seguidas, sua Machine desativa a habilidade até que uma tarefa posterior mostre o que funciona agora ou você a ative de novo.

## Nada é enviado sem sua aprovação

- Uma resposta volta como rascunho. **Revisar e enviar** abre o rascunho para edição. Ele só é enviado quando você toca em **Enviar agora**.
- Se uma tarefa tiver dois ou mais e-mails, um botão no chat permite revisar todos. Cada um aparece por vez com **Próximo**. Na última etapa, todos são enviados. Cada e-mail só aparece como enviado depois que é enviado.
- Um e-mail aparece como será visto, com negrito, listas e links. Uma mensagem do Slack ou de um chat é texto simples.
- **Pedir mudanças** na mesma janela: diga o que mudar e sua Machine refaz o rascunho.
- Uma resposta responde ao e-mail mais recente da conversa, e a origem da tarefa abre esse e-mail.
- Uma etapa que confirma uma ação, como enviar, pagar ou reservar, espera sua confirmação ou que você peça isso no chat. Confirmar uma etapa não libera as outras: a tarefa só é encerrada quando todas as etapas terminam.
- A tarefa e o chat mostram o que uma etapa dessas vai enviar antes de você tocar nela. Um convite de calendário mostra o título, o horário, os convidados e se um link de reunião será adicionado.
- Os calendários conectados são considerados quando ela procura um horário: antes de sugerir horários, ela consulta suas reuniões nesses dias.
- No chat de uma tarefa, um rascunho nunca é enviado na mesma mensagem em que foi escrito.
- Até você aprovar, a tarefa fica em **Para você** como **Preparada**, e a lista informa uma vez que nada será enviado até você aprovar. **Preparada** significa que um rascunho ou resultado está pronto para aprovação. Se o trabalho terminar sem um rascunho ou resultado porque precisa de você (para uma decisão, uma informação que falta, uma entrada na conta ou uma escolha), a tarefa aparece como **Precisa de você**, com uma linha explicando o que falta. O mesmo vale para uma tarefa em que ela apenas respondeu ou explicou algo ("Respondido. Nada feito ainda."), com **Fazer** em primeiro lugar. Isso também vale para a notificação e o resumo da manhã. A tarefa só informa que um rascunho foi enviado depois que ele realmente foi.
- Um rascunho longo mostra as três primeiras linhas. **Mostrar mais**, ou tocar no texto, abre o restante. **Revisar e enviar** sempre mostra o texto completo.

Dependendo da origem, ela pode enviar um e-mail, uma mensagem direta no Slack ou uma mensagem pelo WhatsApp, Telegram, LinkedIn ou X. O artigo de cada conexão explica o que ela pode enviar.

## Editar um e-mail

- Use os botões acima do texto ou `Ctrl B` para negrito, `Ctrl I` para itálico e `Ctrl K` para um link (`⌘` no Mac). Também há botões para listas com marcadores e numeradas.
- O link precisa começar com https://. O texto colado fica sem formatação, cores ou imagens.
- Primeiro, a formatação que não pode ser mantida no e-mail é removida, e a mensagem mostra como será enviada. Toque em **Enviar agora** novamente para enviá-la.
- O e-mail é enviado exatamente como aparece, com uma cópia em texto simples para apps de e-mail que não exibem formatação.

## Quando não é possível

- "Não é possível enviar daqui." significa que você precisa copiar o rascunho com **Copiar rascunho** e enviá-lo por conta própria.
- Uma tarefa marcada como **Precisa de você**, sem nada para enviar, abrir ou ler, começa com **Responder**: diga o que falta e ela continua. Uma etapa que só você pode realizar, como um pagamento no seu banco, começa com **Marcar como feito**.
- **Precisa da sua ajuda** significa que ela tem uma pergunta: **Responder**. **Travada** significa que ela parou sem fazer uma pergunta; a tarefa explica o motivo.
- Pediu mais de uma coisa? Cada pergunta tem opções próprias ou um campo curto, às vezes preenchido com a resposta anterior. **Responder** envia tudo de uma vez.
- Alguém pediu informações ou arquivos? Ela prepara uma resposta com o que encontrou e pede apenas o que falta.
- Falta algo que só você tem? Ela pede isso e prepara apenas o que pode ser enviado sem essa informação, como uma resposta confirmando uma data. Ela não prepara uma resposta dizendo apenas que a informação está a caminho.
- **Tentar de novo** executa a tarefa mais uma vez. **Pedir mudanças** solicita outra coisa. Em uma tarefa travada, **Tentar de novo** aparece primeiro, e **Detalhes** mostra o que ela tentou fazer.
- Se a tarefa ficou travada porque a própria execução falhou, sua Machine tenta executá-la novamente uma vez, depois de ser atualizada.
- Ela tenta executar novamente uma tarefa que falhou no máximo duas vezes por conta própria. Depois, espera algo novo, como uma nova mensagem ou o que você escrever no chat, ou que você toque em **Tentar de novo**.
- Enquanto prepara a tarefa, ela informa o que sua Machine está fazendo em uma linha simples, como "Lendo o e-mail", "Lendo o PDF" ou "Escrevendo o rascunho". As etapas detalhadas ficam no chat da tarefa.
- Uma tarefa marcada como **Preparando…** começa em segundos. Se precisar esperar, ela explica o motivo e dá uma estimativa, como "Começa depois da tarefa atual".
- Uma tarefa que sua Machine prepara antes de você pedir pode esperar enquanto ela economiza uso. Ela ainda mostra **Fazer**: toque para começar agora, antes das outras. Nada é enviado sem sua aprovação. Se o limite de uso do seu plano de IA for atingido, Fazer informa isso e a tarefa começa quando o limite for redefinido.
- Se um site pedir que você entre na conta, toque em **Entrar** ou em **Abrir o navegador** e entre por lá. Depois, ela continua por conta própria. Se não continuar, toque em **Continuar**.
- Um código enviado para o seu celular ou uma permissão que falta pode interromper a tarefa. Ela informa o que precisa e mostra **Continuar** ou **Tentar de novo**. Se uma conexão não estiver configurada, como o Slack, **Conectar Slack** aparece na tarefa. Ela continua por conta própria depois que o Slack estiver conectado.
