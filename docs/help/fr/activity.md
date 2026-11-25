---
title: Activité
area: settings
summary: Une seule liste de tout ce que The Machine a fait pour vous, du plus récent au plus ancien : messages, documents, réponses de Fleet, apprentissages, connexions et plus encore.
covers: settings:activity
code: activity_log.py, dashboard/settings-activity.js
order: 2
keywords: log, history, audit, what did it do, sent, refused, blocked
translated: 1ebeba09417a11e9
---
## Ce qu’elle affiche

Ouvrez **Paramètres**, puis **Activité**. Chaque ligne correspond à une action de The Machine, classée par jour, de la plus récente à la plus ancienne :

- ce qu’elle a fait et comment cela s’est terminé : envoyé, refusé, échoué ou annulé ; pour un message [envoyé plus tard](send-later.md), la date à laquelle il a été programmé, modifié ou annulé
- quand, le compte ou l’application utilisés et [ce qui l’a autorisée](activity.md#what-allowed-it)
- un lien vers la tâche correspondante, le cas échéant
- pour une IA que vous avez connectée, comme ChatGPT ou Claude : son nom suivi de **(IA connectée)**, pour la distinguer de The Machine

La liste comprend les messages et les réponses, les modifications de documents et d’agenda, les actions sur le Web, les correctifs qu’elle a fusionnés, les agents de programmation, les questions et réponses de Fleet, les apprentissages envoyés à l’équipe The Machine, les compétences, les importations dans Graph, les informations que vous avez demandé à votre chat d’oublier (avec **Annuler**), les connexions ajoutées ou supprimées et chaque consultation par notre équipe dans [l’accès au support](get-support.md#support-access), y compris celles qui ont été refusées.

## Ce qui l’a autorisée

Pour chaque message, modification de document ou d’agenda, action sur le Web et correctif fusionné, la liste indique ce qui l’a autorisé au moment où cela s’est produit :

- **Approuvé dans la tâche** ou **Approuvé dans Telegram** : vous avez touché Envoyer, Confirmer ou Fusionner
- **Approuvé à la voix** : vous avez répondu oui dans Talk
- **« Faire » touché** : vous avez touché Faire dans la tâche
- **Demandé dans le chat** : vous l’avez demandé par écrit, avec le début de votre message entre guillemets. La citation s’affiche uniquement tant que ces mots figurent encore dans votre message.
- **Relance qu’elle a envoyée d’elle-même**, **Petit correctif, fusionné automatiquement**, **Nouveau document privé, créé d’elle-même** ou **Préparé à l’avance, d’elle-même** : l’action était autorisée par un de vos paramètres ou par une règle de The Machine
- **Aucune approbation enregistrée** : aucune approbation n’a été enregistrée. L’action figure aussi dans nos [rapports d’erreur](error-reports.md), pour que nous puissions trouver ce qui n’a pas fonctionné.

La liste des actions sur le Web indique aussi quand une tâche a cliqué ou saisi du texte sur une page, et ce qui a autorisé cette action. Les actions qui se poursuivent après une mise en attente conservent l’autorisation qu’elles avaient avant celle-ci.

Les anciennes lignes, enregistrées avant la mise en place de ce suivi, gardent leur ancienne formulation, comme **Après votre accord**.

## Filtrer la liste

Choisissez un type dans la liste en haut, comme **Messages** ou **Fleet**. **Refusé ou bloqué** affiche uniquement les actions qui n’ont pas abouti, avec leur motif. **Afficher plus** charge les lignes plus anciennes.

## Autres emplacements

Le chat d’une tâche raconte toujours son propre historique ; Activité contient un lien vers celui-ci. Dans Fleet, **Activité** affiche les mêmes lignes pour vos Fleet et vos apprentissages, avec l’option **Retirer** pour un apprentissage. Dans **Sécurité**, ouvrez **Voir chaque consultation dans Activité** pour afficher les consultations de notre équipe.

Activité affiche uniquement ce qui s’est passé. Elle ne change jamais ce que The Machine peut faire.
