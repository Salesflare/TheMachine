---
title: Connexions
area: connections
summary: Toutes vos sources au même endroit : leur état, comment en ajouter une ou en déconnecter une.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 9f2a2162fe015e0b
---
## Leur état

L’onglet **Connexions** répertorie vos sources par type, puis affiche **Connexions aux sites** et **Vérifications** sous une ligne. Sur un téléphone, touchez un type pour l’ouvrir, puis **Connexions** pour revenir en arrière. Un type contenant une source qui nécessite votre attention s’ouvre en premier. Chaque source apparaît sur une ligne : son état (Connectée, En attente de la première synchronisation, Reconnexion automatique ou Votre intervention est requise) et les derniers éléments reçus. Touchez-la pour ouvrir sa fiche et ses **Détails**.

Un échec de synchronisation rattrapé par une synchronisation ultérieure apparaît en gris. Seul un échec qui reste le plus récent est signalé comme un problème, avec la date de la prochaine tentative.

Les compteurs indiquent tout ce qu’elle a importé, y compris son [historique](history.md), les éléments reçus au cours des dernières 24 heures et ceux qui n’ont pas encore été vérifiés. Pour un agenda, ils comptent les événements.

Chaque source porte le nom de son compte, tel que le service l’affiche : votre adresse, un profil X, un espace de travail Slack ou le nom de la personne qui utilise Signal ou Telegram. Sous le nom : **Travail** ou **Perso**, puis l’adresse ou l’identifiant si le nom ne le précise pas déjà. Si deux sources du même type portent le même nom, elles indiquent aussi ce qui les distingue, comme Slack ou X, ou l’adresse de l’espace de travail.

Chaque source indique aussi en une ligne ce qu’elle importe et, si elle peut agir, qu’elle le fait uniquement après que vous avez appuyé sur **Envoyer** ou donné votre accord.

## En ajouter une

Ouvrez un type (**E-mail**, **Agenda**, **Chat**, **Réunions**, **Documents et fichiers**, **Clients**, **Projets et code**, **Autres**), puis choisissez une source sous **En ajouter un autre**, ou sous la liste si aucune source n’est encore connectée. Les options génériques apparaissent à la fin : **Autre e-mail** sous E-mail, **Lien d’agenda (ICS)** et **Autre agenda** sous Agenda. Exchange Server importe les réunions, il se trouve donc sous Agenda.

**Suggéré pour vous** apparaît en haut de **Connexions** quand votre Machine repère une raison d’ajouter une source, indiquée en une ligne : des e-mails de Stripe, des réunions Zoom dans votre agenda, des messages contenant des liens vers Google Docs ou une configuration qui n’a pas abouti. La source reste aussi dans son propre groupe, avec la mention **Suggérée**. Ce calcul se fait sur votre Machine, rien ne la quitte. Une source connectée n’est jamais suggérée.

Microsoft Teams apparaît deux fois : sous **Chat** pour ses conversations, et sous **Réunions** sous le nom **Réunions Teams** pour les notes de réunion. Les deux utilisent la même connexion Microsoft. En connecter une connecte donc aussi l’autre.

Une source déjà connectée est indiquée dans la liste avec son compte. Sélectionnez-la pour en ajouter une autre à ses côtés : son formulaire le précise et renvoie vers celle que vous avez déjà.

Renseignez les informations demandées (une clé, une adresse), choisissez **Travail** avec le nom de votre entreprise ou **Perso** (pour les e-mails et les agendas, ce choix n’est demandé que si l’adresse ne permet pas de le déterminer), puis appuyez sur **Se connecter**. Pour un site comme LinkedIn ou X, la page de connexion s’ouvre dans le navigateur de votre Machine. Le processus reprend automatiquement une fois la connexion établie. GitHub, WhatsApp et Codex affichent un code à saisir, et les chats Telegram et Signal affichent un code QR à scanner.

**Annuler** interrompt l’ajout. Vous avez quitté avant la fin ? Rouvrez **Connexions** sur n’importe quel appareil : le processus reprend à l’étape où vous en étiez. Une fois la source connectée, votre Machine commence aussitôt à la lire et vous indique l’avancement de sa première synchronisation.

