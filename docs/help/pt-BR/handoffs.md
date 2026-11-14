---
title: Repasses
area: fleet
summary: Passe uma tarefa para a Machine de um colega, com o que essa pessoa precisa. Faça follow-up mais tarde ou pegue a tarefa de volta.
covers: handoffs
code: fleet_requests.py, dashboard.html
order: 3
translated: acb60a24ef374625
---
## Passar uma tarefa

1. Na tarefa, abra **…**, depois **Passar…** e escolha **Um colega**.
2. Escolha para quem passar, confira o que vai junto (× deixa uma parte de fora) e adicione uma observação. Nada de uma conta pessoal ou de outra empresa vai junto.
3. Envie. A Machine dessa pessoa mostra a tarefa para ela.

A Machine avisa a pessoa no celular ou no Telegram. Se ela não tiver nenhum dos dois configurado, a Machine envia um único e-mail com quem passou a tarefa, o título e um link. Consulte [Notificações](notifications.md).

Uma conversa do Intercom também vai junto. Se a Machine da pessoa tiver acesso ao mesmo espaço de trabalho do Intercom, **Ler mensagem** abre a conversa e a resposta dela volta para o Intercom. Caso contrário, a tarefa inclui um link para a conversa.

Enquanto você espera, a tarefa mostra o que você pediu e quando ("Pedido enviado a Pat na ter. 3 de nov.: …"), mas só quando isso acrescenta algo ao título. Ela fica em **Volta mais tarde**, com o status "Com Pat · aguardando" e uma data para fazer follow-up. **Fazer follow-up agora** prepara um lembrete curto para você enviar a Pat; **Mudar horário** altera a data do follow-up.

Se a Machine de Pat não puder enviar notificações, a tarefa diz "Pat não vai receber uma notificação. Avise Pat." Avise Pat você mesmo. Essa mensagem desaparece quando Pat ativa as notificações.

A tarefa só volta para o topo quando há algo para decidir: Pat respondeu, recusou ou concluiu a tarefa, o repasse falhou ou chegou um prazo. A data do follow-up depende do prazo: algumas horas para tarefas que vencem hoje, o dia útil anterior para as que vencem em breve, a manhã seguinte para as urgentes e, nos demais casos, em 3 dias úteis.

Quando a tarefa voltar para um follow-up, ela diz "Ainda com Pat". **Fazer follow-up agora** prepara um lembrete curto para Pat no canal em que você fez o pedido (Slack, WhatsApp, Telegram ou e-mail), na tarefa. Nada é enviado até você escolher **Enviar**; depois disso, a tarefa fica aguardando Pat novamente. Se nenhum dos serviços conectados puder enviar uma mensagem para Pat, o chat abre e informa isso. **Pegar de volta** e **Passar para outra pessoa** ficam em **…**, depois em **Passar…**.

O chat da tarefa mostra quando ela foi enviada ("Repassada para a Machine de Pat · 14:02") e o que aconteceu depois: aceita, recusada (com a observação da pessoa) ou concluída. Se ainda não houver resposta, aparecem as opções **Marcar como feita**, **Adiar** e **Não precisa**. Para enviar um lembrete ou pegar a tarefa de volta, peça isso no chat.

Se o repasse não for enviado, a tarefa e o chat informam isso e mostram **Tentar de novo**.

## Passar para outra pessoa

Enquanto a tarefa estiver com um colega, uma linha informa isso ("Com Pat · aguardando"). **Pegar de volta** e **Passar para outra pessoa** ficam em **…**, depois em **Passar…**. **Pegar de volta** torna a tarefa sua novamente: a Machine de Pat é avisada e a resposta de Pat deixa de atualizar a tarefa.

**Passar para outra pessoa** abre o formulário de repasse. Você também pode pedir isso no chat da tarefa ("esta tarefa deve ir para Kim"): a tarefa passa a dizer "Ainda está com Pat até você enviar para Kim" e mostra **Revisar repasse para** Kim.

Uma tarefa só é enviada para cada colega uma vez: enquanto Pat estiver com ela, escolher Pat novamente no formulário de repasse serve para fazer um follow-up. **Fazer follow-up** prepara o mesmo lembrete, com uma linha sua se você adicionar uma.

A opção **Pegar de volta de** Pat fica ativada por padrão. Desative-a para que as duas pessoas fiquem com a tarefa. Nada é enviado até você escolher **Passar**. A Machine de Pat é avisada e a cópia da tarefa na Machine de Pat é removida.

## Quando a pessoa recusar

Ela pode explicar o motivo: a tarefa não é dela, já foi concluída ou não tem tempo nesta semana. Depois, escolha **Eu mesmo faço**, **Passar para outra pessoa** ou **Marcar como feita**. O mesmo acontece se ela não responder a tempo. **Eu mesmo faço** torna a tarefa sua novamente, em Para você.

## Alguém fora da Network

Escolha **Por e-mail**: sua Machine prepara um e-mail para você enviar. Enquanto você digita, ela sugere primeiro pessoas da sua Fleet e depois pessoas da sua empresa. Adicione uma página de tarefa para que a pessoa possa responder com um toque: consulte [Páginas de tarefa](task-pages.md).

Disponível apenas para tarefas de Trabalho. Marque o que vai ser incluído: algumas linhas sobre a tarefa, o rascunho, links e arquivos. Conteúdo pessoal e conteúdo de Só você ficam de fora. **Preparar e-mail** adiciona o e-mail à tarefa: leia e depois envie pela sua própria caixa de e-mail. Não há rastreamento.

Uma tarefa do Intercom ou do Slack não tem uma caixa de e-mail própria, então o e-mail é enviado pela sua caixa de e-mail de Trabalho.

A tarefa acompanha isso como uma promessa até a pessoa responder que concluiu a tarefa ou você marcá-la como feita. O e-mail termina com "Assuma esta tarefa na sua própria Machine": se a pessoa se cadastrar por esse link, ela poderá entrar na sua Fleet e a tarefa será movida para a Machine dela. Desative essa frase em **Configurações**, na seção Fleet.
