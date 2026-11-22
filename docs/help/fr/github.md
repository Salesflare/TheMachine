---
title: GitHub
area: connections
summary: Passez en revue les demandes de revue, les mentions, les tâches qui vous sont attribuées et les échecs CI. Les issues ne sont créées qu’après votre confirmation.
covers: connector:github
code: connectors/github.py, onboarding.py
site: Sign in with GitHub, More sources, Remove
translated: e97127e156e56f7d
---
## Ce que The Machine lit

Vos notifications GitHub : demandes de revue, mentions, tâches qui vous sont attribuées, réponses et échecs CI. Elle ne les marque jamais comme lues.

## Ce qu’elle peut faire

La lecture ne modifie rien sur GitHub. Lorsqu’une tâche comporte une étape GitHub, comme la création d’une issue, la tâche vous l’indique. Cette étape ne s’exécute qu’après avoir appuyé sur **Confirmer**, ou si vous l’avez demandée précisément dans le chat. Les captures d’écran passent par le navigateur de votre Machine. Si GitHub n’est pas connecté, la tâche indique qu’elle utilisera le navigateur et affiche **Connecter GitHub**.

## Connecter GitHub

Sur une Machine hébergée :

1. Ouvrez **Connexions**, puis **Projets et code**, et choisissez GitHub.
2. Choisissez **Travail** ou **Perso**, puis appuyez sur **Se connecter avec GitHub**.
3. Appuyez sur **Ouvrir GitHub ↗**, saisissez le code affiché et autorisez la connexion. Elle se fait automatiquement.

La page de configuration de votre Machine, à l’adresse app.themachine.computer/setup, propose la même connexion dans **Plus de sources**.

Sur votre propre ordinateur :

1. Ouvrez **Connexions**, puis **Projets et code**, et choisissez GitHub.
2. Choisissez **Travail** avec le nom de votre entreprise, ou **Perso**, puis appuyez sur **Se connecter**.
3. Si vous y êtes invité, appuyez sur **Ouvrir GitHub ↗**, saisissez le code et autorisez la connexion. Elle se fait automatiquement.

Vous pouvez aussi lancer `assistant connect github` et confirmer votre connexion à GitHub.

## Supprimer la connexion

- Ouvrez **Connexions**, puis GitHub, **Détails** et **Déconnecter**. La lecture s’arrête. Les éléments déjà importés restent.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de GitHub sur votre page de configuration.

## Désinstaller sur GitHub

Sur GitHub, ouvrez Paramètres, Applications, puis Applications OAuth autorisées, et révoquez GitHub CLI. Sur votre propre ordinateur, `gh auth logout` vous déconnecte également.
