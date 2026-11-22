---
title: Activité
area: settings
summary: Une liste de tout ce que The Machine a fait pour vous, du plus récent au plus ancien : messages, documents, réponses de Fleet, apprentissages, connexions et plus encore.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
translated: ebb6a4cf0474a020
---
## Ce qu’elle affiche

Ouvrez **Paramètres**, puis **Activité**. Chaque ligne correspond à une action de The Machine, par jour, de la plus récente à la plus ancienne :

- ce qu’elle a fait et le résultat : envoyé, refusé, échoué ou annulé
- quand elle l’a fait, le compte ou l’application utilisé, et [ce qui l’y a autorisée](activity.md#what-allowed-it)
- un lien vers la tâche correspondante, le cas échéant
- pour une IA que vous avez connectée, comme ChatGPT ou Claude : son nom suivi de **(IA connectée)**, pour la distinguer de The Machine

La liste inclut les messages et les réponses, les modifications de documents et d’agendas, les actions sur le Web, les correctifs qu’elle a fusionnés, les agents de programmation, les questions et réponses de Fleet, les apprentissages transmis à l’équipe The Machine, les compétences, les importations de Graph, les informations que vous avez demandé à votre chat d’oublier (avec **Annuler**), les connexions ajoutées ou supprimées, ainsi que chaque consultation par notre équipe dans le cadre de [l’accès à l’assistance](get-support.md#support-access), y compris les consultations refusées.

## Ce qui l’a autorisée

Pour chaque message, modification de document ou d’agenda, action sur le Web et correctif fusionné, l’activité indique ce qui l’a autorisée, au moment où cela s’est passé :

- **Approuvé dans la tâche** ou **Approuvé dans Telegram** : vous avez appuyé sur **Envoyer**, **Confirmer** ou **Fusionner**
- **Approuvé à la voix** : vous avez répondu oui dans Talk
- **« Faire » touché** : vous avez appuyé sur **Faire** dans la tâche
- **Demandé dans le chat** : vous l’avez demandé par écrit. Le début de votre message apparaît entre guillemets. La citation reste affichée uniquement tant que ces mots figurent encore dans votre message.
- **Relance qu’elle a envoyée d’elle-même**, **Petit correctif, fusionné automatiquement**, **Nouveau document privé, créé d’elle-même** ou **Préparé à l’avance, d’elle-même** : un de vos réglages ou une règle interne de The Machine
- **Aucune approbation enregistrée** : aucune approbation n’a été enregistrée. L’action apparaît aussi dans nos [rapports d’erreur](error-reports.md), pour nous aider à trouver ce qui n’a pas fonctionné.

Les actions sur le Web incluent aussi les exécutions d’une tâche qui a cliqué ou saisi du texte sur une page, avec l’autorisation correspondante. Le travail qui se poursuit après une mise en attente conserve l’autorisation donnée avant celle-ci.

Les anciennes lignes, antérieures à l’enregistrement de ces informations, gardent leur ancien libellé, comme **Après votre accord**.

## Filtrer la liste

Choisissez un type dans la liste en haut, comme **Messages** ou **Fleet**. **Refusé ou bloqué** affiche uniquement les actions qui n’ont pas abouti, et leur raison. **Afficher plus** charge des lignes plus anciennes.

## Autres emplacements

Le chat d’une tâche conserve son propre historique. Activité contient un lien vers celui-ci. Dans Fleet, **Activité** affiche les mêmes lignes pour vos Fleet et vos apprentissages, avec **Retirer** pour un apprentissage. Dans **Sécurité**, sous Paramètres, **Voir chaque consultation dans Activité** ouvre la liste des consultations de notre équipe.

Activité indique uniquement ce qui s’est passé. Elle ne change jamais ce que The Machine peut faire.
