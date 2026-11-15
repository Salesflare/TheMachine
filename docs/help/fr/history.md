---
title: Historique
area: connections
summary: Environ un an d’anciens e-mails, de réunions et de messages WhatsApp, Slack et Teams à rechercher et à lire pour mieux connaître vos contacts. Jamais une tâche.
covers: history
code: machine/app/history.py, machine/store/history.py, machine/store/graph_history.py
keywords: older messages, backfill, archive, past emails
translated: c10fe5fb8d7b2d8b
---
## Ce qu’il conserve

Votre Machine importe environ un an d’anciens e-mails, de réunions et de messages WhatsApp, Slack et Teams. La recherche les retrouve, y compris par sens, les fils de discussion les affichent et le [Calendrier](calendar.md) montre les réunions passées.

Chaque connexion dans **Connexions** indique jusqu’où elle remonte, par exemple **Historique : depuis** novembre 2025.

## Ce que cela ajoute à votre Graph

Votre [Graph](graph.md) en tient compte : votre proximité avec les personnes, la date de votre dernier échange, qui connaît qui, ainsi que les personnes et les organisations elles-mêmes. Leur chronologie l’affiche aussi, pour que le dernier contact soit toujours visible. Les réponses de votre Fleet à la question « qui connaît cette personne ? » s’appuient dessus pour les comptes professionnels, selon les mêmes [règles de partage](sharing-rules.md) que pour les nouveaux e-mails.

## Ce qu’il ne fait jamais

Il ne crée jamais de tâche ni de promesse, ne compte jamais comme du nouveau, ne lance jamais de vérification et n’ajoute rien à un projet. L’historique personnel reste personnel, comme les e-mails personnels. À part la recherche par sens, aucun modèle d’IA ne le lit.

## Quand il s’exécute

Il démarre après le premier examen de vos messages. Pour chaque connexion, il ne commence qu’une fois sa première semaine écoulée, y compris pour celles que vous ajoutez plus tard. Il s’exécute lentement en arrière-plan et se met en pause pendant une vérification ou une synchronisation, si un service lui demande de ralentir ou si votre Machine manque d’espace. Les nouveaux messages passent toujours en premier.

Une fois l’historique d’une boîte mail importé, votre Machine relit les e-mails conservés pour y trouver les détails de réservations et de billets. Les anciennes réservations apparaissent ainsi aussi dans [Voyages et événements](notes.md). La lecture est tout aussi lente et s’interrompt pour les mêmes raisons.

Il utilise les accès déjà accordés à chaque connexion. Rien de nouveau à approuver.

## Jusqu’où il remonte

Environ un an. Sur votre propre ordinateur, `history_days` dans le fichier de paramètres permet de modifier cette durée (0 désactive la fonction, jusqu’à 730). Telegram et les autres sources n’importent pas l’historique plus ancien.

Les messages LinkedIn et X remontent à 90 jours. Ils sont lus très lentement : quelques petites lectures par heure, uniquement pendant la journée, et aucune pendant une journée si le site s’y oppose, afin de protéger votre compte (`social_history_days`, 0 désactive la fonction).
