---
title: Paramètres
area: settings
summary: Où trouver chaque paramètre, du mode clair à la sécurité et à votre compte.
covers: settings:general
code: dashboard.html
order: 1
---
Ouvrez **Paramètres** avec la roue dentée en haut. Ses onglets :

- **Compte** : **Vos adresses**, celles qui comptent comme vous, avec leur provenance. Votre forfait en bref, des boutons vers les pages de votre compte, et **Se déconnecter**. Voir [Forfaits et facturation](plans-and-billing.md).
- **Général** : langue et région, cet appareil, le navigateur de votre Machine, votre Fleet et votre compte.
- **Sécurité** : Standard ou Prudent, et les paramètres qu’ils règlent. Voir [Niveaux de sécurité](security-levels.md). **Accès du support** aussi, tant qu’il est actif : voir [Obtenir de l’aide](get-support.md#support-access).
- **Activité** : tout ce que The Machine a fait pour vous, le plus récent d’abord. Voir [Activité](activity.md).
- **Notifications** : ce qui vous parvient et où, et vos heures de travail. Voir [Notifications](notifications.md) et [Heures de travail](work-hours.md).
- **Rédaction** : signatures et votre façon d’écrire. Voir [Rédaction](writing.md).
- **Compétences** : les modes d’emploi que suit votre Machine. Voir [Compétences](skills.md).
- **Modèle** : ce qui répond pour vous, et ses limites. Voir [Modèle](model.md). **Codex et Claude Code** aussi : voir [Transférer à Claude Code ou Codex](hand-to-agent.md).

Un onglet sans rien à afficher est masqué.

## Général

- **Langue et région** : votre **Région** règle l’affichage des dates (Oct 24 ou 24 oct.) et l’horloge habituelle. **Format de l’heure** choisit plutôt 12 heures (2:05 PM) ou 24 heures (14:05). Les tâches, Telegram, le récap et les messages de la Fleet le suivent. Une Machine hébergée part du pays du fuseau horaire choisi à l’inscription. Les durées comme « il y a 3 heures » et les nombres le suivent aussi.
- **Langue** : English, Nederlands, Français, Deutsch, Español, Italiano ou Português (Brasil). La première fois que vous ouvrez le tableau de bord, il prend la langue de votre navigateur, si c’est l’une de celles-ci (le portugais du Portugal reçoit pour l’instant le portugais du Brésil). Le tableau de bord, les dates, les messages Telegram, les notifications, le récap hebdomadaire et les notes et titres de tâches que votre Machine écrit pour vous la suivent, dès que vous la choisissez ; ce qui était déjà écrit reste tel quel. Les questions de Fleet et de Famille s’affichent dans la langue de chaque membre. Les brouillons destinés à d’autres personnes restent dans la langue de leur conversation. L’Aide et ses pages la suivent aussi.
- **Cet appareil** : l’app (**Installer l’app**), **Notifications** avec **Envoyer un test**, et **Mode clair**, seulement pour ce navigateur ou ce téléphone. Voir [Installer l’app et activer les notifications](phone-app.md).
- **Ouvrir le navigateur de la Machine ↗** : le navigateur que votre Machine utilise pour des sites comme LinkedIn.
- **Règles Fleet** : voir [Règles de partage](sharing-rules.md).
- **Compte** : **Ouvrir le compte** et **Se déconnecter**, sur une Machine hébergée.

## Sur cette Machine

Quelques paramètres se trouvent sur l’ordinateur où tourne votre Machine, pas dans l’app :

- `config.json` : tous les paramètres, dans un seul fichier. Redémarrez la Machine après un changement.
- `assistant connect` : ajouter une source, comme `assistant connect gmail` ou `assistant connect outlook`.
- `assistant telegram on` ou `off` : les messages sur Telegram. Voir [Telegram](telegram.md).
- `assistant doctor` : vérifie tout et affiche une solution pour chaque problème.

## Vos adresses

Toutes vos adresses que la Machine a trouvées : vos comptes, vos alias Gmail ou Outlook, votre agenda, votre profil Slack et Intercom. Les e-mails et réunions de chacune apparaissent comme venant de vous. **Retirer** celle qui n’est pas à vous.

Une adresse partagée, comme info@ ou un Google Group, ne compte jamais d’elle-même. Celle dont la Machine n’est pas sûre est sous **Peut-être à vous**, et rien n’est choisi à votre place. Choisissez :

- **À moi : personne d’autre n’y répond** : elle compte comme la vôtre. Les e-mails qui y arrivent peuvent devenir vos tâches.
- **À l’équipe : d’autres y répondent aussi** : ce n’est pas vous. Un e-mail envoyé seulement à cette adresse ne crée ni tâche ni brouillon pour vous. Elle alimente toujours le Graph, partagé avec votre équipe comme avant.
- **Pas à moi** : elle ne compte pas comme la vôtre.

Choisissez selon qui y répond aujourd’hui. Une boîte d’équipe comme support@ est à l’équipe. Une adresse comme partnerships@ à laquelle personne d’autre ne répond pour l’instant est à vous ; passez-la à l’équipe dès que d’autres y répondent aussi.

**Modifier** sur sa ligne change ce choix plus tard. Votre propre adresse de connexion est toujours la vôtre.

### Les domaines de votre entreprise

Les domaines de vos propres adresses comptent comme ceux de votre entreprise. Si elle en utilise un autre, comme acme.co à côté d’acme.com, saisissez-le sous **Les domaines de votre entreprise** et appuyez sur **Ajouter**.

Les personnes de ce domaine sont alors vos collègues, jamais des clients : leurs fils restent hors du Team Graph comme tout fil entre collègues, et aucune organisation n’est créée. **Retirer** l’enlève. Un domaine d’e-mail gratuit comme gmail.com ne peut pas être ajouté.