Sur une Machine hébergée, les sources qui ont leur propre connexion se connectent ici : Google, Microsoft (Outlook, OneDrive et Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce et Trello.

Choisissez **Travail** ou **Perso**, puis appuyez sur le bouton de connexion correspondant, par exemple **Se connecter avec Google**. Vous revenez à ce formulaire, qui indique le résultat. GitHub, WhatsApp, Codex, les chats Telegram et votre téléphone Android affichent également leur code ici.

Sur votre propre ordinateur, ces mêmes sources se connectent une fois votre Machine associée à votre compte : appuyez sur **Associer cette Machine** la première fois. Certaines proposent aussi une autre méthode, comme votre propre application ou une clé.

Le bouton **Reconnecter**, sur une source ou dans **Vous attend**, ouvre le même formulaire. Sur votre propre ordinateur, `assistant connect` fait la même chose dans un terminal.

## Travail ou perso

Chaque source est considérée comme professionnelle (pour une entreprise que vous indiquez) ou personnelle. Modifiez ce choix sous **Détails**. **Déduit** signifie que votre Machine l’a déterminé à partir de l’adresse. Les tâches professionnelles attendent vos jours de travail.

Pour les e-mails et les agendas Google et Microsoft, le choix est déterminé à partir de l’adresse quand c’est évident : un fournisseur de messagerie comme Gmail ou Outlook.com indique un usage personnel, le domaine de votre équipe un usage professionnel. Sinon, la question est posée une fois, juste après la connexion. **Modifier** permet de faire votre propre choix. Si vos e-mails indiquent ensuite l’autre option, la tâche **Tirez le meilleur de The Machine** vous demandera une fois si vous voulez la changer.

## Autorisations

Une source peut importer des signaux (les éléments reçus deviennent des tâches), agir pour vos tâches (lire un document, envoyer, répondre ou modifier quelque chose après votre accord), ou faire les deux. Si elle fait les deux, **Détails** propose un interrupteur pour chacune : **Apporte des signaux** et **Peut agir**. Il doit toujours y en avoir un d’activé. Pour désactiver les deux, déconnectez la source. Un chat propose uniquement **Peut agir**.

Quand **Apporte des signaux** est désactivé, la synchronisation s’arrête. Quand **Peut agir** est désactivé, votre Machine ne lit, ne rédige et ne modifie jamais rien avec cette source.

## Supprimer une source

Ouvrez la source, puis **Détails** et **Déconnecter**. Elle cesse alors d’être lue. Les éléments déjà importés sont conservés. Sur une Machine hébergée, les sources dont la connexion est gérée par votre page de configuration (Google, Microsoft, Google Meet, Slack, Zoom, Stripe et Salesforce) affichent **Déconnecter ↗**, qui ouvre cette page.

**Déconnecté récemment** répertorie les comptes Google, Microsoft, Zoom, Slack, Stripe et Salesforce que vous avez supprimés au cours des 30 derniers jours, avec la date de suppression. En attendant la confirmation du service, l’état En attente s’affiche et les tentatives se poursuivent. Un compte Google n’apparaît qu’une fois, même si Google Meet ou Docs avait sa propre connexion. Chaque compte apparaît sous son type : un compte Google ou Microsoft sous **E-mail**, Slack sous **Chat**.

## Identifiants enregistrés

Pour les sites comme LinkedIn ou X, cochez **Enregistrer pour la prochaine fois** au moment de vous connecter. Ces sites apparaissent ensuite dans **Connexions aux sites**. Si un site déconnecte votre Machine, une seule pression suffit pour la reconnecter. Les mots de passe restent chiffrés sur votre Machine. **Oublier** supprime un identifiant.

Un site peut avoir plusieurs comptes, par exemple **Travail** et **Perso**. **Enregistrer sous** propose d’abord le choix associé à la tâche, et **Autre nom…** vous permet de saisir le vôtre. Une tâche utilise le compte qui lui correspond. Si ce n’est pas évident, une boîte de dialogue vous demande une fois lequel choisir et le mémorise pour cette tâche.

**Connexions aux sites** répertorie chaque site une seule fois, avec ses comptes en dessous : le nom d’utilisateur et un menu indiquant son usage. Vous pouvez modifier cet usage à tout moment. Les identifiants enregistrés avant l’ajout des comptes affichent **Travail ou perso ?** jusqu’à ce que vous en choisissiez un. Après avoir modifié l’usage d’un identifiant, toute tâche qui l’utilisait vous redemande lequel choisir.

**Importer** ajoute les identifiants d’un gestionnaire de mots de passe : un export CSV de 1Password, LastPass, Bitwarden ou Chrome, ou directement depuis les outils en ligne de commande de 1Password et LastPass si vous y êtes connecté sur cet ordinateur. Vous cochez ceux à conserver. Votre Machine ne se connecte jamais à votre gestionnaire de mots de passe et ne vous demande jamais son mot de passe principal. Supprimez le fichier d’export une fois l’opération terminée.

Un identifiant enregistré est utilisé uniquement sur la même adresse Web : le même site, `https` et le même port. Pas sur une adresse qui lui ressemble ni sur un autre sous-domaine.

## Vérifications

**Vérifications** indique comment votre Machine lit les éléments reçus : les vérifications récentes et ce que chacune a trouvé. Voir [Aucune nouvelle tâche](reviews-paused.md).

Chaque connexion a son propre article dans cette section, qui détaille ce qu’elle lit et ce qu’elle peut envoyer.
