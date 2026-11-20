---
title: Conhecimento para outra IA
area: settings
summary: Leve o que sua Machine aprendeu para qualquer outra IA, em arquivos simples que qualquer IA consegue ler.
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
translated: db1c7f4768a71630
---
Tudo o que sua Machine aprende é seu. Compartilhe com outra IA, como ChatGPT ou Claude, ou guarde para você.

## Exporte

1. Em **Configurações** › **Geral** › **Exportar**, clique em **Exportar** ao lado de **Conhecimento para outra IA**.
2. **Texto das mensagens** vem desativado por padrão: o arquivo inclui apenas a origem de cada item e a data. Ative essa opção para incluir o texto.
3. Ative **Privado e Cuidadoso** somente se quiser incluir projetos só seus, conversas privadas e itens de Fleet no modo Cuidadoso.
4. Se quiser, defina uma **Frase secreta** (com pelo menos 10 caracteres) para criptografar o arquivo.
5. Clique em **Baixar**. Só é possível baixar o arquivo uma vez.

Funciona da mesma forma em uma Machine hospedada e no seu próprio computador.

## O que vem no arquivo

- Pessoas, organizações e projetos: uma página Markdown para cada um, com as relações entre eles.
- Fatos e preferências: o que sua Machine sabe sobre você e sobre essas pessoas e organizações.
- Fatos antigos: o que já não é válido (porque terminou ou foi substituído) e o que entrou no lugar. Fatos removidos por você não são incluídos.
- Regras, seu jeito de escrever e assinaturas: o que orienta seus rascunhos.
- Habilidades: seus guias práticos, ativados ou desativados.
- Contexto: briefings da equipe, linhas de resumo, promessas e tarefas em aberto.
- Fontes: a origem de cada item, com ID e data.

Contatos e tarefas também vêm em planilhas (CSV). Um README no início explica à IA como ler tudo. Envie o arquivo zip para a IA como arquivo de conhecimento ou projeto.

## O que fica de fora

Senhas, chaves e credenciais de acesso nunca são incluídas. Os dados, as configurações e as fotos dos colegas de equipe também ficam de fora. Para transferir sua Machine inteira, consulte [Mudar para outro computador](moving.md).

Para desenvolvedores: [o formato do arquivo](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md).
