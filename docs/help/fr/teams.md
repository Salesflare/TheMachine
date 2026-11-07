---
title: Microsoft Teams
area: connections
summary: Chats Teams, chats de réunion et notes de réunion pour un compte professionnel ou scolaire. Il lit seulement.
covers: connector:teams
code: connectors/teams.py, ms_graph.py, onboarding.py
site: Connect Microsoft Teams
---
## Ce qu’il lit

Vos chats individuels, de groupe et de réunion dans Teams : les 7 derniers jours à la connexion, puis les nouveaux messages toutes les quelques minutes. Les chats plus anciens arrivent plus tard, petit à petit, sans rien bloquer.

Avec l’accord de votre admin, il lit aussi :

- Les fils des canaux de vos équipes.
- Les transcriptions des réunions que vous avez organisées.
- Les notes de réunion et actions de Copilot, si vous avez une licence Microsoft 365 Copilot.

Chaque transcription ou série de notes rejoint sa réunion dans votre agenda, marquée **De Teams**. Sans elles, le chat de la réunion reste là.

Les bots, les applis et les messages système sont laissés de côté.

## Ce qu’il peut faire

Rien dans Teams. Il lit seulement. Pour répondre, ouvrez le chat avec **Ouvrir dans Teams**.

## Ce qu’il demande

Microsoft demande de laisser The Machine lire vos chats et votre profil. Aucun admin n’est nécessaire pour cela.

Les canaux, les transcriptions et les notes Copilot ont besoin une fois de l’accord de l’admin de votre organisation. D’ici là, la carte Teams indique ce qu’il ne peut pas encore lire et pourquoi.

Il fonctionne seulement avec un compte Microsoft professionnel ou scolaire. Les comptes personnels n’ont pas de chats Teams lisibles de cette façon.

## Le connecter

Sur une Machine hébergée :

1. Dans le tableau de bord, ouvrez **Connexions**, **+ Ajouter** et choisissez **Microsoft Teams**.
2. Appuyez sur **Se connecter avec Microsoft** et donnez votre accord. Vous revenez au tableau de bord.
3. Pour les canaux et les notes de réunion, envoyez à votre admin le lien affiché sur la page de connexion. Une fois approuvé, connectez Teams à nouveau.

Pendant la configuration, la page de configuration propose aussi **Connect Microsoft Teams**.

Sur votre propre ordinateur, Teams n’est pas encore disponible.

## Le retirer

Dans le tableau de bord : **Connexions**, ouvrez Microsoft Teams, **Détails**, puis **Déconnecter**. Ce qu’il a déjà récupéré reste.

## Le révoquer chez Microsoft

Ouvrez myapps.microsoft.com et retirez The Machine. Si Outlook est connecté avec la même adresse, il est aussi déconnecté.
