---
title: Mistral
area: connections
summary: Rode sua Machine nos modelos da Mistral, com uma chave de API da Mistral. O Le Chat Pro inclui créditos de API.
covers: mistral
code: docs/models.md, dashboard/settings-models.js
site: Other AI services, Save key, Keys, Remove
translated: 5d782f28fb69efef
---
## Para que serve

A Mistral é uma provedora europeia de IA. Com uma chave de API da Mistral, sua Machine lê e escreve rascunhos com os modelos da Mistral. The Machine não tem IA própria: as solicitações vão direto para a Mistral, na sua conta e sob os termos dela.

## Pegue uma chave

A Mistral não tem login para outros apps, então funciona com uma chave de API. No [console da Mistral](https://console.mistral.ai/), abra API keys e crie uma. O Le Chat Pro inclui créditos de API todo mês; depois deles, a Mistral cobra por uso.

## Conecte

Em uma Machine hospedada, abra sua página de configuração, vá até Sua IA e abra **Outros serviços de IA**. Escolha a Mistral como provedor, cole a chave e clique em **Salvar chave**. Sua Machine testa a chave antes com uma solicitação mínima. Uma chave errada aparece ali mesmo, e nada é salvo.

O Mistral Large vira o modelo principal. O Mistral Small também fica disponível, uma opção mais barata para os chats ou como reserva.

No seu próprio computador, veja o [guia de modelos](https://github.com/Salesflare/TheMachine/blob/main/docs/models.md).

## Uso

**Configurações**, **Modelo** diz "Usa sua chave de API da Mistral". Uma chave de API não tem limites de uso, então o trabalho em segundo plano nunca pausa por ela. Veja [Modelo](model.md).

## Remover

Na sua página de configuração, em Sua IA, toque em **Remover** ao lado de Mistral em **Chaves**. A chave é apagada da sua Machine e, se a Mistral era seu modelo principal, outro modelo conectado assume. Para cancelar a chave em si, apague-a no console da Mistral.
