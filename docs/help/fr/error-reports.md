---
title: Rapports d’erreur
area: security
summary: Quand quelque chose ne fonctionne pas, votre Machine indique à l’équipe The Machine ce qui a échoué et où dans le code. Jamais vos messages, vos noms ni vos adresses.
covers: error-reports
code: error_feed.py, error_words.py, pacing.py, dashboard.html, sw.js
order: 4
translated: d474cfa6bcefd25a
---
## De quoi s’agit-il ?

Quand quelque chose ne fonctionne pas dans The Machine, votre Machine envoie à notre équipe une courte note anonyme sur l’erreur, pour que nous puissions la corriger avant que quelqu’un ne la signale. Cette fonction est activée par défaut et nécessite [The Machine Network](/network).

## Ce qui est envoyé

Uniquement les éléments suivants, pour chaque type d’erreur :

- le type d’erreur, comme `KeyError` ;
- son message, après suppression de tout élément spécifique : nombres, identifiants, texte entre guillemets, adresses e-mail, liens, chemins de fichiers, clés et tout mot qui pourrait être un nom ;
- l’endroit où l’erreur s’est produite dans le code de The Machine, jamais dans un dossier de votre ordinateur ;
- la version de l’application, le nombre d’occurrences et les dates de la première et de la dernière occurrence.

Par exemple : `IndexError`, `list index out of range`, à `machine/faults.py:fault_event:246`, version `05b17ee6ac79`, 1 fois.

## Ce qui n’est jamais envoyé

Le contenu de vos messages, tâches, brouillons ou chats. Les noms, adresses e-mail, numéros de téléphone, liens ou mots de passe. Le compte ou la personne concernée.

## Origine des erreurs

- les tâches en arrière-plan : vérification des nouveaux messages, préparation des tâches, chats, connexions et synchronisations ;
- le tableau de bord, dans votre navigateur ou l’application, y compris les erreurs qui s’y affichent ;
- les requêtes du tableau de bord qui échouent ou expirent : leur nature, jamais leur contenu ;
- les tâches des agents de programmation qui échouent : uniquement l’outil et le type d’échec ;
- le test rapide de votre IA lorsqu’il échoue : l’erreur de l’IA, après suppression de tout élément spécifique.

Une vérification interrompue parce que votre forfait IA a atteint sa limite d’utilisation n’est pas une erreur et n’est pas envoyée : elle attend la réinitialisation. Il en va de même si elle échoue parce que votre IA est déconnectée : **Vous attend** vous invite à vous reconnecter.

Un connecteur que vous avez ajouté vous-même (votre propre fichier dans `connectors/`) envoie uniquement le nom de son service et le libellé de son erreur, comme `notes` et `notes_http: HTTP unauthorized`, pour que nous puissions vous aider à le corriger. Rien d’autre de son code n’est envoyé. La fiche de connexion affiche l’erreur complète.

Les répétitions d’une même erreur sont comptabilisées, sans nouvel envoi. Un lot est envoyé au maximum toutes les 10 minutes. Nous les conservons pendant 30 jours.

## Limiter l’activité

Les tâches en arrière-plan sont mises en attente lorsque les limites de votre forfait IA sont presque atteintes, afin de préserver de la capacité pour vos propres chats (voir [Votre modèle d’IA](model.md)).

Lorsque les rapports d’erreur sont activés, votre Machine nous indique aussi une fois par jour à quelle fréquence cela s’est produit : pour chaque mise en pause, l’heure, la limite concernée, la durée et le nombre de tâches mises en attente. Rien sur la nature de ces tâches.

## Désactiver les rapports

Dans **Paramètres**, **Sécurité**, désactivez **Envoyer des rapports d’erreur**. Plus rien n’est enregistré ni envoyé, et les données en attente sont supprimées. Les erreurs restent visibles sur votre Machine, qui peut vous proposer une solution.

Voir [Sécurité et confidentialité](security-and-privacy.md).
