---
title: WhatsApp
area: connections
summary: Vos discussions WhatsApp, lues comme sur un appareil associé. Les réponses ne sont envoyées qu’après votre approbation.
covers: connector:whatsapp
code: onboarding.py, whatsapp_setup.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 130c64388a71b7d1
---
## Ce qu’elle lit

Vos discussions WhatsApp, comme sur un appareil associé à WhatsApp sur votre téléphone, par exemple WhatsApp sur un ordinateur. Quand vous la connectez, WhatsApp transmet aussi vos anciennes discussions, parfois des années d’historique. Votre Machine les conserve toutes, mais seules les tâches issues des messages des 7 derniers jours sont créées.

Une photo, un message vocal ou un fichier sans légende apparaît sous forme d’élément, par exemple « Photo », avec son icône. Les notifications de WhatsApp, comme celle sur le chiffrement ou l’arrivée d’une personne dans un groupe, ne contiennent pas de texte et sont ignorées.

## Lire les photos

Cette option est désactivée jusqu’à ce que vous l’activiez. Dans **Connexions**, ouvrez WhatsApp, puis **Détails**, et activez **Lire les photos**. The Machine lira alors les photos de vos discussions professionnelles : un reçu, une capture d’écran, une photo de lettre ou de formulaire. L’option **Aussi dans les discussions perso** permet aussi de lire les photos de vos discussions personnelles. Une discussion est considérée comme professionnelle ou personnelle selon les paramètres de partage. Une discussion avec votre famille reste donc personnelle.

The Machine télécharge chaque photo une seule fois et la conserve sur votre Machine comme une pièce jointe à un e-mail : elle est chiffrée si la protection des messages est activée et supprimée en même temps que le message. Son propre modèle lit le contenu de la photo et le texte qu’elle contient. Ces éléments sont considérés comme faisant partie du message, jamais comme des instructions. Les formats JPEG, PNG et WebP sont acceptés, jusqu’à 5 Mo. Les codes à usage unique figurant sur une photo sont ignorés.

La tâche et le message affichent la photo. Touchez-la pour l’agrandir.

## Ce qu’elle peut envoyer

Un texte ou un fichier avec une légende facultative, dans une discussion existante, uniquement après votre approbation dans la tâche. Avant l’envoi, la tâche affiche le fichier et vous pouvez l’ouvrir. La taille maximale d’un fichier est de 18 Mo. Si une tâche provient d’un message WhatsApp auquel quelqu’un a répondu, ou d’un groupe, la réponse cite le message d’origine. Le brouillon porte la mention **En réponse**.

Si une tâche vient d’un e-mail, mais que vous échangez avec cette personne sur WhatsApp, dites-le dans le chat de la tâche. The Machine retrouve votre discussion existante avec cette personne et bascule le brouillon sur WhatsApp pour que vous puissiez le vérifier et l’envoyer. Elle ne démarre jamais de nouvelle discussion.

WhatsApp ne propose pas de méthode officielle pour cela. La lecture et l’envoi occasionnel d’une réponse que vous avez approuvée ne devraient pas poser de problème. En revanche, l’envoi massif ou automatisé peut entraîner le blocage d’un compte.

## Connexion

Sur une Machine hébergée :

1. Dans le tableau de bord, ouvrez **Connexions**, puis **Chat**, et choisissez WhatsApp.
2. Appuyez sur **Afficher le QR code**.
3. Sur votre téléphone, ouvrez WhatsApp, puis Paramètres, Appareils connectés et Connecter un appareil. Scannez le QR code.
4. WhatsApp devrait apparaître comme connecté en moins d’une minute. L’historique de vos discussions continuera ensuite d’arriver. La carte indique le nombre de messages reçus pendant la synchronisation.
   Si la connexion prend trop de temps, un message vous l’indique après quelques minutes. Appuyez sur **Réessayer** pour reprendre là où vous en étiez.

Vous configurez WhatsApp sur votre téléphone, sans deuxième écran pour scanner le code ? Ouvrez **Sur votre téléphone ? Connectez-vous plutôt avec un code**, saisissez votre numéro, puis appuyez sur **Obtenir un code**. WhatsApp vous demandera ensuite de saisir ce code.

Sur votre propre ordinateur : ouvrez **Connexions**, puis **Chat**, choisissez WhatsApp, saisissez votre numéro de téléphone avec l’indicatif du pays et appuyez sur **Connecter**. Un code s’affiche. Sur votre téléphone, ouvrez WhatsApp, puis Paramètres, Appareils connectés, Connecter un appareil, puis **Connecter avec un numéro de téléphone**. Saisissez le code.

Vous pouvez aussi exécuter `assistant connect whatsapp` et scanner le code affiché dans le terminal. La première fois, l’installation du connecteur WhatsApp vous est proposée. Il s’agit d’une version épinglée dont la somme de contrôle a été vérifiée ([source](https://github.com/Salesflare/wacli)).

Dans Appareils connectés, elle apparaît sous le nom The Machine. Une Machine associée auparavant conserve son ancien nom jusqu’à ce que vous la reconnectiez.

Si WhatsApp déconnecte votre Machine, sa carte affiche **WhatsApp a déconnecté cette Machine**. Appuyez sur **Reconnecter** et associez-la à nouveau : saisissez votre numéro de téléphone, puis le code affiché dans WhatsApp, sous Appareils connectés, **Connecter avec un numéro de téléphone**. Elle se reconnecte au même endroit qu’avant, vos discussions sont donc conservées. Si vous avez configuré votre propre service pour synchroniser WhatsApp, il se met en pause pendant la reconnexion et reprend ensuite.

Si WhatsApp tarde à répondre, un message vous l’indique pendant la configuration. Appuyez sur **Réessayer** une minute plus tard pour obtenir un nouveau code.

## Photos de profil

The Machine demande à WhatsApp les photos de profil des personnes de votre Graph qui n’en ont pas, dans la limite de 50 par jour. La demande passe par la synchronisation qui maintient WhatsApp à jour. Aucune notification ne leur est envoyée. Les personnes qui vous cachent leur photo n’en auront toujours pas.

## Supprimer la connexion

- Sur une Machine hébergée : appuyez sur **Retirer** à côté de WhatsApp sur votre page de configuration. Votre Machine se déconnecte et supprime les données WhatsApp qu’elle a conservées.
- Sur votre propre ordinateur : ouvrez WhatsApp dans **Connexions**, puis **Détails** et appuyez sur **Déconnecter**. Déconnectez-la aussi de votre téléphone.

## Déconnecter WhatsApp

Sur votre téléphone, ouvrez WhatsApp, puis Paramètres, Appareils connectés, touchez votre Machine et déconnectez-la.
