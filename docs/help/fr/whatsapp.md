---
title: WhatsApp
area: connections
summary: Vos discussions WhatsApp, lues comme sur un appareil lié. Les réponses sont envoyées uniquement après votre approbation.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 9446d22f96229653
---
## Ce que la Machine lit

Vos discussions WhatsApp, comme sur WhatsApp pour ordinateur, depuis un appareil lié à WhatsApp sur votre téléphone. Quand vous la connectez, WhatsApp lui envoie aussi vos anciennes discussions, parfois des années d’historique. Votre Machine les conserve toutes, mais seules les tâches issues des messages des 7 derniers jours sont créées.

Une photo, un message vocal ou un fichier sans légende apparaît avec son nom, par exemple « Photo », et son icône. Les notifications de WhatsApp, comme celle sur le chiffrement ou l’arrivée d’une personne dans un groupe, ne contiennent pas de texte et sont ignorées.

## Lire les photos

Cette option est désactivée jusqu’à ce que vous l’activiez. Dans **Connexions**, ouvrez WhatsApp, puis **Détails**, et activez **Lire les photos**. The Machine lit alors les photos de vos discussions professionnelles : un reçu, une capture d’écran, une photo de lettre ou de formulaire. L’option **Aussi dans les discussions perso** permet aussi de lire celles de vos discussions personnelles. Le partage détermine si une discussion est professionnelle ou personnelle, donc une discussion avec votre famille reste personnelle.

The Machine télécharge chaque photo une seule fois et la conserve sur votre Machine comme une pièce jointe à un e-mail : elle est chiffrée lorsque la protection des messages est activée, et supprimée avec le message. Son propre modèle lit ce que montre la photo et le texte qu’elle contient. Cela fait partie du message, jamais des instructions. Formats JPEG, PNG et WebP jusqu’à 5 MB. Les codes à usage unique présents sur une photo sont ignorés.

La tâche et le message affichent la photo. Touchez-la pour l’agrandir.

## Ce qu’elle peut envoyer

Un texte ou un fichier avec une légende facultative, dans une discussion existante, uniquement après votre approbation dans la tâche. Avant l’envoi, la tâche affiche le fichier et vous pouvez l’ouvrir. La taille maximale d’un fichier est de 18 MB. Une réponse au message WhatsApp à l’origine d’une tâche cite ce message si d’autres messages ont été envoyés après, ou s’il s’agit d’un groupe. Le brouillon indique **En réponse**.

Si une tâche vient d’un e-mail, mais que vous échangez avec cette personne sur WhatsApp, dites-le dans le chat de la tâche. The Machine trouve la discussion existante avec cette personne et remplace WhatsApp par le canal du brouillon pour que vous puissiez le vérifier et l’envoyer. Elle ne démarre jamais de nouvelle discussion.

WhatsApp ne propose pas de méthode officielle pour cela. La lecture et l’envoi occasionnel d’une réponse approuvée par vous sont très peu susceptibles de poser problème. Les envois massifs ou automatisés peuvent entraîner le blocage d’un compte.

## Connecter WhatsApp

Sur une Machine hébergée :

1. Dans le tableau de bord, ouvrez **Connexions**, puis **Chat**, et choisissez WhatsApp.
2. Appuyez sur **Afficher le code QR**.
3. Sur votre téléphone, dans WhatsApp, ouvrez Paramètres, Appareils connectés, Associer un appareil, puis scannez le code QR.
4. WhatsApp apparaît comme connecté dans la minute. L’historique de vos discussions continue d’arriver ensuite, et sa carte indique le nombre de messages pendant la synchronisation.
   Si la connexion prend trop de temps, un message s’affiche après quelques minutes. Appuyez sur **Réessayer** pour reprendre là où le processus s’était arrêté.

Vous faites la configuration sur votre téléphone et n’avez pas de deuxième écran pour scanner le code ? Ouvrez **Sur ton téléphone ? Connecte-toi plutôt avec un code**, saisissez votre numéro et appuyez sur **Obtenir un code**. WhatsApp vous demandera alors ce code.

Sur votre propre ordinateur : ouvrez **Connexions**, puis **Chat**, choisissez WhatsApp, saisissez votre numéro de téléphone avec son indicatif de pays et appuyez sur **Se connecter**. Un code s’affiche. Sur votre téléphone, dans WhatsApp, ouvrez Paramètres, Appareils connectés, Associer un appareil, puis **Associer avec un numéro de téléphone**, et saisissez le code.

Vous pouvez aussi exécuter `assistant connect whatsapp` et scanner le code affiché dans le terminal. La première fois, l’installation du connecteur WhatsApp vous est proposée. Il s’agit d’une version figée dont la somme de contrôle a été vérifiée ([source](https://github.com/Salesflare/wacli)).

Dans Appareils connectés, elle apparaît sous le nom The Machine. Une Machine déjà liée y conserve son ancien nom jusqu’à ce que vous la reconnectiez.

Si WhatsApp déconnecte votre Machine, sa carte affiche **WhatsApp a déconnecté cette Machine**. Appuyez sur **Reconnecter** pour la lier à nouveau.

## Photos de profil

The Machine demande à WhatsApp les photos de profil des personnes de votre Graph qui n’en ont pas, jusqu’à 50 par jour, lors de la synchronisation qui maintient WhatsApp à jour. Aucun message ne leur est envoyé. Les personnes qui vous cachent leur photo n’en auront pas.

## Supprimer la connexion

- Sur une Machine hébergée : appuyez sur **Retirer** à côté de WhatsApp dans votre page de configuration. Votre Machine se déconnecte et supprime les données WhatsApp qu’elle avait conservées.
- Sur votre propre ordinateur : ouvrez WhatsApp dans **Connexions**, puis **Détails**, et appuyez sur **Déconnecter**. Déconnectez-la aussi sur votre téléphone.

## Déconnecter WhatsApp

Sur votre téléphone, dans WhatsApp, ouvrez Paramètres, Appareils connectés, touchez votre Machine, puis déconnectez-vous.
