---
title: Règles de partage
area: fleet
summary: Ce que votre Machine peut répondre, par Fleet et par type de question. Me demander d’abord, Toujours, Jamais ou Noms uniquement.
covers: 
code: fleet.py, dashboard.html
order: 2
keywords: share, sharing, colleagues, teammates, team, what others see, answer for me
translated: 8c6f3bda9dfdbe8e
---
## Configurez-les

Décidez de ce que votre Machine dit à votre Fleet. Dans l’onglet **Fleet**, ouvrez **Partage**. Chaque type de question a une règle :

- **Me demander d’abord** : vous voyez chaque question et décidez.
- **Toujours** : votre Machine répond d’elle-même.
- **Jamais** : elle refuse.
- **Noms** : indique si la réponse peut préciser de qui il s’agit, par exemple le nom d’un invité, ou si elle doit omettre les noms.

Elle ne partage jamais le contenu des e-mails ni le sujet de vos réunions. **Différent pour quelqu’un ? Ajoutez une exception** permet de définir une règle pour une personne.

Les règles ne peuvent être modifiées que dans le tableau de bord, jamais depuis un message.

## Dans un Fleet de travail

Dans un Fleet de travail standard, les questions sur les personnes que quelqu’un connaît, le contexte des réunions et la personne qui traite les e-mails partagés n’acceptent que **Toujours** et **Jamais**. Avec **Toujours**, votre Machine répond uniquement à partir des informations que le [Graph d’équipe](team-graph.md) partage déjà avec votre équipe, et ne nomme que les personnes qu’il partage. Une règle enregistrée sur **Me demander d’abord** fonctionne comme **Toujours**.

Tant que le Graph d’équipe ne partage rien, les questions sur les personnes que quelqu’un connaît et le contexte des réunions restent aussi réglés sur **Me demander d’abord**. C’est également le cas dans un Fleet prudent. Consultez [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).

## La première fois que quelqu’un pose la question

Une question qui nécessite votre intervention arrive sous forme de tâche, avec les options **Partager une fois**, **Toujours partager**, **Refuser** ou **Ne jamais partager**.
