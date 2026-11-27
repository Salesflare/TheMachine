---
title: Navegue pela internet pelo app para computador
area: troubleshooting
summary: Permita que o navegador da sua Machine hospedada acesse a internet pelo computador onde o app para computador está aberto, para que os sites vejam sua conexão.
code: desktop/src/exit.rs, desktop/src/settings.rs
keywords: desktop app, exit node, home internet, office, ip address, linkedin, sign in, proxy
order: 5
translated: 6da69c78d7e60574
---
Alguns sites, como LinkedIn, recusam logins feitos em navegadores na nuvem. Com o [app para computador](desktop-app.md) conectado, o navegador da sua Machine hospedada pode acessar a internet por esse computador. Assim, os sites veem a conexão da sua casa ou do escritório, e não a de um data center.

## Ative

O recurso fica ativado por padrão assim que está disponível na sua Machine. Nas **Configurações** do app para computador, a opção é **Permitir que minha Machine navegue por este computador**. Desative-a e o navegador da sua Machine volta a acessar a internet diretamente na mesma hora.

Enquanto o navegador da sua Machine estiver usando essa conexão, a caixa do robô e o ícone do app na barra de menus ou na barra de tarefas exibem **Sua Machine está navegando por este computador**.

## O que passa por essa conexão

Somente o navegador da sua Machine, ao acessar sites: portas 80 e 443 em endereços públicos da internet. O app nunca se conecta diretamente a este computador, à sua rede doméstica ou do escritório nem a outros endereços privados. Ele também não abre nenhuma porta no computador. O limite é de 4 MB/s de download, 1 MB/s de upload e 2 GB por dia.

## Quando o computador está desligado

O navegador da sua Machine acessa a internet diretamente e volta a passar pelo computador assim que o app voltar a funcionar.
