---
title: Modelo
area: settings
summary: Qual modelo de IA responde para você, quanto ele raciocina e quanto dos limites do seu plano já foi usado.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: d63ec55d8d0339e6
---
**Configurações**, **Modelo** mostra qual modelo de IA faz o **Trabalho em segundo plano** e como você está conectado, por exemplo, com o ChatGPT.

Em uma Machine hospedada com uma conta do ChatGPT conectada, o modelo principal é GPT-6.2 Sol: respostas mais rápidas que as do GPT-6.1 Sol pelo mesmo preço.

Um plano pessoal do ChatGPT ou do Claude pode usar seus chats para treinamento por padrão: **Desativar o treinamento com seus dados** abre essa configuração no provedor, e **Feito** oculta a linha.

## Modelo e raciocínio nos chats

Em **Chats**, escolha o modelo e o nível de raciocínio para seus chats de tarefas e para a Ajuda. Você só vê os modelos e níveis disponíveis na sua conta conectada.

Mais raciocínio ajuda a responder melhor a perguntas difíceis, mas é mais lento e usa mais do seu plano. **Raciocínio ultra** usa assistentes para as perguntas mais difíceis e consome mais. Uma Machine nova começa com **Raciocínio baixo**: bons resultados usando bem menos do seu plano. A alteração vale a partir da próxima mensagem.

Para mudar a configuração só em um chat, toque no modelo ou no nível de raciocínio abaixo da caixa de mensagem. Escolha **Configurações** novamente para seguir as configurações gerais.

As verificações, seu perfil e os rascunhos preparados com antecedência usam seus próprios modelos.

## Limites

Se seu plano tiver limites de uso, como os limites de 5 horas e semanais de um plano do ChatGPT ou do Claude, você verá quanto já usou e quando cada limite será redefinido. Só consultar essa informação não consome seu plano.

## Espaço para seus próprios chats

O trabalho em segundo plano deixa espaço para seus próprios chats. Ele pausa quando o uso chega a cerca de 65% do limite de 5 horas. As verificações de novas mensagens continuam até cerca de 90% do limite semanal; outros trabalhos usam cerca de um sétimo do limite semanal por dia. Uma conta conectada sem limites, como uma chave de API, nunca pausa.

O trabalho em segundo plano nunca usa GPT-6 Astra. Por enquanto, quando você entra com uma conta do ChatGPT, ele usa GPT-6.1 Sol, mesmo que seu modelo principal seja GPT-6.2 Sol: nessa conta, o 6.2 ainda não reutiliza as instruções em cache, então consome mais do seu plano. Seus chats continuam usando o modelo escolhido.

## Antes de atingir um limite

Se ainda houver redefinições disponíveis no seu plano do ChatGPT, a seção Tarefas mostra uma mensagem curta quando o trabalho em segundo plano fica mais lento: quando o uso chega a cerca de 65% do limite de 5 horas ou 90% do limite semanal. A mensagem informa quanto foi usado e quantas redefinições restam. **Usar uma redefinição** reinicia os limites depois que você confirma. × oculta a mensagem até o limite ser redefinido. Se não houver redefinições disponíveis, nada será exibido.

## Quando um limite é atingido

Na parte superior do painel, você verá qual limite foi atingido e quando será redefinido. O trabalho aguarda e depois continua de onde parou. Nada é perdido. Se seu plano do ChatGPT tiver redefinições disponíveis, **Usar uma redefinição** reinicia os limites. Caso contrário, **Ver redefinições no ChatGPT** abre a página do ChatGPT.

## Com um modelo alternativo

Se sua Machine tiver um modelo alternativo em outro plano ou provedor, ele assume quando um limite é atingido e nada fica aguardando. Na parte superior do painel, aparece "Limite do ChatGPT atingido, usando seu modelo alternativo." Se o modelo alternativo parar de funcionar, as pausas voltam.

## Alterar o modelo principal

O modelo principal é usado pelo restante da The Machine. Em uma Machine hospedada, altere-o na página de configuração, em Sua IA. No seu próprio computador, consulte [ChatGPT](chatgpt.md), [Mistral](mistral.md) e o [guia de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
