---
title: Connexions
area: connections
summary: Toutes vos sources au même endroit : leur état, comment en ajouter une ou en déconnecter une.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 38d682b69cab758d
---
## Leur état

L’onglet **Connexions** répertorie vos sources par type, puis affiche **Connexions aux sites** et **Vérifications** sous une ligne de séparation. Sur un téléphone, touchez un type pour l’ouvrir, puis **Connexions** pour revenir en arrière. Le type qui contient une source nécessitant votre intervention s’affiche en premier. Chaque source apparaît sur une ligne : son état (Connectée, En attente de la première synchronisation, Reconnexion automatique ou Votre aide est nécessaire) et les dernières données reçues. Touchez-la pour afficher sa fiche et ses **Détails**.

Une synchronisation échouée, mais rattrapée par une synchronisation ultérieure, apparaît en gris. Seule une erreur toujours présente lors de la dernière synchronisation s’affiche comme un problème, avec la date de la prochaine tentative.

Les compteurs indiquent tout ce qu’elle a importé, y compris son [historique](history.md), les données reçues au cours des dernières 24 heures et celles qui n’ont pas encore été vérifiées. Pour un agenda, ils comptent les événements.

Chaque source porte le nom que le service donne à son compte : votre adresse, un profil X, un espace de travail Slack ou le nom de la personne qui utilise Signal ou Telegram. Sous le nom : **Travail** ou **Perso**, puis l’adresse ou l’identifiant si le nom ne les indique pas déjà. Si deux sources du même type portent le même nom, une précision permet de les distinguer, comme Slack ou X, ou l’adresse de l’espace de travail.

Chaque source indique aussi en une ligne ce qu’elle importe et, si elle peut agir, précise qu’elle ne le fait qu’après que vous avez appuyé sur **Envoyer** ou donné votre accord.

## En ajouter une

Ouvrez un type (**E-mail**, **Agenda**, **Chat**, **Réunions**, **Documents et fichiers**, **Clients**, **Projets et code**, **Autres**), puis choisissez une source sous **En ajouter un autre**, ou sous la liste si aucune source n’est encore connectée. Les options génériques apparaissent en dernier : **Autre e-mail** sous E-mail, **Lien d’agenda (ICS)** et **Autre agenda** sous Agenda. Exchange Server importe les réunions, il apparaît donc sous Agenda.

**Suggéré pour vous** apparaît en haut de **Connexions** lorsque votre Machine détecte une raison d’ajouter une source. Cette raison est indiquée en une ligne : des e-mails de Stripe, des réunions Zoom dans votre agenda, des messages contenant des liens vers Google Docs ou une configuration inachevée. La source apparaît aussi dans son propre groupe, avec la mention **Suggérée**. Ces vérifications ont lieu sur votre Machine, rien n’en sort. Une source connectée n’est jamais suggérée.

Microsoft Teams apparaît deux fois : sous **Chat** pour les chats et sous **Réunions**, sous **Réunions Teams**, pour les notes de réunion. Les deux utilisent la même connexion Microsoft. En connecter une connecte donc l’autre.

La liste indique les sources que vous avez déjà connectées, avec leur compte. Sélectionnez-en une pour en ajouter une autre à côté : son formulaire le précise et renvoie vers celle que vous avez déjà.

Saisissez les informations demandées (une clé, une adresse), choisissez **Travail** avec le nom de votre entreprise ou **Perso** (pour les e-mails et les agendas, le choix n’est demandé que si l’adresse ne permet pas de le déterminer), puis appuyez sur **Se connecter**. Pour un site comme LinkedIn ou X, la page de connexion s’ouvre dans le navigateur de votre Machine et la connexion se poursuit automatiquement une fois que vous êtes connecté. GitHub, WhatsApp et Codex affichent un code à saisir, tandis que les chats Telegram et Signal affichent un code QR à scanner.

Appuyez sur **Annuler** pour interrompre l’ajout. Vous avez quitté avant la fin ? Rouvrez **Connexions** sur n’importe quel appareil pour reprendre là où vous en étiez. Une fois la source connectée, votre Machine commence tout de suite à la lire et vous indique l’état de sa première synchronisation.

