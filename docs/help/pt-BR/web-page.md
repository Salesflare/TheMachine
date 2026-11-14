---
title: Páginas web acompanhadas
area: connections
summary: Uma página web que você acompanha. Uma tarefa só quando muda algo que importa.
covers: connector:web_page
code: connectors/web_page.py
---
## O que ele lê

O texto de uma página web pública por conexão, a cada poucas horas e no máximo uma vez por hora. Menus, rodapés, avisos de cookies e anúncios ficam de fora. Quando o texto mudou, a The Machine vê o que mudou e só cria uma tarefa se importar, como um preço novo ou uma política alterada. Datas, contadores e pequenas mudanças de redação nunca criam uma tarefa. Uma página sem mudanças não custa nada.

Ela consulta primeiro o robots.txt do site e deixa a página em paz se o site disser não. Páginas atrás de um login ou feitas só com JavaScript não podem ser acompanhadas.

## O que ele pode fazer

Nada. Ele só lê a página.

## Conecte

1. No painel, abra **Conexões**, depois **Outras**, e escolha Página web. Ou rode `assistant connect web_page`.
2. Cole o endereço da página.

Ou peça no seu chat: "Acompanhe esta página para mudanças de preço" com o endereço dela. Pergunte quais páginas você acompanha, ou peça para parar de acompanhar uma.

## Remova

No painel: **Conexões**, abra a página, **Detalhes** e depois **Desconectar**. Ou peça ao seu chat para parar de acompanhá-la.
