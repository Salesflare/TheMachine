---
title: Aucune nouvelle tâche
area: troubleshooting
summary: Les revues sont désactivées, en attente, ou arrêtées par la limite d’utilisation de votre modèle. Comment le savoir et quoi faire.
covers: 
code: dashboard.html, assistant.py
order: 3
---
Les tâches viennent des revues : votre Machine lit ce qui est arrivé, par petits lots, en une heure environ.

## Les revues sont désactivées

Le haut de Tâches indique « Les revues sont désactivées, donc aucune tâche n’arrive pour l’instant. » Sur une Machine hébergée, appuyez sur **Activer les revues**. Sur votre propre ordinateur, lancez `./install.sh --activate`.

## La limite de votre modèle

Les revues de ce qui est arrivé se mettent en pause à environ 65 % de la limite sur 5 heures de votre forfait et à 90 % de sa limite hebdomadaire, pour garder de la marge pour vos propres chats. Un tableau qui parcourt votre historique avance plus lentement, à environ un septième de la semaine par jour. Avec un modèle de secours qui fonctionne, sur un autre forfait ou fournisseur, les revues n’attendent pas. Voir [Modèle](model.md).

Pendant que les revues attendent, le haut du tableau de bord indique jusqu’à quand, par exemple « Les revues attendent jusqu’à 07:15 pour ménager votre semaine ChatGPT. » **Lancer la revue** en démarre une tout de suite. Quand une limite est atteinte, le haut du tableau de bord indique laquelle et quand elle se réinitialise. **Connexions**, puis **Revues**, l’affiche à côté de l’exécution. **Paramètres**, **Modèle** affiche vos limites. Voir [Modèle](model.md).

Rien n’est perdu pendant l’attente : ce qui est arrivé est passé en revue dès que possible.

## Une exécution a échoué

**Exécutions récentes** sous **Revues** affiche chaque exécution. Un lot échoué est relancé automatiquement.
