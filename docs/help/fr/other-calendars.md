---
title: iCloud et autres agendas (CalDAV)
area: connections
summary: Les réunions d’iCloud Calendar ou de tout agenda CalDAV, comme Fastmail, Nextcloud ou Zoho. Lecture seule.
covers: connector:icloud_calendar, connector:caldav
code: caldav_calendar.py, ical.py, machine/sources/calendar_setup.py
order: 14
---
## Ce qu’il lit

Vos réunions, avec leurs invités, salles et notes : la semaine passée et le mois à venir quand vous connectez, puis chaque changement. Elles apparaissent dans l’Agenda et dans la préparation des réunions, comme les réunions Google ou Outlook. Chaque agenda du compte est lu, ou seulement celui que vous nommez.

Il est en lecture seule : il n’ajoute, ne déplace et ne supprime jamais de réunion.

## Connecter iCloud Calendar

1. Créez un mot de passe pour app sur [appleid.apple.com](https://appleid.apple.com), sous **Connexion et sécurité**. Celui créé pour iCloud Mail fonctionne aussi.
2. Dans le tableau de bord, ouvrez **Connexions**, puis **+ Ajouter**, et choisissez **iCloud Calendar**.
3. Saisissez votre Apple ID et le mot de passe pour app, puis appuyez sur **Se connecter**.

## Connecter un autre agenda

1. Ouvrez **Connexions**, puis **+ Ajouter**, et choisissez **Autre agenda**.
2. Saisissez votre adresse e-mail et votre mot de passe. Beaucoup de fournisseurs demandent ici un mot de passe d’application, créé dans les réglages de votre compte.
3. Appuyez sur **Se connecter**.

Le serveur est trouvé pour Fastmail, Yahoo, Zoho et les serveurs qui l’annoncent. Le vôtre n’est pas trouvé ? Ouvrez **Réglages du serveur** et saisissez son adresse CalDAV, comme `nextcloud.example.com/remote.php/dav`. **Seulement cet agenda** lit un seul agenda par son nom.

Des agendas Google ou Microsoft ? Choisissez plutôt **Google Calendar** ou **Outlook Calendar**.

## Quand il s’arrête

- **Le serveur d’agenda a refusé le mot de passe** : vous l’avez changé, ou le mot de passe d’application a été supprimé. Reconnectez-le avec un nouveau.
- **Le serveur d’agenda est injoignable** : il réessaie tout seul. Si cela continue, vérifiez l’adresse dans Réglages du serveur.

## Le retirer

**Connexions**, ouvrez l’agenda, **Détails**, puis **Déconnecter**. Ce qu’il a déjà récupéré reste. Supprimez aussi le mot de passe d’application chez votre fournisseur.
