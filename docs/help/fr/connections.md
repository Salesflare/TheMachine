---
title: Connexions
area: connections
summary: Toutes vos sources au même endroit : leur état, comment en ajouter une ou en déconnecter une.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 0896d8f689ca9699
---
## État des connexions

L’onglet **Connexions** répertorie vos sources par type, puis affiche **Connexions aux sites** et **Vérifications** sous une ligne de séparation. Sur un téléphone, touchez un type pour l’ouvrir, puis **Connexions** pour revenir en arrière. Le type qui contient une source qui vous attend s’ouvre en premier. Chaque source apparaît sur une ligne avec son état (Connectée, En attente de la première synchro, Reconnexion automatique ou Attend votre aide) et les derniers éléments reçus. Touchez-la pour ouvrir sa fiche et consulter **Détails**.

Une synchronisation qui a échoué, mais a été rattrapée par la suivante, apparaît en gris. Seul un échec qui reste le plus récent est signalé comme un problème, avec l’heure de la prochaine tentative.

Les compteurs indiquent tout ce que la source a importé, y compris son [historique](history.md), ce qui est arrivé au cours des dernières 24 heures et ce qui n’a pas encore été vérifié. Pour un agenda, ils comptent les événements.

Chaque source porte le nom de son compte, tel que le service l’affiche : votre adresse, un profil X, un espace de travail Slack, ou la personne à qui appartient le compte Signal ou Telegram. Sous le nom, vous voyez d’abord **Travail** ou **Perso**, puis l’adresse ou le nom d’utilisateur si le nom ne l’indique pas déjà. Si deux sources du même type portent le même nom, leur nom indique aussi ce qui les différencie, comme Slack ou X, ou l’adresse de l’espace de travail.

Chaque source indique aussi en une ligne ce qu’elle importe et, si elle peut agir, précise qu’elle n’agit qu’après avoir appuyé sur **Envoyer** ou confirmé l’action.

## Ajouter une source

Ouvrez un type (**E-mail**, **Agenda**, **Chat**, **Réunions**, **Documents et fichiers**, **Clients**, **Projets et code**, **Autres**), puis choisissez une source sous **En ajouter un autre**, ou sous la liste si aucune source n’est encore connectée. Les options générales apparaissent en dernier : **Autre e-mail** sous E-mail, **Lien d’agenda (ICS)** et **Autre agenda** sous Agenda. Exchange Server importe les réunions, il se trouve donc sous Agenda.

**Suggéré pour vous** apparaît en haut de **Connexions** si votre Machine détecte une raison d’ajouter une source. Cette raison est indiquée en une ligne : des e-mails de Stripe, des réunions Zoom dans votre agenda, des messages contenant des liens vers Google Docs ou une configuration inachevée. La source reste aussi dans son propre groupe, marquée **Suggérée**. Ce calcul se fait sur votre Machine, rien ne la quitte. Une source connectée n’est jamais suggérée.

Microsoft Teams apparaît deux fois : sous **Chat** pour ses conversations et sous **Réunions**, dans **Réunions Teams**, pour les comptes rendus de réunion. Les deux utilisent la même connexion Microsoft. En connecter une connecte donc aussi l’autre.

Une source déjà connectée est signalée dans la liste avec son compte. Sélectionnez-la pour en ajouter une autre à côté : le formulaire l’indique et renvoie à celle qui est déjà connectée.

Saisissez les informations demandées, comme une clé ou une adresse, choisissez **Travail** et le nom de votre entreprise, ou **Perso** (pour les e-mails et les agendas, le choix n’est proposé que si l’adresse ne permet pas de trancher), puis appuyez sur **Connecter**. Pour un service comme LinkedIn ou X, la page de connexion s’ouvre dans le navigateur de votre Machine et la configuration reprend automatiquement une fois la connexion établie. GitHub, WhatsApp et Codex affichent un code à saisir. Pour les conversations Telegram et Signal, un QR code à scanner s’affiche.

**Annuler** interrompt l’ajout. Vous êtes parti avant la fin ? Rouvrez **Connexions** sur n’importe quel appareil : la configuration reprend là où vous en étiez. Une fois la source connectée, votre Machine commence immédiatement à la lire et indique l’état de la première synchronisation.