Sur une Machine hébergée, les sources qui ont leur propre connexion se connectent ici : Google, Microsoft (Outlook, OneDrive et Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce et Trello.

Choisissez **Travail** ou **Perso**, puis appuyez sur le bouton de connexion correspondant, comme **Se connecter avec Google**. Vous revenez à ce formulaire, qui indique le résultat. GitHub, WhatsApp, Codex, les chats Telegram et votre téléphone Android affichent aussi leur code ici.

Sur votre propre ordinateur, ces mêmes sources se connectent une fois votre Machine associée à votre compte : appuyez sur **Associer cette Machine** la première fois. Certaines proposent aussi une autre méthode, comme votre propre application ou une clé.

Le bouton **Reconnecter**, sur une source ou dans **Vous attend**, ouvre le même formulaire. Sur votre propre ordinateur, `assistant connect` fait la même chose dans un terminal.

## Travail ou perso

Chaque source est considérée comme professionnelle (pour une entreprise que vous nommez) ou personnelle. Modifiez ce réglage dans **Détails**. **Déduit** signifie que votre Machine l’a déterminé à partir de l’adresse. Les tâches professionnelles attendent vos jours de travail.

Pour les e-mails et agendas Google et Microsoft, le choix se fait à partir de l’adresse quand c’est évident : une adresse Gmail ou Outlook.com est personnelle, le domaine de votre entreprise est professionnel. Sinon, la question s’affiche une fois, juste après la connexion. **Modifier** permet de choisir vous-même. Si les e-mails indiquent ensuite l’autre option, la tâche **Tirez le meilleur de The Machine** vous demande une fois si vous souhaitez modifier le réglage.

## Capacités

Une source peut importer des signaux (les données reçues deviennent des tâches), agir pour vos tâches (lire un document, ou envoyer, répondre ou modifier quelque chose après votre accord), ou faire les deux. Si elle fait les deux, **Détails** affiche un interrupteur pour chaque capacité : **Apporte des signaux** et **Peut agir**. L’une des deux reste toujours activée. Pour désactiver les deux, déconnectez la source. Un chat ne propose que **Peut agir**.

Lorsque **Apporte des signaux** est désactivé, la synchronisation s’arrête. Lorsque **Peut agir** est désactivé, votre Machine ne lit, ne rédige ni ne modifie jamais quoi que ce soit avec cette source.

## Supprimer une source

Ouvrez la source, puis **Détails** et **Déconnecter**. Elle cesse alors d’être lue. Les données déjà importées sont conservées. Sur une Machine hébergée, le bouton **Déconnecter ↗** s’affiche pour les sources dont la connexion est gérée par votre page de configuration (Google, Microsoft, Google Meet, Slack, Zoom, Stripe et Salesforce). Il ouvre cette page.

**Déconnecté récemment** répertorie les comptes Google, Microsoft, Zoom, Slack, Stripe et Salesforce que vous avez supprimés au cours des 30 derniers jours, ainsi que la date de suppression. Tant que le service n’a pas confirmé la déconnexion, son état reste En attente et les tentatives se poursuivent. Un compte Google n’apparaît qu’une fois, même si Google Meet ou Docs avait sa propre connexion. Chaque compte apparaît sous son type : un compte Google ou Microsoft sous **E-mail**, Slack sous **Chat**.

## Identifiants enregistrés

Pour des sites comme LinkedIn ou X, cochez **Enregistrer pour la prochaine fois** lors de la connexion. **Connexions aux sites** les répertorie alors. Si un site déconnecte votre Machine, celle-ci se reconnecte d’un seul geste. Les mots de passe restent chiffrés sur votre Machine. Appuyez sur **Oublier** pour en supprimer un.

Un site peut avoir plusieurs comptes, par exemple **Travail** et **Perso**. **Enregistrer sous** propose d’abord le type associé à la tâche. **Autre nom…** permet de choisir un nom. Une tâche se connecte avec le compte qui lui convient. Si ce n’est pas évident, une boîte de dialogue vous demande une fois lequel choisir et mémorise votre choix pour cette tâche.

**Connexions aux sites** répertorie chaque site une seule fois, avec ses comptes en dessous : le nom d’utilisateur et un menu indiquant le type de compte. Vous pouvez modifier ce type à tout moment. Les identifiants enregistrés avant l’ajout des comptes affichent **Travail ou perso ?** jusqu’à ce que vous fassiez un choix. Si vous modifiez le type d’un identifiant utilisé par une tâche, celle-ci vous redemande d’en choisir un.

**Importer** permet d’importer des identifiants depuis un gestionnaire de mots de passe. Choisissez-en un :

- **LastPass**, **Bitwarden** ou **Google Password Manager** : la page d’exportation s’ouvre dans le navigateur de votre Machine. Connectez-vous, puis votre Machine poursuit l’exportation. Une ligne indique ce qu’il vous reste à faire, par exemple saisir votre mot de passe principal. Sur un téléphone, la page est agrandie à l’endroit où vous devez saisir le texte. Si la page ne ressemble pas à ce qui était prévu, les étapes à suivre manuellement s’affichent à la place. Votre Machine récupère le fichier, le lit une seule fois, puis le supprime.
- **1Password** : exportez un fichier CSV depuis l’application 1Password sur un ordinateur, puis sélectionnez ce fichier. Si `op` de 1Password est connecté à votre Machine, celle-ci importe les données directement depuis là (c’est aussi le cas pour `lpass` de LastPass).
- **Depuis un fichier d’exportation** : importez un fichier CSV de 1Password, LastPass, Bitwarden ou Chrome. Supprimez-le une fois l’importation terminée.

Cochez ensuite les identifiants à conserver. Votre Machine ne se connecte jamais à votre gestionnaire de mots de passe à votre place, ne saisit ni ne lit jamais votre mot de passe principal et ne montre jamais la page à l’assistante : vous saisissez vous-même le mot de passe dans la page.

Un identifiant enregistré est utilisé uniquement sur son adresse Web : le même site, `https` et le même port. Pas sur une adresse ressemblante ni sur un autre sous-domaine.

## Vérifications

**Vérifications** indique comment votre Machine lit les données reçues : les vérifications récentes et les résultats de chacune. Consultez [Aucune nouvelle tâche](reviews-paused.md).

Chaque connexion a son propre article dans cette section, qui précise ce qu’elle lit et ce qu’elle peut envoyer.
