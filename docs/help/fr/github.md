---
title: GitHub
area: connections
summary: Consultez les demandes de révision, les mentions, les tâches qui vous sont attribuées et les échecs d’exécution de CI. Les problèmes ne sont créés qu’après votre confirmation.
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
translated: e97127e156e56f7d
---
## Ce que lit The Machine

Vos notifications GitHub : demandes de révision, mentions, tâches qui vous sont attribuées, réponses et échecs d’exécution de CI. The Machine ne les marque jamais comme lues.

## Ce qu’elle peut faire

La lecture ne modifie rien sur GitHub. Lorsqu’une tâche se termine par une étape GitHub, comme la création d’un problème, la tâche vous l’indique. L’étape ne s’exécute qu’après votre appui sur **Confirmer**, ou si vous avez demandé exactement cela dans son chat. Les captures d’écran passent par le navigateur de votre Machine. Si GitHub n’est pas connecté, la tâche indique qu’elle utilisera le navigateur et affiche **Connecter GitHub**.

## Connecter GitHub

Sur une Machine hébergée :

1. Ouvrez **Connexions**, puis **Projets et code**, et choisissez GitHub.
2. Choisissez **Travail** ou **Perso**, puis appuyez sur **Se connecter avec GitHub**.
3. Appuyez sur **Ouvrir GitHub ↗**, saisissez le code affiché et autorisez l’accès. La connexion se fait automatiquement.

La page de configuration sur app.themachine.computer/setup propose la même connexion sous **Plus de sources**.

Sur votre propre ordinateur :

1. Ouvrez **Connexions**, puis **Projets et code**, et choisissez GitHub.
2. Choisissez **Travail** avec votre entreprise, ou **Perso**, puis appuyez sur **Se connecter**.
3. Si vous y êtes invité, appuyez sur **Ouvrir GitHub ↗**, saisissez le code et autorisez l’accès. La connexion se fait automatiquement.

Vous pouvez aussi exécuter `assistant connect github` et confirmer votre connexion à GitHub.

## Supprimer la connexion

- Ouvrez **Connexions**, puis GitHub, **Détails** et **Déconnecter**. The Machine cesse alors de lire vos notifications. Les informations déjà importées restent disponibles.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de GitHub sur votre page de configuration.

## Désinstaller l’application sur GitHub

Sur GitHub, ouvrez Settings, Applications, Authorized OAuth Apps et révoquez l’accès à GitHub CLI. Sur votre propre ordinateur, `gh auth logout` déconnecte également votre compte.
