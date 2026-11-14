---
title: Connexions
area: connections
summary: Vos sources au même endroit : leur état, comment en ajouter une ou en déconnecter une.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 60304f2504ee5676
---
## Leur état

L’onglet **Connexions** répertorie vos sources par type, puis affiche **Connexions aux sites** et **Vérifications** sous une ligne. Sur téléphone, touchez un type pour l’ouvrir, puis **Connexions** pour revenir en arrière. Le type contenant une source qui vous attend s’ouvre en premier. Chaque source apparaît sur une ligne : son état (Connectée, En attente de la première synchronisation, Reconnexion automatique ou Votre aide est nécessaire) et les éléments reçus récemment. Touchez-la pour afficher sa fiche et ses **Détails**.

Un échec de synchronisation rattrapé par une synchronisation ultérieure apparaît en gris. Seul un échec qui est toujours le plus récent apparaît comme un problème, avec l’heure de la prochaine tentative.

Les nombres indiquent tout ce qu’elle a importé, y compris son [historique](history.md), les éléments reçus au cours des dernières 24 heures et ceux qui n’ont pas encore été vérifiés. Pour un agenda, ils indiquent le nombre d’événements.

Chaque source porte le nom donné par le service à son compte : votre adresse, un profil X, un espace de travail Slack ou le nom du compte Signal ou Telegram. Sous le nom, vous trouverez d’abord **Travail** ou **Perso**, puis l’adresse ou le nom d’utilisateur si le nom ne l’indique pas déjà. Si deux sources du même type portent le même nom, une précision permet de les distinguer, comme Slack ou X, ou l’adresse de l’espace de travail.

Chaque source indique aussi en une ligne ce qu’elle importe et, si elle peut agir, précise qu’elle n’agit qu’après que vous avez appuyé sur **Envoyer** ou donné votre accord.

## En ajouter une

Ouvrez un type (**E-mail**, **Agenda**, **Chat**, **Réunions**, **Documents et fichiers**, **Clients**, **Projets et code**, **Autres**), puis choisissez une source sous **En ajouter un autre**, ou sous la liste si aucune source n’est encore connectée. Les options génériques apparaissent en dernier : **Autre e-mail** sous E-mail, **Lien d’agenda (ICS)** et **Autre agenda** sous Agenda. Exchange Server importe les réunions, il se trouve donc sous Agenda.

**Suggéré pour vous** apparaît en haut de **Connexions** lorsque votre Machine détecte une raison de vous proposer une source. Cette raison est indiquée en une ligne : des e-mails de Stripe, des réunions Zoom dans votre agenda, des messages contenant des liens vers Google Docs ou une configuration qui n’a pas abouti. La source reste aussi dans son groupe, avec la mention **Suggérée**. Le décompte est effectué sur votre Machine, rien ne la quitte. Une source connectée n’est jamais suggérée.

Microsoft Teams apparaît deux fois : sous **Chat** pour ses conversations et sous **Réunions**, avec l’intitulé **Réunions Teams**, pour les notes de réunion. Les deux utilisent le même identifiant Microsoft. En connecter une connecte donc l’autre.

Une source que vous avez déjà connectée est signalée dans la liste, avec son compte. Sélectionnez-la pour en ajouter une autre à côté : son formulaire l’indique et renvoie à celle que vous avez déjà.

Renseignez les informations nécessaires (une clé, une adresse), choisissez **Travail** avec le nom de l’entreprise ou **Perso** (les services E-mail et Agenda ne le demandent que si l’adresse ne suffit pas à le déterminer), puis appuyez sur **Se connecter**. Pour un site comme LinkedIn ou X, la page de connexion s’ouvre dans le navigateur de votre Machine et la configuration se poursuit automatiquement une fois connecté. GitHub, WhatsApp et Codex affichent un code à saisir. Telegram et Signal affichent un code QR à scanner.

**Annuler** arrête l’ajout. Vous avez quitté la procédure avant la fin ? Rouvrez **Connexions** sur n’importe quel appareil et elle reprend à la même étape. Une fois connectée, votre Machine commence tout de suite à lire la source et affiche l’état de sa première synchronisation.

