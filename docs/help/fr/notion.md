---
title: Notion
area: connections
summary: Commentaires, mentions et tâches qui vous sont attribuées dans Notion. Les réponses, les nouvelles pages, les modifications et le marquage des tâches comme faites attendent votre accord.
covers: connector:notion
code: connectors/notion.py, doc_writes.py, notion_heads_up.py
site: Sign in with Notion, Connect, More sources, Remove
translated: 2e93c261cc09e401
---
## Ce que l’intégration lit

Les pages auxquelles votre connexion Notion peut accéder. Elle importe :

- Les commentaires sur vos pages, les réponses aux discussions auxquelles vous participez et les commentaires qui vous mentionnent. Ceux qui nécessitent votre intervention deviennent des tâches.
- Les éléments de base de données qui vous sont attribués, avec leur date d’échéance et leur statut. Chacun devient une tâche, et sa date d’échéance s’affiche dans **Agenda**. Quand l’élément est marqué comme fait dans Notion, la tâche se clôture automatiquement. **Annuler** la rouvre.
- Les nouvelles pages ajoutées par quelqu’un d’autre auxquelles vous pouvez accéder.
- Une notification discrète quand quelqu’un modifie une page que vous avez demandé de modifier. Elle ne déclenche jamais de sonnerie.

La première synchronisation remonte à 7 jours. Les personnes sont associées à votre [Graph](graph.md) à l’aide de leur adresse e-mail. Quand Notion ne fournit pas d’adresse e-mail, l’association se fait uniquement à l’aide d’un nom complet correspondant exactement à celui d’une seule personne de votre Graph.

Pour utiliser l’intégration uniquement pour effectuer des actions, désactivez **Apporte des signaux** dans **Détails**.

## Ce que l’intégration peut faire

Quand une tâche ou une réunion nécessite le texte d’une page, votre Machine lit cette page, uniquement pendant qu’elle travaille dessus. Pour les fichiers de cette page, elle ne voit que leur nom. Elle recherche les pages par leur titre, pas les fichiers qu’elles contiennent.

Chacune de ces actions attend votre accord dans la tâche correspondante :

- Répondre à un commentaire dans la discussion correspondante.
- Créer une page. Elle reste privée tant que vous ne la partagez pas.
- Modifier une page. Appuyez sur **Relire les modifications** pour voir chaque paragraphe avant et après, puis sur **Enregistrer**. Les modifications sont écrites uniquement dans la page telle que vous l’avez vue. Si quelqu’un l’a modifiée entre-temps, rien n’est écrit et la tâche vous en informe.
- Marquer comme faite une tâche qui vous est attribuée. Seul son statut change.

L’intégration ne supprime, ne partage ni ne déplace jamais de page.

## Connecter l’intégration

1. Dans le tableau de bord : **Connexions**, **Documents et fichiers**, Notion. Ou, sur une Machine hébergée, dans la page de configuration à l’adresse app.themachine.computer/setup : **Autres sources**, Notion. Sur votre propre ordinateur, associez d’abord l’intégration à votre compte.
2. Appuyez sur **Se connecter avec Notion**, choisissez votre espace de travail et les pages auxquelles l’intégration peut accéder, puis autorisez l’accès.
3. De retour dans The Machine, la connexion est vérifiée immédiatement et le nom de l’espace de travail s’affiche.

Pour un autre espace de travail, ajoutez à nouveau Notion.

## Coller un jeton à la place

Sous **Ou collez un jeton d’intégration**, appuyez sur **Obtenir votre jeton**. Notion ouvre sa page des intégrations : créez une intégration interne, autorisez la lecture et l’ajout de contenu et de commentaires, ainsi que la lecture des informations utilisateur avec les adresses e-mail. Copiez son jeton, collez-le, puis appuyez sur **Connecter**.

Partagez ensuite vos pages avec cette intégration dans Notion, sous **Connexions** sur chaque page. Sur votre propre ordinateur, `assistant connect notion` le demande également.

## Retirer l’intégration

- Dans le tableau de bord : **Connexions**, ouvrez Notion, puis **Détails** et **Déconnecter**. Les éléments déjà importés restent.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de Notion dans la page de configuration.

## Révoquer l’accès dans Notion

Dans Notion : **Paramètres**, **Connexions**, puis déconnectez The Machine. Pour un jeton collé : supprimez l’intégration sur la page des intégrations.
