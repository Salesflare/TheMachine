---
title: Historique
area: connections
summary: Environ un an d’anciens e-mails, réunions et discussions WhatsApp, à chercher et lire. Jamais une tâche.
covers: history
code: machine/app/history.py, machine/store/history.py
keywords: older messages, backfill, archive, past emails
---
## Ce qu’il garde

Chaque compte e-mail, agenda et WhatsApp garde environ un an d’anciens messages et réunions. La recherche les trouve, une conversation les montre et l’[Agenda](calendar.md) montre les réunions passées.

Sa carte indique jusqu’où il remonte : **Historique : jusqu’à** un mois, une fois arrivé.

## Ce qu’il ne fait jamais

L’historique sert seulement à retrouver des choses. Il ne crée jamais de tâche ni de promesse, n’entre jamais dans une vérification, ne compte jamais comme nouveau et ne va jamais dans votre Graph ni à votre équipe. Aucun modèle d’IA ne le lit.

Les tâches et promesses viennent toujours seulement des nouveaux messages, comme avant.

## Quand il tourne

Il commence une fois le premier coup d’œil à vos messages terminé, et avance lentement en arrière-plan. Il attend pendant une vérification ou une synchronisation, et quand votre Machine manque d’espace disque ou de mémoire. Après un redémarrage, il reprend là où il en était.

Il utilise l’accès que chaque connexion a déjà. Rien de nouveau n’est demandé.

## Jusqu’où

Environ un an par défaut. Les Machines auto-hébergées peuvent régler `history_days` dans la configuration (0 le coupe, jusqu’à 730). Telegram, Slack et les autres sources gardent ce qu’elles lisent aujourd’hui.
