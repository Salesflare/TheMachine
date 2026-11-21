---
title: Connexions
area: connections
summary: Toutes vos sources au même endroit : leur état, l’ajout d’une source ou la déconnexion.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 353fdfaa67678a1f
---
## Leur état

L’onglet **Connexions** répertorie vos sources par type, puis affiche **Connexions aux sites** et **Vérifications** sous une ligne. Sur un téléphone, touchez un type pour l’ouvrir, puis **Connexions** pour revenir en arrière. Un type contenant une source qui nécessite votre attention s’ouvre en premier. Chaque source apparaît sur une ligne avec son état (Connectée, En attente de la première synchronisation, Reconnexion automatique ou Besoin de votre aide) et les éléments reçus récemment. Touchez-la pour afficher sa fiche et ses **Détails**.

Un échec de synchronisation rattrapé par une synchronisation ultérieure apparaît en gris. Seul le dernier échec, s’il n’a pas encore été résolu, apparaît comme un problème, avec la date de la prochaine tentative.

Les compteurs indiquent tout ce que la source a importé, y compris son [historique](history.md), ce qu’elle a importé au cours des dernières 24 heures et ce qui n’a pas encore été vérifié. Pour un agenda, ils comptent les événements.

Chaque source porte le nom de son compte, tel que le service le présente : votre adresse, un profil X, un espace de travail Slack ou le nom de la personne à qui appartient le compte Signal ou Telegram. Sous le nom, vous voyez d’abord **Travail** ou **Perso**, puis l’adresse ou le nom d’utilisateur si le nom ne l’indique pas déjà. Si deux sources du même type portent le même nom, leur nom précise aussi ce qui les distingue, comme Slack ou X, ou l’adresse de l’espace de travail.

Chaque source indique aussi en une ligne ce qu’elle importe et, si elle peut agir, qu’elle ne le fait qu’après que vous avez appuyé sur **Envoyer** ou donné votre accord.

## En ajouter une

Ouvrez un type (**E-mail**, **Agenda**, **Chat**, **Réunions**, **Documents et fichiers**, **Clients**, **Projets et code**, **Autres**), puis choisissez une source sous **En ajouter un autre**, ou sous la liste si aucune source n’est encore connectée. Les options génériques se trouvent à la fin : **Autre e-mail** sous E-mail, **Lien d’agenda (ICS)** et **Autre agenda** sous Agenda. Exchange Server importe les réunions, il se trouve donc sous Agenda.

**Suggéré pour vous** apparaît en haut de **Connexions** lorsque votre Machine a une raison de vous proposer une source. Cette raison est indiquée en une ligne : des e-mails de Stripe, des réunions Zoom dans votre agenda, des messages contenant des liens vers Google Docs ou une configuration qui n’a pas abouti. La source reste aussi dans son propre groupe, avec la mention **Suggérée**. Ces éléments sont comptés sur votre Machine, rien n’en sort. Une source déjà connectée n’est jamais suggérée.

Microsoft Teams apparaît deux fois : sous **Chat** pour ses chats, et sous **Réunions** sous le nom **Réunions Teams** pour les notes de réunion. Les deux utilisent le même identifiant Microsoft. En connecter un connecte donc aussi l’autre.

Une source déjà connectée est indiquée dans la liste, avec son compte. Sélectionnez-la pour en ajouter une autre à côté : son formulaire le précise et contient un lien vers celle que vous avez déjà.

Renseignez les informations demandées (une clé, une adresse), choisissez **Travail** avec le nom de l’entreprise ou **Perso** (pour les e-mails et les agendas, la question ne s’affiche que si l’adresse ne permet pas de trancher), puis appuyez sur **Se connecter**. Pour un site comme LinkedIn ou X, la page de connexion s’ouvre dans le navigateur de votre Machine et la procédure se poursuit automatiquement une fois la connexion établie. GitHub, WhatsApp et Codex affichent un code à saisir. Telegram et Signal affichent un code QR à scanner.

**Annuler** arrête l’ajout. Vous avez quitté avant la fin ? Rouvrez **Connexions**, sur n’importe quel appareil, et la procédure reprend à la même étape. Une fois la source connectée, votre Machine commence à la lire immédiatement et vous indique l’avancement de la première synchronisation.

