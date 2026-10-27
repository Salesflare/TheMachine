---
title: Niveaux de sécurité
area: security
summary: Un seul choix, Standard ou Prudent, règle vos paramètres de sécurité et de confidentialité. L’admin d’une Fleet Travail en choisit un pour la Fleet.
covers: settings:security
code: security_levels.py, dashboard.html, fleet.py
order: 2
---
## Deux niveaux

Ouvrez **Paramètres**, puis **Sécurité**.

- **Standard** : les réglages par défaut actuels. Rien ne change.
- **Prudent** : plus strict, quand vous voulez moins de choses sur votre téléphone et moins de données conservées.

Un niveau est un point de départ. Changez un paramètre ensuite, et le niveau affiche **Personnalisé**. Choisissez à nouveau un niveau pour tout réinitialiser.

## Ce que Prudent change pour vous

- **Texte dans les notifications** désactivé : une notification indique « Nouvelle tâche » ou « Prête », pas le contenu de la tâche.
- **Proposer d’enregistrer les identifiants** désactivé. Les sites connectés que vous avez enregistrés restent jusqu’à ce que vous appuyiez sur **Oublier tous les identifiants enregistrés**.
- **Rechercher les contacts pro**, **Proposer de partager des apprentissages** et **Partager ce qu’on demande à l’aide** désactivés.
- **Garder les détails de Faire 90 jours** désactivé : ils sont gardés 30 jours.
- Dans une Famille, les disponibilités vous sont d’abord demandées. Avec les Amis, le contexte des réunions est refusé.

## Le niveau d’une Fleet Travail

Le propriétaire ou un admin de la Fleet le choisit sur la page du compte, sous les paramètres de la Fleet. Tous les membres de la Fleet le voient. Quand il est sur Prudent :

- Les réponses aux collègues attendent votre accord, sans noms, et seulement sur des personnes de vos comptes de travail.
- Les présentations et les transferts vous attendent aussi.
- Le Graph d’équipe partage les e-mails clients sans leurs pièces jointes.
- Les notifications des tâches de travail n’affichent aucun texte.
- Les contacts pro ne sont pas recherchés.
- Tout le monde se reconnecte tous les 7 jours.
- Un lien d’invitation ne fonctionne que pour l’adresse e-mail à laquelle il a été envoyé.

Les membres peuvent être plus stricts que la Fleet, pas moins. Leurs propres choix sont gardés, et reviennent si la Fleet repasse sur Standard.

## Pareil dans les deux

Rien n’est envoyé sans votre accord : vous voyez chaque brouillon et appuyez sur Envoyer. Faire et les agents de code fonctionnent de la même façon. La connexion demande toujours un code d’authentification ou une clé d’accès.