Sur une Machine hébergée, les sources qui ont leur propre connexion se connectent ici : Google, Microsoft (Outlook, OneDrive et Teams), Google Meet, Google Docs, Slack, Zoom, Stripe, Intercom, Salesforce et Trello.

Choisissez **Travail** ou **Perso**, puis appuyez sur le bouton de connexion correspondant, par exemple **Se connecter avec Google**. Vous revenez à ce formulaire, qui indique le résultat. GitHub, WhatsApp, Codex, Telegram et votre téléphone Android affichent également leur code ici.

Sur votre propre ordinateur, vous pouvez connecter ces mêmes sources une fois votre Machine associée à votre compte : la première fois, appuyez sur **Associer cette Machine**. Certaines sources proposent aussi une autre méthode, comme votre propre application ou une clé.

**Reconnecter**, sur une source ou dans **Vous attend**, ouvre le même formulaire. Sur votre propre ordinateur, `assistant connect` fait la même chose dans un terminal.

## Travail ou perso

Chaque source est classée comme professionnelle (pour une entreprise que vous nommez) ou personnelle. Vous pouvez modifier ce choix dans **Détails**. **Déduit** signifie que votre Machine l’a déterminé à partir de l’adresse. Les tâches professionnelles attendent vos jours travaillés.

Pour les e-mails et agendas Google et Microsoft, votre Machine se base sur l’adresse si elle permet de déterminer le type de compte : un fournisseur de messagerie comme Gmail ou Outlook.com indique un compte Perso, le domaine de votre équipe un compte Travail. Sinon, la question vous est posée une fois, juste après la connexion. **Modifier** permet de faire votre choix. Si les e-mails reçus par la suite indiquent l’autre type, la tâche **Tirez le meilleur de The Machine** vous demande une fois si vous souhaitez le modifier.

## Fonctionnalités

Une source peut importer des signaux (les éléments reçus deviennent des tâches), effectuer des actions pour vos tâches (lire un document, envoyer, répondre ou modifier quelque chose après votre accord), ou faire les deux. Si elle fait les deux, **Détails** affiche un interrupteur pour chaque option : **Apporte des signaux** et **Peut agir**. Il faut en garder une activée. Pour désactiver les deux, déconnectez la source. Pour un chat, seule l’option **Peut agir** est disponible.

Si **Apporte des signaux** est désactivée, la source n’est pas synchronisée. Si **Peut agir** est désactivée, votre Machine ne lit, ne rédige et ne modifie rien avec cette source.

## Supprimer une source

Ouvrez la source, puis **Détails** et **Déconnecter**. Elle cesse alors d’être lue. Les éléments déjà importés restent disponibles. Sur une Machine hébergée, les sources dont les identifiants sont gérés par votre page de configuration (Google, Microsoft, Google Meet, Slack, Zoom, Stripe et Salesforce) affichent **Déconnecter ↗**, qui ouvre cette page.

**Déconnecté récemment** répertorie les comptes Google, Microsoft, Zoom, Slack, Stripe et Salesforce que vous avez supprimés au cours des 30 derniers jours, ainsi que la date de suppression. Tant que le service n’a pas confirmé la suppression, le statut En attente s’affiche et les tentatives se poursuivent. Un compte Google n’apparaît qu’une fois, même si Google Meet ou Docs avait ses propres identifiants. Chaque compte apparaît sous son propre type : un compte Google ou Microsoft sous **E-mail**, Slack sous **Chat**.

## Identifiants enregistrés

Pour les sites comme LinkedIn ou X, cochez **Enregistrer pour la prochaine fois** lors de la connexion. Vous les retrouverez ensuite sous **Connexions aux sites**. Si un site déconnecte votre Machine, celle-ci s’y reconnecte d’un seul geste. Les mots de passe restent chiffrés sur votre Machine. **Oublier** supprime un identifiant.

## Vérifications

**Vérifications** indique comment votre Machine lit les éléments reçus : les vérifications récentes et ce qu’elles ont trouvé. Consultez [Aucune nouvelle tâche](reviews-paused.md).

Chaque connexion a son propre article dans cette section, qui précise ce qu’elle lit et ce qu’elle peut envoyer.
