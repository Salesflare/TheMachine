---
title: Historique
area: connections
summary: Environ un an d’anciens e-mails, réunions et messages WhatsApp, Slack et Teams, pour chercher, lire et connaître vos contacts. Jamais une tâche.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
---
## Ce qu’il garde

Chaque compte e-mail, agenda, WhatsApp, Slack et Teams garde environ un an d’anciens messages et réunions. La recherche les trouve, aussi par le sens, une conversation les montre et l’[Agenda](calendar.md) montre les réunions passées.

Sa carte indique jusqu’où il remonte : **Historique : jusqu’à** un mois, une fois arrivé.

## Ce qu’il apporte à votre Graph

Votre [Graph](graph.md) le compte : votre proximité avec chacun, votre dernier échange, qui connaît qui, et les personnes et organisations elles-mêmes. Les réponses de votre Fleet à « qui connaît quelqu’un » l’utilisent depuis les comptes de travail, avec les mêmes [règles de partage](sharing-rules.md) que les nouveaux e-mails.

## Ce qu’il ne fait jamais

Il ne crée jamais de tâche ni de promesse, ne compte jamais comme nouveau, ne lance jamais de vérification et n’entre jamais dans un projet. L’historique personnel reste personnel, comme les e-mails personnels. En dehors de la recherche par le sens, aucun modèle d’IA ne le lit.

## Quand il tourne

Il commence une fois le premier coup d’œil à vos messages terminé, et pour chaque connexion seulement quand sa première semaine est arrivée, aussi pour une connexion ajoutée plus tard. Il avance lentement en arrière-plan et attend pendant une vérification ou une synchronisation, quand un service demande de ralentir ou quand votre Machine manque d’espace. Les nouveaux messages passent toujours en premier.

Il utilise l’accès que chaque connexion a déjà. Rien de nouveau n’est demandé.

## Jusqu’où

Environ un an par défaut. Les Machines auto-hébergées peuvent régler `history_days` dans la configuration (0 le coupe, jusqu’à 730). Telegram et les autres sources gardent ce qu’elles lisent aujourd’hui.
