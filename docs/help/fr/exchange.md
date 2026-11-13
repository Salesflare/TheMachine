---
title: Exchange Server
area: connections
summary: Les réunions d’un Exchange Server géré par votre entreprise (2013 à 2019 ou Subscription Edition). Lecture seule.
covers: connector:exchange
code: ews_calendar.py, machine/sources/calendar_setup.py
order: 16
---
## Ce qu’il lit

Vos réunions, avec leurs invités, salles et notes : la semaine passée et le mois à venir quand vous connectez, puis chaque changement. Elles apparaissent dans l’Agenda et dans la préparation des réunions.

Il est en lecture seule : il n’ajoute, ne déplace et ne supprime jamais de réunion. Les e-mails d’Exchange Server ne sont pas encore lus.

## Microsoft 365 ou Exchange Server ?

Exchange Server tourne dans votre entreprise. Microsoft 365 (Exchange Online) est le cloud de Microsoft : choisissez plutôt **Outlook Calendar** pour lui. Si votre adresse s’avère être sur Microsoft 365, le formulaire le dit.

## Le connecter

1. Dans le tableau de bord, ouvrez **Connexions**, puis **Agenda**, et choisissez **Exchange Server**.
2. Saisissez votre adresse e-mail professionnelle et votre mot de passe Windows.
3. Appuyez sur **Se connecter**.

Le serveur est trouvé à partir de votre adresse (Autodiscover). Pas trouvé ? Ouvrez **Réglages du serveur** et saisissez le serveur que votre équipe informatique indique pour Outlook, comme `mail.example.com`. Vous vous connectez avec un autre nom que votre adresse ? Saisissez-le sous la forme `DOMAIN\name` dans **Nom d’utilisateur**.

Il se connecte avec NTLM ou Basic, uniquement en https.

## Quand il s’arrête

- **Le serveur d’agenda a refusé le mot de passe** : votre mot de passe Windows a changé. Reconnectez-le.
- **Une boîte Microsoft 365** : votre boîte est passée sur Microsoft 365. Déconnectez celle-ci et connectez **Outlook Calendar**.
- **Le serveur d’agenda est injoignable** : il réessaie tout seul. Certains serveurs ne sont joignables que depuis le réseau de l’entreprise ou par VPN.

## Le retirer

**Connexions**, ouvrez l’agenda, **Détails**, puis **Déconnecter**. Ce qu’il a déjà récupéré reste.
