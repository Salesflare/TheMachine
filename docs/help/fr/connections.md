---
title: Connexions
area: connections
summary: Toutes vos sources au même endroit : leur état, comment en ajouter une ou en déconnecter une.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 809547189ccfa026
---
## État des connexions

L’onglet **Connexions** répertorie vos sources par catégorie, puis affiche **Connexions aux sites** et **Vérifications** sous une ligne. Sur un téléphone, touchez une catégorie pour l’ouvrir, puis **Connexions** pour revenir en arrière. La catégorie contenant une source qui nécessite votre attention s’ouvre en premier. Chaque source apparaît sur une ligne avec son état (Connectée, En attente de la première synchronisation, Reconnexion automatique ou Vous attend) et les derniers éléments reçus. Touchez-la pour ouvrir sa fiche et ses **Détails**.

Un échec de synchronisation compensé par une synchronisation ultérieure apparaît en gris. Seul un échec toujours récent apparaît comme un problème, avec la date de la prochaine tentative.

Les compteurs indiquent tout ce que la source a importé, y compris son [historique](history.md), ce qu’elle a importé au cours des dernières 24 heures et ce qui n’a pas encore été vérifié. Pour un agenda, ils comptent les événements.

Chaque source porte le nom que le service donne à son compte : votre adresse, un profil X, un espace de travail Slack ou la personne à qui appartient le compte Signal ou Telegram. Sous le nom : **Travail** ou **Perso** d’abord, puis l’adresse ou l’identifiant si le nom ne l’indique pas déjà. Si deux sources de la même catégorie ont le même nom, leur nom précise aussi ce qui les distingue, par exemple Slack ou X, ou l’adresse de l’espace de travail.

Chaque source indique aussi en une ligne ce qu’elle importe et, si elle peut agir, qu’elle ne le fait qu’après que vous avez appuyé sur **Envoyer** ou donné votre accord.

## Ajouter une source

Ouvrez une catégorie (**E-mail**, **Agenda**, **Chat**, **Réunions**, **Documents et fichiers**, **Clients**, **Projets et code**, **Autres**), puis choisissez une source sous **En ajouter un autre**, ou sous la liste si aucune source n’est encore connectée. Les options génériques se trouvent à la fin : **Autre e-mail** sous E-mail, **Lien d’agenda (ICS)** et **Autre agenda** sous Agenda. Exchange Server importe les réunions, il se trouve donc sous Agenda.

**Suggéré pour vous** apparaît en haut de **Connexions** lorsque votre Machine détecte une raison d’ajouter une source. Cette raison est indiquée en une ligne : des e-mails de Stripe, des réunions Zoom dans votre agenda, des messages contenant des liens vers Google Docs ou une configuration inachevée. La source reste aussi dans sa propre catégorie, marquée **Suggérée**. Ces éléments sont comptabilisés sur votre Machine et rien n’en sort. Une source connectée n’est jamais suggérée.

Microsoft Teams apparaît à deux endroits : sous **Chat** pour les chats, et sous **Réunions** sous le nom **Réunions Teams** pour les notes de réunion. Les deux utilisent la même connexion Microsoft. Connecter l’un connecte donc aussi l’autre.

La liste indique si vous avez déjà connecté une source, ainsi que le compte associé. Sélectionnez-la pour en ajouter une autre à côté : son formulaire l’indique et renvoie vers celle que vous avez déjà.

Saisissez les informations demandées (une clé, une adresse), choisissez **Travail** avec le nom de l’entreprise ou **Perso** (pour les e-mails et les agendas, ce choix n’est demandé que si l’adresse ne permet pas de le déterminer), puis appuyez sur **Se connecter**. Pour un site comme LinkedIn ou X, la page de connexion s’ouvre dans le navigateur de votre Machine et la procédure reprend automatiquement une fois la connexion établie. GitHub, WhatsApp et Codex affichent un code à saisir. Telegram et Signal affichent un code QR à scanner.

**Annuler** interrompt l’ajout. Vous avez quitté avant la fin ? Rouvrez **Connexions** sur n’importe quel appareil pour reprendre à l’étape où vous en étiez. Une fois la source connectée, votre Machine commence aussitôt à l’importer et vous indique l’état de la première synchronisation.

