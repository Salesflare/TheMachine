---
title: Aucune nouvelle tâche
area: troubleshooting
summary: Les vérifications sont désactivées, en attente ou arrêtées à cause de la limite d’utilisation de votre modèle. Voici comment le savoir et quoi faire.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py
order: 3
translated: 07aca53acc41694d
---
Les tâches viennent des vérifications : votre Machine examine les nouveaux messages au bout d’environ 15 minutes.

## Vous venez de vous inscrire

Sur une nouvelle Machine hébergée, les vérifications démarrent automatiquement une fois votre IA et vos e-mails connectés. Pendant que votre Machine lit vos e-mails, la section Tâches affiche « Lecture de vos e-mails, premières tâches dans quelques minutes. » Une fois qu’elle sait combien il y a de messages, elle indique un délai approximatif : « Premières tâches dans environ 10 min. » S’il manque une étape, **Vous attend** la signale, par exemple **Connecter vos e-mails**, avec un lien vers cette étape.

Pendant la lecture, la section Tâches indique sa progression (« 20 messages lus sur 132. Lecture des 40 suivants… »), quelques personnes et organisations repérées, et affiche votre première tâche dès qu’elle est prête. Le nombre correspond aux messages dont la lecture est terminée ; la barre continue d’avancer pendant la lecture des suivants. Les noms viennent de vos e-mails et vous seul les voyez.

Si le premier examen ne trouve rien pour vous, il indique ce qui a été lu et propose les prochaines étapes, comme connecter un service qui vous envoie souvent des e-mails ou demander ce qui a changé cette semaine.

## Les vérifications sont désactivées

En haut de la section Tâches, le message « Les vérifications sont désactivées, aucune tâche ne peut donc arriver pour le moment. » s’affiche. Sur une Machine hébergée, appuyez sur **Activer les vérifications**. Sur votre propre ordinateur, exécutez `./install.sh --activate`.

## Limite de votre modèle

Pour garder de la marge pour vos propres chats, les vérifications s’interrompent lorsque votre forfait d’IA atteint environ 65 % de sa limite sur 5 h et 90 % de sa limite hebdomadaire. Si vous disposez d’un modèle de secours associé à un autre forfait, les vérifications n’attendent pas. Consultez [Modèle](model.md).

Pendant l’attente, le haut du tableau de bord indique jusqu’à quand, par exemple : « Les vérifications attendent jusqu’à 07:15 pour préserver votre quota hebdomadaire ChatGPT. » **Vérifier maintenant** en lance une quand même. Dans **Paramètres**, **Modèle** affiche vos limites.

Rien n’est perdu : les nouveaux messages sont vérifiés dès que possible.

## La nuit

De 00:00 à 06:30, les vérifications sont en pause et les nouveaux messages attendent. Ils sont vérifiés ensemble à 06:30, avant votre résumé du matin. **Vérifications** affiche « En pause pour la nuit, rattrapage à 06:30 ». Utilisez l’app, écrivez dans le chat ou appuyez sur une tâche pour relancer les vérifications. Elles continuent jusqu’à ce que vous soyez inactif pendant une heure. **Vérifier maintenant** lance une vérification immédiatement.

## Une exécution a échoué

**Exécutions récentes**, dans **Connexions**, puis **Vérifications**, affiche chaque exécution. En cas d’échec, une nouvelle tentative est lancée automatiquement.

Une exécution arrêtée à cause de la limite d’utilisation de votre forfait d’IA affiche **La limite d’utilisation de l’IA a été atteinte.** ainsi que la date et l’heure de réinitialisation. Il s’agit d’une pause, pas d’un échec : les messages attendent et seront vérifiés après la réinitialisation. Rien n’est envoyé aux [rapports d’erreur](error-reports.md).

## Mis de côté

Lorsqu’une vérification écarte deux fois un message, celui-ci est mis de côté. **Connexions**, **Vérifications** indique combien il y en a, et **Mis de côté** les répertorie. Un message d’une personne qui vous écrit, d’une connaissance ou d’un client est examiné une dernière fois environ 3 jours après son arrivée. Ce nouvel examen crée une tâche ou clôt le message. Ce que vous avez écarté ou mis en attente le reste.
