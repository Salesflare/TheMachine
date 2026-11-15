---
title: Modelo
area: settings
summary: Qual modelo de IA responde por você, qual nível de raciocínio ele usa e quanto dos limites do seu plano já foi usado.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: 744a27a77ab747ac
---
**Configurações**, **Modelo** mostra qual modelo de IA faz o **Trabalho em segundo plano** e como você fez login, por exemplo, com o ChatGPT.

Um plano pessoal do ChatGPT ou Claude pode usar seus chats para treinamento por padrão: **Desativar o treinamento com seus dados** abre essa configuração no serviço, e **Feito** oculta a linha.

## Modelo e raciocínio para chats

Em **Chats**, escolha o modelo e o nível de raciocínio para seus chats de tarefas e para a Ajuda. Você só vê os modelos e níveis disponíveis para a sua conta.

Mais raciocínio ajuda a responder melhor perguntas difíceis, mas é mais lento e usa mais do seu plano. **Raciocínio ultra** chama assistentes para as perguntas mais difíceis e é o que mais consome. Uma Machine nova começa com **Raciocínio baixo**: bons resultados usando bem menos do seu plano. A mudança vale a partir da próxima mensagem.

Para mudar isso em apenas um chat, toque no modelo ou no nível de raciocínio abaixo da caixa de mensagem. Escolha **Configurações** novamente para seguir as Configurações.

As verificações, seu perfil e os rascunhos preparados com antecedência usam um modelo próprio.

## Limites

Se seu plano tiver limites de uso, como os limites de 5 horas e semanais de um plano do ChatGPT ou Claude, você verá quanto já foi usado e quando cada limite será redefinido. Consultar essa tela não consome seu plano.

## Espaço para seus próprios chats

O Trabalho em segundo plano deixa espaço para seus próprios chats. Ele pausa quando o uso chega a cerca de 65% do limite de 5 horas. As verificações de novas mensagens continuam até cerca de 90% do limite semanal; o restante do trabalho usa cerca de um sétimo do limite semanal por dia. Um login sem limites, como uma chave de API, nunca é pausado.

O Trabalho em segundo plano nunca é executado no GPT-6 Astra. Em vez disso, usa o GPT-6.1 Sol.

## Quando um limite é atingido

No topo do painel, você vê qual limite foi atingido e quando será redefinido. O trabalho aguarda e depois continua de onde parou. Nada é perdido. Se seu plano do ChatGPT permitir redefinições, **Usar uma redefinição** reinicia os limites. Caso contrário, **Ver redefinições no ChatGPT** abre a página do ChatGPT.

## Com um modelo alternativo

Se sua Machine tiver um modelo alternativo em outro plano ou serviço, ele assume quando um limite é atingido, e nada fica aguardando. No topo do painel, aparece "Limite do ChatGPT atingido. Usando seu modelo alternativo." Se o modelo alternativo parar de funcionar, as pausas voltam.

## Mudar o modelo principal

O modelo principal é usado no restante da The Machine. Em uma Machine hospedada, mude-o na página de configuração, em Sua IA. No seu próprio computador, consulte [ChatGPT](chatgpt.md), [Mistral](mistral.md) e o [guia de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
