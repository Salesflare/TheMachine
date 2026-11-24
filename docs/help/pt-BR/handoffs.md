---
title: Repasses
area: fleet
summary: Compartilhe uma tarefa com um colega ou passe para a Machine dele usando **Passar…** na tarefa. Faça follow-up depois ou retome a tarefa.
covers: handoffs
code: fleet_requests.py, dashboard.html
order: 3
translated: d9b21c04fb0d34a6
---
## Passe uma tarefa

1. Na tarefa, abra **…**, depois **Passar…** e escolha **Um colega**.
2. Escolha a pessoa, confira o que será enviado (× exclui uma parte) e adicione uma observação. Nada de uma conta Pessoal ou de outra empresa será enviado.
3. Envie. A Machine da pessoa mostra a tarefa para ela.

A Machine da pessoa envia uma notificação para o celular ou pelo Telegram. Se nenhum dos dois estiver configurado, ela recebe um e-mail uma vez, com o nome de quem passou a tarefa, o título e um link. Consulte [Notificações](notifications.md).

Uma conversa do Intercom também é enviada. Se a Machine da pessoa tiver acesso ao mesmo espaço de trabalho do Intercom, **Ler mensagem** abre a conversa e a resposta dela volta para o Intercom. Caso contrário, a tarefa inclui um link para a conversa.

Enquanto você espera, a tarefa mostra o que você pediu e quando ("Pedido feito a Pat na ter., 3 de nov.: …"), mas só quando isso acrescenta algo ao título. Ela fica em **Volta mais tarde**, com o status "Com Pat · aguardando" e uma data para fazer follow-up. **Fazer follow-up agora** prepara um lembrete curto para Pat enviar; **Mudar horário** altera a data do follow-up.

Se a Machine de Pat não puder enviar notificações, a tarefa mostra "Pat não vai receber uma notificação. Avise a pessoa." Avise Pat por conta própria. Essa mensagem desaparece quando Pat ativa as notificações.

A tarefa só volta para o topo quando há algo para decidir: Pat respondeu, recusou ou concluiu a tarefa, o repasse falhou ou chegou um prazo. A data do follow-up depende do prazo: algumas horas antes, se for hoje; no último dia útil, se estiver próximo; na manhã seguinte, se for urgente; ou em 3 dias úteis, nos outros casos.

Quando voltar para fazer follow-up, a tarefa mostra "Ainda com Pat". **Fazer follow-up agora** prepara um lembrete curto para Pat no canal em que você fez o pedido (Slack, WhatsApp, Telegram ou e-mail), direto na tarefa. Nada é enviado até você escolher **Enviar**. Depois, a tarefa volta a aguardar Pat. Se nenhum dos serviços conectados puder enviar uma mensagem para Pat, o chat será aberto com essa informação. **Retomar** e **Passar para outra pessoa** ficam em **…**, depois em **Passar…**.

O chat da tarefa mostra quando ela foi enviada ("Passada para a Machine de Pat · 14:02") e o que aconteceu depois: foi aceita, recusada (com uma observação) ou concluída. Se ainda não houver resposta, aparecem as opções **Marcar como feito**, **Adiar** e **Não precisa**. Para lembrar Pat ou retomar a tarefa, diga isso no chat.

Se o repasse não for enviado, a tarefa e o chat mostram essa informação, com a opção **Tentar de novo**.

## O que a outra pessoa vê

Somente essa tarefa: o que você pediu, sua observação, o prazo e o contato, além de cópias das mensagens enviadas (até três, sem anexos). Ela não vê sua caixa de entrada nem suas outras tarefas. A pessoa escolhe **Aceitar** ou **Recusar**.

Quando a pessoa aceita, a tarefa passa a ser dela. A sua é concluída ou fica aguardando o resultado, se tiver **Concluído quando**. Vocês não trabalham na mesma tarefa ao mesmo tempo. Para pedir a opinião de alguém sem deixar de ser responsável pela tarefa, use [Pedir revisão](ask-to-review.md).

## Passe para outra pessoa

Enquanto um colega estiver com a tarefa, uma linha informa isso ("Com Pat · aguardando"). As opções **Retomar** e **Passar para outra pessoa** ficam em **…**, depois em **Passar…**. **Retomar** faz a tarefa voltar para você: a Machine de Pat recebe uma notificação, e a resposta dela deixa de alterar a tarefa.

**Passar para outra pessoa** abre o formulário de repasse. Você também pode pedir isso no chat da tarefa ("essa tarefa deve ir para Kim"): a tarefa mostra "Ainda com Pat até você enviar para Kim", com a opção **Revisar repasse para** Kim.

Cada tarefa só é enviada uma vez para cada colega. Enquanto Pat estiver com ela, escolher Pat novamente no formulário de repasse inicia um follow-up. **Fazer follow-up** prepara o mesmo lembrete, com uma mensagem sua se você adicionar uma.

**Retomar de** Pat vem ativado por padrão. Desative essa opção para deixar a tarefa com as duas pessoas. Nada será enviado até você escolher **Passar**. A Machine de Pat recebe uma notificação, e a cópia da tarefa é removida.

## Quando a pessoa recusar

Ela pode explicar o motivo: a tarefa não é dela, já foi concluída ou não tem tempo nesta semana. Depois, escolha **Eu faço**, **Passar para outra pessoa** ou **Marcar como feito**. O mesmo vale se a pessoa não responder a tempo. **Eu faço** faz a tarefa voltar para você, em Para você.

## Alguém de fora da Network

Escolha **Por e-mail**. Sua Machine prepara um e-mail para você enviar. Enquanto você digita, ela sugere primeiro pessoas do seu Fleet e depois pessoas da sua empresa. Inclua uma página de tarefa para a pessoa responder com um toque. Consulte [Páginas de tarefa](task-pages.md).

Disponível apenas para tarefas de Trabalho. Marque o que incluir: algumas linhas sobre a tarefa, o rascunho, links e arquivos. Conteúdos Pessoal e Só você ficam de fora. **Preparar e-mail** adiciona o e-mail à tarefa. Leia e envie pela sua própria caixa de entrada. Não há rastreamento.

Uma tarefa do Intercom ou do Slack não tem uma caixa de entrada própria, então o e-mail é enviado pela sua caixa de entrada de Trabalho.

A tarefa acompanha o compromisso até a pessoa responder que concluiu, ou você marcar a tarefa como concluída. O e-mail termina com "Assuma esta tarefa na sua própria Machine". Se a pessoa se cadastrar por esse link, poderá entrar no seu Fleet e a tarefa passará para a Machine dela. Desative essa mensagem em **Configurações**, na seção Fleet.
