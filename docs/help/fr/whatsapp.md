---
title: WhatsApp
area: connections
summary: Vos chats WhatsApp, lus comme sur un appareil associé. Les réponses ne sont envoyées qu’après votre accord.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 4ceded6544e535eb
---
## Ce qui est lu

Vos chats WhatsApp, comme sur un appareil associé à WhatsApp sur votre téléphone, par exemple WhatsApp sur un ordinateur. Quand vous connectez WhatsApp, l’application envoie aussi vos anciens chats, parfois plusieurs années d’historique. Votre Machine conserve tout, mais seules les tâches créées à partir des messages des 7 derniers jours.

Une photo, un message vocal ou un fichier sans légende apparaît sous son nom, par exemple « Photo », avec son icône. Les notifications de WhatsApp, comme celle sur le chiffrement ou l’arrivée d’une personne dans un groupe, ne contiennent pas de texte et sont ignorées.

## Lire les photos

Cette option est désactivée jusqu’à ce que vous l’activiez. Dans **Connexions**, ouvrez WhatsApp, puis **Détails**, et activez **Lire les photos**. The Machine lira alors les photos de vos chats professionnels : un reçu, une capture d’écran, une photo de lettre ou un formulaire. **Aussi dans les discussions perso** permet aussi de lire les photos de vos chats personnels. Le caractère professionnel ou personnel d’un chat dépend de vos paramètres de partage. Un chat avec votre famille reste donc personnel.

The Machine télécharge chaque photo une seule fois et la conserve sur votre Machine, comme une pièce jointe d’e-mail : elle est chiffrée lorsque la protection des messages est activée et supprimée en même temps que le message. Son propre modèle lit ce que montre la photo et le texte qu’elle contient. Ces éléments sont considérés comme faisant partie du message, jamais comme des instructions. Les formats JPEG, PNG et WebP sont acceptés, jusqu’à 5 Mo. Les codes à usage unique figurant sur une photo sont ignorés.

La tâche et le message affichent la photo. Touchez-la pour l’agrandir.

## Ce qui peut être envoyé

Un texte ou un fichier avec une légende facultative peut être envoyé dans un chat existant, uniquement après votre approbation dans la tâche. Avant l’envoi, la tâche affiche le fichier et vous pouvez l’ouvrir. La taille d’un fichier peut aller jusqu’à 18 Mo. Lorsqu’une tâche vient d’un message WhatsApp et que d’autres messages ont été envoyés ensuite, ou qu’elle vient d’un groupe, la réponse au message cite celui-ci. Le brouillon indique **En réponse**.

Si une tâche vient d’un e-mail, mais que vous échangez avec cette personne sur WhatsApp, dites-le dans le chat de la tâche. The Machine retrouve le chat existant avec cette personne et crée un brouillon WhatsApp, que vous pouvez vérifier et envoyer. Elle ne démarre jamais de nouveau chat.

WhatsApp ne propose pas de méthode officielle pour cela. La lecture des messages et l’envoi occasionnel d’une réponse que vous avez approuvée ne devraient très probablement pas poser de problème. L’envoi massif ou automatisé peut entraîner le blocage d’un compte.

## Connecter WhatsApp

Sur une Machine hébergée :

1. Dans le tableau de bord, ouvrez **Connexions**, puis **Chat**, et choisissez WhatsApp.
2. Appuyez sur **Afficher le code QR**.
3. Sur votre téléphone, ouvrez WhatsApp, puis Paramètres, Appareils connectés, Connecter un appareil, et scannez le code QR.
4. WhatsApp apparaît comme connecté dans la minute. L’historique de vos chats continue d’être importé ensuite, et sa fiche indique le nombre de messages pendant l’importation.
   Si la connexion prend trop de temps, un message vous l’indique après quelques minutes. Appuyez sur **Réessayer** pour reprendre là où le processus s’est arrêté.

Vous configurez WhatsApp sur votre téléphone sans avoir un deuxième écran pour scanner le code ? Ouvrez **Sur ton téléphone ? Connecte-toi plutôt avec un code**, saisissez votre numéro et appuyez sur **Obtenir un code**. WhatsApp vous demandera alors ce code.

Sur votre propre ordinateur : ouvrez **Connexions**, puis **Chat**, choisissez WhatsApp, saisissez votre numéro de téléphone avec son indicatif de pays et appuyez sur **Se connecter**. Un code s’affiche. Sur votre téléphone, ouvrez WhatsApp, puis Paramètres, Appareils connectés, Connecter un appareil, puis **Associer avec un numéro de téléphone** et saisissez le code.

Vous pouvez aussi exécuter `assistant connect whatsapp` et scanner le code affiché dans le terminal. La première fois, The Machine vous propose d’installer le connecteur WhatsApp, une version épinglée dont la somme de contrôle a été vérifiée ([source](https://github.com/Salesflare/wacli)).

WhatsApp indique que l’appareil associé est The Machine. Une Machine associée précédemment conserve son ancien nom dans la liste jusqu’à ce que vous l’associiez de nouveau.

## Photos de profil

The Machine demande à WhatsApp les photos de profil des personnes de votre Graph qui n’en ont pas, jusqu’à 50 par jour, via la synchronisation qui maintient WhatsApp à jour. Rien ne leur est envoyé. Les personnes qui vous cachent leur photo de profil n’en auront toujours pas.

## Supprimer la connexion

- Sur une Machine hébergée : appuyez sur **Retirer** à côté de WhatsApp sur votre page de configuration. Votre Machine se déconnecte et supprime les données conservées pour WhatsApp.
- Sur votre propre ordinateur : ouvrez **Connexions**, puis WhatsApp, **Détails**, et appuyez sur **Déconnecter**. Déconnectez aussi WhatsApp sur votre téléphone.

## Déconnecter WhatsApp

Sur votre téléphone, ouvrez WhatsApp, puis Paramètres, Appareils connectés. Touchez votre Machine et déconnectez-la.
