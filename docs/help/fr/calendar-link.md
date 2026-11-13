---
title: Proton Calendar et liens d’agenda (ICS)
area: connections
summary: Les réunions du lien de partage d’un agenda : Proton Calendar, agendas publiés, scolaires ou sportifs. Lecture seule.
covers: connector:proton_calendar, connector:ics
code: ics_feed.py, ical.py, machine/sources/calendar_setup.py
order: 15
---
## Ce qu’il lit

Les événements de l’agenda derrière le lien, avec les événements récurrents et les fuseaux horaires : la semaine passée et le mois à venir, puis chaque changement. Ils apparaissent dans l’Agenda et dans la préparation des réunions.

Un lien ne peut qu’être lu, il ne change donc jamais une réunion. Le lien est consulté au plus toutes les 15 minutes. Selon Proton, les changements peuvent mettre quelques heures à arriver dans un lien.

## Connecter Proton Calendar

Proton Calendar n’a pas d’autre accès pour les apps, il passe donc par un lien de partage.

1. Ouvrez Proton Calendar sur le web, sur calendar.proton.me. Les apps mobiles ne permettent pas de créer des liens de partage.
2. Allez dans "Paramètres", "Tous les paramètres", "Calendriers", et choisissez l’agenda.
3. Sous "Share with anyone", appuyez sur "Create link" et choisissez "Full view". Limited view montre seulement quand vous êtes occupé.
4. Appuyez sur "Copy link".
5. Dans le tableau de bord, ouvrez **Connexions**, puis **Agenda**, choisissez **Proton Calendar**, collez le lien et appuyez sur **Se connecter**.

## Connecter un autre lien d’agenda

Choisissez **Lien d’agenda (ICS)** et collez le lien : une adresse https ou webcal qui finit par .ics, comme un agenda iCloud public, un agenda Outlook publié ou l’agenda de l’école de votre enfant.

## Gardez le lien privé

Toute personne qui a le lien peut lire l’agenda. The Machine le garde comme un mot de passe : jamais dans un journal ni à l’écran. Pour arrêter, supprimez le lien là où vous l’avez créé, puis appuyez ici sur **Déconnecter**.

## Quand il s’arrête

- **Le lien d’agenda ne fonctionne plus** : le lien a été supprimé ou modifié. Créez-en un nouveau et reconnectez-le.
- **Le serveur d’agenda est injoignable** : il réessaie tout seul.
