---
title: Règles de partage
area: fleet
summary: Définissez ce que votre Machine peut répondre pour chaque Fleet et chaque type de question. Choisissez de vous demander d’abord, de toujours répondre ou de ne jamais répondre, et indiquez si les noms peuvent être partagés.
covers:
code: fleet.py, dashboard.html
order: 2
keywords: share, sharing, colleagues, teammates, team, what others see, answer for me
translated: d8d11dd5b221c885
---
## Les définir

Choisissez ce que votre Machine dit à votre Fleet. Dans l’onglet **Fleet**, ouvrez **Partage**. Chaque type de question a une règle :

- **Me demander d’abord** : vous voyez chaque question et décidez.
- **Toujours** : votre Machine répond toute seule.
- **Jamais** : elle refuse.
- **Noms** : indiquez si la réponse peut préciser de qui il s’agit, par exemple en donnant le nom d’un invité, ou si elle doit omettre les noms.

Elle ne partage jamais un e-mail entier ni le contenu de vos réunions. Dans votre Fleet Famille, les **Questions** (comme « Des nouvelles du tapis ? ») sont réglées sur **Me demander d’abord** ou **Jamais** : consultez [Famille](family.md). **Différent pour quelqu’un ? Ajoutez une exception** permet de définir une règle pour une personne.

Les règles se modifient uniquement dans le tableau de bord, jamais depuis un message.

## Dans une Fleet Travail

Dans une Fleet Travail standard, les règles pour savoir qui connaît qui, le contexte des réunions et la personne qui gère les e-mails partagés sont limitées à **Toujours** et **Jamais**. Avec **Toujours**, votre Machine répond uniquement à partir des informations que le [Graph d’équipe](team-graph.md) partage déjà avec votre équipe, et ne cite que les personnes qui y figurent. Une règle enregistrée sur **Me demander d’abord** fonctionne comme **Toujours**.

Tant que le Graph d’équipe ne partage rien, les règles pour savoir qui connaît qui et le contexte des réunions peuvent aussi rester sur **Me demander d’abord**. C’est également le cas dans une Fleet prudente. Consultez [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).

## La première fois que quelqu’un pose une question

Une question qui nécessite votre intervention arrive sous forme de tâche, avec les options **Partager une fois**, **Toujours partager**, **Refuser** ou **Ne jamais partager**.
