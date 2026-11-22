---
title: Contacter le support
area: troubleshooting
summary: Signalez un bug depuis votre tableau de bord, écrivez-nous ou autorisez notre équipe à examiner votre Machine pendant une journée.
covers: support-bundle, support-access
code: support.py, cli.py, dashboard.html, fleet.py
site: Report a problem
order: 9
translated: 419a75e887b25e20
---
## Écrivez-nous

Envoyez un e-mail à support@themachine.computer. Une personne vous répond.

Sur une Machine hébergée, le pied de page du tableau de bord contient « Un problème ? », qui ouvre le formulaire **Signaler un problème** de votre compte.

## Signaler un bug

Ouvrez **Aide**, puis **Signaler un bug**. Un message d’erreur comporte aussi un bouton **Signaler un bug**.

1. Expliquez ce qui s’est passé.
2. Ajoutez une capture d’écran si cela peut aider : **Faire une capture d’écran** du tableau de bord ou **Joindre une image**.
3. Laissez **Joindre un rapport pour le support** activé si possible. Le rapport inclut les versions, les vérifications et les erreurs récentes, mais pas vos messages, clés ni adresses. Il permet à notre équipe de consulter les journaux et les paramètres de votre Machine pendant 24 heures. Consultez [Accès au support](get-support.md#support-access). Si l’option n’est pas cochée, seuls votre texte et votre capture d’écran sont envoyés.
4. Appuyez sur **Envoyer**. Le formulaire se ferme aussitôt et le rapport pour le support est envoyé automatiquement.

Nous prenons le relais. Une Machine auto-hébergée peut en envoyer un lorsqu’elle est sur le Network. Sinon, écrivez-nous.

Vous pouvez aussi simplement expliquer à votre Machine dans le chat qu’il y a un problème. Elle ouvre **Signaler un bug** pour vous, avec votre texte et un bref résumé déjà renseignés. Rien n’est envoyé avant que vous appuyiez sur **Envoyer**.

Une fois le bug que vous avez signalé corrigé et le correctif installé sur votre Machine, nous vous en informons une seule fois : avec un bref message sur votre tableau de bord et un court e-mail. Une Machine auto-hébergée en est informée lorsqu’elle est sur le Network.

Le message vous demande si le problème est bien résolu. Appuyez sur **Ça marche**, ou sur **Toujours pas correct** pour expliquer ce qui ne va toujours pas, avec une image si cela peut aider. Cela nous est envoyé sous forme d’un nouveau rapport, lié au premier. **×** ferme le message sans réponse.

Vous êtes hors ligne ou avez envoyé plusieurs rapports d’affilée ? Votre rapport n’est pas perdu. Votre Machine le conserve et l’envoie automatiquement plus tard. En attendant, il apparaît sous **En attente d’envoi**.

## Accès au support

Notre équipe peut examiner votre Machine, mais seulement si vous l’y autorisez. Lorsque vous signalez un bug avec **Joindre un rapport pour le support** activé, l’accès est accordé quand vous appuyez sur **Envoyer**. Sur votre propre ordinateur, votre Machine doit être [associée à votre compte](friends.md).

- Lecture seule : journaux, paramètres, versions, synchronisation de chaque connexion et erreurs récentes, expurgés comme dans le rapport pour le support. Jamais vos messages, clés, mots de passe ni l’identité de vos contacts.
- L’accès expire automatiquement après 24 heures. Tant qu’il est actif, il apparaît dans **Paramètres**, **Sécurité** : **Désactiver** y met fin immédiatement.
- Chaque consultation est répertoriée dans **Paramètres**, **Activité**, avec sa date et son heure. Consultez [Activité](activity.md).

## Depuis votre propre ordinateur

Exécutez `assistant support-bundle`. Un fichier est créé avec les versions, les vérifications de `assistant doctor`, les journaux récents et vos paramètres, sans clés, jetons, mots de passe ni adresses. Examinez-le, puis envoyez-le à la personne qui vous aide.

Pour signaler un bug dans l’application open source, ouvrez un ticket sur [GitHub](https://github.com/Salesflare/TheMachine/issues), en utilisant uniquement des données fictives.
