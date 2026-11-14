---
title: Rapports d’erreur
area: security
summary: En cas de problème, votre Machine indique à l’équipe The Machine ce qui a échoué et où dans le code. Jamais le contenu de vos messages, ni vos noms ou adresses.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: 03a8649f2f634b59
---
## De quoi s’agit-il

Quand un problème survient dans The Machine, votre Machine envoie à notre équipe une courte note anonyme sur l’erreur, afin que nous puissions la corriger avant que quelqu’un ne la signale. Cette option est activée par défaut et nécessite [The Machine Network](/network).

## Données envoyées

Uniquement les éléments suivants, pour chaque type d’erreur :

- le type d’erreur, comme `KeyError` ;
- son message, après suppression de tout élément spécifique : nombres, identifiants, texte cité, adresses e-mail, liens, chemins d’accès aux fichiers, clés et tout mot susceptible d’être un nom ;
- l’endroit où l’erreur s’est produite dans le code de The Machine, jamais dans un dossier de votre ordinateur ;
- la version de l’application, le nombre d’occurrences, ainsi que la date de la première et de la dernière occurrence.

Par exemple : `IndexError`, `list index out of range`, à `machine/faults.py:fault_event:246`, version `05b17ee6ac79`, 1 fois.

## Ce qui n’est jamais envoyé

Le contenu de vos messages, tâches, brouillons ou chats. Les noms, adresses e-mail, numéros de téléphone, liens ou mots de passe. Le compte ou la personne concernés.

## Origine des erreurs

- les tâches en arrière-plan : vérification des nouveaux messages, préparation des tâches, chats, connexions et synchronisations ;
- le tableau de bord, dans votre navigateur ou l’application, y compris les erreurs qui s’y affichent ;
- les requêtes du tableau de bord qui échouent ou expirent : lesquelles, jamais ce qu’elles ont envoyé ;
- les tâches des agents de programmation qui échouent : uniquement l’outil et le type d’échec.

Les occurrences répétées d’une même erreur sont comptabilisées, mais ne sont pas renvoyées. Au maximum, un lot est envoyé toutes les 10 minutes. Nous les conservons pendant 30 jours.

## Rythme d’envoi

Les tâches en arrière-plan sont mises en pause lorsque les limites de votre forfait IA sont presque atteintes, afin de laisser de la place à vos propres chats (voir [Votre modèle d’IA](model.md)).

Lorsque les rapports d’erreur sont activés, votre Machine nous indique aussi une fois par jour à quelle fréquence cela s’est produit : pour chaque pause, l’heure, la limite concernée, sa durée et le nombre de tâches mises en attente. Rien sur la nature des tâches.

## Désactiver cette option

Dans **Paramètres**, sous **Sécurité**, désactivez **Envoyer des rapports d’erreur**. Plus rien n’est enregistré ni envoyé, et les éléments en attente sont supprimés. Les erreurs restent visibles sur votre Machine, qui peut vous proposer une solution.

Voir [Sécurité et confidentialité](security-and-privacy.md).