Sur une Machine hébergée, les sources qui ont leur propre connexion se connectent ici : Google, Microsoft (Outlook, OneDrive et Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce et Trello.

Choisissez **Travail** ou **Perso**, puis appuyez sur le bouton de connexion, comme **Se connecter avec Google**. Vous revenez à ce formulaire, qui indique le résultat. GitHub, WhatsApp, Codex, les chats Telegram et votre téléphone Android affichent aussi leur code ici.

Sur votre propre ordinateur, ces mêmes sources se connectent une fois votre Machine associée à votre compte. La première fois, appuyez sur **Associer cette Machine**. Certaines proposent aussi une autre méthode, comme votre propre application ou une clé.

Le bouton **Reconnecter**, sur une source ou dans **Vous attend**, ouvre le même formulaire. Sur votre propre ordinateur, `assistant connect` fait la même chose dans un terminal.

## Travail ou perso

Chaque source est définie comme professionnelle (pour une entreprise que vous indiquez) ou personnelle. Modifiez ce choix dans **Détails**. **Devinez** signifie que votre Machine l’a déduit de l’adresse. Les tâches professionnelles attendent vos jours ouvrés.

Pour les e-mails et les agendas Google et Microsoft, le choix est déduit de l’adresse lorsqu’elle permet de trancher : un fournisseur de messagerie comme Gmail ou Outlook.com correspond à Perso, le domaine de votre équipe à Travail. Si ce n’est pas clair, la question s’affiche une fois, juste après la connexion. **Modifier** vous permet de choisir vous-même. Si vos e-mails indiquent ensuite le contraire, la tâche **Tirez le meilleur de The Machine** vous demande une fois si vous souhaitez modifier ce choix.

## Capacités

Une source peut importer des signaux (ce qui est reçu devient des tâches), agir pour vos tâches (lire un document, ou envoyer, répondre ou modifier quelque chose après votre accord), ou faire les deux. Si elle fait les deux, **Détails** affiche un interrupteur pour chaque capacité : **Apporte des signaux** et **Peut agir**. L’une reste toujours activée. Pour les désactiver toutes les deux, déconnectez la source. Un chat ne propose que **Peut agir**.

Lorsque **Apporte des signaux** est désactivé, la source n’est pas synchronisée. Lorsque **Peut agir** est désactivé, votre Machine ne lit, ne rédige et ne modifie jamais rien à l’aide de cette source.

## Supprimer une source

Ouvrez la source, puis **Détails** et **Déconnecter**. Elle cesse alors d’être lue. Les éléments déjà importés sont conservés. Sur une Machine hébergée, une source dont les identifiants de connexion sont gérés par votre page de configuration (Google, Microsoft, Google Meet, Slack, Zoom, Stripe et Salesforce) affiche **Déconnecter ↗**, qui ouvre cette page.

**Déconnecté récemment** répertorie les comptes Google, Microsoft, Zoom, Slack, Stripe et Salesforce que vous avez supprimés au cours des 30 derniers jours, avec la date. En attendant la confirmation du service, la mention En attente s’affiche et la Machine continue d’essayer. Un compte Google n’apparaît qu’une fois, même si Google Meet ou Docs avait son propre identifiant de connexion. Chaque compte apparaît sous son propre type : un compte Google ou Microsoft sous **E-mail**, Slack sous **Chat**.

## Identifiants enregistrés

Pour des sites comme LinkedIn ou X, cochez **Enregistrer pour la prochaine fois** lorsque vous vous connectez. Ils apparaissent alors dans **Connexions aux sites**. Si un site déconnecte votre Machine, celle-ci s’y reconnecte d’un seul geste. Les mots de passe restent chiffrés sur votre Machine. **Oublier** en supprime un.

Un site peut avoir plusieurs comptes, par exemple **Travail** et **Perso**. **Enregistrer sous** sélectionne d’abord le contexte de la tâche, et **Autre nom…** permet de donner le nom de votre choix. Une tâche se connecte avec le compte qui lui correspond. Si ce n’est pas clair, une boîte de dialogue vous demande une fois lequel utiliser et mémorise votre choix pour cette tâche.

**Connexions aux sites** répertorie chaque site une seule fois, avec ses comptes en dessous : le nom d’utilisateur et un menu indiquant le contexte. Vous pouvez le modifier à tout moment dans ce menu. Les identifiants enregistrés avant l’ajout des comptes affichent **Travail ou perso ?** jusqu’à ce que vous en choisissiez un. Une tâche qui a utilisé un identifiant vous le redemande si vous modifiez son contexte.

**Importer** permet d’importer des identifiants depuis un gestionnaire de mots de passe. Choisissez-en un :

- **LastPass**, **Bitwarden** ou **Google Password Manager** : la page d’exportation s’ouvre dans le navigateur de votre Machine et s’affiche directement dans la boîte de dialogue, comme lorsque vous lancez **Faire** pour une tâche. Connectez-vous sur cette page. Votre Machine poursuit ensuite l’exportation. Une ligne vous indique ce qu’il vous reste à faire, par exemple saisir votre mot de passe principal. Sur un téléphone, la vue zoome sur le champ de saisie. Si la page ne correspond pas à ce qui était prévu, les étapes à suivre manuellement s’affichent à la place. Votre Machine récupère le fichier, le lit une fois, puis le supprime.
- **1Password** : exportez un fichier CSV depuis l’application 1Password sur un ordinateur, puis sélectionnez ce fichier. Si `op` de 1Password est connecté sur votre Machine, elle importe plutôt les données depuis là (et celles de `lpass` LastPass aussi).
- **Depuis un fichier d’exportation** : un fichier CSV de 1Password, LastPass, Bitwarden ou Chrome. Supprimez-le une fois l’importation terminée.

Cochez ensuite les identifiants à conserver. Votre Machine ne se connecte jamais à votre gestionnaire de mots de passe à votre place, ne saisit ni ne lit jamais votre mot de passe principal et ne montre jamais la page à l’assistante. Vous saisissez vous-même le mot de passe sur la page.

Un identifiant enregistré ne fonctionne que sur son adresse Web : le même site, `https` et le même port. Il ne fonctionne ni sur une adresse qui lui ressemble ni sur un autre sous-domaine.

## Vérifications

**Vérifications** indique comment votre Machine traite les éléments reçus : les vérifications récentes et ce que chacune a trouvé. Consultez [Aucune nouvelle tâche](reviews-paused.md).

Chaque connexion a son propre article dans cette section, qui indique ce qu’elle lit et ce qu’elle peut envoyer.
