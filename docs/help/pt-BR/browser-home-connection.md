---
title: A conexão de casa do seu navegador
area: troubleshooting
summary: Faça o navegador da sua Machine hospedada sair pela sua internet de casa com o Tailscale, para os sites aceitarem os logins dele.
code: browser_login.py
site: Tailscale, Sign in to Tailscale, Use this exit node, Open it in Tailscale, Test it, Sign in again, Stop using it, Sign it out of Tailscale too
keywords: tailscale, exit node, home internet, ip address, cloudflare, linkedin
order: 4
---
Alguns sites, como LinkedIn, X e sites atrás de uma verificação do Cloudflare, recusam logins de um navegador na nuvem. Sua página de configuração pode fazer o navegador da sua Machine hospedada sair pela sua internet de casa, com o Tailscale. É grátis, leva uns 10 minutos e quase tudo acontece sozinho.

## Configurar

1. Na sua página de configuração, no navegador da sua Machine, escolha **Tailscale** e toque em **Entrar no Tailscale**. Entre, ou crie uma conta grátis lá.
2. Instale o Tailscale num computador em casa que fica ligado e entre lá com a mesma conta. Celular não: ele dorme.
3. Transforme esse computador num exit node. A página de configuração mostra o menu para o sistema dele. No Linux, rode `sudo tailscale set --advertise-exit-node`.
4. Toque em **Abrir no Tailscale** e permita: Machine settings, Edit route settings, Use as exit node, Save. No mesmo menu, escolha Disable key expiry.

A página de configuração marca cada passo sozinha. Com um exit node, seu navegador começa a usá-lo na hora. Com mais de um, escolha um e toque em **Usar este exit node**.

## Conferir

Toque em **Testar**. A página mostra onde a web vê seu navegador: sua cidade e seu provedor de internet.

## Quando o computador de casa está desligado

Seu navegador então sai direto da sua Machine, e volta a passar pela sua casa assim que o computador liga de novo. Saiu do Tailscale? Toque em **Entrar de novo**. O Tailscale desconecta os dispositivos depois de 6 meses, a não ser que key expiry esteja desligado. A página de configuração mostra a data.

## Parar de usar

Toque em **Parar de usar** para voltar a ir direto. **Sair também do Tailscale** também tira o navegador da sua Machine do Tailscale. O console de administração do Tailscale mostra ele então como Expired, e você pode removê-lo lá.
