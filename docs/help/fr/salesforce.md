---
title: Salesforce
area: connections
summary: Deals, tâches et activité de Salesforce sur vos contacts et projets. Si vous l’activez, il tient les coordonnées à jour là-bas.
covers: connector:salesforce
code: connectors/salesforce.py, crm_sync.py, onboarding.py
site: Connect Salesforce, More sources, Remove, Sign in with Salesforce
---
## Ce qu’il lit

Les nouveaux deals, et les deals qui changent d’étape ou de montant. Vos tâches ouvertes, les appels et autres tâches enregistrés comme faits avec des notes, et les réunions avec une description. Les 7 derniers jours à la connexion, puis les nouveaux toutes les 15 minutes.

Chaque deal devient un projet dans votre Graph, et ses contacts apparaissent sur leur fiche, comme contact Salesforce chez leur compte.

## Ce qu’il peut modifier

Rien, tant que vous n’activez pas **Mettre à jour les coordonnées**. Votre connexion Salesforce reste sur votre Machine.

## Le connecter

Sur une Machine hébergée :

1. Ouvrez votre page de configuration sur app.themachine.computer/setup et allez dans **Plus de sources**.
2. Ouvrez Salesforce et appuyez sur **Connecter Salesforce**.
3. Connectez-vous à Salesforce et autorisez The Machine (créée par Salesflare).

Ou dans le tableau de bord : **Connexions**, **+ Ajouter**, choisissez Salesforce et appuyez sur **Se connecter avec Salesforce**.

Votre utilisateur Salesforce a besoin de l’accès API, inclus dans la plupart des éditions.

## Mettre à jour les coordonnées

Quand votre Machine connaît des coordonnées plus récentes pour l’un de vos contacts Salesforce, elle peut mettre ce contact à jour là-bas : poste, téléphone, et le lien LinkedIn si votre org a un champ LinkedIn sur les contacts.

1. Dans **Connexions**, ouvrez Salesforce et appuyez sur **Voir ce qui changerait**.
2. Vérifiez la liste, puis appuyez sur **Activer** ou **Pas maintenant**.

Ce qu’elle respecte :

- Seulement des coordonnées dans les propres mots de la personne, comme son profil LinkedIn ou Slack, ou celles que vous avez saisies sur sa fiche. Jamais une supposition.
- Seulement si la coordonnée est plus récente que la dernière modification du contact dans Salesforce. Une modification faite là-bas l’emporte.
- Seulement les champs qui diffèrent, et jamais une valeur vide. Elle ne change jamais l’adresse e-mail ni le compte.
- Chaque modification est une ligne datée sur la fiche de la personne.

Appuyez sur **Désactiver** pour arrêter. Une connexion partagée par votre Fleet ne fait que lire.

## Le retirer

- Dans le tableau de bord : **Connexions**, ouvrez Salesforce, **Détails**, puis **Déconnecter**. Ce qu’il a déjà importé reste.
- Sur une Machine hébergée, vous pouvez aussi appuyer sur **Retirer** à côté sur votre page de configuration.

## Le révoquer dans Salesforce

Dans Salesforce, ouvrez vos paramètres personnels, puis Connected Apps OAuth Usage, ou demandez à votre admin, et révoquez The Machine. Elle ne peut alors plus rien lire ni modifier.
