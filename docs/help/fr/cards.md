---
title: Tâches
area: cards
summary: Une tâche par élément qui nécessite votre attention, prête à être validée. Voici ce que signifient les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e0fd02e557e6daee
---
Votre Machine lit tous les nouveaux messages et crée une tâche uniquement quand quelque chose nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où trouver les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, une dernière étape que vous avez confirmée, comme un formulaire ou un problème, a été effectuée pendant votre absence. Elle reste là jusqu’à ce que vous touchiez **Compris**, pendant un jour maximum. Votre téléphone vous en informe aussi.
- **Pour vous** : tout ce qui attend une action de votre part, classé du plus urgent au moins urgent. Chaque tâche indique **Préparée** (un brouillon ou un résultat est prêt, et **Faire** ou **Envoyer** permet de le finaliser), **Vous attend** (une décision ou une réponse de votre part est nécessaire ; si le travail est bloqué par quelque chose que vous seule pouvez fournir, comme une information, une connexion ou un choix, une ligne sous le titre l’indique), **En préparation…** (votre Machine s’en occupe) ou **À lire** (un récap ou un compte rendu, sans décision à prendre).
- **Plus anciennes** : les tâches repliées qui n’ont rien de nouveau depuis une semaine (voir ci-dessous).
- **En attente des autres** : les tâches repliées dont la prochaine étape dépend de quelqu’un d’autre (voir ci-dessous).
- **Revient plus tard** : les tâches mises en attente et celles sans réponse à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : vos promesses et celles des autres envers vous. Consultez [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, des plus récentes aux plus anciennes, avec leur date de fin, par exemple « Terminée il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après un envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé vers Fait. » ou « Envoyé. Déplacé vers Plus tard jusqu’à lun. ». Une réponse qui ne fait que promettre de s’en occuper, comme « Je l’enverrai d’ici mardi », laisse la tâche ouverte : « Envoyé. Tâche gardée ouverte. » **Ouvrir** vous y mène. La recherche trouve une tâche par son titre ou par son destinataire, y compris dans Plus tard et Fait.

Dans **Pour vous**, les tâches en retard ou à échéance demain au plus tard apparaissent d’abord, suivies des questions de votre Fleet, des relances d’un tableau, puis du reste. Dans chaque groupe, les plus récentes apparaissent en premier. Une tâche garde sa place pendant que votre Machine la prépare et une fois terminée : seul son indicateur change. Dans les autres groupes ouverts, les tâches en retard ou à échéance demain au plus tard apparaissent d’abord, puis le reste des plus récentes aux plus anciennes. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore close. **Rouvrir** la remet dans votre liste et permet à votre Machine d’en tirer des enseignements. Ces tâches ne sont jamais considérées comme en retard. Si la mention apparaît sur un message, la tâche se ferme automatiquement au bout d’un jour et vous pouvez **Annuler** cette action. Sinon, elle attend que vous la **Marquiez comme faite**. Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se ferme aussi automatiquement.

Quand un message provient d’une adresse qui ressemble à celle d’une personne que vous connaissez, comme sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche l’indique clairement : « Ce n’est pas Sam Lee. » La personne est identifiée par sa propre adresse, jamais par le nom qu’elle a utilisé. Votre Machine vérifie le message auprès de la personne dont vous avez déjà l’adresse, jamais auprès de celle qui l’a écrit.

Une tâche qui attend toujours quelqu’un d’autre, pour une vérification ou une réponse par exemple, indique l’étape sous **En attente de :**. Elle apparaît dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est aussi le cas après que vous avez posé une question en retour : la tâche réapparaît le matin avant son échéance, à l’échéance si elle tombe plus tard dans la journée, ou le lendemain matin si l’échéance est passée. Elle indique alors qui doit encore répondre.

Quand une tâche concerne un résultat que quelqu’un d’autre doit vous fournir, comme un contrat signé, **Détails** l’indique sous **Terminé quand**. L’envoi de votre partie ne clôt pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se ferme automatiquement. Vous pouvez **Annuler** cette action. Si rien n’arrive au moment de relancer la personne, la tâche réapparaît avec **Écrivez une courte relance** dans son chat. Pour changer ce qui compte comme terminé, précisez-le dans le chat.

Une tâche sans nouveauté pendant une semaine passe de Pour vous à **Plus anciennes**, afin que les tâches récentes s’affichent en premier après quelques jours d’absence. Il n’y a pas de nouveauté s’il n’y a aucun nouveau message et que vous n’avez rien fait sur la tâche, comme envoyer un message dans le chat, la modifier ou la mettre en attente. Le simple fait de la consulter ne compte pas.

Les tâches urgentes, celles qui arrivent bientôt à échéance et celles dont l’envoi est en cours restent dans Pour vous. **Tout écarter** marque chaque tâche de Plus anciennes comme non nécessaire après une seule confirmation, comme **Pas nécessaire** le fait pour une tâche à la fois. Vous pouvez **Annuler** cette action. Toute nouveauté sur une tâche la ramène dans Pour vous.

Une tâche qui n’a été touchée par personne depuis une semaine demande une fois : **Toujours utile ?** **Pas nécessaire** la clôt et vous pouvez **Annuler** cette action. **Garder** la conserve et elle ne vous le demandera plus. Sans réponse pendant une semaine supplémentaire, elle est repliée dans Revient plus tard et n’est plus comptée dans le nombre affiché sur l’icône de l’app ni dans le récap du matin. Si vous l’ouvrez, envoyez un message dans le chat, la modifiez, la mettez en attente ou recevez un nouveau message, elle réapparaît.

Une fois par semaine, un projet resté inactif et sans tâche ouverte peut donner lieu à une tâche indiquant une prochaine étape précise, dans la limite de trois par semaine. Consultez [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine fait une pause et la liste reste vide. Pendant une vérification, elle se réveille et vous le signale. Si une vérification a échoué ou est en retard, la ligne l’indique et affiche **Vérifier maintenant** en dessous.

Les options **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou uniquement celles d’un type donné. Votre téléphone et votre ordinateur utilisent le même choix. Lorsque Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à l’ensemble des tâches. Une alerte concernant votre Machine elle-même, comme un composant qui redémarre sans cesse, n’est ni Travail ni Perso et apparaît uniquement sous Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre filtre : sous **Perso uniquement**, touchez **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le titre de votre dernier récap du matin ou du soir et ce qu’il comptait, par exemple **Récap d’hier soir** · 12 terminées, 3 ouvertes. Touchez-la pour relire le récap, puis utilisez **Copier** pour le coller où vous voulez. Une fois ouvert ou après avoir touché son **×**, il reste affiché sur tous vos appareils jusqu’au prochain récap.

Sans récap récent, la liste affiche **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui est encore en cours, pour Travail et Perso, ou uniquement pour le filtre sélectionné.

Une tâche associée à un projet affiche le nom de celui-ci sous son titre. Touchez-le pour ouvrir le projet. **Projet**, sous **Détails**, permet de le modifier ou de le retirer. Consultez [Les tâches d’un projet](projects.md#a-project-s-to-dos).

**Domaine**, sous **Détails**, permet de déplacer une tâche vers votre autre domaine. Les sources qu’elle peut lire et les messages qu’elle peut envoyer suivent le déplacement. **Annuler**, dans la notification, permet de la remettre à sa place.

Quand une tâche doit passer dans votre autre domaine et que tous les messages dont elle provient s’y trouvent, elle s’y déplace et continue automatiquement. Sinon, elle affiche **Déplacer vers Travail**, et rien ne bouge tant que vous ne touchez pas cette option. Une tâche que vous avez ajoutée sans choisir Travail ou Perso se déplace automatiquement dès qu’elle trouve sa place. En attendant, elle n’est ni Travail ni Perso et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Quand elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte de réception professionnelle que vous avez indiquée comme Perso compte comme personnelle. Les messages destinés à une autre de vos entreprises vont dans les tâches de cette entreprise. Une tâche concernant votre vie personnelle, comme un message de votre famille envoyé à votre adresse professionnelle, est personnelle dès le départ.

Le travail qui vous parvient sur un compte personnel, comme un client sur WhatsApp ou une commande dans votre boîte de réception personnelle, est professionnel dès le départ. Une tâche que vous avez déplacée ou classée vous-même reste toujours à l’endroit choisi. Travail ou Perso détermine où la tâche apparaît et avec qui elle est partagée, jamais l’endroit où elle répond : une réponse est toujours envoyée dans la conversation d’origine, même après un déplacement, sauf si vous choisissez une autre option.

Une telle tâche personnelle répond tout de même depuis l’adresse professionnelle qui a reçu l’e-mail. Elle n’apparaît jamais dans une Fleet Travail ni dans le Graph d’équipe.

S’il y a au moins deux tâches en attente, **Passer en revue** dans l’en-tête de Pour vous les parcourt une par une, dans l’ordre de la liste, avec chaque brouillon complet et les options **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur ordinateur, Entrée envoie ce qui est affiché, `S` met en attente, `→` ignore et Échap arrête le parcours. L’en-tête indique le temps nécessaire à votre rythme, par exemple « environ 2 min ».

À la fin, un bilan indique ce qui a été envoyé ou clôturé, ainsi que ce qui est encore en préparation.

Une tâche qui vous pose une question n’est incluse dans aucun des deux groupes : elle attend votre réponse, pas un simple clic.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès qu’il y en a 40 en attente ou que le message le plus ancien d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus sont traités lors de la vérification suivante, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont toujours lus et conservés, puis vérifiés ensemble à 06:30, pour que vos tâches soient prêtes avant votre récap du matin. Sous Connexions, les vérifications affichent « Suspendues pour la nuit, reprise à 06:30 ». Si vous cliquez, saisissez du texte ou faites défiler l’app, écrivez dans le chat ou touchez une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous vous absentiez pendant une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit immédiatement toutes les sources. Si aucune tâche n’est ouverte, touchez la ligne de votre Machine pour afficher les vérifications, avec **Détails**, qui ouvre la page Vérifications sous Connexions. Si des tâches sont ouvertes, l’option se trouve en haut de la liste sur ordinateur. Une courte ligne s’affiche uniquement pendant une vérification, ou si une vérification a échoué ou est en retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare ont leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans chaque source consultée, par exemple « 13 messages vérifiés à 16:11 · aucune nouvelle tâche » ou « · 2 nouvelles tâches ». Elle ne concerne que cette vérification : les tâches déjà dans votre liste restent inchangées. Quand une nouvelle tâche attend un moment plus opportun, comme votre récap du matin, la ligne indique jusqu’à quand : « 1 tâche retenue jusqu’à demain 08:30 ».

Touchez la ligne pour voir chaque fil d’e-mails, chat et notification avec l’icône de sa source : l’expéditeur, l’objet ou les premiers mots, ainsi que la nouvelle tâche ou la raison pour laquelle aucun suivi n’était nécessaire, comme « En copie seulement, un collègue répond » ou « Réunion déjà prévue jeudi ». Un fil n’affiche aucune raison si la vérification n’en a donné qu’une vague. Touchez un élément pour le lire avec le contexte de la conversation.

Les 10 premiers éléments s’affichent. Touchez en dessous pour voir le reste. Un nombre après un nom, comme (3), indique le nombre de nouveaux messages dans ce chat. Une notification sur votre téléphone concernant un message déjà répertorié n’apparaît qu’une fois. La ligne reste affichée pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptés. Vos propres réponses sont lues pour leur contexte et les promesses qu’elles contiennent, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que The Machine vous envoie, comme votre récap du matin ou une notification de correction, ne sont jamais lus ni répertoriés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus comme d’habitude.

## Les boutons

Une tâche affiche sa prochaine étape, comme **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Consultez [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** permet de préciser ce qu’il faut changer : la façon de s’y prendre ou, une fois le brouillon prêt, les modifications à y apporter. **Marquer comme fait** indique que la tâche est traitée : cette option est visible sur une tâche prête sans brouillon ou une tâche qui vous pose une question. Dans les autres cas, elle se trouve en haut du menu **…**. La tâche quitte immédiatement la liste et une notification vous propose **Annuler**. Balayez le message ou faites-le glisser hors de l’écran avec la souris pour le fermer plus vite. La modification est conservée.

Pour que la tâche soit effectuée autrement, dites-le dans son **Chat**. La réponse indique uniquement ce qui a changé, comme la mise en attente et sa durée. Si un élément ne peut pas être modifié, comme une échéance, elle vous le signale.

Sous **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez à quelqu’un de la vérifier](ask-to-review.md).
- **Répéter…** : la tâche [revient à intervalles réguliers](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez préciser pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Touchez le titre ou **Nom**, sous **Détails**, pour le modifier. Vous pouvez aussi le demander dans le chat, par exemple : « Renomme-la en… ». Votre titre est conservé.

**Rouvrir** fait réapparaître une tâche close. Elle revient aussi automatiquement en cas de nouveauté, comme un nouveau message de leur part, mais pas après votre propre réponse. La tâche indique alors qu’elle est revenue et apparaît comme nouvelle dans la liste. La conversation reprend là où elle s’était arrêtée, même après plusieurs semaines.

Une facture que vous devez payer vous-même, quel que soit le pays, devient une tâche indiquant le montant, la date d’échéance et les informations de paiement fournies. Les factures payées automatiquement, par exemple par prélèvement ou avec une carte enregistrée, ne deviennent pas des tâches. Quand un e-mail ultérieur confirme le paiement, par exemple un message de l’expéditeur indiquant qu’il a reçu votre règlement, la tâche se ferme automatiquement. Vous pouvez **Annuler** cette action pendant un jour.

Une tâche qui n’est utile que jusqu’à une heure précise, comme une confirmation à envoyer avant une réunion, se ferme automatiquement une fois ce moment passé. Elle rejoint **Fait / écarté** avec la mention « N’est plus nécessaire ». Vous pouvez **Annuler** cette action pendant un jour.

Avant qu’un message ou un transfert pour quelqu’un soit indiqué comme prêt, votre Machine vérifie vos conversations récentes avec les personnes concernées, y compris les conversations de groupe, et attend que Slack les ait lues. Si un message ultérieur montre que la tâche est déjà terminée, par exemple si une demande a reçu une réponse positive, elle se ferme automatiquement. Vous pouvez **Annuler** cette action pendant un jour.

Si quelqu’un d’autre a écrit dans la même conversation après la création du brouillon, **Envoyer** est suspendu : « Non envoyé : nouveau message dans le fil ». La tâche affiche ce message avec **La lire** et **Refaire pour ce message**. Appuyez de nouveau sur **Envoyer** pour envoyer le brouillon tel quel.

Quand un message plus récent change le programme, par exemple si une fête est déplacée ou si une réservation est annulée, The Machine met elle-même ses tâches à jour. Une tâche toujours nécessaire suit le nouveau programme. Si elle n’a plus rien à faire, elle passe dans **Fait / écarté** avec la mention « Pas nécessaire ». Le chat indique « Mise à jour : » et en précise la raison. Vous pouvez **Annuler** cette action pendant un jour.

Lors de vos premières tâches, une courte astuce présente les principales actions : **Demander des modifications** et **Pas nécessaire**, et vous rappelle que rien n’est envoyé tant que vous n’appuyez pas sur **Envoyer**. L’astuce disparaît définitivement dès que vous utilisez son bouton ou appuyez sur ×.

Le premier jour, un message d’accueil apparaît en haut de Tâches et indique qui attend votre réponse depuis le plus longtemps. Cette réponse est préparée en premier afin d’être prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique les personnes concernées, l’organisation si elle l’est (pas uniquement parce qu’une personne y travaille), le projet, Travail ou Perso et la date de réception. Touchez un nom pour ouvrir sa page dans le Graph.

Les noms et les organisations affichent leur photo ou leur logo si le Graph en possède un, ou leurs initiales. Si le logo est illisible à cette taille, par exemple s’il est blanc sur fond transparent ou s’il s’agit d’un long nom stylisé, l’initiale s’affiche aussi.

Une ligne discrète indique parfois ce qui n’est pas connu, comme « Dernier contact il y a 12 jours par e-mail ; rien depuis ». Elle s’affiche si votre dernier échange avec cette personne remonte à longtemps ou est resté sans réponse. Elle indique aussi les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine précise ce qu’elle ne sait pas au lieu de faire des suppositions.

Si un canal non connecté est indiqué, **Connecter** à côté permet de le connecter.

Le titre indique ce qu’il faut faire et ne change que si la tâche change. Une tâche terminée garde son titre, avec la façon dont elle s’est conclue en dessous, par exemple « Terminée : Sam l’a signée mardi ».

Une ligne discrète au-dessus du brouillon indique le message dont il provient, avec le logo du service correspondant. Touchez-la pour lire le fil. Le brouillon affiche le logo de sa destination, ce qui permet de voir tout de suite s’il s’agit d’une réponse Slack ou d’un e-mail.

Si le brouillon tient compte de l’avis d’une personne dans un autre espace, comme la suggestion d’un collègue dans Slack, une ligne le précise, par exemple « D’après Sam dans #ops ». Touchez-la pour lire le message.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche sous forme d’une conversation, de la plus ancienne à la plus récente : les messages qui précèdent celui dont traite la tâche, puis les réponses qui suivent. Dans WhatsApp, Telegram ou Signal, vos messages apparaissent à droite, comme dans l’app. Le message associé à la tâche porte la mention « Cette tâche » et s’ouvre à l’écran. **Afficher les messages précédents** ajoute les messages plus anciens. Les autres e-mails du fil sont repliés au-dessus et en dessous du message concerné.

Un message s’ouvre de la même façon depuis la recherche, le Graph, les réponses d’Ask ou la dernière vérification. Il porte la mention « Ce message » ou « Nouveaux messages ».

**Ouvrir dans Gmail** ouvre l’e-mail dans le compte Gmail qui l’a reçu. Sur Android, il s’ouvre dans l’app Gmail si elle est installée.

Les **Détails** d’un e-mail affichent uniquement les informations absentes de son en-tête, comme les adresses complètes en copie, les destinataires en copie cachée ou une autre adresse de réponse. Si rien n’est à ajouter, cette section est vide.

Une réponse dans un fil Slack affiche aussi les messages qui ont précédé l’ouverture du fil. Le lien d’une tâche vers son propre message l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet et le domaine de la tâche (touchez l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de programmation. Touchez son titre pour ouvrir le chat. Une tâche terminée reste compacte : le message dont elle provient se trouve sous **Détails**.

Une tâche qui attend quelqu’un d’autre renvoie au dernier message que vous lui avez envoyé, celui auquel vous attendez une réponse : « E-mail à Pat · mar. »

## Créer une tâche

**Nouvelle tâche** (sous **Rechercher** sur ordinateur, **+** sur téléphone ou `N`) permet d’ajouter une tâche pour n’importe quel sujet. Sa création n’envoie aucun message. Si vous ne choisissez ni **Travail** ni **Perso**, la tâche est classée automatiquement selon la personne et le sujet concernés. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il est ancien.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », aussi dans votre langue. L’icône du calendrier propose des raccourcis et l’option **Choisir une date**.
- **Répéter** : la tâche revient à intervalles réguliers. Consultez [Tâches récurrentes](recurring.md).
- **Personne** : associez les personnes ou les entreprises concernées, jusqu’à 5.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, d’un message Slack, Teams, WhatsApp, Telegram ou d’un autre message accessible à The Machine. Recherchez par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : touchez le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur téléphone, l’appareil photo à côté permet de prendre une photo. Jusqu’à 5 fichiers, comme dans le chat (consultez [Ajouter des fichiers](card-chat.md#add-files)). Touchez × pour en retirer un.

Les fichiers restent associés à la tâche et The Machine les lit lorsqu’elle s’en occupe. Vous pouvez joindre uniquement des fichiers : elle crée la tâche à partir d’un PDF ou d’un fichier texte. Une photo s’affiche sous forme de vignette. Touchez-la pour l’agrandir.
