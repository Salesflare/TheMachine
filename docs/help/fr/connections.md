---
title: Connexions
area: connections
summary: Vos sources au même endroit : leur état, comment en ajouter une ou en déconnecter une.
covers: tab:health, saved-signins
code: dashboard.html, onboarding.py
order: 1
translated: 1ca62ab8f65b77ff
---
## Leur état

L’onglet **Connexions** répertorie vos sources par type, puis affiche **Connexions aux sites** et **Vérifications** sous une ligne. Sur téléphone, touchez un type pour l’ouvrir, puis **Connexions** pour revenir en arrière. Le type qui contient une source nécessitant votre attention s’ouvre en premier. Chaque source apparaît sur une ligne, avec son état (Connectée, En attente de la première synchronisation, Reconnexion automatique ou Vous attend) et les dernières données reçues. Touchez-la pour ouvrir sa fiche et accéder à **Détails**.

Une synchronisation échouée qu’une synchronisation ultérieure a rattrapée apparaît en gris. Seul un échec qui reste le plus récent est signalé comme un problème, avec l’heure de la prochaine tentative.

Ses compteurs indiquent tout ce qu’elle a importé, y compris son [historique](history.md), ce qui est arrivé au cours des dernières 24 heures et ce qui n’a pas encore été vérifié. Pour un agenda, le compteur indique le nombre d’événements.

Chaque source porte le nom attribué à son compte par le service : votre adresse, un profil X, un espace de travail Slack ou le nom de la personne dont c’est le compte Signal ou Telegram. Sous le nom figurent d’abord **Travail** ou **Perso**, puis l’adresse ou l’identifiant si le nom ne l’indique pas déjà. Si deux sources du même type portent le même nom, leur nom précise aussi ce qui les distingue, comme Slack ou X, ou l’adresse de l’espace de travail.

Chaque source indique aussi en une ligne ce qu’elle importe et, si elle peut agir, précise qu’elle ne le fait qu’après que vous avez appuyé sur **Envoyer** ou donné votre accord.

## En ajouter une

Ouvrez un type (**E-mail**, **Agenda**, **Chat**, **Réunions**, **Documents et fichiers**, **Clients**, **Projets et code**, **Autres**), puis choisissez une source sous **En ajouter un autre**, ou sous la liste si aucune source n’est encore connectée. Les options générales se trouvent à la fin : **Autre e-mail** sous E-mail, **Lien d’agenda (ICS)** et **Autre agenda** sous Agenda. Exchange Server lit les réunions, il se trouve donc sous Agenda.

**Suggéré pour vous** apparaît en haut de **Connexions** lorsque votre Machine détecte une raison de vous proposer une source. Cette raison est indiquée en une ligne : des e-mails de Stripe, des réunions Zoom dans votre agenda, des messages contenant des liens vers Google Docs ou une configuration qui n’a pas abouti. La source reste aussi dans son propre groupe, avec la mention **Suggérée**. Ces suggestions sont calculées sur votre Machine, rien ne la quitte. Une source connectée n’est jamais suggérée.

Microsoft Teams apparaît deux fois : sous **Chat** pour ses chats et sous **Réunions** comme **Réunions Teams** pour les notes de réunion. Les deux utilisent la même connexion Microsoft. En connecter une connecte donc l’autre.

Une source que vous avez déjà connectée est indiquée dans la liste, avec son compte. Sélectionnez-la pour en ajouter une autre à côté : son formulaire le précise et renvoie vers celle que vous avez déjà.

Renseignez les informations demandées (une clé, une adresse), choisissez **Travail** avec le nom de votre entreprise ou **Perso** (pour les e-mails et les agendas, cette étape n’apparaît que si l’adresse ne permet pas de le déterminer), puis appuyez sur **Se connecter**. Pour un site comme LinkedIn ou X, la page de connexion s’ouvre dans le navigateur de votre Machine. La connexion se poursuit automatiquement une fois que vous êtes connecté. GitHub, WhatsApp et Codex affichent un code à saisir, et Telegram un code QR à scanner.

