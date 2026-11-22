---
title: Exchange Server
area: connections
summary: Réunions depuis un Exchange Server géré par votre entreprise (de 2013 à 2019 ou Subscription Edition). En lecture seule.
covers: connector:exchange
code: ews_calendar.py, machine/sources/calendar_setup.py
order: 16
translated: f2b98c9bd4f08dba
---
## Ce qui est lu

À la connexion, vos réunions de la semaine passée et du mois à venir, avec leurs invités, leurs salles et leurs notes. Ensuite, chaque modification. Elles apparaissent dans Agenda et dans la préparation des réunions.

La connexion est en lecture seule : elle n’ajoute, ne déplace ni ne supprime jamais de réunion. Les e-mails d’Exchange Server ne sont pas encore lus.

## Microsoft 365 ou Exchange Server ?

Exchange Server est hébergé par votre entreprise. Microsoft 365 (Exchange Online) est le service cloud de Microsoft : choisissez plutôt **Outlook Calendar**.

Saisissez d’abord votre adresse. Si elle est associée à Microsoft 365, le formulaire l’indique et affiche **Se connecter avec Microsoft** à la place du champ du mot de passe. Cela ouvre la connexion à Outlook Calendar, sans mot de passe. Si le serveur est introuvable après quelques secondes, ou si votre entreprise gère son propre serveur, le formulaire de mot de passe reste affiché.

## Connecter l’agenda

1. Dans le tableau de bord, ouvrez **Connexions**, puis **Agenda**, et choisissez **Exchange Server**.
2. Saisissez votre adresse e-mail professionnelle et votre mot de passe Windows.
3. Sélectionnez **Connecter**.

Le serveur est détecté à partir de votre adresse (Autodiscover). S’il est introuvable, ouvrez **Réglages du serveur** et saisissez le serveur Outlook indiqué par votre équipe informatique, par exemple `mail.example.com`. Si vous vous connectez avec un nom différent de votre adresse, saisissez-le dans **Nom d’utilisateur** sous la forme `DOMAIN\name`.

La connexion utilise NTLM ou Basic, uniquement via https.

## En cas de problème

- **Le serveur d’agenda a refusé le mot de passe** : votre mot de passe Windows a changé. Reconnectez l’agenda.
- **Une boîte aux lettres Microsoft 365** : votre boîte aux lettres a été déplacée vers Microsoft 365. Déconnectez cet agenda et connectez **Outlook Calendar**.
- **Le serveur d’agenda est injoignable** : une nouvelle tentative est lancée automatiquement. Certains serveurs ne sont accessibles que depuis le réseau de l’entreprise ou via un VPN.

## Supprimer l’agenda

**Connexions**, ouvrez l’agenda, **Détails**, puis **Déconnecter**. Les réunions déjà importées restent.
