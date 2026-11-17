---
title: Connexions
area: connections
summary: Vos sources réunies au même endroit : leur état, comment en ajouter une ou en déconnecter une.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: ec53596a1636fee7
---
## État des connexions

L’onglet **Connexions** répertorie vos sources par type, puis affiche **Connexions aux sites** et **Vérifications** sous une ligne. Sur téléphone, touchez un type pour l’ouvrir, puis **Connexions** pour revenir en arrière. Le type qui contient une source nécessitant votre attention s’affiche en premier. Chaque source apparaît sur une ligne, avec son état (Connectée, En attente de la première synchronisation, Reconnexion automatique ou Vous attend) et les derniers éléments reçus. Touchez-la pour ouvrir sa fiche et afficher les **Détails**.

Une synchronisation échouée, rattrapée par une synchronisation ultérieure, apparaît en gris. Seul un échec qui reste le plus récent est signalé comme un problème, avec la date de la prochaine tentative.

Les compteurs indiquent tout ce que la source a importé, y compris son [historique](history.md), ce qui est arrivé au cours des dernières 24 heures et ce qui n’a pas encore été vérifié. Un agenda compte ses événements.

Chaque source porte le nom de son compte, tel que le service l’affiche : votre adresse, un profil X, un espace de travail Slack ou le nom de la personne à qui appartient le compte Signal ou Telegram. Sous le nom, vous voyez d’abord **Travail** ou **Perso**, puis l’adresse ou l’identifiant si le nom ne les indique pas déjà. Si deux sources du même type portent le même nom, leur nom précise aussi ce qui les distingue, par exemple Slack ou X, ou l’adresse de l’espace de travail.

Chaque source indique aussi en une ligne ce qu’elle importe et, si elle peut agir, qu’elle ne le fait qu’après que vous avez appuyé sur **Envoyer** ou donné votre accord.

## Ajouter une source

Ouvrez un type (**E-mail**, **Agenda**, **Chat**, **Réunions**, **Documents et fichiers**, **Clients**, **Projets et code**, **Autres**), puis choisissez une source sous **En ajouter un autre**, ou sous la liste si aucune source n’est encore connectée. Une option générique apparaît à la fin : **Autre e-mail** sous E-mail, **Lien d’agenda (ICS)** et **Autre agenda** sous Agenda. Exchange Server importe les réunions, il se trouve donc sous Agenda.

**Suggéré pour vous** apparaît en haut de **Connexions** lorsque votre Machine détecte une raison de vous proposer une source. Cette raison est indiquée en une ligne : des e-mails de Stripe, des réunions Zoom dans votre agenda, des messages contenant des liens vers Google Docs ou une configuration inachevée. La source reste également dans son groupe, où elle porte la mention **Suggérée**. Ces suggestions sont calculées sur votre Machine, rien ne la quitte. Une source connectée n’est jamais suggérée.

Microsoft Teams apparaît deux fois : sous **Chat** pour ses conversations et sous **Réunions** sous le nom **Réunions Teams** pour les comptes rendus de réunion. Les deux utilisent la même connexion Microsoft. En connecter une connecte donc aussi l’autre.

La liste indique si vous avez déjà connecté une source, ainsi que le compte associé. Sélectionnez-la pour en ajouter une autre à côté : le formulaire le précise et propose un lien vers celle que vous avez déjà.

Renseignez les informations demandées (une clé, une adresse), choisissez **Travail** avec le nom de votre entreprise ou **Perso** (pour les e-mails et les agendas, ce choix n’est demandé que si l’adresse ne permet pas de le déterminer), puis appuyez sur **Se connecter**. Pour un site comme LinkedIn ou X, la page de connexion s’ouvre dans le navigateur de votre Machine et la procédure reprend automatiquement une fois la connexion établie. GitHub, WhatsApp et Codex affichent un code à saisir, tandis que les chats Telegram et Signal affichent un code QR à scanner.

**Annuler** interrompt l’ajout. Vous avez quitté la procédure avant la fin ? Rouvrez **Connexions** sur n’importe quel appareil pour reprendre à l’étape où vous en étiez. Une fois la source connectée, votre Machine commence tout de suite à la consulter et vous indique l’état de la première synchronisation.

