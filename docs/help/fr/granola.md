---
title: Granola
area: connections
summary: Notes et transcriptions de vos réunions dans Granola. Lecture seule.
covers: connector:granola
code: connectors/granola.py, meeting_notes.py, onboarding.py
site: Connect, More sources, Remove
translated: fb6244142af7800d
---
## Ce que l’intégration lit

Les notes et transcriptions des réunions auxquelles vous avez participé dans Granola : celles des 7 derniers jours au moment de la connexion, puis les nouvelles au fur et à mesure. Les notes encore en cours de rédaction sont importées une fois que Granola les a terminées.

Chaque élément est associé à la réunion correspondante dans votre agenda, celle que Granola a nommée ou, à défaut, la réunion prévue au même moment. Les notes de Granola apparaissent sous Notes, et la transcription sous Transcription, avec la mention **Depuis Granola**. Ce que vous avez ajouté vous-même reste en place.

Après la réunion, The Machine lit ces éléments pour repérer ce qui a été promis, décidé ou reste à faire, comme « Je vous envoie le diaporama », et crée des tâches uniquement pour les prochaines étapes clairement définies. Les personnes présentes à la réunion sont associées à votre [Graph](graph.md) à l’aide de leur adresse e-mail.

## Ce que l’intégration peut faire

Aucune action dans Granola. L’intégration se contente de lire et ne modifie, ne partage ni ne supprime jamais de notes.

## Ce que l’intégration demande

Une clé API personnelle Granola. Granola propose des clés API avec ses forfaits Business et Enterprise. La clé permet de lire vos notes et celles qui sont partagées avec vous, telles qu’elles apparaissent dans Granola.

## Connecter Granola

1. Dans l’application de bureau Granola : **Paramètres**, **Connecteurs**, **Clés API**. Créez une clé avec l’accès aux notes personnelles et copiez-la.
2. Dans le tableau de bord : **Connexions**, **Réunions**, Granola. Ou, sur la page de configuration d’une Machine hébergée, à l’adresse app.themachine.computer/setup : **Plus de sources**, Granola. Sur votre propre ordinateur, `assistant connect granola` vous la demande aussi.
3. Collez la clé, choisissez **Travail** ou **Perso**, puis appuyez sur **Connecter**.

La clé est vérifiée immédiatement. Si Granola la refuse par la suite, la connexion Granola dans **Connexions** vous demandera une nouvelle clé.

## Supprimer la connexion

- Dans le tableau de bord : **Connexions**, ouvrez Granola, puis **Détails** et **Déconnecter**. Les données déjà importées restent en place.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté de Granola sur la page de configuration.

## Révoquer la clé dans Granola

Dans l’application de bureau Granola : **Paramètres**, **Connecteurs**, **Clés API**, puis supprimez la clé.
