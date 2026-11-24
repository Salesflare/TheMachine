---
title: Fazer e o que é enviado
area: cards
summary: Fazer prepara o trabalho. Nada é enviado, pago ou alterado até você aprovar essa etapa.
covers: do-it
code: dashboard.html, next_actions.py, assistant.py
order: 2
translated: 9e0936e0d9712ce3
---
## O que Fazer faz

**Fazer** pede para sua Machine preparar a tarefa: escrever um rascunho de resposta, pesquisar informações, preencher um formulário. Ela usa suas próprias contas e o próprio navegador, como você faria.

Enquanto trabalha no navegador, a tarefa e o chat exibem a página ao vivo, inclusive entre as etapas, até que ela termine. Clique na imagem para abrir o navegador. Na tarefa, ela aparece maior, com **Parar**: um toque encerra a execução na hora.

Antes de fazer um follow-up ou repasse, ela verifica se há respostas mais recentes, inclusive de alguém da equipe. Se a tarefa já foi resolvida, ela avisa. Se a sua Machine alterou um documento ou uma página, a tarefa inclui um link para ele.

Quando sua Machine conclui uma tarefa difícil em um site ou fluxo de trabalho, ela guarda as etapas como uma habilidade, sem dados de ninguém. As tarefas seguintes nesse site recebem essas etapas como orientação, nunca como permissão: para enviar ou pagar, ela ainda espera você. As habilidades aparecem em **Configurações > Skills** como **Aprendido em uma tarefa**.

Se as etapas de uma habilidade deixarem de funcionar em três tarefas seguidas, sua Machine a desativa. Ela só volta a ativá-la quando uma tarefa posterior mostrar o que funciona agora ou quando você a ativar novamente.

## Nada é enviado antes de você aprovar

- Uma resposta volta como rascunho. **Revisar e enviar** abre o rascunho para edição; ele só é enviado quando você pressiona **Enviar agora**.
- Se uma tarefa tiver dois ou mais e-mails, um botão no chat da tarefa permite revisar todos. Eles aparecem um de cada vez com **Próximo**. Na última etapa, todos são enviados. Cada e-mail só aparece como enviado depois que é enviado.
- Um e-mail aparece como será enviado, com negrito, listas e links. Uma mensagem do Slack ou de um chat aparece como texto simples.
- Use **Pedir mudanças** na mesma janela: diga o que quer alterar e sua Machine refaz o rascunho.
- Uma resposta é enviada como resposta ao e-mail mais recente da conversa, e a fonte da tarefa abre esse e-mail.
- Uma etapa que confirma algo, como enviar, pagar ou reservar, espera sua confirmação ou que você peça isso no chat. Confirmar uma etapa não libera as outras: a tarefa só termina quando todas as etapas forem concluídas.
- A tarefa e o chat mostram o que essa etapa vai enviar antes de você tocar nela. Um convite de calendário mostra o título, o horário, os convidados e se um link para a reunião será incluído.
- Ao procurar um horário, os calendários conectados são levados em conta: ela consulta suas reuniões nesses dias antes de sugerir horários.
- No chat de uma tarefa, um rascunho nunca é enviado na mesma mensagem em que foi escrito.
- Até você aprovar, a tarefa fica em **Para você** como **Preparada**, e a lista informa uma vez que nada será enviado até você aprovar. **Preparada** significa que há um rascunho ou resultado pronto para aprovação. Se o trabalho terminar sem um rascunho ou resultado porque precisa de você, por exemplo, de uma decisão, informação que falta, login ou escolha, a tarefa aparece como **Precisa de você**, com uma linha dizendo do que ela precisa. O mesmo vale para uma tarefa que apenas respondeu ou explicou algo ("Respondido. Nada feito ainda."), com **Fazer** em primeiro plano. O mesmo acontece com a notificação e o resumo da manhã. A tarefa só informa que um rascunho foi enviado depois que ele realmente foi.
- Um rascunho que ainda não pode ser usado, como uma proposta sem preço, também aparece como **Precisa de você**: a pergunta aparece na linha, e **Responder** leva até ela. O rascunho continua na tarefa, com **Enviar** em **⋯** ou **Copiar rascunho** acima dos botões. Preencha o que falta e ele volta a aparecer como **Preparada**.
- Um rascunho que já pode ser enviado fica como **Preparada**. Se ainda houver algo que possa melhorar, a linha avisa: "O rascunho está pronto. Uma pergunta: …".
- Um rascunho longo mostra as três primeiras linhas. **Mostrar mais** ou tocar no texto abre o restante. **Revisar e enviar** sempre mostra o rascunho completo.

