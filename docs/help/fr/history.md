---
title: Historique
area: connections
summary: Environ un an d’anciens e-mails, de réunions et de messages WhatsApp, Slack et Teams, à rechercher et à consulter pour mieux connaître vos contacts. Jamais de tâche.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: 2b5e84c61892c8e4
---
## Ce qu’elle conserve

Votre Machine importe environ un an d’anciens e-mails, de réunions et de messages WhatsApp, Slack et Teams. La recherche les retrouve, y compris par sens, les fils de discussion les affichent et l’[Agenda](calendar.md) présente les réunions passées.

Chaque connexion dans **Connexions** indique jusqu’où elle remonte, par exemple **Historique : depuis** novembre 2025.

## Ce qu’elle ajoute à votre Graph

Votre [Graph](graph.md) en tient compte : votre proximité avec les gens, la date de votre dernier échange, qui connaît qui, ainsi que les personnes et les organisations elles-mêmes. La chronologie d’une personne ou d’une organisation l’affiche aussi, pour que son dernier contact soit toujours visible. Les réponses de votre Fleet à la question « qui connaît qui » s’appuient sur ces données des comptes professionnels, selon les mêmes [règles de partage](sharing-rules.md) que pour les nouveaux e-mails.

## Ce qu’elle ne fait jamais

Elle ne crée jamais de tâche ni de promesse, ne considère jamais ces éléments comme nouveaux, ne lance jamais de vérification et ne les ajoute jamais à un projet. L’historique personnel reste privé, comme les e-mails personnels.

En dehors de la recherche sémantique, votre modèle d’IA ne lit ces éléments que dans trois cas :

- dans les résultats d’une recherche, par exemple pour répondre à une question ou traiter une tâche
- dans les e-mails contenant des détails de réservation, pour les [voyages et événements](calendar.md#trips-and-events)
- dans un [briefing de réunion](calendar.md#ready-for-your-meetings) : des notes de réunions précédentes et quelques anciens messages échangés avec les personnes que vous rencontrez

## Quand elle fonctionne

Elle démarre après le premier examen de vos messages. Pour chaque connexion, elle attend que la première semaine soit importée, y compris pour celles que vous ajoutez plus tard. Elle fonctionne lentement en arrière-plan et s’interrompt pendant une vérification ou une synchronisation, quand un service lui demande de ralentir ou quand votre Machine manque d’espace. Les nouveaux messages passent toujours en premier.

Une fois l’historique d’une boîte aux lettres importé, votre Machine relit les e-mails qu’elle conserve pour repérer les détails de réservation et de billets. Les anciennes réservations apparaissent ainsi aussi dans les [voyages et événements](calendar.md#trips-and-events). Elle avance tout aussi lentement et s’interrompt pour les mêmes raisons.

Elle utilise les autorisations déjà accordées à chaque connexion. Rien de nouveau à approuver.

## Jusqu’où remonte l’historique

Environ un an. Sur votre propre ordinateur, `history_days` dans le fichier de paramètres permet de modifier cette durée (0 la désactive, jusqu’à 730). Telegram et les autres sources n’importent pas d’historique plus ancien.

Les messages LinkedIn et X remontent à 90 jours et sont lus très lentement : quelques petites lectures par heure, uniquement en journée, et aucune pendant une journée si le site s’y oppose, pour protéger votre compte (`social_history_days`, 0 désactive cette option).
