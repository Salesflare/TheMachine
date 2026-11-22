---
title: Salesforce
area: connections
summary: Les affaires, tâches et activités Salesforce liées à vos contacts et projets. The Machine peut aussi tenir à jour les coordonnées des contacts, si vous activez cette option.
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
translated: eee5e084bac6dbd1
---
## Ce que The Machine consulte

Les nouvelles affaires, ainsi que celles qui passent à une autre étape ou dont le montant change. Vos tâches en cours, vos appels et les autres tâches marquées comme faites avec des notes, ainsi que les réunions avec une description. Les 7 derniers jours au moment de la connexion, puis les nouvelles données toutes les 15 minutes.

Chaque affaire devient un projet dans votre Graph, et les contacts qui y sont associés apparaissent sur leur fiche, comme contacts Salesforce rattachés à leur compte.

## Ce que The Machine peut modifier

Rien, tant que vous n’activez pas **Mettre à jour les coordonnées**. Vos identifiants Salesforce restent sur votre Machine.

## Connecter Salesforce

Sur une Machine hébergée :

1. Ouvrez votre page de configuration sur app.themachine.computer/setup et accédez à **Plus de sources**.
2. Ouvrez Salesforce et sélectionnez **Connecter Salesforce**.
3. Connectez-vous à Salesforce et autorisez The Machine (créée par Salesflare).

Ou dans le tableau de bord : **Connexions**, **Clients**, choisissez Salesforce et sélectionnez **Se connecter avec Salesforce**. Sur votre propre ordinateur, associez d’abord votre Machine à votre compte.

Votre utilisateur Salesforce doit disposer d’un accès à l’API, inclus dans la plupart des éditions.

## Mettre à jour les coordonnées

Lorsque votre Machine dispose de coordonnées plus récentes pour l’un de vos contacts Salesforce, elle peut les mettre à jour : fonction, téléphone et lien LinkedIn si votre organisation dispose d’un champ LinkedIn sur les contacts.

1. Dans **Connexions**, ouvrez Salesforce et sélectionnez **Voir ce qui changerait**.
2. Vérifiez la liste, puis sélectionnez **Activer** ou **Pas maintenant**.

Voici les règles appliquées :

- Uniquement les informations que la personne a données elle-même, par exemple sur son profil LinkedIn ou Slack, ou celles que vous avez ajoutées à sa fiche. Aucune supposition.
- Uniquement si l’information est plus récente que la dernière modification du contact dans Salesforce. Toute modification faite dans Salesforce est prioritaire.
- Uniquement les champs qui diffèrent, et jamais un champ vide. L’adresse e-mail et le compte ne sont jamais modifiés.
- Chaque modification apparaît sous forme de ligne datée sur la fiche de la personne.

Sélectionnez **Désactiver** pour arrêter. Une connexion partagée par votre Fleet ne fait que consulter les données.

## Supprimer la connexion

- Dans le tableau de bord : **Connexions**, ouvrez Salesforce, sélectionnez **Détails**, puis **Déconnecter**. Les données déjà importées restent.
- Sur une Machine hébergée, sélectionnez **Déconnecter ↗** pour ouvrir votre page de configuration, puis sélectionnez **Retirer** à côté de Salesforce.

## Révoquer l’accès dans Salesforce

Dans Salesforce, ouvrez vos paramètres personnels, puis Connected Apps OAuth Usage, ou demandez à votre administrateur de révoquer l’accès de The Machine. Elle ne pourra alors plus consulter ni modifier aucune donnée.