Dependendo da fonte, ela pode enviar um e-mail, uma mensagem direta no Slack ou uma mensagem pelo WhatsApp, Telegram, LinkedIn ou X. O artigo de cada conexão explica o que ela pode enviar.

## Editar um e-mail

- Use os botões acima do texto ou `Ctrl B` para negrito, `Ctrl I` para itálico e `Ctrl K` para um link (`⌘` no Mac). Também há botões para listas com marcadores e numeradas.
- Um link precisa ter um endereço que comece com https://. O texto colado é inserido sem formatação, cores ou imagens.
- A formatação que não pode ser usada em um e-mail é removida antes, e a mensagem mostra como será enviada. Pressione **Enviar agora** de novo para enviá-la.
- O e-mail é enviado exatamente como aparece, com uma cópia em texto simples para apps de e-mail que não exibem formatação.

## Quando não é possível

- "Não é possível enviar daqui." significa que você precisa copiar o rascunho com **Copiar rascunho** e enviar por conta própria.
- Se uma tarefa aparecer como **Precisa de você** e ainda não houver nada que possa ser enviado, aberto ou lido, ela mostra **Responder**: diga do que ela precisa para que o trabalho continue. Se houver uma etapa que só você pode fazer, como um pagamento no seu banco, ela mostra **Marcar como feito**.
- **Precisa da sua ajuda** significa que há uma pergunta: **Responder**. **Travada** significa que a tarefa parou sem uma pergunta; ela explica o motivo.
- Se alguém pediu mais de uma coisa, cada pergunta tem suas próprias opções ou um campo curto, às vezes preenchido com a resposta da última vez. **Responder** envia todas de uma vez.
- Se alguém pediu informações ou arquivos, ela prepara a resposta com o que encontrou e pede apenas o que falta.
- Se falta algo que só você tem, ela pede isso e prepara apenas o que pode ser enviado sem essa informação, como uma resposta confirmando uma data. Ela não prepara uma resposta que apenas diga que a informação será enviada depois.
- **Tentar de novo** executa a tarefa mais uma vez. **Pedir mudanças** pede outra coisa. Em uma tarefa travada, **Tentar de novo** aparece em primeiro plano, e **Detalhes** mostra o que ela tentou.
- Se a tarefa travou porque a própria execução falhou, sua Machine tenta executá-la mais uma vez depois de ser atualizada.
- Ela tenta executar de novo uma tarefa que falhou, no máximo duas vezes por conta própria. Depois disso, espera por algo novo, como uma nova mensagem ou uma mensagem sua no chat da tarefa, ou que você pressione **Tentar de novo**.
- Enquanto prepara a tarefa, ela informa em uma linha simples o que sua Machine está fazendo, como "Lendo o e-mail", "Lendo o PDF" ou "Escrevendo o rascunho". As etapas detalhadas ficam no chat da tarefa.
- Uma tarefa marcada como **Preparando…** começa em segundos. Se precisar esperar, ela explica o motivo e dá uma estimativa, como "Começa depois da tarefa atual".
- Uma tarefa que sua Machine prepara antes de você pedir pode esperar enquanto ela economiza uso. Ela ainda mostra **Fazer**: pressione para iniciar agora, antes das outras tarefas. Nada é enviado antes de você aprovar. Se o limite de uso do seu plano de IA for atingido, Fazer avisa, e a tarefa começa quando o limite for renovado.
- Se um site pedir que você entre na sua conta, pressione **Entrar** ou **Abrir o navegador** e faça login por lá. Depois, ela continua sozinha. Se não continuar, pressione **Continuar**.
- Um código enviado para seu celular ou uma permissão que falta interrompe a tarefa. Ela informa do que precisa e mostra **Continuar** ou **Tentar de novo**. Se uma fonte não estiver conectada, como o Slack, **Conectar Slack** aparece na tarefa. Ela continua sozinha depois que o Slack estiver conectado.
