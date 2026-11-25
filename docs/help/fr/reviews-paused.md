---
title: Aucune nouvelle tâche
area: troubleshooting
summary: Les vérifications sont désactivées, en attente ou arrêtées à cause de la limite d’utilisation de votre modèle. Voici comment le savoir et quoi faire.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py
order: 3
translated: f0e9e4dc6c850b25
---
Les tâches viennent des vérifications : votre Machine examine ce qui est arrivé au cours des 15 dernières minutes environ.

## Vous venez de vous inscrire

Sur une nouvelle Machine hébergée, les vérifications démarrent automatiquement une fois votre IA et votre messagerie connectées. Pendant que votre Machine lit vos e-mails, la page Tâches affiche « Lecture de vos e-mails, premières tâches dans quelques minutes ». Une fois qu’elle connaît le volume à traiter, elle indique une estimation : « Premières tâches dans environ 10 min ». S’il manque une étape, **Vous attend** l’indique, par exemple **Connecter vos e-mails**, avec un lien vers cette étape.

Pendant la lecture, la page Tâches indique où elle en est (« 20 messages lus sur 132. Lecture des 40 suivants… »), quelques personnes et organisations qu’elle a trouvées, et votre première tâche dès qu’elle est prête. Le nombre indique les messages qu’elle a fini de lire. La barre continue de progresser pendant qu’elle lit les suivants. Les noms viennent de vos e-mails et vous seul les voyez.

Si la première analyse ne trouve rien pour vous, elle indique ce qu’elle a lu et propose les prochaines étapes, par exemple connecter un service qui vous envoie souvent des e-mails ou demander ce qui a changé cette semaine.

## Les vérifications sont désactivées

En haut de la page Tâches, le message « Les vérifications sont désactivées. Aucune tâche ne vous parviendra pour le moment. » s’affiche. Sur une Machine hébergée, appuyez sur **Activer les vérifications**. Sur votre ordinateur, exécutez `./install.sh --activate`.

## Limite de votre modèle

Pour garder de la marge pour vos propres chats, les vérifications se mettent en pause lorsque vous atteignez environ 65 % de la limite de 5 heures de votre forfait d’IA et 90 % de sa limite hebdomadaire. Si vous avez un modèle de secours associé à un autre forfait, les vérifications n’attendent pas. Consultez [Modèle](model.md).

Pendant l’attente, le haut du tableau de bord indique jusqu’à quand, par exemple : « Les vérifications attendent jusqu’à 07:15 pour préserver votre quota hebdomadaire ChatGPT. » **Vérifier maintenant** lance quand même une vérification. Vos limites sont indiquées dans **Paramètres**, **Modèle**.

Rien n’est perdu : les nouveaux éléments sont vérifiés dès que possible. Après une longue attente, les messages récents de personnes sont traités en premier, et chaque vérification traite aussi une partie des plus anciens.

## La nuit

De 00:00 à 06:30, les vérifications sont en pause et les nouveaux messages attendent. Ils sont vérifiés ensemble à 06:30, avant votre résumé du matin. **Vérifications** indique « En pause pour la nuit, rattrapage à 06:30 ». Utilisez l’application, écrivez dans le chat ou appuyez sur une tâche pour relancer les vérifications. Elles continuent jusqu’à ce que vous soyez resté inactif pendant une heure. **Vérifier maintenant** lance une vérification immédiatement.

## Une exécution a échoué

**Exécutions récentes**, sous **Connexions**, **Vérifications**, affiche chaque exécution. En cas d’échec, une nouvelle tentative est lancée automatiquement.

Une exécution arrêtée à cause de la limite d’utilisation de votre forfait d’IA affiche **La limite d’utilisation de l’IA a été atteinte.** et indique quand elle sera réinitialisée. Il s’agit d’une pause, pas d’un échec : les messages attendent et seront vérifiés après la réinitialisation. Rien n’est envoyé aux [rapports d’erreur](error-reports.md).

## Mis de côté

Quand une vérification écarte deux fois un message, celui-ci est mis de côté. **Connexions**, **Vérifications** indique combien il y en a, et **Mis de côté** les répertorie. Un message envoyé par une personne qui vous écrit, une connaissance ou un client est vérifié une dernière fois environ 3 jours après sa réception. Cette vérification crée une tâche ou clôt le message. Les messages que vous avez marqués comme inutiles ou mis en attente le restent.
