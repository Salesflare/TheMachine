---
title: Fazer e o que é enviado
area: cards
summary: Fazer prepara o trabalho. Nada é enviado, pago ou alterado até você aprovar essa etapa.
covers: do-it
code: dashboard.html, next_actions.py, assistant.py
order: 2
translated: b0f79ee45009cfde
---
## O que Fazer faz

**Fazer** pede para sua Machine preparar a tarefa: escrever um rascunho de resposta, pesquisar informações, preencher um formulário. Ela usa suas próprias contas e o próprio navegador, como você faria.

Enquanto trabalha no navegador, a tarefa e o chat dela mostram a página ao vivo, inclusive entre as etapas, até terminar ali. Clique na imagem para abrir o navegador. Na tarefa, a página abre maior, com **Parar**: um toque interrompe essa execução imediatamente.

Antes de fazer um follow-up ou passar algo adiante, ela verifica se há respostas mais recentes, inclusive de alguém da equipe. Se alguém já resolveu, a tarefa informa isso. Se ela alterou um documento ou uma página, a tarefa inclui um link para ele.

Quando consegue concluir uma tarefa difícil em um site ou fluxo de trabalho, sua Machine guarda as etapas como uma habilidade, sem dados de ninguém. Tarefas futuras nesse site recebem essas etapas como orientação, nunca como autorização: enviar ou pagar ainda depende de você. Elas aparecem em **Configurações > Habilidades** como **Aprendido em uma tarefa**.

## Nada é enviado antes do seu ok

- Uma resposta volta como rascunho. **Revisar e enviar** abre o rascunho pronto para edição. Ele só é enviado quando você toca em **Enviar agora**.
- Se houver dois ou mais e-mails na mesma tarefa, um botão no chat dela permite revisar todos. Eles aparecem um por vez com **Próximo**, e a última etapa envia todos. Cada e-mail só aparece como enviado depois que realmente for enviado.
- Um e-mail aparece como será enviado, com negrito, listas e links. Uma mensagem do Slack ou de um chat aparece como texto simples.
- **Pedir mudanças** na mesma janela: diga o que alterar e sua Machine refaz o rascunho.
- Uma resposta responde ao e-mail mais recente da conversa, e a fonte da tarefa abre esse e-mail.
- Uma etapa que confirma uma ação, como enviar, pagar ou reservar, espera sua confirmação ou que você peça isso no chat. Confirmar uma etapa não libera as outras: a tarefa só é encerrada quando todas as etapas estiverem concluídas.
- A tarefa e o chat dela mostram o que uma etapa desse tipo vai enviar antes de você tocar no botão. Um convite de calendário mostra o título, o horário, os convidados e se um link para a reunião será incluído.
- Os calendários conectados são considerados na busca por horários: ela consulta suas reuniões nesses dias antes de sugerir horários.
- No chat de uma tarefa, um rascunho nunca é enviado na mesma mensagem em que foi escrito.
- Até você aprovar, a tarefa fica em **Para você** com o status **Preparada**, e a lista informa uma vez que nada será enviado até você aprovar. **Preparada** significa que há um rascunho ou resultado pronto para aprovação. Se o trabalho terminar sem um resultado porque ela precisa de você, por exemplo, para tomar uma decisão, fornecer uma informação que falta ou entrar em uma conta, a tarefa mostra **Precisa de você** e informa o que está faltando. O mesmo acontece quando ela apenas responde ou explica algo ("Respondido. Nada feito ainda."), com **Fazer** em destaque. Isso também vale para a notificação e o resumo da manhã. A tarefa só informa que um rascunho foi enviado depois que ele realmente for enviado.
- Um rascunho longo mostra as 3 primeiras linhas. **Mostrar mais** ou tocar no texto abre o restante. **Revisar e enviar** sempre mostra o texto completo.

Dependendo da fonte, ela pode enviar um e-mail, uma mensagem direta no Slack ou uma mensagem pelo WhatsApp, Telegram, LinkedIn ou X. O artigo de cada conexão explica o que ela pode enviar.

## Editar um e-mail

- Use os botões acima do texto ou `Ctrl B` para negrito, `Ctrl I` para itálico e `Ctrl K` para um link (`⌘` no Mac). Também há botões para listas com marcadores e numeradas.
- Um link precisa ter um endereço que comece com https://. O texto colado é inserido sem formatação, cores ou imagens.
- A formatação que não pode ser mantida em um e-mail é removida primeiro, e a mensagem mostra como ficará. Toque em **Enviar agora** novamente para enviar.
- O e-mail é enviado exatamente como aparece, com uma cópia em texto simples para aplicativos de e-mail que não exibem formatação.

## Quando ela não consegue

- "Não é possível enviar daqui." significa que você pode copiar o rascunho com **Copiar rascunho** e enviá-lo por conta própria.
- Quando **Precisa de você** aparece sem nada para enviar, abrir ou ler, a tarefa começa com **Responder**: diga o que falta e ela continua. Se só você puder fazer uma etapa, como um pagamento no seu banco, ela começa com **Marcar como feito**.
- **Precisa da sua ajuda** significa que ela tem uma pergunta: **Responder**. **Travada** significa que ela parou sem fazer uma pergunta. A tarefa informa o motivo.
- Se ela fizer mais de uma pergunta, cada uma terá opções próprias ou um campo curto, às vezes preenchido com a resposta anterior. **Responder** envia todas juntas.
- Se faltar algo que só você tem, ela pede e prepara apenas o que pode fazer sem essa informação, como uma resposta confirmando uma data. Ela não prepara uma resposta que só diga que a informação será enviada depois.
- **Tentar de novo** executa a tarefa mais uma vez. **Pedir mudanças** solicita outra coisa. Em uma tarefa travada, **Tentar de novo** aparece em destaque, e **Detalhes** mostra o que ela tentou fazer.
- Se a execução em si falhar e a tarefa ficar travada, sua Machine tenta executá-la mais uma vez depois de ser atualizada.
- Ela tenta executar novamente uma tarefa que falhou, no máximo duas vezes por conta própria. Depois disso, espera algo novo, como uma nova mensagem ou uma mensagem sua no chat, ou que você toque em **Tentar de novo**.
- Enquanto prepara a tarefa, ela informa em uma linha simples o que sua Machine está fazendo, como "Lendo os e-mails", "Lendo o PDF" ou "Escrevendo o rascunho". As etapas detalhadas ficam no chat da tarefa.
- Uma tarefa com o status **Preparando…** começa em segundos. Se precisar esperar, ela informa o motivo e uma estimativa de quando começará, como "Começa depois da tarefa atual".
- Uma tarefa que sua Machine prepara antes de você pedir pode esperar enquanto ela economiza uso. Mesmo assim, ela mostra **Fazer**: toque para começar agora, antes das outras. Nada é enviado antes do seu ok. Se o limite de uso do seu plano de IA for atingido, Fazer informa isso e começa quando o limite for redefinido.
- Se um site pedir que você entre na sua conta, toque em **Entrar** ou em **Abrir o navegador** e entre por lá. Depois, ela continua por conta própria. Se não continuar, toque em **Continuar**.
- Um código enviado para o seu celular ou uma permissão que esteja faltando pode interromper a tarefa. Ela informa do que precisa e mostra **Continuar** ou **Tentar de novo**. Se uma fonte não estiver conectada, como o Slack, **Conectar ao Slack** aparece na tarefa. Ela continua por conta própria depois que o Slack for conectado.