Sur une Machine hébergée, les sources qui ont leur propre connexion se connectent ici : Google, Microsoft (Outlook, OneDrive et Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce et Trello.

Choisissez **Travail** ou **Perso**, puis appuyez sur le bouton de connexion correspondant, comme **Se connecter avec Google**. Vous revenez à ce formulaire, qui indique le résultat. GitHub, WhatsApp, Codex, les chats Telegram et votre téléphone Android affichent également leur code ici.

Sur votre propre ordinateur, ces mêmes sources se connectent une fois votre Machine associée à votre compte : la première fois, appuyez sur **Associer cette Machine**. Certaines proposent aussi une autre méthode, comme votre propre application ou une clé.

L’option **Reconnecter**, sur une source ou dans **Vous attend**, ouvre le même formulaire. Sur votre propre ordinateur, `assistant connect` fait la même chose dans un terminal.

## Travail ou perso

Chaque source est classée Travail (pour une entreprise que vous nommez) ou Perso. Modifiez ce choix sous **Détails**. **Déduit** signifie que votre Machine l’a déterminé à partir de l’adresse. Les tâches professionnelles attendent vos jours de travail.

Pour les e-mails et les agendas Google et Microsoft, le choix est déterminé à partir de l’adresse quand c’est évident : une adresse d’un fournisseur de messagerie comme Gmail ou Outlook.com est classée Perso, et le domaine de votre équipe est classé Travail. Sinon, la question s’affiche une fois, juste après votre connexion. **Modifier** vous permet de choisir vous-même. Si vos e-mails indiquent ensuite l’autre catégorie, la tâche **Tirez le meilleur de The Machine** vous demande une fois si vous souhaitez modifier ce choix.

## Capacités

Une source peut importer des signaux (les éléments reçus deviennent des tâches), effectuer des actions pour vos tâches (lire un document, envoyer, répondre ou modifier quelque chose après votre accord), ou faire les deux. Si elle fait les deux, les **Détails** comprennent une option pour chacune : **Apporte des signaux** et **Peut agir**. L’une des deux reste toujours activée. Pour désactiver les deux, déconnectez la source. Un chat n’a que l’option **Peut agir**.

Si **Apporte des signaux** est désactivé, la source ne se synchronise pas. Si **Peut agir** est désactivé, votre Machine ne lit, ne rédige ni ne modifie jamais rien avec cette source.

## Supprimer une source

Ouvrez la source, puis **Détails** et **Déconnecter**. Elle cesse d’être consultée. Les éléments qu’elle a déjà importés sont conservés. Sur une Machine hébergée, les sources dont la connexion est gérée par votre page de configuration (Google, Microsoft, Google Meet, Slack, Zoom, Stripe et Salesforce) affichent **Déconnecter ↗**, qui ouvre cette page.

**Déconnecté récemment** répertorie les comptes Google, Microsoft, Zoom, Slack, Stripe et Salesforce que vous avez supprimés au cours des 30 derniers jours, avec la date de suppression. Tant que le service n’a pas confirmé la suppression, l’état En attente s’affiche et la Machine réessaie. Un compte Google ne s’affiche qu’une fois, même si Google Meet ou Docs avait sa propre connexion. Chaque compte apparaît sous son type : un compte Google ou Microsoft sous **E-mail**, Slack sous **Chat**.

## Identifiants enregistrés

Pour des sites comme LinkedIn ou X, cochez **Enregistrer pour la prochaine fois** au moment de vous connecter. Ils apparaissent ensuite dans **Connexions aux sites**. Si un site déconnecte votre Machine, vous pourrez vous reconnecter d’un seul geste. Les mots de passe restent chiffrés sur votre Machine. **Oublier** supprime un identifiant.

Un site peut avoir plusieurs comptes, par exemple **Travail** et **Perso**. **Enregistrer sous** propose d’abord le côté correspondant à la tâche, et **Autre nom…** vous permet de donner le nom de votre choix. Une tâche se connecte avec le compte qui lui correspond. Si ce n’est pas évident, une boîte de dialogue vous demande une fois lequel choisir, puis s’en souvient pour cette tâche.

**Connexions aux sites** répertorie chaque site une seule fois, avec ses comptes en dessous. Les connexions enregistrées avant l’ajout de la gestion des comptes apparaissent sous **Par défaut** jusqu’à ce que vous leur attribuiez une catégorie.

**Importer** permet d’importer des identifiants depuis un gestionnaire de mots de passe : un fichier CSV exporté depuis 1Password, LastPass, Bitwarden ou Chrome, ou une importation directe depuis 1Password et LastPass à l’aide de leurs outils en ligne de commande si vous y êtes connecté sur cet ordinateur. Cochez les identifiants à conserver. Votre Machine ne se connecte jamais à votre gestionnaire de mots de passe et ne vous demande jamais son mot de passe principal. Supprimez le fichier exporté une fois l’importation terminée.

Un identifiant enregistré ne s’utilise qu’à l’adresse web qui lui correspond : le même site, `https` et le même port. Il ne s’utilise ni sur une adresse qui lui ressemble ni sur un autre sous-domaine.

## Vérifications

**Vérifications** indique comment votre Machine traite les éléments reçus : les vérifications récentes et ce que chacune a trouvé. Consultez [Aucune nouvelle tâche](reviews-paused.md).

Chaque connexion a son propre article dans cette section, qui explique ce qu’elle lit et ce qu’elle peut envoyer.
