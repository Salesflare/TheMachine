---
title: Obtenir de l’aide
area: troubleshooting
summary: Signalez un bug depuis votre tableau de bord, écrivez-nous, ou laissez notre équipe regarder votre Machine pendant une journée.
covers: support-bundle, support-access
code: support.py, cli.py, dashboard.html, fleet.py
site: Report a problem
order: 9
---
## Nous écrire

Écrivez à support@themachine.computer. Une vraie personne répond.

Sur une Machine hébergée, le pied de page du tableau de bord affiche « Un problème ? », qui ouvre le formulaire **Signaler un problème** de votre compte.

## Signaler un bug

Ouvrez **Aide**, puis **Signaler un bug**. Un message d’erreur a aussi un bouton **Signaler un bug**.

1. Dites ce qui n’a pas marché.
2. Ajoutez une capture d’écran si cela aide : **Faire une capture d’écran** du tableau de bord, ou **Joindre une image**.
3. Laissez **Joindre un rapport pour le support** activé, sauf si vous préférez ne pas le faire. Il ajoute versions, vérifications et erreurs récentes, sans messages, clés ni adresses, et permet à notre équipe de lire les journaux et paramètres de votre Machine pendant 24 heures. Voir [Accès du support](get-support.md#support-access). Décoché, seuls votre texte et votre capture partent.
4. Touchez **Envoyer**. Le formulaire se ferme tout de suite. Votre Machine ajoute le rapport pour le support d’elle-même ; une vérification lente ne retarde jamais votre signalement.

Nous prenons le relais. Une Machine auto-hébergée peut en envoyer un quand elle est sur le Network ; sinon, écrivez-nous.

Quand nous corrigeons un bug que vous avez signalé et que votre Machine a le correctif, nous vous le disons une fois : une courte ligne sur votre tableau de bord (**Compris** la ferme) et un court e-mail. Une Machine auto-hébergée l'apprend quand elle est sur le Network.

Si un signalement ne peut pas partir tout de suite (vous êtes hors ligne, ou vous en avez envoyé beaucoup en peu de temps), il n’est pas perdu. Votre Machine le garde, indique quand il partira et l’envoie d’elle-même. Les signalements encore en attente s’affichent sous **En attente d’envoi**.

## Accès du support

Notre équipe peut regarder votre Machine pour vous, mais seulement une fois que vous l’autorisez. Quand vous signalez un bug avec **Joindre un rapport pour le support** coché, l’accès s’active quand vous appuyez sur **Envoyer**. Sur votre propre ordinateur, votre Machine doit pour cela être [associée à votre compte](friends.md).

- Lecture seule : journaux, paramètres, versions, la synchro de chaque connexion et les erreurs récentes, nettoyés comme le rapport pour le support. Jamais vos messages, clés, mots de passe, ni qui sont vos contacts.
- L’accès se termine de lui-même après 24 heures. Tant qu’il est actif, **Paramètres**, **Sécurité** l’affiche : **Désactiver** y met fin tout de suite.
- Chaque consultation figure dans Paramètres, **Activité**, avec sa date. Voir [Activité](activity.md).

## Depuis votre propre ordinateur

Lancez `assistant support-bundle`. Cela enregistre un fichier avec les versions, les vérifications de `assistant doctor`, les journaux récents et vos paramètres, sans clés, jetons, mots de passe ni adresses. Parcourez-le, puis envoyez-le à la personne qui vous aide.

Pour un bug dans l’app open source, ouvrez une issue sur [GitHub](https://github.com/Salesflare/TheMachine/issues), avec uniquement des données inventées.
