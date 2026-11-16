---
title: Rapports d’erreur
area: security
summary: Quand quelque chose ne fonctionne pas, votre Machine indique à l’équipe de The Machine ce qui a échoué et où dans le code. Jamais vos messages, noms ou adresses.
covers: error-reports
code: error_feed.py, pacing.py, dashboard.html, sw.js
order: 4
translated: 4dc53a854d15f1a3
---
## De quoi s’agit-il

Quand quelque chose ne fonctionne pas dans The Machine, votre Machine envoie à notre équipe une courte note anonyme sur l’erreur, pour que nous puissions la corriger avant que quelqu’un ne la signale. Cette option est activée par défaut et nécessite [The Machine Network](/network).

## Ce qui est envoyé

Uniquement les informations suivantes, pour chaque type d’erreur :

- le type d’erreur, par exemple `KeyError` ;
- le message, après suppression de toute information spécifique : nombres, identifiants, texte cité, adresses e-mail, liens, chemins de fichiers, clés et tout mot susceptible d’être un nom ;
- l’endroit où l’erreur s’est produite dans le code de The Machine, jamais dans un dossier de votre ordinateur ;
- la version de l’application, le nombre d’occurrences et les dates de la première et de la dernière occurrence.

Par exemple : `IndexError`, `list index out of range`, à `machine/faults.py:fault_event:246`, version `05b17ee6ac79`, 1 fois.

## Ce qui n’est jamais envoyé

Le contenu de vos messages, tâches, brouillons ou chats. Les noms, adresses e-mail, numéros de téléphone, liens ou mots de passe. Le compte ou la personne concernés.

## D’où viennent les erreurs

- le travail en arrière-plan : vérification des nouveaux messages, préparation des tâches, chats, connexions et synchronisations ;
- le tableau de bord, dans votre navigateur ou dans l’application, y compris les erreurs qui vous ont été affichées ;
- les requêtes du tableau de bord qui échouent ou expirent : lesquelles, jamais leur contenu ;
- les tâches d’agent de programmation qui échouent : uniquement l’outil et le type d’échec ;
- le bref test de votre IA en cas d’échec : l’erreur de l’IA, après suppression de toute information spécifique.

Les répétitions d’une même erreur sont comptabilisées et ne sont pas renvoyées. Un lot est envoyé au maximum toutes les 10 minutes. Nous les conservons pendant 30 jours.

## Limitation du travail

Le travail en arrière-plan est mis en pause lorsque les limites de votre forfait d’IA sont presque atteintes, afin de garder de la marge pour vos propres chats (voir [Votre modèle d’IA](model.md)).

Lorsque les rapports d’erreur sont activés, votre Machine nous indique aussi une fois par jour à quelle fréquence cela s’est produit : pour chaque pause, l’heure, la limite concernée, la durée et le nombre de tâches mises en attente. Rien sur la nature des tâches.

## Désactiver cette option

Dans **Paramètres**, **Sécurité**, désactivez **Envoyer des rapports d’erreur**. Plus rien n’est enregistré ni envoyé, et les éléments en attente sont supprimés. Les erreurs restent visibles sur votre Machine, qui peut proposer une solution.

Voir [Sécurité et confidentialité](security-and-privacy.md).
