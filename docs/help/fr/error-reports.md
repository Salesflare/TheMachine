---
title: Rapports d’erreur
area: security
summary: En cas de problème, votre Machine indique à l’équipe de The Machine ce qui a échoué et où dans le code. Elle ne transmet jamais vos messages, noms ou adresses.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: 2253a0d695fe898c
---
## De quoi s’agit-il ?

Quand un problème survient dans The Machine, votre Machine envoie à notre équipe une courte note anonyme sur l’erreur, pour que nous puissions la corriger avant que quelqu’un ne la signale. Cette option est activée par défaut et nécessite [The Machine Network](/network).

## Données envoyées

Uniquement les éléments suivants, pour chaque type d’erreur :

- le type d’erreur, comme `KeyError` ;
- son message, expurgé de toute donnée spécifique : nombres, identifiants, texte entre guillemets, adresses e-mail, liens, chemins de fichiers, clés et tout mot pouvant être un nom ;
- l’emplacement dans le code de The Machine où l’erreur s’est produite, jamais un dossier sur votre ordinateur ;
- la version de l’app, le nombre d’occurrences et les dates de première et de dernière occurrence.

Par exemple : `IndexError`, `list index out of range`, à `machine/faults.py:fault_event:246`, version `05b17ee6ac79`, 1 fois.

## Ce qui n’est jamais envoyé

Le contenu de vos messages, tâches, brouillons ou chats. Les noms, adresses e-mail, numéros de téléphone, liens ou mots de passe. Le compte ou la personne concernés.

## D’où viennent les erreurs

- les tâches en arrière-plan : vérification des nouveaux messages, préparation des tâches, chat, connexions et synchronisations ;
- le tableau de bord, dans votre navigateur ou l’app, y compris les erreurs affichées ;
- les requêtes du tableau de bord qui échouent ou expirent : lesquelles, jamais leur contenu ;
- les tâches d’agent de codage qui échouent : l’outil et le type d’échec uniquement ;
- le court test de votre IA en cas d’échec : l’erreur de l’IA, expurgée de toute donnée spécifique.

Un connecteur que vous avez ajouté vous-même (votre propre fichier dans `connectors/`) n’envoie que le nom de son service et le libellé de son erreur, comme `notes` et `notes_http: HTTP unauthorized`, pour que nous puissions vous aider à la corriger. Rien d’autre de son code. Sa carte de connexion affiche l’erreur complète.

Les erreurs qui se répètent sont comptabilisées, mais ne sont pas renvoyées. Au maximum, un lot est envoyé toutes les 10 minutes. Nous les conservons pendant 30 jours.

## Rythme d’envoi

Les tâches en arrière-plan se mettent en pause lorsque les limites de votre forfait d’IA sont presque atteintes, afin de laisser de la place pour vos chats (voir [Votre modèle d’IA](model.md)).

Lorsque les rapports d’erreur sont activés, votre Machine nous indique aussi une fois par jour la fréquence de ces pauses : pour chacune, l’heure, la limite concernée, sa durée et le nombre de tâches mises en attente. Rien sur la nature de ces tâches.

## Désactiver les rapports

Dans **Paramètres**, dans **Sécurité**, désactivez **Envoyer des rapports d’erreur**. Plus rien n’est enregistré ni envoyé, et les rapports en attente sont supprimés. Les erreurs restent visibles sur votre Machine, qui peut vous proposer une solution.

Voir [Sécurité et confidentialité](security-and-privacy.md).
