---
title: Modelo
area: settings
summary: Qual modelo de IA responde para você, quanto ele raciocina e quanto dos limites do seu plano já foi usado.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: f34db396a7290252
---
**Configurações**, **Modelo** mostra qual modelo de IA faz seu **Trabalho em segundo plano** e como você entrou na conta, por exemplo, com o ChatGPT.

Em uma Machine hospedada com login do ChatGPT, o modelo principal é GPT-6.2 Sol: respostas mais rápidas que as do GPT-6.1 Sol pelo mesmo preço.

Um plano pessoal do ChatGPT ou Claude pode usar seus chats para treinamento por padrão: **Desativar o treinamento com seus dados** abre essa configuração no provedor, e **Feito** oculta a linha.

## Modelo e raciocínio nos chats

Em **Chats**, escolha o modelo e o nível de raciocínio para seus chats de tarefas e para a Ajuda. Você só vê os modelos e níveis disponíveis no seu login.

Mais raciocínio ajuda a responder melhor a perguntas difíceis, mas é mais lento e consome mais do seu plano. **Raciocínio ultra** usa assistentes para as perguntas mais difíceis e consome mais que os outros níveis. Uma nova Machine começa com **Raciocínio baixo**: bons resultados com muito menos consumo do seu plano. A alteração vale a partir da próxima mensagem.

Para alterar isso em apenas um chat, toque no modelo ou no nível de raciocínio abaixo da caixa de mensagem. Escolha novamente a opção Configurações para seguir as Configurações.

As verificações, seu perfil e os rascunhos preparados com antecedência usam cada um seu próprio modelo.

## Limites

Se seu plano tiver limites de uso, como os limites de 5 horas e semanais de um plano do ChatGPT ou Claude, você verá quanto já foi usado e quando cada limite será redefinido. Consultar não consome seu plano.

## Espaço para seus próprios chats

O Trabalho em segundo plano deixa espaço para seus próprios chats. Ele pausa quando o limite de 5 horas chega a cerca de 65%. As verificações de novas mensagens continuam até o limite semanal chegar a cerca de 90%; os outros trabalhos usam cerca de um sétimo do limite semanal por dia. Um login sem limites, como uma chave de API, nunca pausa.

O Trabalho em segundo plano nunca é executado no GPT-6 Astra. Com um login do ChatGPT e uma versão do OpenClaw anterior à 2026.11.10, ele usa GPT-6.1 Sol, mesmo quando o modelo principal é GPT-6.2 Sol: nesse caso, o 6.2 não reutiliza as instruções em cache, então consome mais do seu plano. A partir do OpenClaw 2026.11.10, o Trabalho em segundo plano volta a usar seu modelo principal. Seus chats continuam usando o modelo escolhido.

Antes de uma verificação, um modelo pequeno (GPT-6 Luna com ChatGPT, Haiku com Claude) separa newsletters, promoções e avisos de apps que claramente não exigem nenhuma ação, para que as verificações consumam menos do seu plano. Esses itens continuam aparecendo nas buscas. Mensagens escritas por pessoas, contas, alertas de segurança e códigos de login sempre são verificados.

## Antes de atingir um limite

Se ainda houver redefinições disponíveis no seu plano do ChatGPT, Tarefas mostra uma mensagem curta quando o Trabalho em segundo plano fica mais lento: quando o limite de 5 horas chega a cerca de 65% ou o limite semanal chega a cerca de 90%. A mensagem informa quanto já foi usado e quantas redefinições restam. **Usar uma redefinição** reinicia os limites depois que você confirmar. × oculta a mensagem até o limite ser redefinido. Se não houver redefinições, nada de novo aparece.

Em uma Machine hospedada, sua Machine vê e usa as redefinições assim que o Codex na sua Machine entra na mesma conta do ChatGPT. Até lá, Tarefas e Configurações mostram **Ativar redefinições**. Essa opção abre a etapa do Codex na página de configuração, onde você entra com um código, como no login do ChatGPT.

## Quando um limite é atingido

No topo do painel, aparece qual limite foi atingido e quando será redefinido. O trabalho aguarda e depois continua de onde parou. Nada se perde. Se seu plano do ChatGPT tiver redefinições, **Usar uma redefinição** reinicia os limites. Em uma Machine hospedada sem login no Codex, **Ativar redefinições** abre a página de configuração. Nos demais casos, **Ver redefinições no ChatGPT** abre a página do ChatGPT.

## Com um modelo alternativo

Se sua Machine tiver um modelo alternativo em outro plano ou provedor, ele assume quando um limite é atingido e nada fica aguardando. No topo do painel, aparece “Limite do ChatGPT atingido, usando seu modelo alternativo.” Se o modelo alternativo parar de funcionar, as pausas voltam.

## Alterar o modelo principal

O modelo principal é usado pelo restante da The Machine. Em uma Machine hospedada, altere-o na página de configuração, em Sua IA. No seu próprio computador, consulte [ChatGPT](chatgpt.md), [Mistral](mistral.md) e o [guia de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
