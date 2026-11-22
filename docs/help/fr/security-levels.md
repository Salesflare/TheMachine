---
title: Niveaux de sécurité
area: security
summary: Un seul commutateur, **Standard** ou **Prudent**, définit vos paramètres de sécurité et de confidentialité. L’admin d’une Fleet Travail choisit le niveau pour toute la Fleet.
covers: settings:security
code: security_levels.py, dashboard.html, fleet.py
order: 2
translated: cf3ba86c8c1a23f3
---
## Deux niveaux

Ouvrez **Paramètres**, puis **Sécurité**.

- **Standard** : les réglages par défaut actuels. Rien ne change.
- **Prudent** : des réglages plus stricts, si vous voulez moins de données sur votre téléphone et que moins de données soient conservées.

Un niveau sert de point de départ. Modifiez ensuite n’importe quel réglage et le niveau affichera **Personnalisé**. Choisissez de nouveau un niveau pour rétablir ses réglages.

## Ce que le niveau Prudent change pour vous

- **Texte dans les notifications** désactivé : une notification indique « Nouvelle tâche » ou « Prête », sans préciser le contenu de la tâche.
- **Proposer d’enregistrer les identifiants** désactivé. Les connexions enregistrées aux sites restent en place jusqu’à ce que vous appuyiez sur **Oublier tous les identifiants enregistrés**.
- **Rechercher les contacts pro**, **Proposer de partager des apprentissages** et **Partager ce qu’on demande à l’aide** désactivés.
- **Vérifier lesquels de mes contacts ont une Machine** et **Laisser les personnes qui ont mon e-mail me trouver** désactivés.
- **Garder les détails de Faire 90 jours** désactivé : ils sont conservés pendant 30 jours.
- **Ce que d’autres Machines peuvent demander à la mienne** réglé sur **Désactivé** : aucune planification avec d’autres Machines. Consultez [Les amis et le Network](friends.md#scheduling-with-other-machines).
- Dans une famille, le partage de vos disponibilités vous demande d’abord votre accord. Avec des amis, le contexte des réunions est refusé.

## Le niveau d’une Fleet Travail

Le propriétaire ou un admin de la Fleet le choisit dans les paramètres de la Fleet : dans **Paramètres** › **Compte**, appuyez sur **Fleet**. Tout le monde dans la Fleet peut le voir. Lorsque le niveau est Prudent :

- Les réponses destinées à vos collègues attendent votre accord, ne contiennent pas de noms et concernent uniquement des personnes issues de vos comptes professionnels.
- Les mises en relation et les transferts attendent aussi votre accord.
- Le Graph d’équipe partage les e-mails des clients sans leurs pièces jointes.
- Les notifications des tâches professionnelles n’affichent aucun texte.
- Les contacts professionnels ne sont pas recherchés.
- Votre Machine ne vérifie pas vos contacts sur le Network et ne permet pas qu’on vous trouve avec votre adresse e-mail, sauf si vous avez activé ces options vous-même.
- Tout le monde doit se reconnecter tous les 7 jours.
- Un lien d’invitation ne fonctionne qu’avec l’adresse e-mail à laquelle il a été envoyé.

Les membres peuvent choisir des réglages plus stricts que ceux de la Fleet, mais pas moins stricts. Leurs propres choix sont conservés et réappliqués si la Fleet revient à Standard.

## Ce qui ne change pas

Rien n’est envoyé sans votre accord : vous voyez chaque brouillon et appuyez sur **Envoyer**. **Faire** et les agents de programmation fonctionnent de la même manière. La connexion nécessite toujours un code d’authentification ou une clé d’accès.
