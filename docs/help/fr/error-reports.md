---
title: Rapports d’erreur
area: security
summary: Quand un problème survient, votre Machine indique à l’équipe de The Machine ce qui a échoué et où dans le code. Jamais le contenu de vos messages, vos noms ou vos adresses.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: f67d18a44999cfce
---
## De quoi s’agit-il

Quand un problème survient dans The Machine, votre Machine envoie à notre équipe une courte note anonyme sur l’erreur, pour que nous puissions la corriger avant que quelqu’un nous la signale. Cette option est activée par défaut et nécessite [The Machine Network](/network).

## Données envoyées

Uniquement les éléments suivants, pour chaque type d’erreur :

- le type d’erreur, par exemple `KeyError` ;
- son message, après suppression de tout élément précis : nombres, identifiants, texte entre guillemets, adresses e-mail, liens, chemins d’accès aux fichiers, clés et tout mot pouvant être un nom ;
- l’endroit où l’erreur s’est produite dans le code de The Machine, jamais un dossier de votre ordinateur ;
- la version de l’application, le nombre d’occurrences, ainsi que les dates de la première et de la dernière occurrence.

Par exemple : `IndexError`, `list index out of range`, à `machine/faults.py:fault_event:246`, version `05b17ee6ac79`, 1 fois.

## Données jamais envoyées

Le contenu de vos messages, tâches, brouillons ou chats. Les noms, adresses e-mail, numéros de téléphone, liens ou mots de passe. Le compte ou la personne concernée.

## Origine des erreurs

- les tâches en arrière-plan : vérification des nouveaux messages, préparation des tâches, chats, connexions et synchronisations ;
- le tableau de bord, dans votre navigateur ou l’application, y compris les erreurs affichées ;
- les requêtes du tableau de bord qui échouent ou expirent : lesquelles, jamais leur contenu ;
- les tâches des agents de programmation qui échouent : uniquement l’outil et le type d’échec ;
- le bref test de votre IA en cas d’échec : l’erreur de l’IA, après suppression de tout élément précis.

Un connecteur que vous avez ajouté vous-même (votre propre fichier dans `connectors/`) n’envoie jamais ses erreurs. Elles s’affichent sur sa fiche de connexion.

Les répétitions d’une même erreur sont comptabilisées, mais ne sont pas envoyées à nouveau. Au maximum, un lot est envoyé toutes les 10 minutes. Nous les conservons pendant 30 jours.

## Limiter l’activité

Les tâches en arrière-plan sont mises en pause quand les limites de votre forfait IA sont presque atteintes, afin de laisser de la place à vos propres chats (voir [Votre modèle d’IA](model.md)).

Lorsque les rapports d’erreur sont activés, votre Machine nous indique aussi une fois par jour à quelle fréquence cela s’est produit : pour chaque pause, l’heure, la limite concernée, la durée et le nombre de tâches mises en attente. Rien sur le contenu des tâches.

## Désactiver les rapports

Dans **Paramètres**, **Sécurité**, désactivez **Envoyer des rapports d’erreur**. Rien d’autre n’est enregistré ni envoyé, et les rapports en attente sont supprimés. Les erreurs continuent de s’afficher sur votre Machine, qui peut proposer une solution.

Voir [Sécurité et confidentialité](security-and-privacy.md).
