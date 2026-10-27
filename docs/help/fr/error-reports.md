---
title: Rapports d’erreur
area: security
summary: Quand quelque chose casse, votre Machine indique à l’équipe The Machine ce qui a échoué et où dans le code. Jamais vos messages, noms ou adresses.
covers: error-reports
code: error_feed.py, dashboard.html
order: 4
---
## Ce que c’est

Quand quelque chose casse dans The Machine, votre Machine envoie à l’équipe une courte signature de l’erreur, pour que nous puissions la corriger avant que quelqu’un doive la signaler. C’est activé par défaut et cela nécessite [The Machine Network](/network).

## Ce qui part

Seulement ceci, pour chaque type d’erreur :

- le type d’erreur, comme `KeyError` ou `TypeError` ;
- son message, sans tout ce qui est spécifique : nombres, identifiants, texte cité, adresses e-mail, liens, chemins de fichiers et tout ce qui ressemble à une clé. Tout autre mot qui pourrait être un nom est retiré aussi ;
- l’endroit où c’est arrivé dans le code de The Machine : fichier, fonction et ligne, jamais un dossier de votre ordinateur ;
- la version de l’app, combien de fois c’est arrivé, et quand la première et la dernière fois.

Un vrai exemple : `IndexError`, `list index out of range`, à `assistant.py:fault_event:7899`, version `05b17ee6ac79`, 1 fois.

## Ce qui ne part jamais

Le contenu de vos messages, tâches, brouillons ou chats. Les noms, adresses e-mail, numéros de téléphone, liens, jetons ou mots de passe. Le compte ou la personne concernés.

## D’où viennent les erreurs

- le service et ses traitements : revues, préparation des tâches, chat, connexions et synchros ;
- le tableau de bord dans votre navigateur ;
- les traitements Claude Code et Codex qui échouent : seulement l’outil et le type d’échec.

La même erreur compte une fois, avec un nombre. Au plus un lot toutes les 10 minutes. L’équipe les garde 30 jours.

## Les désactiver

Dans Paramètres, Sécurité, désactivez **Envoyer des rapports d’erreur**. Plus rien n’est enregistré ni envoyé, et ce qui attendait est supprimé. Les erreurs s’affichent toujours sur votre propre Machine, qui peut proposer une correction.

Voir [Sécurité et confidentialité](security-and-privacy.md).
