---
title: Activité
area: settings
summary: Une liste de tout ce que The Machine a fait pour vous, le plus récent d’abord : messages, documents, réponses de Fleet, apprentissages, connexions et plus.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
---
## Ce qu’elle montre

Ouvrez **Paramètres**, **Activité**. Chaque ligne est une chose que The Machine a faite, la plus récente d’abord, par jour :

- ce qu’elle a fait, et comment cela s’est terminé : envoyé, refusé, échoué ou annulé
- quand, le compte ou l’app utilisé, et [ce qui l’a permis](activity.md#what-allowed-it)
- un lien vers sa tâche, quand il y en a une
- pour une IA que vous avez connectée, comme ChatGPT ou Claude : son nom avec **(IA connectée)**, pour la distinguer de The Machine

Elle liste les messages et réponses, les modifications de documents et d’agenda, les étapes sur le web, les corrections qu’elle a fusionnées, les agents de code, les questions et réponses de Fleet, les apprentissages envoyés à l’équipe de The Machine, les compétences, les imports dans le Graph, les faits que vous lui avez demandé d’oublier dans le chat (avec **Annuler**), les connexions ajoutées ou retirées, et chaque consultation de notre équipe via l’[Accès du support](get-support.md#support-access), refusées comprises.

## Ce qui l’a permis

Chaque message, modification de document ou d’agenda, étape sur le web et correctif fusionné indique ce qui l’a laissé partir, au moment où c’est arrivé :

- **Approuvé dans la tâche** ou **Approuvé dans Telegram** : votre appui sur Envoyer, Confirmer ou Fusionner
- **Approuvé à la voix** : votre oui dans Talk
- **« Faire » touché** : votre Faire sur la tâche
- **Demandé dans le chat** : vous l’avez demandé avec des mots, avec le début de votre message entre guillemets. Une citation ne s’affiche que tant que ces mots restent dans votre propre message.
- **Relance qu’elle a envoyée d’elle-même**, **Petit correctif, fusionné d’elle-même**, **Nouveau document privé, créé d’elle-même** ou **Préparé à l’avance, d’elle-même** : un de vos réglages ou une règle propre à The Machine
- **Aucune approbation enregistrée** : rien n’a été enregistré. Cela part aussi dans nos [rapports d’erreurs](error-reports.md), pour trouver le chemin qui l’a manqué.

Étapes sur le web liste aussi l’exécution d’une tâche qui a cliqué ou tapé sur une page, avec ce qui a permis cette exécution.

Les lignes plus anciennes, d’avant cet enregistrement, gardent leurs anciens mots, comme **Après votre accord**.

## Filtrer

Choisissez un type dans la liste en haut, comme **Messages** ou **Fleet**. **Refusé ou bloqué** montre seulement ce qui n’est pas parti, et pourquoi. **Afficher plus** charge des lignes plus anciennes.

## Autres endroits

Le chat d’une tâche raconte toujours sa propre histoire ; Activité y renvoie. Fleet, **Activité** montre les mêmes lignes pour vos Fleets et apprentissages, avec **Retirer** pour un apprentissage. Dans Paramètres, **Sécurité**, **Voir chaque consultation dans Activité** ouvre les consultations de notre équipe.

Activité montre seulement ce qui s’est passé. Elle ne change jamais ce que The Machine a le droit de faire.
