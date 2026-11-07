---
title: Aucune nouvelle tâche
area: troubleshooting
summary: Les vérifications sont désactivées, en attente, ou arrêtées par la limite d’utilisation de votre modèle. Comment le savoir et quoi faire.
covers: 
code: dashboard.html, assistant.py
order: 3
---
Les tâches viennent des vérifications : votre Machine lit ce qui est arrivé, par petits lots, en 15 minutes environ.

## Tout juste inscrit

Sur une nouvelle Machine hébergée, les vérifications démarrent d’elles-mêmes dès que votre IA et vos e-mails sont connectés. Pendant que votre Machine lit vos e-mails, Tâches affiche "Lecture de vos e-mails, premières tâches dans quelques minutes". S’il manque une étape, **Vous attend** la nomme, comme **Connecter vos e-mails**, avec un lien vers cette étape.

Pendant qu’elle lit, Tâches montre où elle en est, quelques-unes des personnes et organisations qu’elle a croisées, et votre première tâche dès qu’elle arrive. Les noms viennent de vos propres e-mails et ne sont visibles que par vous.

## Les vérifications sont désactivées

Le haut de Tâches indique « Les vérifications sont désactivées, donc aucune tâche n’arrive pour l’instant. » Sur une Machine hébergée, appuyez sur **Activer les vérifications**. Sur votre propre ordinateur, lancez `./install.sh --activate`.

## La limite de votre modèle

Les vérifications de ce qui est arrivé se mettent en pause à environ 65 % de la limite sur 5 heures de votre forfait et à 90 % de sa limite hebdomadaire, pour garder de la marge pour vos propres chats. Un tableau qui parcourt votre historique avance plus lentement, à environ un septième de la semaine par jour. Avec un modèle de secours qui fonctionne, sur un autre forfait ou fournisseur, les vérifications n’attendent pas. Voir [Modèle](model.md).

Pendant que les vérifications attendent, le haut du tableau de bord indique jusqu’à quand, par exemple « Les vérifications attendent jusqu’à 07:15 pour ménager votre semaine ChatGPT. » **Vérifier maintenant** en démarre une tout de suite. Quand une limite est atteinte, le haut du tableau de bord indique laquelle et quand elle se réinitialise. **Connexions**, puis **Vérifications**, l’affiche à côté de l’exécution. **Paramètres**, **Modèle** affiche vos limites. Voir [Modèle](model.md).

Rien n’est perdu pendant l’attente : ce qui est arrivé est vérifié dès que possible.

## Une exécution a échoué

**Exécutions récentes** sous **Vérifications** affiche chaque exécution. Un lot échoué est relancé automatiquement.
