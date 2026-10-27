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

Le haut des Suggestions indique « Les revues sont désactivées, donc aucune suggestion n’arrive encore. » Sur une Machine hébergée, appuyez sur **Activer les revues**. Sur votre propre ordinateur, lancez `./install.sh --activate`.

## La limite de votre modèle

Les revues se mettent en pause à environ 65 % de la limite sur 5 heures de votre forfait et répartissent la limite hebdomadaire, pour garder de la marge pour vos propres chats. Quand une limite est atteinte, le haut du tableau de bord indique laquelle et quand elle se réinitialise. **Connexions**, puis **Revues**, l’affiche à côté de l’exécution. **Paramètres**, **Modèle** affiche vos limites. Voir [Modèle](model.md).

Rien n’est perdu pendant l’attente : ce qui est arrivé est passé en revue dès que possible.

## Une exécution a échoué

**Exécutions récentes** sous **Revues** affiche chaque exécution. Un lot échoué est relancé automatiquement.