Sur une Machine hébergée, les sources qui ont leur propre connexion se connectent ici : Google, Microsoft (Outlook, OneDrive et Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce et Trello.

Choisissez **Travail** ou **Perso**, puis appuyez sur le bouton de connexion, par exemple **Se connecter avec Google**. Vous revenez à ce formulaire, qui indique le résultat. GitHub, WhatsApp, Codex, les conversations Telegram et votre téléphone Android affichent aussi leur code ici.

Sur votre propre ordinateur, ces mêmes sources se connectent une fois votre Machine associée à votre compte. Appuyez sur **Associer cette Machine** la première fois. Certaines proposent aussi une autre méthode, comme votre propre application ou une clé.

Appuyez sur **Reconnecter** sur une source ou dans **Vous attend** pour ouvrir le même formulaire. Sur votre propre ordinateur, `assistant connect` fait la même chose dans un terminal.

## Travail ou perso

Chaque source est classée comme professionnelle, pour une entreprise que vous indiquez, ou personnelle. Vous pouvez modifier ce choix dans **Détails**. **Estimée** signifie que votre Machine l’a déduit de l’adresse. Les tâches professionnelles attendent vos jours de travail.

Pour les e-mails et les agendas Google et Microsoft, le choix est déterminé à partir de l’adresse quand c’est évident : un fournisseur de messagerie comme Gmail ou Outlook.com est personnel, le domaine de votre entreprise est professionnel. Sinon, la question est posée une fois, juste après la connexion. **Modifier** vous permet de faire votre propre choix. Si vos e-mails indiquent ensuite l’autre catégorie, la tâche **Tirez le meilleur de The Machine** vous demande une fois si vous souhaitez la modifier.

## Capacités

Une source peut importer des signaux (les éléments reçus deviennent des tâches), agir pour vos tâches (lire un document, envoyer, répondre ou modifier quelque chose après votre confirmation), ou faire les deux. Si elle peut faire les deux, **Détails** affiche un interrupteur pour chacune des options : **Apporte des signaux** et **Peut agir**. L’une des deux reste activée. Pour désactiver les deux, déconnectez la source. Un chat propose uniquement **Peut agir**.

Si **Apporte des signaux** est désactivé, la synchronisation s’arrête. Si **Peut agir** est désactivé, votre Machine ne lit, ne rédige et ne modifie jamais quoi que ce soit avec cette source.

## Supprimer une source

Ouvrez la source, puis **Détails** et **Déconnecter**. Elle cesse alors de lire vos données. Les éléments déjà importés sont conservés. Sur une Machine hébergée, pour une source dont les informations de connexion sont gérées par votre page de configuration (Google, Microsoft, Google Meet, Slack, Zoom, Stripe et Salesforce), l’option **Déconnecter ↗** ouvre cette page.

**Déconnecté récemment** répertorie les comptes Google, Microsoft, Zoom, Slack, Stripe et Salesforce que vous avez supprimés au cours des 30 derniers jours, ainsi que la date de suppression. En attendant la confirmation du service, l’état indique En attente et les tentatives se poursuivent. Un compte Google n’apparaît qu’une fois, même si Google Meet ou Docs avait sa propre connexion. Chaque compte apparaît sous son propre type : un compte Google ou Microsoft sous **E-mail**, Slack sous **Chat**.

## Identifiants enregistrés

Pour des sites comme LinkedIn ou X, cochez **Enregistrer pour la prochaine fois** lors de la connexion. **Connexions aux sites** répertorie alors ces sites. Si un site déconnecte votre Machine, elle s’y reconnecte en un seul geste. Les mots de passe restent chiffrés sur votre Machine. **Oublier** permet d’en supprimer un.

Un site peut avoir plusieurs comptes, par exemple **Travail** et **Perso**. **Enregistrer sous** démarre avec la catégorie de la tâche, tandis que **Autre nom…** vous permet d’en choisir une. Une tâche se connecte avec le compte qui lui correspond. Si le choix n’est pas évident, une boîte de dialogue vous demande une fois lequel utiliser et s’en souvient pour cette tâche.

**Connexions aux sites** répertorie chaque site une seule fois, avec ses comptes en dessous : le nom d’utilisateur et un menu indiquant sa catégorie. Vous pouvez modifier cette catégorie à tout moment. Les identifiants enregistrés avant l’ajout des catégories affichent **Travail ou perso ?** jusqu’à ce que vous en choisissiez une. Si une tâche a utilisé un identifiant, elle vous redemande lequel utiliser après que vous avez modifié sa catégorie.

**Importer** permet d’importer des identifiants depuis un gestionnaire de mots de passe. Choisissez-en un :

- **LastPass**, **Bitwarden** ou **Gestionnaire de mots de passe de Google** : la page d’exportation du gestionnaire s’ouvre dans le navigateur de votre Machine, directement dans la boîte de dialogue, comme pour l’action **Faire** d’une tâche. Connectez-vous sur cette page. Votre Machine poursuit ensuite l’exportation. Une ligne indique ce qu’il vous reste à faire, par exemple saisir votre mot de passe principal. LastPass envoie par e-mail un lien de confirmation de l’exportation. Votre Machine lance l’exportation une fois, puis ouvre elle-même le lien si l’e-mail arrive dans une boîte de réception connectée dans les 10 minutes. Sinon, elle vous demande de confirmer et de relancer l’exportation. Sur un téléphone, la vue s’agrandit autour du champ de saisie. Si la page ne correspond pas à ce qui était prévu, les instructions pour terminer manuellement s’affichent à la place. Votre Machine récupère le fichier, le lit une fois, puis le supprime.
- **1Password** : exportez un fichier CSV depuis l’application 1Password sur un ordinateur, puis sélectionnez-le. Si la connexion à `op` de 1Password est établie sur votre Machine, elle importe les identifiants depuis cette connexion (et depuis `lpass` de LastPass aussi).
- **Depuis un fichier d’exportation** : importez un fichier CSV de 1Password, LastPass, Bitwarden ou Chrome. Supprimez-le une fois l’importation terminée.

Cochez ensuite les identifiants à conserver. Votre Machine ne se connecte jamais à votre gestionnaire de mots de passe à votre place, ne saisit ni ne lit jamais votre mot de passe principal et ne montre jamais la page à l’IA : vous saisissez vous-même le mot de passe sur la page.

Un identifiant enregistré n’est utilisé que pour l’adresse web à laquelle il correspond : le même site, `https` et le même port. Il ne fonctionne ni sur une adresse qui lui ressemble ni sur un autre sous-domaine.

## Vérifications

**Vérifications** indique comment votre Machine analyse les éléments reçus : les vérifications récentes et les résultats de chacune. Consultez [Aucune nouvelle tâche](reviews-paused.md).

Chaque connexion a son propre article dans cette section, qui précise ce qu’elle lit et ce qu’elle peut envoyer.
