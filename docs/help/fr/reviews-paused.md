---
title: Aucune nouvelle tâche
area: troubleshooting
summary: Les vérifications sont désactivées, en attente ou arrêtées parce que votre modèle a atteint sa limite d’utilisation. Voici comment le savoir et quoi faire.
covers:
code: dashboard.html, assistant.py, machine/app/review.py, machine/night_pause.py, model_budget.py, machine/app/ahead_hold.py
order: 3
translated: 40617b8ac692660b
---
Les tâches viennent des vérifications : votre Machine examine ce qui est arrivé depuis environ 15 minutes.

## Vous venez de vous inscrire

Sur une nouvelle Machine hébergée, les vérifications démarrent automatiquement une fois votre IA et vos e-mails connectés. Pendant que votre Machine lit vos e-mails, la section Tâches indique « Lecture de vos e-mails, premières tâches dans quelques minutes ». Une fois qu’elle sait quelle quantité de messages traiter, elle donne une estimation, par exemple : « Premières tâches dans environ 10 min ». Si une étape manque, **Vous attend** vous indique laquelle, par exemple **Connecter vos e-mails**, avec un lien vers cette étape.

Pendant la lecture, la section Tâches indique sa progression (« 20 messages lus sur 132. Lecture des 40 suivants… »), quelques personnes et organisations trouvées, et affiche votre première tâche dès qu’elle est prête. Le nombre correspond aux messages dont la lecture est terminée. La barre continue d’avancer pendant la lecture des suivants. Les noms proviennent de vos e-mails et vous seul les voyez.

Si la première vérification ne trouve rien pour vous, elle indique ce qu’elle a lu et propose des étapes suivantes, comme connecter un service qui vous envoie souvent des e-mails ou demander ce qui a changé cette semaine.

## Les vérifications sont désactivées

En haut de la section Tâches, le message « Les vérifications sont désactivées, aucune tâche ne peut donc arriver pour le moment » s’affiche. Sur une Machine hébergée, appuyez sur **Activer les vérifications**. Sur votre ordinateur, exécutez `./install.sh --activate`.

## Limite de votre modèle

Pour garder de la marge pour vos propres chats, les vérifications se mettent en pause lorsque votre forfait IA atteint environ 65 % de sa limite sur 5 heures et 90 % de sa limite hebdomadaire. Avec un modèle de secours associé à un autre forfait, les vérifications n’attendent pas. Consultez [Modèle](model.md).

Pendant l’attente, le haut du tableau de bord indique jusqu’à quand, par exemple : « Les vérifications attendent jusqu’à 07:15 pour préserver votre quota ChatGPT de la semaine ». **Vérifier maintenant** en lance une malgré tout. Dans **Paramètres**, **Modèle** affiche vos limites.

Rien n’est perdu : les messages reçus sont vérifiés dès que possible. Après une longue attente, les messages récents de personnes passent en premier, et chaque vérification traite aussi une partie des plus anciens.

En attendant d’avoir rattrapé son retard, votre assistante crée les nouvelles tâches sans brouillon, pour que votre forfait serve d’abord à traiter vos messages. Les brouillons arrivent ensuite, et les tâches urgentes n’attendent pas. Appuyez sur **Faire** pour en obtenir une tout de suite.

## La nuit

De 00:00 à 06:30, les vérifications sont en pause et les nouveaux messages attendent. Ils sont vérifiés ensemble à 06:30, avant votre récapitulatif du matin. **Vérifications** indique « En pause pour la nuit, rattrapage à 06:30 ». Utilisez l’application, écrivez dans le chat ou appuyez sur une tâche pour relancer les vérifications. Elles continuent jusqu’à ce que vous soyez absent depuis une heure. **Vérifier maintenant** lance une vérification tout de suite.

## Une exécution a échoué

**Exécutions récentes**, sous **Connexions**, **Vérifications**, affiche chaque exécution. Une exécution échouée est automatiquement relancée.

Une exécution arrêtée parce que votre forfait IA a atteint sa limite d’utilisation indique **La limite d’utilisation de l’IA a été atteinte.** ainsi que l’heure à laquelle elle sera levée. Il s’agit d’une pause, pas d’un échec : les messages attendent et seront vérifiés après la réinitialisation. Rien n’est envoyé aux [rapports d’erreur](error-reports.md).

## Mis de côté

Lorsqu’une vérification met un message de côté deux fois, il est mis de côté. **Connexions**, **Vérifications** indique combien il y en a, et **Mis de côté** les répertorie. Un message envoyé par une personne qui vous écrit, une connaissance ou un client est réexaminé environ 3 jours après son arrivée. Cette vérification crée une tâche ou clôt le message. Ce que vous avez écarté ou mis en attente reste ainsi.
