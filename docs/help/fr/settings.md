---
title: Paramètres
area: settings
summary: Où trouver chaque paramètre, du mode clair à la sécurité et à votre compte.
covers: settings:general
code: dashboard.html
order: 1
translated: 4b0cf1cc99529e64
---
Ouvrez **Paramètres** avec la roue dentée en haut. Les onglets disponibles :

- **Compte** : **Vos adresses** (celles qui sont considérées comme les vôtres) et **Se déconnecter**, en haut. Sur une Machine hébergée, vous trouverez aussi votre forfait, vos factures, Fleet, vos amis, vos informations de connexion et vos données, avec **Résilier le forfait** et **Supprimer le compte** tout en bas. Sur une Machine installée sur votre ordinateur et associée au Network : votre Fleet, votre nom d’utilisateur, vos amis et vos informations de connexion, chacun avec un lien vers la section correspondante de votre compte (connectez-vous sur cette page), ainsi que **Supprimer le compte** tout en bas. Si elle n’est pas encore associée : **Rejoindre le Network**, en haut. Consultez [Forfaits et facturation](plans-and-billing.md).
- **Général** : la langue et la région, cet appareil, la saisie vocale, le navigateur de votre Machine, votre Fleet, l’exportation et l’importation, ainsi que la version utilisée. Si l’onglet Compte n’apparaît pas, **Rejoindre le Network** se trouve à la fin.
- **Sécurité** : Standard ou Prudent. Consultez [Niveaux de sécurité](security-levels.md). Vous trouverez aussi **Accès du support** tant qu’il est activé : consultez [Contacter le support](get-support.md#support-access).
- **Activité** : tout ce que The Machine a fait pour vous, du plus récent au plus ancien. Consultez [Activité](activity.md).
- **Notifications** : où vous recevez vos notifications et vos heures de travail. Consultez [Notifications](notifications.md) et [Heures de travail](work-hours.md).
- **Rédaction** : vos signatures et votre façon d’écrire. Consultez [Rédaction](writing.md).
- **Compétences** : les guides que suit votre Machine. Consultez [Compétences](skills.md).
- **Applis** : les applis de The Machine pour votre téléphone et votre ordinateur, puis Claude, ChatGPT et les autres IA que vous avez connectées, et ce que chacune peut faire. Consultez [L’app mobile](mobile-app.md) et [Connecter d’autres IA](ai-connections.md).
- **Modèle** : l’IA qui lit et rédige pour vous, et ses limites. Consultez [Modèle](model.md). Vous trouverez aussi **Codex et Claude Code** : consultez [Transférer à Claude Code ou Codex](hand-to-agent.md). Et **Recherche par le sens**, plus bas.

Un onglet sans contenu est masqué.

## Général

- **Langue et région** : votre **Région** détermine le format des dates, des heures et des nombres (Oct 24 ou 24 Oct). **Format de l’heure** permet de choisir le format sur 12 heures (2:05 PM) ou sur 24 heures (14:05). Les tâches, Telegram, le récap et les messages Fleet suivent ces deux paramètres. Une Machine hébergée utilise le fuseau horaire choisi lors de l’inscription.
- **Langue** : English, Nederlands, Français, Deutsch, Español, Italiano, Português (Brasil), 简体中文, 日本語, 한국어 ou Русский. La langue de votre navigateur est utilisée par défaut. Le tableau de bord, l’aide, les notifications, Telegram, le récap hebdomadaire et les tâches rédigées par votre Machine changent dès que vous choisissez une langue. Les anciens textes ne changent pas. Les membres de l’équipe reçoivent les questions Fleet et Famille dans leur propre langue, et les brouillons destinés à d’autres personnes restent dans la langue de leur conversation.
- **Cet appareil** : **Installer l’app**, **Notifications** avec **Envoyer un test**, et **Mode clair**, uniquement pour ce navigateur ou ce téléphone. Consultez [Installer l’app et activer les notifications](phone-app.md). Sur [Omarchy](omarchy.md), vous trouverez aussi **Thème Omarchy**.
- **Saisie vocale** : comment votre parole est convertie en texte et quelle voix est utilisée pour Parler en direct. Consultez [Saisie vocale](voice-input.md) et [Parler en direct](talk-live.md).
- **Ouvrir le navigateur de la Machine ↗** : le navigateur utilisé par votre Machine pour des sites comme LinkedIn.
- **Règles Fleet** : consultez [Règles de partage](sharing-rules.md).
- **Exporter** :
  - **Tout** : tout ce que votre Machine sait, dans un seul fichier chiffré, à transférer ou à conserver, et **Importer** pour en importer un. Consultez [Passer sur un autre ordinateur](moving.md).
  - **Connaissances pour une autre IA** : ce que votre Machine a appris, dans des fichiers lisibles par n’importe quelle IA. Consultez [Connaissances pour une autre IA](knowledge-export.md).

## Version

La version utilisée par votre Machine. Les mises à jour s’installent automatiquement. Quand une nouvelle version est disponible sur une Machine hébergée, **Mettre à jour** l’installe immédiatement. L’opération prend quelques minutes et vos données sont conservées.

Sur votre propre ordinateur, une tâche quotidienne installe chaque nouvelle version signée sous Linux. Consultez [Lancer The Machine sur votre propre ordinateur](self-hosted-setup.md).

## Recherche par le sens

Dans **Paramètres**, sous **Modèle**. Cette fonction trouve des e-mails, des messages et des notes selon leur sujet, et pas seulement selon les mots qu’ils contiennent. Sur une Machine hébergée, une petite IA exécutée directement sur la Machine s’en charge. Aucune donnée n’est envoyée ailleurs. La fonction est activée à partir de 8 Go de mémoire. Avec 4 Go, activez-la avec son interrupteur. Elle utilise environ un demi-gigaoctet. Une Machine très sollicitée peut donc ralentir.

Sur votre propre ordinateur, c’est le bloc `embeddings` dans `config.json`. Redémarrez la Machine après toute modification.

## Sur cette Machine

Quand votre Machine est installée sur votre propre ordinateur, quelques opérations se font sur celui-ci, dans un terminal :

- Le fichier de paramètres, `config.json` : tous les paramètres réunis au même endroit. Redémarrez la Machine après toute modification.
- `assistant connect` : ajoutez une source, comme `assistant connect gmail` ou `assistant connect outlook`.
- `assistant telegram on` ou `off` : les messages sur Telegram. Consultez [Telegram](telegram.md).
- `assistant doctor` : vérifie tout et affiche une correction pour chaque problème.

## Vos adresses

Toutes les adresses que la Machine a trouvées pour vous : vos comptes, vos alias Gmail ou Outlook, votre agenda, vos profils Slack et Intercom. Les e-mails et les réunions provenant de ces adresses sont considérés comme venant de vous. **Retirer** une adresse qui n’est pas la vôtre.

Une adresse partagée, comme info@ ou un Google Group, n’est jamais considérée comme la vôtre par défaut. Les adresses dont la Machine n’est pas sûre apparaissent sous **Peut-être à vous**. Choisissez une option :

- **À moi : personne d’autre n’y répond** : l’adresse est considérée comme la vôtre. Les e-mails qui y sont envoyés peuvent devenir vos tâches.
- **À l’équipe : d’autres y répondent aussi** : l’adresse n’est pas considérée comme la vôtre. Les e-mails envoyés uniquement à cette adresse ne génèrent pas de tâches ni de brouillons pour vous. Ils alimentent tout de même le Graph.
- **Pas à moi** : l’adresse ne sera pas considérée comme la vôtre.

Choisissez en fonction de la personne qui répond aux messages aujourd’hui. Une boîte d’équipe comme support@ appartient à l’équipe. Une adresse comme partnerships@ à laquelle vous êtes la seule personne à répondre est à vous. Modifiez ce choix dès que d’autres personnes y répondent aussi.

**Modifier** sur la ligne correspondante vous permet de changer ce choix plus tard. Votre propre adresse de connexion est toujours considérée comme la vôtre.

### Domaines de votre entreprise

Les domaines associés à vos propres adresses sont considérés comme ceux de votre entreprise. Vous en utilisez un autre aussi, comme acme.co en plus de acme.com ? Saisissez-le sous **Les domaines de votre entreprise**, puis appuyez sur **Ajouter**.

Les personnes qui utilisent ces domaines sont alors considérées comme des collègues, jamais comme des clients : leurs conversations n’apparaissent pas dans le Graph d’équipe et aucune organisation n’est créée pour elles. **Retirer** permet de supprimer un domaine. Les domaines de messagerie gratuits comme gmail.com ne peuvent pas être ajoutés.

Un alias Gmail qui vous appartient peut aussi être utilisé comme adresse **De** d’un brouillon, si Gmail confirme que vous pouvez envoyer des messages avec cette adresse. Consultez [Gmail](gmail.md#what-it-can-send).
