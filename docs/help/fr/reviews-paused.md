---
title: Aucune nouvelle tâche
area: troubleshooting
summary: Les vérifications sont désactivées, en attente ou arrêtées parce que votre modèle a atteint sa limite d’utilisation. Voici comment le savoir et quoi faire.
covers: 
code: dashboard.html, assistant.py
order: 3
translated: d265e540d9ecef0e
---
Les tâches viennent des vérifications : votre Machine examine ce qui est arrivé au cours des 15 dernières minutes environ.

## Vous venez de vous inscrire

Sur une nouvelle Machine hébergée, les vérifications démarrent automatiquement une fois votre IA et vos e-mails connectés. Pendant que votre Machine lit vos e-mails, la page Tâches affiche « Lecture de vos e-mails, premières tâches dans quelques minutes. » Une fois qu’elle sait quelle quantité il y a à lire, elle indique un délai approximatif : « Premières tâches dans environ 10 min. » S’il manque une étape, **Vous attend** l’indique, par exemple **Connecter vos e-mails**, avec un lien vers cette étape.

Pendant la lecture, la page Tâches indique sa progression (« 20 messages lus sur 132. Lecture des 40 suivants… »), quelques personnes et organisations repérées, ainsi que votre première tâche dès qu’elle est prête. Le nombre correspond aux messages dont la lecture est terminée ; la barre continue d’avancer pendant la lecture des suivants. Les noms viennent de vos propres e-mails et vous seul les voyez.

Si la première vérification ne trouve rien pour vous, elle indique ce qu’elle a lu et propose les prochaines étapes, comme connecter un service qui vous envoie souvent des e-mails ou demander ce qui a changé cette semaine.

## Les vérifications sont désactivées

En haut de la page Tâches, le message « Les vérifications sont désactivées, aucune tâche ne vous parvient pour le moment. » s’affiche. Sur une Machine hébergée, appuyez sur **Activer les vérifications**. Sur votre ordinateur, exécutez `./install.sh --activate`.

## La limite de votre modèle

Pour vous laisser de la marge pour vos propres chats, les vérifications se mettent en pause à environ 65 % de la limite sur 5 heures de votre forfait d’IA et à 90 % de sa limite hebdomadaire. Si vous avez un modèle de secours associé à un autre forfait, les vérifications ne se mettent pas en attente. Consultez [Modèle](model.md).

Pendant l’attente des vérifications, le haut du tableau de bord indique jusqu’à quand, par exemple : « Les vérifications sont en attente jusqu’à 07:15 pour préserver votre quota hebdomadaire ChatGPT. » **Vérifier maintenant** en lance une malgré tout. Dans **Paramètres**, **Modèle** affiche vos limites.

Rien n’est perdu : les éléments reçus sont vérifiés dès que possible.

## La nuit

De 00:00 à 06:30, les vérifications sont en pause et les nouveaux messages attendent. Ils sont vérifiés ensemble à 06:30, avant votre résumé du matin. **Vérifications** affiche « En pause pour la nuit, rattrapage à 06:30 ». Utilisez l’application, écrivez dans le chat ou touchez une tâche pour relancer les vérifications. Elles continueront jusqu’à une heure d’inactivité. **Vérifier maintenant** lance une vérification immédiatement.

## Une exécution a échoué

**Exécutions récentes**, sous **Connexions**, **Vérifications**, affiche chaque exécution. Une exécution ayant échoué est automatiquement relancée.

## Mis de côté

Lorsqu’une vérification met un message en attente deux fois, il est mis de côté. **Connexions**, **Vérifications** indique combien de messages sont concernés, et **Mis de côté** les répertorie. Un message d’une personne qui vous écrit, d’une connaissance ou d’un client est examiné une fois de plus environ 3 jours après son arrivée. Cette vérification crée une tâche ou clôt le message. Ce que vous avez marqué comme inutile ou mis en attente le reste.