**Annuler** interrompt l’ajout. Vous avez quitté avant la fin ? Rouvrez **Connexions** sur n’importe quel appareil : vous retrouverez l’étape où vous en étiez. Une fois connectée, votre Machine commence aussitôt à lire la source et vous indique l’état de sa première synchronisation.

Sur une Machine hébergée, la connexion à Google, Microsoft, Microsoft OneDrive, Zoom, Stripe et Intercom se fait directement ici : choisissez **Travail** ou **Perso**, puis appuyez sur **Se connecter**. Vous revenez à ce formulaire, qui indique le résultat. GitHub, WhatsApp, Codex, Telegram et votre téléphone Android affichent aussi leur code ici.

**Reconnecter**, sur une source ou dans **Vous attend**, ouvre le même formulaire. Sur votre propre ordinateur, `assistant connect` fait la même chose dans un terminal.

## Travail ou perso

Chaque source est classée comme professionnelle (pour une entreprise que vous nommez) ou personnelle. Vous pouvez modifier ce choix dans **Détails**. **Devinez** signifie que votre Machine l’a déduit de l’adresse. Les tâches professionnelles attendent vos jours de travail.

Pour les e-mails et les agendas Google et Microsoft, la catégorie est déterminée à partir de l’adresse quand c’est évident : un fournisseur de messagerie comme Gmail ou Outlook.com indique **Perso**, tandis que le domaine de votre entreprise indique **Travail**. Sinon, la question s’affiche une fois, juste après la connexion. **Modifier** vous permet de faire votre choix. Si le contenu de vos e-mails indique ensuite l’autre catégorie, la tâche **Tirez le meilleur de The Machine** vous demande une fois si vous souhaitez la modifier.

## Fonctionnalités

Une source peut importer des signaux (les éléments reçus deviennent des tâches), agir pour vos tâches (lire un document, ou envoyer, répondre ou modifier quelque chose après votre accord), ou faire les deux. Si elle fait les deux, **Détails** affiche un interrupteur pour chacune de ces options : **Apporte des signaux** et **Peut agir**. L’une des deux reste activée. Pour désactiver les deux, déconnectez la source. Un chat ne propose que **Peut agir**.

Si **Apporte des signaux** est désactivé, la source n’est pas synchronisée. Si **Peut agir** est désactivé, votre Machine ne lit, ne rédige et ne modifie jamais quoi que ce soit avec cette source.

## En supprimer une

Ouvrez la source, puis **Détails** et **Déconnecter**. Elle cesse alors de lire. Les données qu’elle a déjà importées sont conservées. Sur une Machine hébergée, Google, Microsoft, Microsoft OneDrive, Zoom et Stripe affichent **Déconnecter ↗**, qui ouvre votre page de configuration.

**Déconnecté récemment** répertorie les comptes Google, Microsoft, Zoom, Slack, Stripe et Salesforce que vous avez supprimés au cours des 30 derniers jours, ainsi que la date de leur suppression. Un compte Google n’apparaît qu’une fois, même si Google Meet ou Docs avait sa propre connexion. Chaque compte apparaît sous son type : un compte Google ou Microsoft sous **E-mail**, Slack sous **Chat**.

## Connexions enregistrées

Pour des sites comme LinkedIn ou X, cochez **Enregistrer pour la prochaine fois** lorsque vous vous connectez. **Connexions aux sites** les répertorie ensuite. Si un site déconnecte votre Machine, elle s’y reconnecte d’un simple toucher. Les mots de passe restent chiffrés sur votre Machine. **Oublier** en supprime un.

## Vérifications

**Vérifications** indique comment votre Machine traite les éléments reçus : les vérifications récentes et ce que chacune a trouvé. Consultez [Aucune nouvelle tâche](reviews-paused.md).

Chaque connexion dispose d’un article dans cette section, qui indique ce qu’elle lit et ce qu’elle peut envoyer.
