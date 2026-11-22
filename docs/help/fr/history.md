---
title: Historique
area: connections
summary: Environ un an d’anciens e-mails, de réunions et de messages WhatsApp, Slack et Teams, à rechercher et à lire pour mieux connaître vos contacts. Jamais de tâche.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: 93575cd78b3085f7
---
## Ce qu’elle conserve

Votre Machine importe environ un an d’anciens e-mails, de réunions et de messages WhatsApp, Slack et Teams. La recherche les retrouve, y compris par sens, les fils de discussion les affichent et l’[Agenda](calendar.md) montre les réunions passées.

Chaque connexion dans **Connexions** indique jusqu’où elle remonte, par exemple **Historique : depuis** novembre 2025.

## Ce que cela ajoute à votre Graph

Votre [Graph](graph.md) en tient compte : la proximité de vos relations, la date de votre dernier échange, qui connaît qui, ainsi que les personnes et les organisations elles-mêmes. La chronologie d’une personne ou d’une organisation l’affiche aussi, pour que son dernier contact soit toujours visible. Les réponses de votre Fleet à la question « qui connaît quelqu’un » en tiennent compte pour les comptes professionnels, selon les mêmes [règles de partage](sharing-rules.md) que pour les nouveaux e-mails.

## Ce qu’elle ne fait jamais

Elle ne crée jamais de tâche ni de promesse, ne compte jamais comme du nouveau, ne lance jamais de vérification et n’ajoute jamais rien à un projet. L’historique personnel reste personnel, comme les e-mails personnels. À l’exception de la recherche par sens, aucun modèle d’IA ne le lit.

## Quand elle s’exécute

Elle démarre après la première analyse de vos messages. Pour chaque connexion, elle ne démarre qu’une fois la première semaine écoulée, y compris pour une connexion ajoutée plus tard. Elle s’exécute lentement en arrière-plan et se met en pause pendant une vérification ou une synchronisation, lorsqu’un service lui demande de ralentir ou lorsque votre Machine manque d’espace. Les nouveaux messages passent toujours en premier.

Une fois l’historique d’une boîte aux lettres importé, votre Machine relit une fois les e-mails conservés pour en extraire les détails de réservation et de billets. Les anciennes réservations apparaissent ainsi aussi dans [voyages et événements](calendar.md#trips-and-events). Cette opération est tout aussi lente et se met en pause pour les mêmes raisons.

Elle utilise les accès déjà accordés à chaque connexion. Aucune nouvelle autorisation n’est nécessaire.

## Jusqu’où elle remonte

Environ un an. Sur votre propre ordinateur, `history_days` dans le fichier de paramètres permet de modifier cette durée (0 la désactive, jusqu’à 730). Telegram et les autres sources n’importent pas d’historique plus ancien.

Les messages LinkedIn et X remontent à 90 jours. Leur lecture est très lente : quelques consultations légères par heure, uniquement en journée, et aucune pendant une journée si le site s’y oppose, pour protéger votre compte (`social_history_days`, 0 désactive cette lecture).
