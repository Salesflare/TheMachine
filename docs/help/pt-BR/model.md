---
title: Modelo
area: settings
summary: Qual modelo de IA responde por você, quanto ele raciocina e quanto dos limites do seu plano ele já usou.
covers: settings:model, chat-model
code: dashboard.html, docs/models.md, chat_model.py
order: 5
---
Em **Configurações**, **Modelo** mostra o modelo que o trabalho em segundo plano usa (marcado como **Trabalho em segundo plano**) e como você entrou, por exemplo com o ChatGPT.

## Modelo e raciocínio para os chats

Em **Chats**, escolha o modelo e o nível de raciocínio que os chats das suas tarefas e a Ajuda usam. A lista só tem os modelos que o seu login oferece, como os do ChatGPT se você entrou com o ChatGPT, e cada modelo só os níveis que ele tem.

Mais raciocínio responde melhor perguntas difíceis, mas é mais lento e usa mais do seu plano. **Raciocínio ultra** traz ajudantes para as perguntas mais difíceis: é o mais lento e o que mais usa. Uma mudança vale a partir da próxima mensagem. Uma Machine nova começa com **Raciocínio baixo** quando o modelo dela tem: bons resultados usando bem menos do seu plano.

Um chat pode usar outra coisa: abaixo da caixa de mensagem dele, toque no modelo ou no nível de raciocínio. Essa escolha vale só para esse chat. Escolha de novo o mesmo das Configurações para seguir as Configurações.

Revisões, seu perfil e rascunhos preparados com antecedência mantêm o próprio modelo.

## Limites

Se o seu plano tem limites de uso, aparece quanto de cada um já foi usado e quando ele zera, por exemplo o limite de 5 horas e o semanal de um plano do ChatGPT ou do Claude. Ver isso nunca consome seu plano.

## Espaço para os seus chats

O trabalho em segundo plano (revisões, seu perfil, rascunhos preparados com antecedência) deixa espaço para os seus próprios chats. Ele pausa em cerca de 65% do limite de 5 horas. As revisões do que chegou seguem até cerca de 90% do limite semanal; o resto o distribui em cerca de um sétimo por dia. Um login sem limites de uso, como uma chave de API, nunca é pausado.

O trabalho em segundo plano nunca roda no GPT-6 Astra. Ele usa o GPT-6.1 Sol no lugar.

## Quando um limite é atingido

O topo do painel diz qual limite foi atingido e quando ele zera. O trabalho espera e depois continua de onde parou. Nada se perde. Alguns planos do ChatGPT vêm com redefinições: **Usar uma redefinição** zera os limites, depois de uma confirmação. Se não, **Ver redefinições no ChatGPT** abre a página do próprio ChatGPT.

## Com um modelo reserva

Se a sua Machine tem um modelo reserva em outro plano ou provedor, como uma chave de API, ele assume quando um limite é atingido. Enquanto o modelo reserva funciona, nada pausa nem espera pelos seus limites, e o topo do painel diz "Limite do ChatGPT atingido, usando seu modelo reserva." Se ele parar de funcionar, as pausas voltam.

## Mudar o modelo principal

O modelo principal é o que o resto da The Machine usa. Em uma Machine hospedada, escolha outro na sua página de configuração, em Seu modelo. No seu próprio computador, mude no OpenClaw. Veja [ChatGPT](chatgpt.md) e o [guia de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).
