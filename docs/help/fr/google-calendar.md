---
title: Google Agenda
area: connections
summary: Vos réunions, pour arriver préparé et assurer le suivi. Il ne change rien sans que vous appuyiez.
covers: connector:calendar
code: onboarding.py, google_api.py
site: Connect Google, Mail and Calendar, Disconnect, Sign in with Google
order: 11
---
## Ce qu’il lit

Vos événements de 7 jours en arrière à 30 jours en avant, avec les événements récurrents. Ils s’affichent dans l’onglet [Agenda](calendar.md) et aident les tâches liées à une réunion.

## Ce qu’il peut faire

Rien de lui-même. Il ne répond jamais à une invitation, et n’invite que les personnes que vous indiquez vous-même.

Si la connexion peut écrire dans les agendas, vous pouvez ajouter, modifier ou supprimer un événement sans invités, dans votre propre agenda ou dans un agenda partagé que vous pouvez modifier. Chaque changement vient de vous : dans l’[Agenda](calendar.md), ou sur une tâche qui le propose. Une connexion via **Connecter Google** ne fait que lire.

Dans votre propre agenda, vous pouvez aussi inviter des personnes depuis le formulaire de l’[Agenda](calendar.md). Le bouton indique combien de personnes reçoivent une invitation, et Google envoie les invitations quand vous appuyez. Une tâche n’invite jamais personne.

## Le connecter

Sur une Machine hébergée, il se connecte avec Gmail : sur votre page de configuration, sous **E-mail et agenda**, appuyez sur **Connecter Google**.

Sur votre propre ordinateur, une fois [associé à votre compte](friends.md#a-machine-on-your-own-computer) : ouvrez **Connexions**, puis **+ Ajouter**, choisissez Google Agenda et appuyez sur **Se connecter avec Google**. Il se connecte avec Gmail.

Avec votre propre app : lancez `assistant connect calendar`, ou ouvrez **Utiliser votre propre app** à cet endroit. Il demande quel agenda lire.

## Le retirer

- Sur une Machine hébergée : appuyez sur **Déconnecter** à côté de l’adresse sur votre page de configuration. Cela retire Gmail et l’agenda pour cette adresse.
- Sur votre propre ordinateur : **Connexions**, ouvrez l’agenda, **Détails**, puis **Déconnecter**.

## Le désinstaller chez Google

Dans votre compte Google, ouvrez Sécurité, puis Vos connexions à des applications et services tiers, et retirez l’app. Voir [Gmail](gmail.md).
