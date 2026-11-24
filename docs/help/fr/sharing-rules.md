---
title: Règles de partage
area: fleet
summary: Par Fleet et par type de question, ce que votre Machine peut répondre. Choisissez **Me demander d’abord**, **Toujours** ou **Jamais**, et si les noms peuvent être partagés.
covers:
code: fleet.py, dashboard.html
order: 2
keywords: share, sharing, colleagues, teammates, team, what others see, answer for me
translated: 53c4e81f9f5deef4
---
## Les définir

Choisissez ce que votre Machine dit à votre Fleet. Dans l’onglet **Fleet**, ouvrez **Partage**. Chaque type de question a une règle :

- **Me demander d’abord** : vous voyez chaque question et décidez.
- **Toujours** : votre Machine répond automatiquement.
- **Jamais** : elle refuse.
- **Noms** : indique si la réponse peut mentionner des personnes, par exemple le nom d’un invité, ou si elle omet les noms.

Votre Machine ne partage jamais un e-mail entier ni le sujet de vos réunions. Dans votre Fleet Famille, **Questions** (comme « Des nouvelles du tapis ? ») sont réglées sur **Me demander d’abord** ou **Jamais**, avec **Toujours** pour une personne à la fois : voir [Famille](family.md#always-for-one-person). **Différent pour quelqu’un ? Ajoutez une exception** permet de définir une règle pour une personne.

Les règles se modifient uniquement dans le tableau de bord, jamais depuis un message.

## Dans une Fleet Travail

Dans une Fleet Travail standard, les règles concernant qui connaît qui, le contexte des réunions et la gestion des e-mails partagés proposent uniquement **Toujours** et **Jamais**. **Toujours** répond uniquement avec les informations que le [Graph d’équipe](team-graph.md) partage déjà avec votre équipe, et ne mentionne que les personnes dont il partage le nom. Une règle enregistrée sur **Me demander d’abord** fonctionne comme **Toujours**.

Tant que le Graph d’équipe ne partage rien, les règles concernant qui connaît qui et le contexte des réunions proposent aussi **Me demander d’abord**, tout comme dans une Fleet prudente. Voir [Fleets](fleet.md#answered-by-itself-in-a-work-fleet).

## La première fois qu’on vous pose une question

Une question qui nécessite votre intervention arrive sous forme de tâche, avec les choix **Partager une fois**, **Toujours partager**, **Refuser** ou **Ne jamais partager**.
