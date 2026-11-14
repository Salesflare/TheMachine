---
title: Modelo
area: settings
summary: Qual modelo de IA responde para você, quanto ele raciocina e quanto dos limites do seu plano já foi usado.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: eee77413a4bdbf0b
---
**Configurações**, **Modelo** mostra qual modelo de IA realiza seu **Trabalho em segundo plano** e como você fez login, por exemplo, com ChatGPT.

## Modelo e raciocínio nos chats

Em **Chats**, escolha o modelo e o nível de raciocínio para seus chats de tarefas e para a Ajuda. Você só vê os modelos e níveis disponíveis com a sua forma de login.

Mais raciocínio ajuda a responder melhor a perguntas difíceis, mas é mais lento e consome mais do seu plano. **Raciocínio ultra** usa assistentes para responder às perguntas mais difíceis e consome mais do que qualquer outro nível. Uma nova Machine começa com **Raciocínio baixo**: bons resultados usando bem menos do seu plano. A mudança vale a partir da próxima mensagem.

Para mudar o modelo ou o nível de raciocínio em apenas um chat, toque nele abaixo da caixa de mensagem. Escolha **Configurações** novamente para usar a opção definida em Configurações.

As verificações, seu perfil e os rascunhos preparados com antecedência usam o próprio modelo.

## Limites

Se seu plano tiver limites de uso, como os limites de 5 horas e semanais de um plano do ChatGPT ou Claude, você verá quanto já foi usado e quando cada limite será redefinido. Consultar essas informações não consome seu plano.

## Espaço para seus próprios chats

O trabalho em segundo plano deixa espaço para seus próprios chats. Ele pausa quando o limite de 5 horas chega a cerca de 65%. As verificações de novas mensagens continuam até o limite semanal chegar a cerca de 90%. O restante do trabalho consome cerca de um sétimo do limite semanal por dia. Um login sem limites, como uma chave de API, nunca pausa.

O trabalho em segundo plano nunca é executado no GPT-6 Astra. Em vez disso, ele usa o GPT-6.1 Sol.

## Quando um limite é atingido

No topo do painel, você verá qual limite foi atingido e quando ele será redefinido. O trabalho aguarda e depois continua de onde parou. Nada se perde. Se seu plano do ChatGPT tiver redefinições, **Usar uma redefinição** reinicia os limites. Caso contrário, **Ver redefinições no ChatGPT** abre a página do ChatGPT.

## Com um modelo alternativo

Se sua Machine tiver um modelo alternativo em outro plano ou provedor, ele assume quando um limite é atingido, sem que nenhum trabalho fique aguardando. No topo do painel, você verá "Limite do ChatGPT atingido, usando seu modelo alternativo." Se o modelo alternativo parar de funcionar, as pausas voltam.

## Mudar o modelo principal

O modelo principal é usado no restante da The Machine. Em uma Machine hospedada, mude-o na página de configuração, em Your AI. No seu próprio computador, consulte [ChatGPT](chatgpt.md), [Mistral](mistral.md) e o [guia de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
