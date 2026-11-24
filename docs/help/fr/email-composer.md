---
title: Rédiger un nouvel e-mail
area: cards
summary: Cliquez sur une adresse e-mail pour écrire à cette personne depuis votre propre boîte mail, dans la même fenêtre que le brouillon d’une tâche.
covers: email-composer
code: machine/app/mail.py, dashboard/todos-compose.js, dashboard/todos-kept.js
order: 12
translated: 539fd36f92d31aad
---
## Ouvrir la fenêtre

Cliquez sur une adresse e-mail, sur la page d’une personne dans Graph ou dans un lien d’une tâche ou d’un chat. La fenêtre **Nouvel e-mail** s’ouvre avec cette adresse et un objet et un message vides. Sur téléphone, elle occupe tout l’écran.

**De** est réglé par défaut sur la boîte mail associée à cette personne : votre boîte Travail pour un contact professionnel, votre boîte Personnel pour la famille et les amis. Cliquez dessus pour choisir une autre de vos boîtes mail ou un alias confirmé.

## Envoyer

Rédigez l’objet et le message, avec du texte en gras, des listes et des liens, si vous le souhaitez. Aucun e-mail n’est envoyé tant que vous n’appuyez pas sur **Envoyer maintenant**. Vous pouvez aussi appuyer sur **Envoyer plus tard** et choisir quand l’envoyer : consultez [Envoyer plus tard](send-later.md).

L’e-mail est ensuite envoyé comme n’importe quel brouillon que vous approuvez : il apparaît comme envoyé dans sa propre tâche, sur la page de la personne et dans votre boîte mail. S’il ne peut pas être envoyé, la tâche le conserve pour que vous puissiez l’envoyer depuis là.

## Si vous ne l’envoyez pas

Fermez la fenêtre avec Échap, × ou Retour. Ce que vous avez écrit est conservé, avec l’objet, l’expéditeur et le destinataire. L’e-mail n’est jamais envoyé automatiquement.

- Un nouvel e-mail reste au-dessus de vos tâches sous le libellé **E-mail non envoyé à**, avec les options **Continuer** et **Supprimer**.
- Un brouillon modifié affiche **Modifié, non envoyé** dans sa tâche, sur tous les canaux. Rouvrez-le pour retrouver votre texte. Une réponse que vous modifiez dans **Vérifier** fonctionne de la même façon.
- Après un rechargement, ou si votre téléphone a fermé l’application, la fenêtre dans laquelle vous écriviez se rouvre.

L’option **Supprimer** dans la fenêtre efface ce que vous avez écrit, et **Annuler** le restaure. Un message envoyé, programmé ou supprimé ne peut pas être restauré.

Si le brouillon a changé entre-temps, vous voyez le nouveau brouillon, et **L’utiliser** affiche ce que vous avez écrit. Aucun des deux ne remplace l’autre tant que vous n’avez pas envoyé le message. Deux onglets avec des textes différents fonctionnent de la même façon.

Ce que vous avez écrit reste uniquement dans ce navigateur, chiffré, pendant 30 jours. Il est supprimé lorsque vous vous déconnectez ou qu’une autre personne se connecte. Les autres appareils ne le voient pas. Sans https, il est conservé tant que la page reste ouverte.

## Votre messagerie

**Ouvrir dans votre messagerie** ouvre plutôt votre propre application de messagerie, avec le texte que vous avez écrit jusque-là. Vous pouvez aussi cliquer sur l’adresse en maintenant Ctrl ou Cmd.

Seules les boîtes mail pour lesquelles **Peut agir** est activé peuvent envoyer des e-mails. Si aucune ne l’est, un clic sur une adresse ouvre votre application de messagerie, comme avant.
