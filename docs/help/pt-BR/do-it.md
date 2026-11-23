---
title: Fazer e o que é enviado
area: cards
summary: Fazer prepara o trabalho. Nada é enviado, pago ou alterado até você aprovar essa etapa.
covers: do-it
code: dashboard.html, next_actions.py, assistant.py
order: 2
translated: 81798e7a2a6fa66e
---
## O que Fazer faz

**Fazer** pede para sua Machine preparar a tarefa: escrever um rascunho da resposta, pesquisar informações, preencher um formulário. Ela usa suas próprias contas e o navegador dela, como você faria.

Enquanto trabalha no navegador, a tarefa e o chat mostram essa página ao vivo, inclusive entre as etapas, até a tarefa ser concluída ali. Clique na imagem para abrir o navegador. Na tarefa, a imagem aparece maior, com **Parar**: um toque encerra a execução na hora.

Antes de fazer um follow-up ou passar a tarefa adiante, ela verifica se há respostas mais recentes, inclusive de alguém da equipe. Se alguém já resolveu a tarefa, ela avisa. Quando altera um documento ou uma página, a tarefa inclui um link para ele.

Quando conclui uma tarefa difícil em um site ou fluxo de trabalho, sua Machine guarda as etapas como uma habilidade, sem dados de ninguém. Tarefas futuras nesse site recebem essas etapas como orientação, nunca como autorização: enviar ou pagar ainda depende de você. Elas aparecem em **Configurações > Habilidades** como **Aprendido em uma tarefa**.

## Nada é enviado sem sua aprovação

- A resposta volta como rascunho. **Revisar e enviar** abre o rascunho pronto para edição; ele só é enviado quando você toca em **Enviar agora**.
- Se houver dois ou mais e-mails na mesma tarefa, um botão no chat permite revisar todos. Eles aparecem um de cada vez com **Próximo**. Na última etapa, você envia todos. Cada e-mail só aparece como enviado depois de ser enviado.
- O e-mail aparece como vai ser enviado, com negrito, listas e links. Uma mensagem do Slack ou de um chat aparece como texto simples.
- **Pedir mudanças** na mesma janela: diga o que quer alterar e sua Machine refaz o rascunho.
- A resposta vai para o e-mail mais recente da conversa, e a fonte da tarefa abre esse e-mail.
- Uma etapa que confirma uma ação, como enviar um formulário, pagar ou fazer uma reserva, espera sua confirmação ou que você peça isso no chat. Confirmar uma etapa não libera as outras: a tarefa só é encerrada quando todas as etapas estão concluídas.
- A tarefa e o chat mostram o que essa etapa vai enviar antes de você tocar no botão. Um convite de calendário mostra o título, o horário, os convidados e se inclui um link para a reunião.
- Os calendários conectados são considerados na busca por um horário: ela consulta suas reuniões nesses dias antes de sugerir horários.
- No chat de uma tarefa, um rascunho nunca é enviado na mesma mensagem em que foi escrito.
- Até você aprovar, a tarefa fica em **Para você** como **Preparada**, e a lista avisa uma vez que nada será enviado até você aprovar. **Preparada** significa que há um rascunho ou resultado pronto para aprovação. Se o trabalho terminar sem um rascunho ou resultado porque precisa de você (para tomar uma decisão, fornecer uma informação que falta, entrar em uma conta ou fazer uma escolha), a tarefa mostra **Precisa de você** e explica o que está faltando. O mesmo acontece quando ela apenas responde ou explica algo ("Respondido. Nada feito ainda."), com **Fazer** em destaque. Isso também vale para a notificação e o resumo da manhã. A tarefa só avisa que um rascunho foi enviado depois que ele for enviado.
- Um rascunho longo mostra as três primeiras linhas. **Mostrar mais** ou tocar no texto abre o restante. **Revisar e enviar** sempre mostra o texto completo.

