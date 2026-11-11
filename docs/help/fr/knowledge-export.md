---
title: Connaissances pour une autre IA
area: settings
summary: Emportez ce que votre Machine a appris vers n’importe quelle autre IA, en simples fichiers Markdown, JSONL et CSV.
covers: knowledge-export
code: machine/export/knowledge.py, machine/app/knowledge_export.py, cli.py
order: 6
---
Tout ce que votre Machine apprend vous appartient. Emportez-le vers une autre IA, ou gardez-le, même si vous n’utilisez plus The Machine.

## Exporter

1. Dans **Paramètres** › **Général**, appuyez sur **Exporter** à côté de **Connaissances pour une autre IA**.
2. Laissez **Texte des messages** désactivé pour n’exporter que l’origine de chaque élément, et sa date. Activez-le pour ajouter le texte.
3. **Privé et Prudent** reste désactivé, sauf si vous voulez aussi les projets pour vous seul, les fils privés et les Fleets en mode Prudent.
4. Définissez si vous le souhaitez une **Phrase secrète** d’au moins 10 caractères pour chiffrer le fichier.
5. Appuyez sur **Télécharger**. Le fichier est créé sur votre Machine et se télécharge une seule fois.

Sur une Machine hébergée, c’est pareil, depuis les Paramètres de votre Machine. Sur votre propre ordinateur, `assistant export-knowledge` crée le même fichier.

## Ce qu’il contient

- Personnes, organisations et projets : une page Markdown pour chacun, avec leurs liens.
- Faits et préférences : ce que votre Machine sait, sur vous et sur eux.
- Faits passés : ce qui ne vaut plus (terminé, mis de côté ou remplacé), avec ce qui l’a remplacé. Les faits que vous avez retirés restent dehors.
- Règles, votre façon d’écrire et signatures : ce que suivent vos brouillons.
- Compétences : vos méthodes, actives ou non.
- Contexte : briefs d’équipe, lignes de résumé, promesses et tâches ouvertes.
- Sources : l’origine de chaque élément, par identifiant et date.

Les enregistrements sont en JSONL, les contacts et les tâches aussi en CSV. Un README.md en tête explique l’organisation et indique à une IA comment s’en servir. Donnez le dossier, ou le zip, à l’IA comme fichier de connaissances ou projet.

## Ce qui reste dehors

Mots de passe, clés et connexions n’y entrent jamais. Ce qui ressemble à une clé est remplacé. Les données de vos coéquipiers et d’autres Machines, les réglages et les photos restent aussi dehors. Pour une copie complète afin de déplacer votre Machine, voir [Passer sur votre propre ordinateur](moving.md).

Le format est ouvert et versionné : voir [le schéma](https://github.com/Salesflare/TheMachine/blob/main/docs/knowledge-export.md).
