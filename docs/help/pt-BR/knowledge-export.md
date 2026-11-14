---
title: Conhecimento para outra IA
area: settings
summary: Leve o que sua Machine aprendeu para qualquer outra IA, em arquivos simples que qualquer IA consegue ler.
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
translated: 6a917f8ee2aabaa9
---
Tudo o que sua Machine aprende pertence a você. Compartilhe com outra IA, como ChatGPT ou Claude, ou guarde para você.

## Exportar

1. Em **Configurações** › **Geral** › **Exportar**, clique em **Exportar** ao lado de **Conhecimento para outra IA**.
2. **Texto das mensagens** fica desativado por padrão: o arquivo inclui apenas a origem de cada informação e a data. Ative essa opção para incluir o texto.
3. Ative **Privado e Cuidadoso** somente se quiser incluir projetos só seus, conversas privadas e Fleet cuidadosas.
4. Se quiser, defina uma **Frase secreta** (com pelo menos 10 caracteres) para criptografar o arquivo.
5. Clique em **Baixar**. O arquivo só pode ser baixado uma vez.

O processo é o mesmo em uma Machine hospedada e no seu próprio computador.

## O que está incluído

- Pessoas, organizações e projetos: uma página Markdown para cada um, com as relações entre eles.
- Fatos e preferências: o que sua Machine sabe sobre você e sobre eles.
- Fatos antigos: informações que não são mais válidas (porque chegaram ao fim, foram deixadas de lado ou substituídas), junto com o que as substituiu. Fatos que você removeu não são incluídos.
- Regras, seu jeito de escrever e assinaturas: o que orienta seus rascunhos.
- Habilidades: seus tutoriais, ativados ou desativados.
- Contexto: resumos da equipe, linhas de resumo, promessas e tarefas em aberto.
- Fontes: a origem de cada informação, com ID e data.

Os contatos e as tarefas também são incluídos em planilhas (CSV). Um README no início explica à IA como ler tudo. Envie o arquivo zip para a IA como arquivo de conhecimento ou projeto.

## O que não está incluído

Senhas, chaves e dados de acesso nunca são incluídos. Os dados, as configurações e as fotos dos colegas de equipe também ficam de fora. Para transferir sua Machine inteira, consulte [Mudar para outro computador](moving.md).

Para desenvolvedores: [o formato do arquivo](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md).