Sur une Machine hébergée, les sources qui ont leur propre connexion se connectent directement ici : Google, Microsoft (Outlook, OneDrive et Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce et Trello.

Choisissez **Travail** ou **Perso**, puis appuyez sur le bouton de connexion, par exemple **Se connecter avec Google**. Vous revenez à ce formulaire, qui indique le résultat. GitHub, WhatsApp, Codex, Telegram et votre téléphone Android affichent aussi leur code ici.

Sur votre propre ordinateur, ces mêmes sources se connectent une fois votre Machine associée à votre compte : la première fois, appuyez sur **Associer cette Machine**. Certaines proposent aussi une autre méthode, comme votre propre application ou une clé.

Le bouton **Reconnecter**, sur une source ou dans **Vous attend**, ouvre le même formulaire. Sur votre propre ordinateur, `assistant connect` fait la même chose dans un terminal.

## Travail ou perso

Chaque source est classée comme professionnelle (pour une entreprise que vous nommez) ou personnelle. Modifiez ce choix dans **Détails**. **Déduite** signifie que votre Machine l’a déterminé à partir de l’adresse. Les tâches professionnelles attendent vos jours de travail.

Pour les e-mails et les agendas Google et Microsoft, le type est déterminé à partir de l’adresse quand c’est évident : une adresse chez un fournisseur de messagerie comme Gmail ou Outlook.com est personnelle, tandis que le domaine de votre équipe indique un compte professionnel. Sinon, la question est posée une seule fois, juste après la connexion. **Modifier** permet de faire votre propre choix. Si vos e-mails indiquent ensuite l’autre type, la tâche **Tirez le meilleur de The Machine** vous demande une fois si vous souhaitez le modifier.

## Fonctionnalités

Une source peut importer des signaux (les éléments reçus deviennent des tâches), agir pour vos tâches (lire un document, ou envoyer, répondre ou modifier quelque chose après votre accord), ou faire les deux. Si elle peut faire les deux, **Détails** contient un bouton pour chacune des options : **Apporte des signaux** et **Peut agir**. L’une reste toujours activée. Pour désactiver les deux, déconnectez la source. Un chat ne propose que **Peut agir**.

Si **Apporte des signaux** est désactivé, la source n’est pas synchronisée. Si **Peut agir** est désactivé, votre Machine ne lit, ne rédige ni ne modifie jamais rien avec cette source.

## Supprimer une source

Ouvrez la source, puis **Détails** et **Déconnecter**. La source cesse d’être consultée. Les éléments qu’elle a déjà importés sont conservés. Sur une Machine hébergée, les sources dont la connexion est gérée par votre page de configuration (Google, Microsoft, Google Meet, Slack, Zoom, Stripe et Salesforce) affichent **Déconnecter ↗**, qui ouvre cette page.

**Déconnecté récemment** répertorie les comptes Google, Microsoft, Zoom, Slack, Stripe et Salesforce supprimés au cours des 30 derniers jours, ainsi que la date de leur suppression. En attendant la confirmation du service, le statut indique En attente et les tentatives se poursuivent. Un compte Google n’apparaît qu’une fois, même si Google Meet ou Docs avait sa propre connexion. Chaque compte apparaît dans sa propre catégorie : un compte Google ou Microsoft sous **E-mail**, Slack sous **Chat**.

## Identifiants enregistrés

Pour les sites comme LinkedIn ou X, cochez **Enregistrer pour la prochaine fois** lorsque vous vous connectez. **Connexions aux sites** les répertorie alors. Si un site déconnecte votre Machine, elle s’y reconnecte d’un seul geste. Les mots de passe restent chiffrés sur votre Machine. **Oublier** en supprime un.

Un site peut avoir plusieurs comptes, par exemple **Travail** et **Perso**. **Enregistrer sous** commence par reprendre la catégorie de la tâche, et **Autre nom…** permet de choisir un nom. Une tâche se connecte avec le compte qui lui convient. Si ce n’est pas évident, une boîte de dialogue vous demande une fois lequel choisir et s’en souvient pour cette tâche.

**Connexions aux sites** répertorie chaque site une fois, avec ses comptes en dessous : le nom d’utilisateur et un menu indiquant sa catégorie. Vous pouvez la modifier à tout moment dans ce menu. Les connexions enregistrées avant la gestion des comptes affichent **Travail ou perso ?** jusqu’à ce que vous choisissiez une catégorie. Une tâche qui utilisait une connexion vous redemande d’en choisir une après que vous avez changé sa catégorie.

**Importer** permet d’importer des connexions depuis un gestionnaire de mots de passe. Choisissez-en un :

- **LastPass**, **Bitwarden** ou **Google Password Manager** : la page d’exportation du gestionnaire s’ouvre dans le navigateur de votre Machine. Connectez-vous et exportez vos données. Les étapes s’affichent à côté. Votre Machine récupère le fichier, le lit une fois, puis le supprime.
- **1Password** : exportez un fichier CSV depuis l’application 1Password sur un ordinateur, puis sélectionnez-le. Si la connexion `op` à 1Password est active sur votre Machine, elle importe plutôt les données directement depuis là (et fait de même pour LastPass avec `lpass`).
- **Depuis un fichier d’exportation** : importez un fichier CSV de 1Password, LastPass, Bitwarden ou Chrome. Supprimez-le une fois l’importation terminée.

Cochez ensuite les connexions à conserver. Votre Machine ne se connecte jamais à votre gestionnaire de mots de passe à votre place et ne vous demande jamais son mot de passe principal. Vous le saisissez vous-même sur la page.

Une connexion enregistrée ne fonctionne qu’avec sa propre adresse Web : le même site, le même `https` et le même port. Pas avec une adresse ressemblante ni un autre sous-domaine.

## Vérifications

**Vérifications** indique comment votre Machine traite les éléments reçus : les vérifications récentes et ce que chacune a trouvé. Consultez l’article [Aucune nouvelle tâche](reviews-paused.md).

Chaque connexion a son propre article dans cette section, qui indique ce qu’elle lit et ce qu’elle peut envoyer.
