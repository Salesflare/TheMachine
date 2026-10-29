---
title: Mudar para o seu próprio computador
area: getting-started
summary: Exporte tudo de uma Machine hospedada em um único arquivo criptografado e importe no seu próprio computador.
covers: moving
code: moving.py, cli.py
site: Export everything, Delete it now, Download
order: 5
---
## Exportar

1. Na página da sua conta, abra Dados e clique em **Exportar tudo**.
2. Se quiser, defina uma senha para levar suas chaves junto. Sem ela, a exportação recebe um código e essas fontes precisam ser conectadas de novo.
3. Clique em **Baixar**. O arquivo vem direto da sua Machine, que o exclui depois de 24 horas, ou na hora com **Excluir agora**.

O arquivo é sempre criptografado. O Google sempre pede um novo login do outro lado. O login do seu modelo e o histórico do chat ficam para trás.

## Importar

No seu próprio computador, [instale The Machine](self-hosted-setup.md) e depois rode `assistant import` com o arquivo.

Depois cancele seu plano hospedado se não precisar mais dele: veja [Cancelar ou excluir](cancel-and-delete.md).
