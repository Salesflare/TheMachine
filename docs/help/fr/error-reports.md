---
title: Rapports d’erreur
area: security
summary: Quand quelque chose ne fonctionne pas, votre Machine indique à l’équipe The Machine ce qui a échoué et où dans le code. Jamais vos messages, noms ou adresses.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: fd3e1c2d68b93a35
---
## Qu’est-ce que c’est ?

Quand quelque chose ne fonctionne pas dans The Machine, votre Machine envoie à notre équipe une courte note anonyme sur l’erreur, pour que nous puissions la corriger avant que quelqu’un ne nous la signale. Cette option est activée par défaut et nécessite [The Machine Network](/network).

## Quelles données sont envoyées

Uniquement les informations suivantes, pour chaque type d’erreur :

- le type d’erreur, comme `KeyError` ;
- son message, après suppression de tout élément spécifique : nombres, identifiants, texte entre guillemets, adresses e-mail, liens, chemins d’accès aux fichiers, clés et tout mot pouvant être un nom ;
- l’endroit où l’erreur s’est produite dans le code de The Machine, jamais dans un dossier de votre ordinateur ;
- la version de l’application, le nombre de fois où l’erreur s’est produite, et les dates de sa première et de sa dernière occurrence.

Voici un exemple réel : `IndexError`, `list index out of range`, à `assistant.py:fault_event:7899`, version `05b17ee6ac79`, 1 fois.

## Quelles données ne sont jamais envoyées

Le contenu de vos messages, tâches, brouillons ou chats. Vos noms, adresses e-mail, numéros de téléphone, liens ou mots de passe. Le compte ou la personne concernée.

## D’où viennent les erreurs

- des tâches en arrière-plan : vérification des nouveaux messages, préparation des tâches, chats, connexions et synchronisations ;
- du tableau de bord, dans votre navigateur ou l’application, y compris les erreurs qui s’y affichent ;
- des requêtes du tableau de bord qui échouent ou expirent : lesquelles, jamais leur contenu ;
- des tâches des agents de programmation qui échouent : uniquement l’outil et le type d’échec.

Les répétitions d’une même erreur sont comptabilisées, mais ne sont pas renvoyées. Au maximum, un lot est envoyé toutes les 10 minutes. Nous les conservons pendant 30 jours.

## Limiter les tâches en arrière-plan

Les tâches en arrière-plan sont mises en pause lorsque les limites de votre forfait d’IA sont presque atteintes, afin de laisser de la place à vos propres chats (voir [Votre modèle d’IA](model.md)).

Lorsque les rapports d’erreur sont activés, votre Machine nous indique aussi une fois par jour à quelle fréquence cela s’est produit : pour chaque pause, l’heure, la limite concernée, sa durée et le nombre de tâches mises en attente. Aucune information sur le contenu des tâches.

## Désactiver les rapports

Dans **Paramètres**, **Sécurité**, désactivez **Envoyer des rapports d’erreur**. Plus rien n’est enregistré ni envoyé, et les données en attente sont supprimées. Les erreurs continuent de s’afficher sur votre Machine, qui peut proposer une solution.

Voir [Sécurité et confidentialité](security-and-privacy.md).
