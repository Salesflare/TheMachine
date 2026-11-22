---
title: Rapports d’erreur
area: security
summary: Quand quelque chose ne fonctionne pas, votre Machine indique à l’équipe de The Machine ce qui a échoué et où dans le code. Jamais le contenu de vos messages, ni vos noms ou adresses.
covers: error-reports
code: error_feed.py, error_words.py, pacing.py, dashboard.html, sw.js
order: 4
translated: e1d4d602255cde39
---
## De quoi s’agit-il

Quand quelque chose ne fonctionne pas dans The Machine, votre Machine envoie à notre équipe une courte note anonyme sur l’erreur, afin que nous puissions la corriger avant que quelqu’un ne la signale. Cette option est activée par défaut et nécessite [The Machine Network](/network).

## Données envoyées

Uniquement les éléments suivants, pour chaque type d’erreur :

- le type d’erreur, comme `KeyError` ;
- son message, après suppression de tout élément spécifique : nombres, identifiants, texte entre guillemets, adresses e-mail, liens, chemins de fichiers, clés et tout mot pouvant être un nom ;
- l’endroit où l’erreur s’est produite dans le code de The Machine, jamais dans un dossier de votre ordinateur ;
- la version de l’application, le nombre de fois où l’erreur s’est produite, ainsi que la date de sa première et de sa dernière occurrence.

Par exemple : `IndexError`, `list index out of range`, à `machine/faults.py:fault_event:246`, version `05b17ee6ac79`, 1 fois.

## Ce qui n’est jamais envoyé

Le contenu de vos messages, tâches, brouillons ou chats. Les noms, adresses e-mail, numéros de téléphone, liens ou mots de passe. Le compte ou la personne concernés.

## Origine des erreurs

- les tâches en arrière-plan : vérification des nouveaux messages, préparation des tâches, chats, connexions et synchronisations ;
- le tableau de bord, dans votre navigateur ou l’application, y compris les erreurs qui s’y affichent ;
- les requêtes du tableau de bord qui échouent ou expirent : lesquelles, jamais leur contenu ;
- les tâches d’agent de programmation qui échouent : uniquement l’outil et le type d’échec ;
- le bref test de votre IA en cas d’échec : l’erreur de l’IA, après suppression de tout élément spécifique.

Une vérification interrompue parce que votre forfait IA a atteint sa limite d’utilisation n’est pas une erreur et n’est pas envoyée : elle attend la réinitialisation de la limite.

Un connecteur que vous avez ajouté vous-même (votre propre fichier dans `connectors/`) n’envoie que le nom de son service et le libellé de son erreur, comme `notes` et `notes_http: HTTP unauthorized`, afin que nous puissions vous aider à la corriger. Rien d’autre de son code n’est envoyé. Sa fiche de connexion affiche l’erreur complète.

Les occurrences répétées d’une même erreur sont comptées, mais ne sont pas renvoyées. Un seul lot peut être envoyé toutes les 10 minutes au maximum. Nous les conservons pendant 30 jours.

## Gestion du rythme

Les tâches en arrière-plan sont mises en pause lorsque les limites de votre forfait IA sont presque atteintes, afin de laisser de la place à vos propres chats (voir [Votre modèle d’IA](model.md)).

Lorsque les rapports d’erreur sont activés, votre Machine nous indique aussi une fois par jour à quelle fréquence cela s’est produit : pour chaque pause, l’heure, la limite concernée, la durée et le nombre de tâches en attente. Rien sur le contenu de ces tâches.

## Désactiver les rapports

Dans **Paramètres**, **Sécurité**, désactivez **Envoyer des rapports d’erreur**. Plus rien n’est enregistré ni envoyé, et les rapports en attente sont supprimés. Les erreurs restent visibles sur votre Machine, qui peut proposer une solution.

Voir [Sécurité et confidentialité](security-and-privacy.md).
