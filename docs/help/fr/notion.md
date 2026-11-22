---
title: Notion
area: connections
summary: Commentaires, mentions et tâches qui vous sont attribuées dans Notion. Les réponses, les nouvelles pages, les modifications et la validation des tâches attendent votre accord.
covers: connector:notion
code: connectors/notion.py, doc_writes.py, notion_heads_up.py
site: Sign in with Notion, Connect, More sources, Remove
translated: 8544baf8c60cc40b
---
## Ce qu’elle lit

Les pages accessibles à votre connexion Notion. Elle récupère :

- Les commentaires sur vos pages, les réponses aux discussions auxquelles vous participez et les commentaires qui vous mentionnent. Ceux qui nécessitent votre intervention deviennent des tâches.
- Les éléments de base de données qui vous sont attribués, avec leur échéance et leur statut. Chacun devient une tâche, et son échéance apparaît dans **Agenda**. Quand l’élément est terminé dans Notion, la tâche se ferme automatiquement. **Annuler** la rouvre.
- Les nouvelles pages ajoutées par une autre personne auxquelles vous avez accès.
- Une notification discrète quand quelqu’un modifie une page dont vous avez demandé la modification. Elle ne vous alerte jamais par un son.

La première synchronisation remonte à 7 jours. Les personnes sont associées à votre [Graph](graph.md) par leur adresse e-mail. Si Notion n’en fournit pas, elles sont associées uniquement si leur nom complet correspond à celui d’une seule personne dans votre Graph.

Pour utiliser cette connexion uniquement pour effectuer des actions, désactivez **Apporte des signaux** dans **Détails**.

## Ce qu’elle peut faire

Quand une tâche ou une réunion nécessite le texte d’une page, votre Machine lit cette page uniquement pendant qu’elle s’en occupe.

Chacune de ces actions attend votre accord dans la tâche correspondante :

- Répondre à un commentaire dans la discussion correspondante.
- Créer une nouvelle page. Elle reste privée jusqu’à ce que vous la partagiez.
- Modifier une page. Appuyez sur **Relire les modifications** pour voir chaque paragraphe avant et après, puis sur **Enregistrer**. Les modifications sont écrites uniquement dans la page telle que vous l’avez vue. Si quelqu’un l’a modifiée entre-temps, rien n’est écrit et la tâche vous l’indique.
- Marquer comme terminée une tâche qui vous est attribuée. Seul son statut change.

Elle ne supprime, ne partage ni ne déplace jamais de page.

## Connecter Notion

1. Dans le tableau de bord : **Connexions**, **Documents et fichiers**, Notion. Ou, sur la page de configuration d’une Machine hébergée, à l’adresse app.themachine.computer/setup : **Plus de sources**, Notion. Sur votre propre ordinateur, associez-la d’abord à votre compte.
2. Appuyez sur **Se connecter avec Notion**, choisissez votre espace de travail et les pages auxquelles elle peut accéder, puis autorisez l’accès.
3. De retour dans The Machine, la connexion est vérifiée immédiatement et le nom de l’espace de travail s’affiche.

Pour connecter un autre espace de travail, ajoutez Notion à nouveau.

## Coller un jeton à la place

Sous **Ou collez un jeton d’intégration**, appuyez sur **Obtenir votre jeton**. Notion ouvre sa page d’intégrations : créez une intégration interne, autorisez la lecture et l’ajout de contenu et de commentaires, ainsi que la lecture des informations utilisateur et des adresses e-mail. Copiez son jeton, collez-le et appuyez sur **Connecter**.

Partagez ensuite vos pages avec cette intégration dans Notion, sous **Connexions** sur chaque page. Sur votre propre ordinateur, `assistant connect notion` vous le demande aussi.

## Supprimer la connexion

- Dans le tableau de bord : **Connexions**, ouvrez Notion, puis **Détails** et **Déconnecter**. Les informations déjà récupérées restent disponibles.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de Notion sur la page de configuration.

## Révoquer l’accès dans Notion

Dans Notion : **Paramètres**, **Connexions**, puis **Déconnecter** The Machine. Pour un jeton collé, supprimez l’intégration sur la page des intégrations.