Ela pode enviar e-mails, mensagens diretas do Slack ou mensagens pelo WhatsApp, Telegram, LinkedIn ou X, dependendo da fonte. O artigo de cada conexão explica o que ela pode enviar.

## Editar um e-mail

- Use os botões acima do texto ou `Ctrl B` para negrito, `Ctrl I` para itálico e `Ctrl K` para um link (`⌘` no Mac). Também há botões para listas com marcadores e numeradas.
- O endereço de um link precisa começar com https://. O texto colado é inserido sem formatação, cores ou imagens.
- A formatação que não funciona em um e-mail é removida antes do envio, e a mensagem mostra como ficará. Toque em **Enviar agora** outra vez para enviar.
- O e-mail é enviado exatamente como aparece, com uma cópia em texto simples para os aplicativos de e-mail que não exibem formatação.

## Quando ela não consegue

- "Não é possível enviar isso por aqui." significa que você precisa copiar o rascunho com **Copiar rascunho** e enviar por conta própria.
- Quando a tarefa mostra **Precisa de você**, mas não há nada para enviar, abrir ou ler, ela começa com **Responder**: diga o que está faltando para ela continuar. Se houver uma etapa que só você pode fazer, como um pagamento no seu banco, ela começa com **Marcar como feito**.
- **Precisa da sua ajuda** significa que há uma pergunta: **Responda**. **Travada** significa que a tarefa parou sem fazer uma pergunta; ela explica o motivo.
- Se ela perguntar mais de uma coisa, cada pergunta tem suas próprias opções ou um campo curto, às vezes preenchido com sua resposta da última vez. **Responder** envia todas as respostas de uma vez.
- Se alguém pediu informações ou arquivos, ela prepara uma resposta com o que encontrou e pede apenas o que falta.
- Se faltar algo que só você tem, ela pede isso e prepara apenas o que pode ser feito sem essa informação, como uma resposta confirmando uma data. Ela não prepara uma resposta que apenas diga que vai enviar a informação depois.
- **Tentar de novo** executa a tarefa mais uma vez. **Pedir mudanças** pede outra coisa. Em uma tarefa travada, **Tentar de novo** aparece em destaque, e **Detalhes** mostra o que ela tentou fazer.
- Se a tarefa travou porque a própria execução falhou, sua Machine tenta executá-la mais uma vez depois de ser atualizada.
- Ela tenta executar uma tarefa que falhou por conta própria no máximo duas vezes. Depois disso, espera algo novo, como uma nova mensagem ou o que você escrever no chat, ou que você toque em **Tentar de novo**.
- Enquanto prepara a tarefa, ela mostra em uma frase simples o que sua Machine está fazendo, como "Lendo o e-mail", "Lendo o PDF" ou "Escrevendo o rascunho". As etapas detalhadas ficam no chat da tarefa.
- Uma tarefa marcada como **Preparando…** começa em alguns segundos. Se precisar esperar, ela explica o motivo e dá uma previsão aproximada, como "Começa depois da tarefa atual".
- Uma tarefa que sua Machine prepara antes de você pedir pode esperar enquanto economiza seu uso. Ela continua mostrando **Fazer**: toque para começar agora, antes das outras tarefas. Nada é enviado sem sua aprovação. Se o limite de uso do seu plano de IA for atingido, Fazer avisa e inicia a tarefa quando o limite for redefinido.
- Se um site pedir para você entrar na sua conta, toque em **Entrar** ou em **Abrir o navegador** e entre por lá. Depois, ela continua sozinha. Se isso não acontecer, toque em **Continuar**.
- Um código enviado para o seu celular ou uma permissão que esteja faltando pode interromper a tarefa. Ela explica o que precisa e mostra **Continuar** ou **Tentar de novo**. Se uma fonte não estiver conectada, como o Slack, **Conectar Slack** aparece na tarefa. Ela continua sozinha depois que o Slack estiver conectado.
