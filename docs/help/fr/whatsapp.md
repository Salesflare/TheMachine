---
title: WhatsApp
area: connections
summary: Vos discussions WhatsApp, lues comme un appareil associé. Il ne répond qu’après votre accord.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
---
## Ce qu’il lit

Vos discussions WhatsApp, comme un appareil associé au WhatsApp de votre téléphone, comme WhatsApp sur un ordinateur. À la connexion, il lit les 7 derniers jours.

Une photo, un message vocal ou un fichier sans légende apparaît tel quel, par exemple « Image envoyée ». Les notifications de WhatsApp lui-même, comme l’avis de chiffrement ou l’arrivée de quelqu’un dans un groupe, n’ont pas de texte et sont exclues.

## Lire les photos

Désactivé tant que vous ne l’activez pas. Sur la connexion WhatsApp, dans **Connexions**, activez **Lire les photos** et The Machine lit les photos de vos discussions pro : un reçu, une capture d’écran, la photo d’une lettre ou d’un formulaire. **Aussi dans les discussions perso** lit aussi celles de vos discussions perso. Une discussion est pro ou perso comme le partage la voit : une discussion en famille reste perso.

The Machine télécharge chaque photo une fois et la garde sur votre Machine comme une pièce jointe d’e-mail : chiffrée quand la protection des messages est active, et supprimée quand son message disparaît. Son propre modèle lit ce que montre la photo et le texte qu’elle contient. Cela fait partie du message, jamais des instructions. JPEG, PNG et WebP jusqu’à 5 Mo. Un code à usage unique sur une photo est laissé de côté.

La tâche et le message montrent la photo. Touchez-la pour la voir en grand.

## Ce qu’il peut envoyer

Un texte dans une discussion qui existe déjà, seulement après votre accord sur la tâche. Une réponse au message WhatsApp d’où vient une tâche cite ce message quand d’autres messages ont suivi, ou dans un groupe ; le brouillon indique **En réponse**.

Si une tâche est arrivée par e-mail mais que vous parlez à cette personne sur WhatsApp, dites-le dans le chat de la tâche. The Machine trouve votre discussion existante avec elle et passe le brouillon sur WhatsApp, pour que vous le vérifiiez et l’envoyiez. Il ne lance jamais de nouvelle discussion.

## Le connecter

Sur une Machine hébergée :

1. Dans le tableau de bord, ouvrez **Connexions**, puis **+ Ajouter**, et choisissez WhatsApp.
2. Appuyez sur **Afficher le code QR**.
3. Sur votre téléphone, dans WhatsApp, ouvrez Paramètres, Appareils connectés, Connecter un appareil, et scannez le code QR.

Vous configurez sur votre téléphone, sans second écran pour scanner ? Ouvrez **Sur votre téléphone ? Associez avec un code**, saisissez votre numéro et appuyez sur **Obtenir un code**. WhatsApp vous demande ensuite ce code.

Sur votre propre ordinateur, lancez `assistant connect whatsapp` et scannez le code affiché dans le terminal. Sans wacli, il propose d’installer la version épinglée de [Salesflare/wacli](https://github.com/Salesflare/wacli), vérifiée avec sa somme de contrôle.

## Photos

The Machine demande à WhatsApp les photos de profil des personnes de votre graph qui n’en ont pas, 50 par jour au maximum, via la synchro qui tient WhatsApp à jour. Rien ne leur est envoyé. Une personne qui vous cache sa photo reste sans photo.

## Le retirer

- Sur une Machine hébergée : appuyez sur **Retirer** à côté sur votre page de configuration. Votre Machine se dissocie et supprime ce qu’elle gardait pour WhatsApp.
- Sur votre propre ordinateur : **Connexions**, ouvrez WhatsApp, **Détails**, puis **Déconnecter**. Puis dissociez-le aussi sur votre téléphone.

## Le dissocier dans WhatsApp

Sur votre téléphone, dans WhatsApp, ouvrez Paramètres, Appareils connectés, appuyez sur votre Machine et déconnectez-vous.
