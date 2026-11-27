---
title: Aucune nouvelle tâche
area: troubleshooting
summary: Les vérifications sont désactivées, en attente ou arrêtées à cause de la limite d’utilisation de votre modèle. Comment le savoir et quoi faire.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py, machine/app/ahead_hold.py
order: 3
translated: d8a15909ab8164e8
---
Les tâches viennent des vérifications : votre Machine examine les nouveaux messages reçus depuis environ 15 minutes.

## Vous venez de vous inscrire

Sur une nouvelle Machine hébergée, les vérifications démarrent automatiquement une fois votre IA et vos e-mails connectés. Pendant que votre Machine lit vos e-mails, la section Tâches affiche « Lecture de vos e-mails, premières tâches dans quelques minutes ». Une fois qu’elle sait quelle quantité de messages traiter, elle indique une durée approximative : « Premières tâches dans environ 10 min ». S’il manque une étape, **Vous attend** vous l’indique, par exemple **Connecter vos e-mails**, avec un lien vers cette étape.

Pendant la lecture, la section Tâches indique où elle en est (« 20 messages sur 132 lus. Lecture des 40 suivants… »), quelques personnes et organisations repérées, ainsi que votre première tâche dès qu’elle est prête. Le nombre correspond aux messages dont la lecture est terminée ; la barre continue d’avancer pendant la lecture des suivants. Les noms proviennent de vos e-mails, et vous seul les voyez.

Si la première analyse ne trouve rien pour vous, elle indique ce qu’elle a lu et propose des étapes suivantes, comme connecter un service qui vous envoie souvent des e-mails ou demander ce qui a changé cette semaine.

## Les vérifications sont désactivées

En haut de la section Tâches, le message « Les vérifications sont désactivées, aucune tâche ne sera donc créée pour le moment » s’affiche. Sur une Machine hébergée, appuyez sur **Activer les vérifications**. Sur votre ordinateur, exécutez `./install.sh --activate`.

## La limite de votre modèle

Pour laisser de la marge à vos propres chats, les vérifications se mettent en pause à environ 65 % de la limite sur 5 h de votre forfait IA et à 90 % de sa limite hebdomadaire. Si vous avez un modèle de secours avec un autre forfait, les vérifications n’attendent pas. Consultez [Modèle](model.md).

Pendant l’attente des vérifications, le haut du tableau de bord indique jusqu’à quand elles sont en pause, par exemple « Les vérifications attendent jusqu’à 07:15 pour préserver votre quota hebdomadaire ChatGPT ». **Vérifier maintenant** en lance une quand même. Dans **Paramètres**, **Modèle** affiche vos limites.

Rien n’est perdu : les nouveaux messages sont vérifiés dès que possible. Après une longue attente, les messages récents de personnes sont traités en premier, et chaque vérification traite aussi une partie des plus anciens.

Tant que le rattrapage n’est pas terminé, les nouvelles tâches arrivent sans brouillon, afin que votre forfait soit d’abord consacré à vos messages. Les brouillons suivent ensuite, sans retarder les tâches urgentes. Appuyez sur **Faire** pour en obtenir une tout de suite.

## La nuit

De 00:00 à 06:30, les vérifications sont en pause et les nouveaux messages attendent. Ils sont vérifiés ensemble à 06:30, avant votre récapitulatif du matin. **Vérifications** affiche « En pause pour la nuit, rattrapage à 06:30 ». Utilisez l’application, écrivez dans le chat ou appuyez sur une tâche pour relancer les vérifications. Elles continuent jusqu’à ce que vous soyez absent depuis une heure. **Vérifier maintenant** lance une vérification immédiatement.

## Une exécution a échoué

**Exécutions récentes**, sous **Connexions**, **Vérifications**, affiche chaque exécution. En cas d’échec, la vérification est relancée automatiquement. Si votre IA cesse de répondre, par exemple parce que votre session a expiré, reconnectez-vous dans **Paramètres**, **Modèle** : les vérifications reprennent aussitôt.

Une exécution interrompue parce que la limite d’utilisation de votre forfait IA a été atteinte affiche **La limite d’utilisation de l’IA a été atteinte.** ainsi que l’heure à laquelle elle sera réinitialisée. Il s’agit d’une pause, pas d’un échec : les messages attendent et sont vérifiés après la réinitialisation. Rien n’est envoyé aux [rapports d’erreur](error-reports.md).

## Mis de côté

Quand une vérification met un message de côté deux fois, il est mis de côté. **Connexions**, **Vérifications** indique leur nombre, et **Mis de côté** les répertorie.

Un message qui fait échouer chaque vérification alors que votre IA fonctionne est mis de côté de la même manière, afin que les autres messages soient vérifiés.

Un message envoyé par une personne, une connaissance ou un client est réexaminé environ 3 jours après son arrivée. Ce nouvel examen crée une tâche ou clôt le message. Ce que vous avez écarté ou mis en attente le reste.
