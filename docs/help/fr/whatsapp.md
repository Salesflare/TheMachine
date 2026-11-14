---
title: WhatsApp
area: connections
summary: Vos discussions WhatsApp, lues comme sur un appareil connecté. Les réponses ne sont envoyées qu’après votre approbation.
covers: connector:whatsapp
code: onboarding.py, next_actions.py, whatsapp_images.py
site: Show the QR code, Get a code, On your phone? Link with a code instead, Remove
translated: 881c555219a98f0f
---
## Ce que The Machine lit

Vos discussions WhatsApp, comme sur un appareil connecté à WhatsApp sur votre téléphone, à l’image de WhatsApp sur un ordinateur. Quand vous connectez WhatsApp, l’application envoie aussi vos anciennes discussions, parfois plusieurs années d’historique. Votre Machine les conserve toutes, mais seules les 7 derniers jours de messages deviennent des tâches.

Une photo, un message vocal ou un fichier sans légende apparaît sous la forme de son contenu, par exemple « Photo », avec son icône. Les notifications de WhatsApp, comme celle sur le chiffrement ou l’arrivée d’une personne dans un groupe, n’ont pas de texte et sont ignorées.

## Lire les photos

Cette option est désactivée tant que vous ne l’activez pas. Dans **Connexions**, ouvrez WhatsApp, puis **Détails**, et activez **Lire les photos**. The Machine lira alors les photos de vos discussions professionnelles : un reçu, une capture d’écran, la photo d’une lettre ou d’un formulaire. **Aussi dans les discussions perso** permet aussi de lire les photos de vos discussions personnelles. Le partage détermine si une discussion est professionnelle ou personnelle. Une discussion avec votre famille reste donc personnelle.

The Machine télécharge chaque photo une seule fois et la conserve sur votre Machine comme une pièce jointe à un e-mail : elle est chiffrée si la protection des messages est activée, et supprimée quand le message l’est. Son propre modèle lit le contenu de la photo et le texte qu’elle contient. Ces éléments font partie du message et ne sont jamais considérés comme des instructions. Formats JPEG, PNG et WebP, jusqu’à 5 MB. Les codes à usage unique présents sur une photo sont ignorés.

La tâche et le message affichent la photo. Touchez-la pour l’agrandir.

## Ce que The Machine peut envoyer

Un texte dans une discussion existante, uniquement après votre approbation dans la tâche. Une réponse au message WhatsApp à l’origine d’une tâche cite ce message si quelqu’un a répondu entre-temps ou s’il s’agit d’un groupe. Le brouillon porte la mention **En réponse**.

Si une tâche provient d’un e-mail, mais que vous échangez avec cette personne sur WhatsApp, dites-le dans le chat de la tâche. The Machine retrouve votre discussion existante avec cette personne et bascule le brouillon sur WhatsApp, afin que vous puissiez le vérifier et l’envoyer. Elle ne crée jamais de nouvelle discussion.

WhatsApp ne propose pas de méthode officielle pour cela. La lecture des messages et l’envoi occasionnel d’une réponse que vous avez approuvée ne devraient pas poser de problème. L’envoi massif ou automatisé peut entraîner le blocage d’un compte.

## Connecter WhatsApp

Sur une Machine hébergée :

1. Dans le tableau de bord, ouvrez **Connexions**, puis **Chat**, et choisissez WhatsApp.
2. Appuyez sur **Afficher le code QR**.
3. Sur votre téléphone, ouvrez les paramètres de WhatsApp, puis Appareils connectés, Connecter un appareil, et scannez le code QR.
4. WhatsApp apparaît comme connecté en moins d’une minute. L’historique de vos discussions continue ensuite d’arriver, et la carte affiche le nombre de messages reçus pendant ce temps.
   Si la connexion prend trop de temps, un message vous l’indique après quelques minutes. Appuyez sur **Réessayer** pour reprendre là où vous en étiez.

Vous faites la configuration sur votre téléphone, sans deuxième écran pour scanner le code ? Ouvrez **Sur ton téléphone ? Connecte-toi plutôt avec un code**, saisissez votre numéro et appuyez sur **Obtenir un code**. WhatsApp vous demandera ensuite ce code.

Sur votre propre ordinateur : ouvrez **Connexions**, puis **Chat**, choisissez WhatsApp, saisissez votre numéro de téléphone avec son indicatif pays et appuyez sur **Se connecter**. Un code s’affiche. Sur votre téléphone, ouvrez les paramètres de WhatsApp, puis Appareils connectés, Connecter un appareil, **Lier avec un numéro de téléphone**, et saisissez le code.

Vous pouvez aussi exécuter `assistant connect whatsapp` et scanner le code affiché dans le terminal. La première fois, The Machine vous propose d’installer le connecteur WhatsApp, une version figée dont la somme de contrôle a été vérifiée ([source](https://github.com/Salesflare/wacli)).

Dans Appareils connectés, l’appareil apparaît sous le nom The Machine. Une Machine connectée auparavant conserve son ancien nom jusqu’à ce que vous la reconnectiez.

## Photos de profil

The Machine demande à WhatsApp les photos de profil des personnes de votre Graph qui n’en ont pas, dans le cadre de la synchronisation qui actualise WhatsApp, à raison de 50 par jour maximum. Aucun message ne leur est envoyé. Les personnes qui vous cachent leur photo n’en auront pas.

## Supprimer la connexion

- Sur une Machine hébergée : appuyez sur **Retirer** à côté de WhatsApp, sur la page de configuration. Votre Machine se déconnecte et supprime les données WhatsApp qu’elle conservait.
- Sur votre propre ordinateur : ouvrez **Connexions**, puis WhatsApp et **Détails**, et appuyez sur **Déconnecter**. Déconnectez aussi l’appareil depuis votre téléphone.

## Déconnecter l’appareil dans WhatsApp

Sur votre téléphone, ouvrez les paramètres de WhatsApp, puis Appareils connectés. Touchez votre Machine et déconnectez-la.
