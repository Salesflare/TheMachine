---
title: Connaissances pour une autre IA
area: settings
summary: Emportez ce que votre Machine a appris vers n’importe quelle autre IA, dans des fichiers simples qu’elle peut lire.
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
translated: 6a917f8ee2aabaa9
---
Tout ce que votre Machine apprend vous appartient. Transmettez-le à une autre IA, comme ChatGPT ou Claude, ou gardez-le.

## Exporter

1. Dans **Paramètres** › **Général** › **Exporter**, appuyez sur **Exporter** à côté de **Connaissances pour une autre IA**.
2. **Texte des messages** est désactivé par défaut : seuls sont inclus la source de chaque élément et sa date. Activez-le pour ajouter le texte.
3. Activez **Privé et Prudent** uniquement pour inclure les projets auxquels vous seul avez accès, les fils privés et les Fleet pour lesquelles le mode Prudent est activé.
4. Vous pouvez définir une **Phrase secrète** (10 caractères minimum) pour chiffrer le fichier.
5. Appuyez sur **Télécharger**. Le fichier ne peut être téléchargé qu’une seule fois.

La procédure est la même sur une Machine hébergée et sur votre propre ordinateur.

## Contenu

- Personnes, organisations et projets : une page Markdown par élément, avec leurs relations.
- Faits et préférences : ce que votre Machine sait de vous et des autres.
- Faits passés : ce qui n’est plus d’actualité (terminé, mis de côté ou remplacé), et ce qui l’a remplacé. Les faits que vous avez supprimés ne sont pas inclus.
- Règles, style d’écriture et signatures : ce que suivent vos brouillons.
- Compétences : vos procédures, activées ou non.
- Contexte : briefs d’équipe, lignes de résumé, promesses et tâches en cours.
- Sources : la provenance de chaque élément, par identifiant et date.

Les contacts et les tâches sont aussi fournis sous forme de feuilles de calcul (CSV). Un README en tête indique à l’IA comment tout lire. Importez le fichier zip dans l’IA comme fichier de connaissances ou projet.

## Éléments exclus

Les mots de passe, clés et identifiants de connexion ne sont jamais inclus. Les données, paramètres et photos de vos coéquipiers sont également exclus. Pour déplacer toute votre Machine, consultez [Passer à un autre ordinateur](moving.md).

Pour les développeurs : [le format de fichier](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md).
