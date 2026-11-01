---
title: Repasses
area: fleet
summary: Passe uma tarefa para a Machine de um colega, com o que a pessoa precisa. Faça follow-up depois, ou pegue de volta.
covers: handoffs
code: fleet_requests.py, dashboard.html
order: 3
---
## Passar uma tarefa

1. Na tarefa, escolha **Passar para um colega**.
2. Escolha para quem, confira o que vai junto (tire qualquer parte com ×) e adicione uma nota. O texto começa com a tarefa e por que ela importa, tirados da tarefa, e de onde ela veio (o link). Nada de uma conta Pessoal ou de outra empresa vai junto.
3. Envie. A Machine da pessoa mostra o pedido como uma tarefa.

Uma conversa do Intercom vai junto com o lugar dela no Intercom. Se a Machine da pessoa lê o mesmo workspace do Intercom, a tarefa dela fica nessa conversa: **Ler mensagem** abre a conversa, o cliente aparece nela e a resposta volta pelo Intercom. Se não, a tarefa ainda tem o link da conversa no Intercom.

Enquanto você espera, a tarefa fica em **Volta mais tarde**, "Com Pat · aguardando", com uma data de follow-up. **Fazer follow-up agora** pergunta como está indo. **Mudar horário** muda a data do follow-up.

Ela só volta para o topo quando há algo para decidir: Pat respondeu, recusou ou marcou como feita, o repasse falhou, ou chegou um prazo. Uma tarefa que vence hoje faz follow-up algumas horas depois, uma que vence em breve no dia de trabalho anterior, uma urgente sem data na manhã de trabalho seguinte, e qualquer outra em 3 dias de trabalho.

De volta para um follow-up, ela mostra "Ainda com Pat · fazer follow-up?": Pat ainda está com ela, nada voltou. **Fazer follow-up agora** abre o chat; **Pegar de volta** e **Passar para outra pessoa** ficam ao lado, e Marcar como feita, Adiar e Não precisa ficam em Mais.

O chat da tarefa mostra quando ela foi ("Passada para a Machine de Pat · 14:02") e o que voltou: aceita, recusada (com a nota da pessoa) ou feita. Quando volta para um follow-up ainda sem resposta, "Pat ainda não respondeu" aparece abaixo dessa linha, com **Marcar como feita**, **Adiar** e **Não precisa** (sem Fazer: a tarefa está com a pessoa). Para lembrar a pessoa ou pegar a tarefa de volta, diga isso no chat.

Se o repasse não saiu, a tarefa e o chat dela avisam, com **Tentar de novo**.

## Passar para outra pessoa

Enquanto um colega está com ela, a tarefa diz isso em uma linha ("Com Pat · aguardando"), com **Pegar de volta** e **Passar para outra pessoa**. **Pegar de volta** faz a tarefa voltar a ser sua: a Machine de Pat é avisada, e a resposta de Pat não move mais a tarefa.

**Passar para outra pessoa** abre o formulário de repasse, para alguém que ainda não está com ela. Ou diga isso no chat da tarefa ("isso deve ir para a Kim"). O novo repasse espera na tarefa até você ler: "Ainda com Pat até você enviar para Kim", com **Revisar repasse para** Kim. Isso abre o formulário com o texto, já para Kim.

Uma tarefa vai para cada colega uma vez só: enquanto Pat está com ela, passá-la de novo para Pat mostra "Pat já tem esta tarefa".

**Pegar de volta de** Pat vem ativado. Desative para que as duas pessoas fiquem com a tarefa. Nada sai até você escolher **Passar**. Aí o chat mostra "Pegada de volta de Pat" e "Passada para a Machine de Kim". A Machine de Pat também é avisada, e a tarefa que ela criou para Pat some.

## Quando a pessoa recusa

A pessoa pode dizer por quê: não é dela, já foi feita, ou sem tempo esta semana. Aí escolha **Eu mesmo faço**, **Passar para outra pessoa** ou **Marcar como feita**.

## Alguém fora da Network

Escolha **Por e-mail**: sua Machine escreve um rascunho de e-mail para você enviar. Enquanto você digita o endereço, ela sugere colegas primeiro: pessoas no seu Fleet, depois pessoas no domínio da sua empresa, depois o que você digitou com esse domínio. Adicione uma página de tarefa para a pessoa responder com um toque: veja [Páginas de tarefa](task-pages.md).

Só para tarefas de Trabalho. Marque o que vai no e-mail: algumas linhas sobre a tarefa, o rascunho pronto, links e arquivos. Só aparece o que seu Team Graph compartilha com a equipe, então o que é Pessoal e Só você fica de fora. **Preparar e-mail** deixa o e-mail na tarefa: leia e depois envie da sua própria caixa como qualquer e-mail. Sem pixels de rastreamento.

A tarefa então mostra "Passada para <nome> por e-mail" e acompanha como uma promessa até a pessoa responder que está feito, ou até você marcar como feita. O e-mail termina com "Assuma isso na sua própria Machine": quem se cadastra por esse link pode entrar no seu Fleet e a tarefa vai para a Machine da pessoa como um repasse normal. Desligue essa linha em **Configurações**, em Fleet.
