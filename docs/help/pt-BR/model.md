---
title: Modelo
area: settings
summary: Qual modelo de IA responde para você, quanto ele raciocina e quanto do limite do seu plano já foi usado.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: a6db52984a6fddeb
---
**Configurações**, **Modelo** mostra qual modelo de IA faz seu **Trabalho em segundo plano** e como você está conectado, por exemplo, com o ChatGPT.

Em uma Machine hospedada com uma conexão do ChatGPT, o modelo principal é o GPT-6.2 Sol: respostas mais rápidas que as do GPT-6.1 Sol pelo mesmo preço.

Um plano pessoal do ChatGPT ou do Claude pode usar seus chats para treinamento por padrão: **Desativar o treinamento com seus dados** abre essa configuração no serviço, e **Feito** oculta a linha.

## Modelo e raciocínio dos chats

Em **Chats**, escolha o modelo e o nível de raciocínio para seus chats de tarefas e para a Ajuda. Você só vê os modelos e níveis disponíveis na sua conexão.

Mais raciocínio ajuda a responder melhor a perguntas difíceis, mas é mais lento e consome mais do seu plano. **Raciocínio ultra** usa assistentes para as perguntas mais difíceis e consome mais do seu plano. Uma Machine nova começa com **Raciocínio baixo**: bons resultados usando bem menos do seu plano. A alteração vale a partir da próxima mensagem.

Para mudar isso em apenas um chat, toque no modelo ou no nível de raciocínio abaixo da caixa de mensagem. Escolha novamente a opção de Configurações para seguir as Configurações.

As verificações, seu perfil e os rascunhos preparados com antecedência usam seus próprios modelos.

## Limites

Se seu plano tiver limites de uso, como os limites de 5 horas e semanais de um plano do ChatGPT ou Claude, você verá quanto já foi usado e quando cada limite será redefinido. Consultar não consome seu plano.

## Espaço para seus próprios chats

O trabalho em segundo plano deixa espaço para seus próprios chats. Ele pausa quando o limite de 5 horas chega a cerca de 65%. As verificações de novas mensagens continuam até o limite semanal chegar a cerca de 90%; outros trabalhos usam cerca de um sétimo do limite semanal por dia. Uma conexão sem limites, como uma chave de API, nunca pausa.

O trabalho em segundo plano nunca é executado no GPT-6 Astra. Por enquanto, com uma conexão do ChatGPT, ele usa o GPT-6.1 Sol, mesmo quando seu modelo principal é o GPT-6.2 Sol: nessa conexão, o 6.2 ainda não reutiliza as instruções em cache, então consome mais do seu plano. Seus chats continuam usando o modelo escolhido.

## Quando um limite é atingido

No topo do painel, aparece qual limite foi atingido e quando será redefinido. O trabalho aguarda e depois continua de onde parou. Nada se perde. Se seu plano do ChatGPT tiver redefinições, **Usar uma redefinição** reinicia os limites. Caso contrário, **Ver redefinições no ChatGPT** abre a página do ChatGPT.

## Com um modelo alternativo

Se sua Machine tiver um modelo alternativo em outro plano ou serviço, ele assume quando um limite é atingido, e nada fica aguardando. No topo do painel, aparece "Limite do ChatGPT atingido. Usando seu modelo alternativo." Se o modelo alternativo parar de funcionar, as pausas voltam.

## Mudar o modelo principal

O modelo principal é usado pelo restante da The Machine. Em uma Machine hospedada, mude-o na página de configuração, em Sua IA. No seu próprio computador, consulte [ChatGPT](chatgpt.md), [Mistral](mistral.md) e o [guia de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
