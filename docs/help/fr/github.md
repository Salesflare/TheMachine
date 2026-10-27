---
title: GitHub
area: connections
summary: Demandes de revue, mentions, assignations et exécutions CI échouées. Il ne fait que lire.
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
---
## Ce qu’il lit

Vos notifications GitHub : demandes de revue, mentions, assignations, réponses et exécutions CI échouées. Il ne marque jamais une notification comme lue.

## Ce qu’il peut faire

Rien sur GitHub. Chaque appel qu’il fait est une lecture.

## Le connecter

Sur une Machine hébergée :

1. Ouvrez votre page de configuration sur app.themachine.computer/setup et allez dans **Plus de sources**.
2. Ouvrez GitHub et appuyez sur **Se connecter avec GitHub**.
3. Tapez sur GitHub le code qu’il affiche, sur votre téléphone ou votre ordinateur.

Sur votre propre ordinateur :

1. Connectez-vous d’abord à la CLI GitHub : `gh auth login`.
2. Dans le tableau de bord, ouvrez **Connexions**, puis **+ Ajouter**, et choisissez GitHub. Ou lancez `assistant connect github`.
3. Confirmez votre identifiant GitHub. The Machine vérifie qu’il correspond à chaque synchro.

## Le retirer

- Dans le tableau de bord : **Connexions**, ouvrez GitHub, **Détails**, puis **Déconnecter**. Il arrête de lire. Ce qu’il a déjà récupéré reste.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté sur votre page de configuration.

## Le désinstaller sur GitHub

Révoquez l’accès de la CLI GitHub dans GitHub, sous Settings, Applications, Authorized OAuth Apps. Sur votre propre ordinateur, `gh auth logout` déconnecte aussi la CLI.
