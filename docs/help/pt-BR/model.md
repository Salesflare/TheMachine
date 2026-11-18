---
title: Modelo
area: settings
summary: Qual modelo de IA responde por você, quanto ele raciocina e quanto dos limites do seu plano já foi usado.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
translated: 249d2d7d6c368cfe
---
**Configurações**, **Modelo** mostra qual modelo de IA faz seu **Trabalho em segundo plano** e como você entrou, por exemplo, com o ChatGPT.

Em uma Machine hospedada com uma conta do ChatGPT, o modelo principal é o GPT-6.2 Sol: respostas mais rápidas que as do GPT-6.1 Sol pelo mesmo preço.

Um plano pessoal do ChatGPT ou do Claude pode usar seus chats para treinar por padrão: **Desativar o treinamento com seus dados** abre essa configuração no provedor, e **Feito** oculta essa linha.

## Modelo e raciocínio nos chats

Em **Chats**, escolha o modelo e o nível de raciocínio para seus chats de tarefas e para a Ajuda. Você só vê os modelos e níveis disponíveis na sua conta.

Mais raciocínio ajuda a responder melhor a perguntas difíceis, mas é mais lento e consome mais do seu plano. **Raciocínio ultra** usa assistentes para as perguntas mais difíceis e consome mais do que os outros níveis. Uma Machine nova começa com **Raciocínio baixo**: bons resultados usando bem menos do seu plano. A mudança vale a partir da próxima mensagem.

Para alterar isso em apenas um chat, toque no modelo ou no nível de raciocínio abaixo da caixa de mensagem. Selecione novamente a opção Configurações para seguir as Configurações.

As verificações, seu perfil e os rascunhos preparados com antecedência usam um modelo próprio.

## Limites

Se seu plano tiver limites de uso, como os limites de 5 horas e semanais dos planos do ChatGPT ou do Claude, você verá quanto já foi usado e quando cada limite será redefinido. Consultar essas informações não consome seu plano.

## Espaço para seus próprios chats

O trabalho em segundo plano deixa espaço para seus próprios chats. Ele pausa quando o limite de 5 horas chega a cerca de 65%. As verificações de novas mensagens continuam até cerca de 90% do limite semanal. Outros trabalhos consomem cerca de um sétimo do limite semanal por dia. Uma conta sem limites, como uma com chave de API, nunca pausa.

O trabalho em segundo plano nunca é executado no GPT-6 Astra. Em vez disso, ele usa o GPT-6.2 Sol ou, quando o 6.2 não está configurado, o GPT-6.1 Sol.

## Quando um limite é atingido

No topo do painel, você vê qual limite foi atingido e quando ele será redefinido. O trabalho aguarda e depois continua de onde parou. Nada é perdido. Se seu plano do ChatGPT tiver redefinições, **Usar uma redefinição** reinicia os limites. Caso contrário, **Ver redefinições no ChatGPT** abre a página do ChatGPT.

## Com um modelo alternativo

Se sua Machine tiver um modelo alternativo em outro plano ou provedor, ele assume quando um limite é atingido, sem que nenhum trabalho precise esperar. No topo do painel, aparece “Limite do ChatGPT atingido. Usando seu modelo alternativo.” Se o modelo alternativo parar de funcionar, as pausas voltam.

## Alterar o modelo principal

O modelo principal é usado pelo restante da The Machine. Em uma Machine hospedada, altere-o na página de configuração, em Sua IA. No seu próprio computador, consulte [ChatGPT](chatgpt.md), [Mistral](mistral.md) e o [guia de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
