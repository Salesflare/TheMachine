---
title: Paramètres
area: settings
summary: Où trouver chaque paramètre, du mode clair à la sécurité et à votre compte.
covers: settings:general
code: dashboard.html
order: 1
translated: 31820c6221312d35
---
Ouvrez **Paramètres** avec l’engrenage en haut. Voici ses onglets :

- **Compte** : **Vos adresses** (celles qui sont considérées comme les vôtres) et **Se déconnecter**, en haut. Sur une Machine hébergée, vous trouverez aussi votre forfait, vos factures, Fleet, vos amis, la connexion et vos données, avec **Résilier le forfait** et **Supprimer le compte** tout en bas. Sur une Machine installée sur votre ordinateur et associée au Network : votre Fleet, votre nom d’utilisateur, vos amis et la connexion, chacun avec un lien vers la partie correspondante de votre compte (où vous connecter), ainsi que **Supprimer le compte** en bas. Si votre Machine n’est pas encore associée : **Rejoindre le Network**, en haut. Consultez [Forfaits et facturation](plans-and-billing.md).
- **Général** : la langue et la région, cet appareil, la saisie vocale, le navigateur de votre Machine, votre Fleet, l’exportation et l’importation, ainsi que la version utilisée. S’il n’y a pas d’onglet Compte, **Rejoindre le Network** se trouve tout en bas.
- **Sécurité** : Standard ou Prudent. Consultez [Niveaux de sécurité](security-levels.md). Vous y trouverez aussi **Accès du support** lorsqu’il est activé : consultez [Contacter le support](get-support.md#support-access).
- **Activité** : tout ce que The Machine a fait pour vous, du plus récent au plus ancien. Consultez [Activité](activity.md).
- **Notifications** : où vous les recevez, et vos heures de travail. Consultez [Notifications](notifications.md) et [Heures de travail](work-hours.md).
- **Rédaction** : vos signatures et votre façon d’écrire. Consultez [Rédaction](writing.md).
- **Compétences** : les guides que votre Machine suit. Consultez [Compétences](skills.md).
- **Applis** : les applis de The Machine pour votre téléphone et votre ordinateur, puis Claude, ChatGPT et les autres IA que vous avez connectées, ainsi que les actions autorisées pour chacune. Consultez [L’app mobile](mobile-app.md) et [Connecter d’autres IA](ai-connections.md).
- **Modèle** : l’IA qui lit et rédige pour vous, ainsi que ses limites. Consultez [Modèle](model.md). Vous y trouverez aussi **Codex et Claude Code** : consultez [Transférer à Claude Code ou Codex](hand-to-agent.md). Et **Recherche par le sens**, plus bas.

Un onglet sans contenu est masqué.

## Général

- **Langue et région** : votre **Région** détermine l’affichage des dates, des heures et des nombres (24 oct. ou oct. 24). **Format de l’heure** permet de choisir le format 12 heures (2:05 PM) ou 24 heures (14:05). Les tâches, Telegram, le récap et les messages Fleet utilisent ces deux paramètres. Une Machine hébergée utilise le fuseau horaire choisi lors de l’inscription.
- **Langue** : English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 ou Русский. La langue de votre navigateur est utilisée par défaut. Le tableau de bord, l’aide, les notifications, Telegram, le récap hebdo et les tâches rédigées par votre Machine changent dès que vous faites votre choix. Les anciens textes ne changent pas. Les membres de l’équipe reçoivent les questions Fleet Travail et Fleet Famille dans leur langue, et les brouillons destinés à d’autres personnes restent dans la langue de leur conversation.
- **Cet appareil** : **Installer l’app**, **Notifications** avec **Envoyer un test**, et **Mode clair**, pour ce navigateur ou ce téléphone uniquement. Consultez [Installer l’app et activer les notifications](phone-app.md). Sur [Omarchy](omarchy.md), vous trouverez aussi **Thème Omarchy**.
- **Saisie vocale** : comment vos paroles sont converties en texte et quelle voix est utilisée pour Talk live. Consultez [Saisie vocale](voice-input.md) et [Parler en direct](talk-live.md).
- **Ouvrir le navigateur de la Machine ↗** : le navigateur utilisé par votre Machine pour des sites comme LinkedIn.
- **Règles Fleet** : consultez [Règles de partage](sharing-rules.md).
- **Exporter** :
  - **Tout** : toutes les connaissances de votre Machine dans un seul fichier chiffré, à transférer ou à conserver, et **Importer** pour en importer un. Consultez [Passer sur un autre ordinateur](moving.md).
  - **Connaissances pour une autre IA** : ce que votre Machine a appris, dans des fichiers lisibles par toutes les IA. Consultez [Connaissances pour une autre IA](knowledge-export.md).

## Version

La version utilisée par votre Machine. Les mises à jour s’installent automatiquement. Quand une nouvelle version est prête sur une Machine hébergée, **Mettre à jour** l’installe immédiatement. L’opération prend quelques minutes et vos données sont conservées.

Sur votre ordinateur, une tâche planifiée quotidienne installe chaque nouvelle version signée sous Linux. Consultez [Lancer The Machine sur votre propre ordinateur](self-hosted-setup.md).

## Recherche par le sens

Dans **Paramètres**, sous **Modèle**. Cette fonction recherche des e-mails, des messages et des notes selon leur sujet, et pas seulement selon les mots qu’ils contiennent. Sur une Machine hébergée, une petite IA installée directement sur la Machine s’en charge, sans envoyer de données ailleurs. Elle est activée à partir de 8 Go de mémoire. Avec 4 Go, activez-la à l’aide de son interrupteur. Elle utilise environ 500 Mo : une Machine très sollicitée peut donc ralentir. Lorsqu’elle est désactivée, la préparation d’une tâche recherche quand même les messages associés, à partir de leurs mots.

Sur votre ordinateur, il s’agit du bloc `embeddings` dans `config.json`. Redémarrez la Machine après toute modification.

## Sur cette Machine

Lorsque votre Machine fonctionne sur votre ordinateur, quelques opérations s’effectuent directement dans un terminal :

- Le fichier de paramètres, `config.json` : tous les paramètres réunis au même endroit. Redémarrez la Machine après toute modification.
- `assistant connect` : ajouter une source, comme `assistant connect gmail` ou `assistant connect outlook`.
- `assistant telegram on` ou `off` : les messages sur Telegram. Consultez [Telegram](telegram.md).
- `assistant doctor` : vérifie tout et affiche une solution pour chaque problème.

## Vos adresses

Toutes les adresses que votre Machine a trouvées : vos comptes, vos alias Gmail ou Outlook, votre agenda, vos profils Slack et Intercom. Les e-mails et les réunions associés à ces adresses sont considérés comme les vôtres. **Retirer** celles qui ne vous appartiennent pas.

Une adresse partagée, comme info@ ou un Google Group, n’est jamais considérée comme la vôtre par défaut. Les adresses dont votre Machine n’est pas sûre apparaissent dans **Peut-être à vous**. Choisissez une option :

- **À moi : personne d’autre n’y répond** : l’adresse est considérée comme la vôtre. Les e-mails qui y sont envoyés peuvent devenir vos tâches.
- **À l’équipe : d’autres y répondent aussi** : l’adresse ne vous est pas attribuée. Les e-mails envoyés uniquement à cette adresse ne génèrent ni tâches ni brouillons pour vous. Ils alimentent tout de même le Graph.
- **Pas à moi** : l’adresse ne sera pas considérée comme la vôtre.

Choisissez selon la personne qui répond aux messages aujourd’hui. Une boîte d’équipe comme support@ appartient à l’équipe. Une adresse comme partnerships@, à laquelle vous êtes la seule personne à répondre, vous appartient. Changez le réglage dès que d’autres personnes commencent aussi à répondre.

**Modifier** sur la ligne correspondante permet de changer le réglage plus tard. Votre propre adresse de connexion vous appartient toujours.

### Les domaines de votre entreprise

Les domaines de vos propres adresses sont considérés comme ceux de votre entreprise. Vous utilisez aussi un autre domaine, comme acme.co en plus de acme.com ? Saisissez-le sous **Les domaines de votre entreprise**, puis appuyez sur **Ajouter**.

Les personnes qui utilisent ces domaines sont alors considérées comme des collègues, jamais comme des clients : leurs conversations n’apparaissent pas dans le Team Graph et aucune organisation n’est créée pour elles. **Retirer** permet de supprimer à nouveau un domaine. Les domaines de messagerie gratuits comme gmail.com ne peuvent pas être ajoutés.

Un alias Gmail qui vous appartient peut aussi être utilisé dans le champ **From** d’un brouillon, si Gmail confirme que vous pouvez envoyer des e-mails avec cette adresse. Consultez [Gmail](gmail.md#what-it-can-send).
