---
title: Feeds RSS
area: connections
summary: Publicações de um feed RSS ou Atom que você acompanha.
covers: connector:rss
code: connectors/rss.py
site: More sources
translated: efeb27dadc6163e9
---
## O que ela lê

Novas publicações de um feed RSS ou Atom por conexão. Adicione uma conexão para cada feed.

Ela lê o feed a cada 30 minutos e nunca com intervalos menores que 15 minutos. Só lê endereços públicos https://.

## O que ela pode fazer

Nada. Ela só lê o feed.

## Conectar

1. No painel, abra **Conexões**, depois **Outras** e selecione Feed RSS. Em uma Machine hospedada, a página de configuração também tem essa opção, em **Mais fontes**. No seu computador, você também pode executar `assistant connect rss`.
2. Cole o endereço do feed.

## Remover

No painel: abra o feed em **Conexões**, selecione **Detalhes** e depois **Desconectar**. Não há nada para desinstalar em outro lugar.
