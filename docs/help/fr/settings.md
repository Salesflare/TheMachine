---
title: Paramètres
area: settings
summary: Où trouver chaque paramètre, du mode clair à la sécurité et à votre compte.
covers: settings:general
code: dashboard.html
order: 1
translated: 4b0cf1cc99529e64
---
Ouvrez **Paramètres** avec la roue dentée en haut. Voici les onglets :

- **Compte** : **Vos adresses** (celles qui sont reconnues comme étant les vôtres) et **Se déconnecter**, en haut. Sur une Machine hébergée, vous trouverez aussi votre forfait, vos factures, Fleet, vos amis, vos connexions et vos données, avec **Résilier le forfait** et **Supprimer le compte** tout en bas. Sur une Machine installée sur votre ordinateur et associée au Network, vous trouverez Fleet, votre nom d’utilisateur, vos amis et vos connexions, chacun avec un lien qui ouvre la partie correspondante de votre compte (connectez-vous sur cette page), ainsi que **Supprimer le compte** en bas. Si elle n’est pas encore associée au Network, **Rejoindre le Network** apparaît en haut. Consultez [Forfaits et facturation](plans-and-billing.md).
- **Général** : la langue et la région, cet appareil, la saisie vocale, le navigateur de votre Machine, votre Fleet, l’exportation et l’importation, ainsi que la version utilisée. Sans onglet Compte, **Rejoindre le Network** apparaît à la fin.
- **Sécurité** : Standard ou Prudent. Consultez [Niveaux de sécurité](security-levels.md). Vous trouverez aussi **Accès du support** lorsqu’il est activé : consultez [Obtenir de l’aide](get-support.md#support-access).
- **Activité** : tout ce que The Machine a fait pour vous, du plus récent au plus ancien. Consultez [Activité](activity.md).
- **Notifications** : ce que vous recevez et où, ainsi que vos heures de travail. Consultez [Notifications](notifications.md) et [Heures de travail](work-hours.md).
- **Rédaction** : vos signatures et votre façon d’écrire. Consultez [Rédaction](writing.md).
- **Compétences** : les guides que suit votre Machine. Consultez [Compétences](skills.md).
- **Applis** : les applis de The Machine pour votre téléphone et votre ordinateur, puis Claude, ChatGPT et les autres IA que vous avez connectées, et ce que chacune peut faire. Consultez [L’application mobile](mobile-app.md) et [Connecter d’autres IA](ai-connections.md).
- **Modèle** : l’IA qui lit et rédige pour vous, et ses limites. Consultez [Modèle](model.md). Vous trouverez aussi **Codex et Claude Code** : consultez [Transmettre à Claude Code ou Codex](hand-to-agent.md). Et **Recherche par le sens**, plus bas.

Un onglet sans contenu est masqué.

## Général

- **Langue et région** : votre **Région** détermine le format des dates, des heures et des nombres (24 oct. ou 24 oct.). **Format de l’heure** permet de choisir entre le format sur 12 heures (2:05 PM) et celui sur 24 heures (14:05). Les tâches, Telegram, le récap et les messages Fleet utilisent ces deux paramètres. Une Machine hébergée utilise le fuseau horaire choisi lors de l’inscription.
- **Langue** : English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 ou Русский. La langue de votre navigateur est utilisée par défaut. Le tableau de bord, l’aide, les notifications, Telegram, le récap hebdomadaire et les tâches rédigées par votre Machine changent dès que vous choisissez une langue. Les textes plus anciens restent tels quels. Les questions Fleet et Family sont envoyées à vos collègues dans leur langue, et les brouillons destinés à d’autres personnes restent dans la langue de leur conversation.
- **Cet appareil** : **Installer l’app**, **Notifications** avec **Envoyer un test**, et **Mode clair**, uniquement pour ce navigateur ou ce téléphone. Consultez [Installer l’app et activer les notifications](phone-app.md). Sur [Omarchy](omarchy.md), vous trouverez aussi **Thème Omarchy**.
- **Saisie vocale** : comment vos paroles sont converties en texte et quelle voix est utilisée pour Talk live. Consultez [Saisie vocale](voice-input.md) et [Talk live](talk-live.md).
- **Ouvrir le navigateur de la Machine ↗** : le navigateur utilisé par votre Machine pour des sites comme LinkedIn.
- **Règles Fleet** : consultez [Règles de partage](sharing-rules.md).
- **Exporter** :
  - **Tout** : tout ce que sait votre Machine, dans un seul fichier chiffré, à transférer ou à conserver, et **Importer** pour en importer un. Consultez [Passer à un autre ordinateur](moving.md).
  - **Connaissances pour une autre IA** : ce que votre Machine a appris, dans des fichiers lisibles par n’importe quelle IA. Consultez [Connaissances pour une autre IA](knowledge-export.md).

## Version

La version utilisée par votre Machine. Les mises à jour s’installent automatiquement. Lorsqu’une nouvelle version est disponible sur une Machine hébergée, **Mettre à jour** l’installe immédiatement. L’opération prend quelques minutes et vos données sont conservées.

Sur votre propre ordinateur, une minuterie quotidienne installe chaque nouvelle version signée sous Linux. Consultez [Installer la Machine sur votre propre ordinateur](self-hosted-setup.md).

## Recherche par le sens

Dans **Paramètres**, sous **Modèle**. Cette fonction trouve des e-mails, des messages et des notes selon leur sujet, pas seulement selon les mots utilisés. Sur une Machine hébergée, une petite IA intégrée à la Machine effectue la recherche, sans rien envoyer ailleurs. La fonction est activée à partir de 8 Go de mémoire. Avec 4 Go, activez-la à l’aide de son interrupteur. Elle utilise environ un demi-gigaoctet, ce qui peut ralentir une Machine très sollicitée.

Sur votre propre ordinateur, c’est le bloc `embeddings` dans `config.json`. Redémarrez la Machine après toute modification.

## Sur cette Machine

Lorsque votre Machine fonctionne sur votre propre ordinateur, certaines opérations sont effectuées dans un terminal :

- Le fichier de paramètres, `config.json` : tous les paramètres au même endroit. Redémarrez la Machine après toute modification.
- `assistant connect` : ajouter une source, comme `assistant connect gmail` ou `assistant connect outlook`.
- `assistant telegram on` ou `off` : les messages sur Telegram. Consultez [Telegram](telegram.md).
- `assistant doctor` : tout vérifier et afficher une correction pour chaque problème.

## Vos adresses

Toutes les adresses que la Machine a trouvées : vos comptes, vos alias Gmail ou Outlook, votre calendrier, vos profils Slack et Intercom. Les e-mails et les réunions provenant de ces adresses sont considérés comme les vôtres. **Retirer** une adresse qui ne vous appartient pas.

Une adresse partagée, comme info@ ou un groupe Google, n’est jamais considérée comme la vôtre par défaut. Les adresses dont la Machine n’est pas sûre apparaissent sous **Peut-être à vous**. Choisissez l’une des options suivantes :

- **À moi : personne d’autre n’y répond** : l’adresse est considérée comme la vôtre. Les e-mails qui y sont envoyés peuvent devenir vos tâches.
- **À l’équipe : d’autres y répondent aussi** : l’adresse n’est pas considérée comme la vôtre. Les e-mails envoyés uniquement à cette adresse ne créent ni tâches ni brouillons pour vous. Ils alimentent tout de même le Graph.
- **Pas à moi** : l’adresse ne sera pas considérée comme la vôtre.

Choisissez selon la personne qui répond aux messages aujourd’hui. Une boîte d’équipe comme support@ appartient à l’équipe. Une adresse comme partnerships@, à laquelle vous êtes la seule personne à répondre, vous appartient. Modifiez ce choix si d’autres personnes commencent à y répondre.

L’option **Modifier** sur la ligne permet de changer ce choix plus tard. Votre adresse de connexion personnelle est toujours considérée comme la vôtre.

### Les domaines de votre entreprise

Les domaines de vos adresses personnelles sont considérés comme ceux de votre entreprise. Vous en utilisez aussi un autre, comme acme.co en plus de acme.com ? Saisissez-le sous **Les domaines de votre entreprise**, puis appuyez sur **Ajouter**.

Les personnes qui en font partie sont alors considérées comme des collègues, jamais comme des clients : leurs fils de discussion ne sont pas ajoutés au Graph de l’équipe, et aucune organisation n’est créée pour ce domaine. **Retirer** permet de le supprimer. Les domaines de messagerie gratuits comme gmail.com ne peuvent pas être ajoutés.

Un alias Gmail qui vous appartient peut aussi être indiqué comme **De** dans un brouillon, si Gmail confirme que vous pouvez envoyer des messages depuis cette adresse. Consultez [Gmail](gmail.md#what-it-can-send).
