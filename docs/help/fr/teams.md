---
title: Microsoft Teams
area: connections
summary: Chats Teams, chats de réunion et notes de réunion avec un compte professionnel ou scolaire. Les réponses sont envoyées uniquement après votre approbation.
covers: connector:teams
code: connectors/teams.py, teams_send.py, ms_graph.py, onboarding.py
site: Connect Microsoft Teams
translated: 9ca0bb08466b4d58
---
## Ce que l’application lit

Vos chats individuels, de groupe et de réunion dans Teams : les 7 derniers jours au moment de la connexion, puis les nouveaux messages toutes les quelques minutes. Environ un an d’anciens chats et de fils de discussion de canal, avec l’accord de votre administrateur, est importé plus tard sous forme d’[historique](history.md), petit à petit, sans rien ralentir.

Avec l’accord de votre administrateur, elle lit aussi :

- Les fils de discussion des canaux de vos équipes.
- Les transcriptions des réunions que vous avez organisées.
- Les notes de réunion et les tâches de Copilot, si vous avez une licence Microsoft 365 Copilot.

Chaque transcription ou ensemble de notes est associé à la réunion correspondante dans votre agenda, avec la mention **De Teams**. Sans ces éléments, le chat de la réunion reste disponible.

Les bots, les applications et les messages système sont exclus.

## Ce qu’elle peut faire

Répondre dans le chat individuel, de groupe ou de réunion à l’origine d’une tâche. The Machine rédige la réponse. Elle est envoyée en votre nom dans ce chat uniquement après que vous l’avez relue et que vous avez appuyé sur **Envoyer maintenant**. Elle ne démarre jamais de nouveau chat.

Elle ne publie pas dans les canaux. Pour répondre dans un fil de discussion de canal, ouvrez-le avec **Ouvrir dans Teams**.

## Ce qu’elle demande

Microsoft demande l’autorisation de laisser The Machine lire vos chats et votre profil, et d’envoyer des messages dans les chats en votre nom. L’accord d’un administrateur n’est pas nécessaire.

Si vous avez connecté Teams avant que l’envoi soit possible, sa fiche indique **Reconnectez-vous pour envoyer des réponses.** Appuyez sur **Reconnecter** et autorisez de nouveau l’accès. En attendant, le brouillon reste disponible pour que vous l’envoyiez dans Teams.

L’accès aux canaux, aux transcriptions et aux notes de Copilot doit être autorisé une fois par l’administrateur de votre organisation. En attendant, la fiche Teams indique ce que l’application ne peut pas encore lire et pourquoi.

Cette connexion fonctionne uniquement avec un compte Microsoft professionnel ou scolaire. Les comptes personnels ne contiennent pas de chats Teams accessibles de cette façon.

## Connecter Teams

Sur une Machine hébergée :

1. Dans le tableau de bord, ouvrez **Connexions**, puis **Chat** pour **Microsoft Teams** ou **Réunions** pour **Réunions Teams**. Les deux options utilisent la même connexion.
2. Appuyez sur **Se connecter avec Microsoft** et autorisez l’accès. Vous reviendrez au tableau de bord.
3. Pour les canaux et les notes de réunion, envoyez à votre administrateur le lien affiché sur la page de connexion. Une fois l’accès autorisé, reconnectez Teams.

Pendant la configuration, la page de configuration propose également **Connecter Microsoft Teams**.

Sur votre propre ordinateur, une fois celui-ci [associé à votre compte](friends.md#a-machine-on-your-own-computer) : ouvrez **Connexions**, puis **Chat** ou **Réunions**, choisissez **Microsoft Teams** ou **Réunions Teams**, puis appuyez sur **Se connecter avec Microsoft**. The Machine y lit vos chats et vos chats de réunion. Les canaux et les notes de réunion n’y sont pas encore disponibles.

## Supprimer la connexion

Dans le tableau de bord : ouvrez **Connexions**, puis Microsoft Teams, **Détails** et enfin **Déconnecter**. Les éléments déjà importés restent disponibles.

## Révoquer l’accès dans Microsoft

Ouvrez myapps.microsoft.com et supprimez The Machine. Si Outlook est connecté avec la même adresse, il sera également déconnecté.
