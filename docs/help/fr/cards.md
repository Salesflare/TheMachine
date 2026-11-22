---
title: Tâches
area: cards
summary: Une tâche par sujet qui nécessite votre attention, prête à être validée. Voici ce que signifient les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e7e5d78b3291e556
---
Votre Machine lit tout ce qui est nouveau et crée une tâche uniquement quand quelque chose nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où se trouvent les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, une dernière étape que vous avez confirmée, comme un formulaire ou un problème, a abouti pendant votre absence. Elle reste là jusqu’à ce que vous appuyiez sur **Compris**, pendant un jour maximum, et votre téléphone en est aussi informé.
- **Pour vous** : tout ce qui attend votre intervention, par ordre d’urgence. Chaque tâche porte l’un de ces statuts : **Préparée** (un brouillon ou un résultat est prêt, et les boutons **Faire** ou **Envoyer** permettent de passer à l’action), **Vous attend** (elle nécessite d’abord votre décision ou votre réponse ; quand le travail est bloqué par un élément que vous seul pouvez fournir, comme une information, une connexion ou un choix, une ligne sous le titre l’indique), **En préparation…** (votre Machine s’en occupe) ou **À lire** (un récap ou un compte rendu, sans décision à prendre).
- **Plus anciennes** : les tâches repliées sur lesquelles il n’y a rien de nouveau depuis une semaine (voir ci-dessous).
- **En attente des autres** : les tâches repliées dont la prochaine étape revient à quelqu’un d’autre (voir ci-dessous).
- **Revient plus tard** : les tâches mises en attente et celles qui n’ont pas reçu de réponse à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : ce que vous avez promis et ce que les autres vous ont promis. Consultez [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec la date de fin, par exemple « Fait il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après l’envoi, une courte note indique où la tâche est passée, par exemple « Envoyé. Tâche déplacée dans Fait. » ou « Envoyé. Tâche déplacée dans Plus tard jusqu’à lundi. » Si la réponse promet seulement que le travail sera fait, par exemple « Je l’enverrai d’ici mardi », la tâche reste ouverte : « Envoyé. Tâche laissée ouverte. » **Ouvrir** vous y conduit. La recherche trouve une tâche par son titre ou par son destinataire, y compris dans Plus tard et Fait.

Dans **Pour vous**, les tâches en retard ou à échéance demain au plus tard s’affichent d’abord, puis les questions de votre Fleet, les suivis d’un tableau et le reste. Dans chaque groupe, les plus récentes s’affichent en premier. Une tâche garde sa place pendant que votre Machine la prépare et une fois terminée : seul son indicateur change. Dans les autres groupes ouverts, les tâches en retard ou à échéance demain au plus tard s’affichent d’abord, puis les autres, des plus récentes aux plus anciennes. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine pense que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore clôturée. **Rouvrir** la remet dans votre liste et votre Machine en tire des enseignements. Ces tâches ne sont jamais signalées comme étant en retard. Au bout d’un jour, elles se clôturent automatiquement, avec la possibilité d’**Annuler**. Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se clôture aussi automatiquement.

Lorsqu’un message provient d’une adresse qui ressemble seulement à celle d’une personne que vous connaissez, par exemple sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche l’indique clairement : « Ce n’est pas Sam Lee. » La personne apparaît sous sa propre adresse, jamais sous le nom qu’elle a utilisé. Votre Machine vérifie le message auprès de la personne correspondant à l’adresse que vous connaissez déjà, jamais auprès de son expéditeur.

Une tâche qui attend toujours quelqu’un d’autre, comme une vérification ou une réponse, indique l’étape sous **En attente de :**. Elle reste dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est aussi le cas après que vous avez posé une question en retour : la tâche revient le matin avant son échéance, à l’heure de l’échéance si celle-ci est plus tard dans la journée, ou le lendemain matin si l’échéance est passée. Elle indique alors qui doit encore répondre.

Quand une tâche porte sur un résultat fourni par quelqu’un d’autre, comme un contrat signé, **Détails** l’indique sous **Terminé quand**. L’envoi de votre partie ne clôture pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se clôture automatiquement, avec la possibilité d’**Annuler**. Si rien n’arrive au moment de relancer la personne, la tâche réapparaît avec **Écrivez une courte relance** dans son chat. Dites dans le chat ce qui compte comme terminé pour modifier ce critère.

Une tâche sans nouveauté depuis une semaine passe de Pour vous à **Plus anciennes**, afin que les tâches récentes apparaissent en premier après quelques jours d’absence. Il n’y a pas de nouveauté lorsqu’aucun nouveau message n’a été reçu et que vous n’avez rien fait sur la tâche, comme envoyer un message dans le chat, la modifier ou la mettre en attente. La consulter ne compte pas.

Les tâches urgentes, celles qui arrivent bientôt à échéance et celles dont l’envoi est en cours restent dans Pour vous. **Tout écarter** marque comme non nécessaires toutes les tâches de Plus anciennes, après une confirmation, comme le fait **Pas nécessaire** pour une tâche à la fois, avec la possibilité d’**Annuler**. Toute nouveauté sur une tâche la ramène dans Pour vous.

Une tâche à laquelle personne n’a touché depuis une semaine pose une seule fois la question **Toujours utile ?**. **Pas nécessaire** la clôture, avec la possibilité d’**Annuler**. **Garder** la conserve et la question ne sera plus posée. Sans réponse pendant une semaine supplémentaire, elle est repliée dans Revient plus tard et n’est plus comptée dans le nombre affiché sur l’icône de l’application ni dans le récap du matin. L’ouvrir, envoyer un message dans le chat, la modifier, la mettre en attente ou recevoir un nouveau message la fait réapparaître.

Une fois par semaine, un projet inactif sans tâche ouverte peut donner lieu à une tâche indiquant une prochaine étape précise, dans la limite de trois par semaine. Consultez [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine se repose et la liste reste vide. Pendant une vérification, elle se réveille et vous le signale. Si une vérification échoue ou prend du retard, la ligne l’indique, avec **Vérifier maintenant** en dessous.

Les options **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou seulement celles d’un type. Votre téléphone et votre ordinateur conservent le même choix. Lorsque Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à toutes les tâches. Une alerte concernant votre Machine elle-même, comme un composant qui redémarre sans cesse, n’est ni Travail ni Perso et n’apparaît que sous Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre vue : sous **Perso uniquement**, appuyez sur **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le titre de votre dernier récap du matin ou du soir et ce qu’il comptabilisait, par exemple **Récap d’hier soir** · 12 terminées, 3 ouvertes. Appuyez dessus pour relire le récap, puis sur **Copier** pour le coller où vous voulez. Dès que vous l’ouvrez ou que vous appuyez sur son **×**, il reste accessible sur tous vos appareils jusqu’au récap suivant.

En l’absence de récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui est toujours en cours, pour Travail et Perso, ou seulement pour la catégorie sélectionnée.

Une tâche liée à un projet affiche le nom du projet sous son titre. Appuyez dessus pour ouvrir le projet. **Projet** sous **Détails** permet de le modifier ou de retirer la tâche du projet. Consultez [Les tâches d’un projet](projects.md#a-project-s-to-dos).

**Domaine** sous **Détails** déplace une tâche vers votre autre domaine. Les sources que votre Machine peut lire et les services depuis lesquels elle peut envoyer des messages changent avec elle. **Annuler** dans la notification la remet à sa place.

Quand une tâche doit passer dans votre autre domaine pour continuer et que tous les messages dont elle provient s’y trouvent, elle y est déplacée automatiquement et le travail reprend. Sinon, elle affiche **Déplacer vers Travail** et rien ne bouge tant que vous n’appuyez pas dessus. Une tâche ajoutée sans choisir Travail ou Perso est déplacée automatiquement dès que votre Machine détermine où elle doit aller. En attendant, elle n’est ni Travail ni Perso et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Si elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte professionnelle que vous avez classée dans Perso est considérée comme personnelle. Les messages concernant une autre de vos entreprises sont associés aux tâches de cette entreprise. Une tâche concernant votre vie personnelle, comme un message de votre famille envoyé à votre adresse professionnelle, est personnelle dès le départ.

Un sujet professionnel qui vous parvient sur un compte personnel, comme un client sur WhatsApp ou une commande dans votre boîte personnelle, est professionnel dès le départ. Une tâche que vous avez déplacée ou classée vous-même reste toujours à l’endroit choisi. Travail ou Perso détermine où une tâche apparaît et avec qui elle est partagée, jamais où elle répond : la réponse est toujours envoyée dans la conversation d’origine, même après un déplacement, sauf si vous choisissez un autre moyen.

Une tâche personnelle de ce type répond tout de même depuis l’adresse professionnelle à laquelle son e-mail est arrivé. Elle n’apparaît jamais dans une Fleet Travail ni dans le Graph d’équipe.

Quand au moins deux tâches vous attendent, **Passer en revue** dans l’en-tête de Pour vous les affiche une par une, dans l’ordre de la liste, avec chaque brouillon en entier et les options **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur un ordinateur, Entrée envoie ce qui est affiché, `S` met en attente, `→` passe à la tâche suivante et Échap arrête le parcours. Sous le titre, l’en-tête indique aussi le temps nécessaire à votre rythme, par exemple « environ 2 min ».

Une tâche qui vous pose une question n’est incluse dans aucun des deux groupes : elle attend votre réponse, pas un clic.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès qu’il y en a 40 ou qu’un message d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus sont ajoutés à la prochaine vérification, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont quand même lus et conservés, puis vérifiés ensemble à 06:30 pour que vos tâches soient prêtes avant le récap du matin. Dans Connexions, la section Vérifications indique « En pause pour la nuit, rattrapage à 06:30. ». Si vous cliquez, saisissez du texte ou faites défiler l’application, écrivez dans le chat ou appuyez sur une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous soyez absent depuis une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit immédiatement toutes les sources. Si aucune tâche n’est ouverte, appuyez sur la ligne de votre Machine pour afficher son état et **Détails**, qui ouvre Vérifications sous Connexions. S’il y a des tâches ouvertes, l’option se trouve en haut de la page sur ordinateur. Une courte ligne s’affiche uniquement pendant une vérification, ou si l’une d’elles a échoué ou prend du retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare ont leur propre rythme.

## Dernière vérification

Après une vérification ayant lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans toutes les sources consultées, par exemple « 13 messages vérifiés à 16:11 · rien ne nécessite votre attention » ou « · 2 nouvelles tâches ». Lorsqu’une nouvelle tâche attend le bon moment, comme le récap du matin, la ligne indique jusqu’à quand : « 1 tâche mise de côté jusqu’à demain 08:30 ».

Appuyez sur la ligne pour afficher chaque fil d’e-mails, chat et notification avec l’icône de sa source : l’expéditeur, l’objet ou les premiers mots, ainsi que la nouvelle tâche ou la raison pour laquelle rien n’était nécessaire, par exemple « Vous étiez en copie, un collègue répond » ou « Réunion déjà prévue jeudi ». Un fil n’indique aucune raison si la vérification n’en a fourni qu’une vague. Appuyez sur un élément pour le lire.

Les 10 premiers éléments s’affichent ; appuyez en dessous pour voir le reste. Un nombre après un nom, comme (3), indique le nombre de nouveaux messages dans ce chat. Une notification sur votre téléphone concernant un message déjà affiché ne s’affiche qu’une fois. La ligne reste visible pendant les 12 heures suivant la vérification.

Seuls les e-mails qui vous sont adressés sont comptabilisés. Vos réponses sont lues pour le contexte et les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que The Machine vous envoie, comme le récap du matin ou un avis de correction, ne sont jamais lus ni affichés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche affiche la prochaine étape, par exemple **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Consultez [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** permet de préciser ce qu’il faut changer : la façon de faire ou, lorsqu’un brouillon est prêt, les modifications à y apporter. **Marquer comme fait** indique que la tâche est traitée : cette option est visible directement sur une tâche prête sans brouillon, sinon en haut du menu **…**, y compris pour une tâche qui nécessite votre décision. La tâche disparaît aussitôt de la liste, avec la possibilité d’**Annuler** dans la notification. Faites glisser le message pour le fermer, ou déplacez-le avec la souris pour le fermer plus rapidement. La modification est conservée.

Pour que la tâche soit faite autrement, précisez-le dans son **Chat**.

Dans le menu **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez à quelqu’un de la vérifier](ask-to-review.md).
- **Répéter…** : la tâche [revient à intervalles réguliers](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez aussi indiquer pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Appuyez sur le titre ou sur **Nom** sous **Détails** pour renommer la tâche, ou demandez-le dans son chat, par exemple « Renomme-la en… ». Votre titre est conservé.

**Rouvrir** fait réapparaître une tâche clôturée. Elle revient aussi automatiquement lorsqu’un nouvel événement survient, comme un nouveau message de cette personne, mais pas après votre propre réponse. La tâche indique alors quand elle est revenue et est classée comme nouvelle. Son chat reprend là où il s’était arrêté, même après plusieurs semaines.

Une facture que vous devez encore payer vous-même, quel que soit le pays, devient une tâche indiquant le montant, la date d’échéance et les modalités de paiement fournies par la facture. Ce n’est pas le cas des factures payées automatiquement, par prélèvement ou avec une carte enregistrée. Si un e-mail ultérieur confirme le paiement, par exemple un message de l’expéditeur indiquant que votre paiement a été reçu, la tâche se clôture automatiquement. **Annuler** permet de la rétablir pendant un jour.

Une tâche qui n’est utile que jusqu’à une heure précise, comme une confirmation à obtenir avant une réunion, se clôture automatiquement après cette heure. Elle passe dans **Fait / écarté** avec la mention « Plus nécessaire ». **Annuler** permet de la rétablir pendant un jour.

Avant qu’un message ou un transfert destiné à quelqu’un soit marqué comme prêt, votre Machine vérifie vos conversations récentes avec les personnes concernées, y compris les discussions de groupe, et attend que Slack les ait lues. Si un message ultérieur indique que la tâche est déjà terminée, par exemple si la personne a été sollicitée et a répondu oui, la tâche se clôture automatiquement. **Annuler** permet de la rétablir pendant un jour.

Quand un message plus récent modifie le plan, par exemple si une fête a lieu dans un autre endroit ou si une réservation est annulée, The Machine met elle-même ses tâches à jour. Une tâche qui reste utile suit le nouveau plan. Une tâche qui n’a plus rien à faire passe dans **Fait / écarté** avec la mention « Pas nécessaire ». Son chat indique « Mise à jour : » et en explique la raison. **Annuler** permet de la rétablir pendant un jour.

Lors de vos premières tâches, une courte astuce vous présente les actions clés : **Demander des modifications** et **Pas nécessaire**, et vous rappelle que rien n’est envoyé avant que vous appuyiez sur **Envoyer**. L’astuce disparaît définitivement dès que vous utilisez son bouton ou appuyez sur ×.

Le premier jour, un message d’accueil apparaît en haut de Tâches et indique qui attend votre réponse depuis le plus longtemps. La réponse à cette personne est préparée en priorité pour être prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique de qui il s’agit, l’organisation concernée le cas échéant, mais pas uniquement parce qu’une personne y travaille, le projet, Travail ou Perso, ainsi que la date de réception. Appuyez sur un nom pour ouvrir sa page dans le Graph.

Les noms et les organisations affichent leur photo ou leur logo si le Graph en a un, et leurs initiales dans le cas contraire. Un logo illisible en petit, par exemple du texte blanc sur fond transparent ou un long nom stylisé, est remplacé par l’initiale.

Une ligne discrète indique parfois ce qui est inconnu, par exemple « Dernier contact par e-mail il y a 12 jours, rien depuis ». Elle apparaît lorsque votre dernier échange avec cette personne remonte à longtemps ou est resté sans réponse. Elle signale aussi les canaux non connectés, comme WhatsApp. Votre Machine indique ce qu’elle ignore au lieu de faire des suppositions.

Quand elle mentionne un canal non connecté, l’option Connecter à côté ouvre la connexion correspondante.

Le titre indique ce qu’il faut faire et ne change que si la tâche change. Une tâche terminée conserve son titre, avec la façon dont elle s’est conclue en dessous, par exemple « Fait : Sam l’a signée mardi ».

Juste au-dessus du brouillon, une ligne discrète indique le message d’origine, avec le logo du service concerné. Appuyez dessus pour lire le fil. Le brouillon affiche le logo du service auquel il sera envoyé pour voir tout de suite s’il s’agit d’une réponse Slack ou d’un e-mail.

Si le brouillon tient compte de la contribution de quelqu’un dans un autre endroit, comme une suggestion d’un collègue dans Slack, une ligne le précise, par exemple « D’après Sam dans #ops ». Appuyez dessus pour lire ce message.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche comme une seule conversation, dans l’ordre chronologique : les messages précédant celui qui concerne la tâche, puis les réponses. Dans WhatsApp, Telegram ou Signal, vos messages sont à droite, comme dans l’application. Le message lié à la tâche porte la mention « Cette tâche » et s’ouvre dans la conversation. **Afficher les messages précédents** ajoute les messages plus anciens. Le reste d’un fil d’e-mails est replié au-dessus et en dessous du message concerné.

**Ouvrir dans Gmail** ouvre l’e-mail dans le compte Gmail où il est arrivé. Sur Android, il s’ouvre dans l’application Gmail si vous l’avez installée.

Les **Détails** d’un e-mail affichent uniquement les informations absentes de son en-tête, comme les adresses complètes en Cc, les adresses en Cci ou une adresse de réponse différente. Si rien n’est à ajouter, cette section n’apparaît pas.

Une réponse dans un fil Slack affiche aussi les messages qui ont précédé le début du fil. Le lien d’une tâche vers le message concerné l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet et le domaine de la tâche, que vous pouvez modifier en appuyant dessus, ainsi que votre dernière note et le résultat d’un agent de programmation. Le titre ouvre le chat. Une tâche terminée reste compacte ; le message d’origine se trouve sous **Détails**.

Une tâche « En attente de » contient un lien vers votre dernier message à la personne, celui dont vous attendez la réponse : « E-mail à Pat · mar. »

## Créer une tâche

**Nouvelle tâche** (sous **Rechercher** sur ordinateur, **+** sur téléphone ou `N`) permet de créer une tâche pour n’importe quel sujet. Sa création n’envoie rien. Si vous ne choisissez ni **Travail** ni **Perso**, la tâche est classée là où elle doit l’être, selon la personne et le sujet concernés. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il est ancien.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », y compris dans votre langue. L’icône du calendrier propose des choix rapides et **Choisir une date**.
- **Répéter** : la tâche revient à intervalles réguliers. Consultez [Tâches récurrentes](recurring.md).
- **Personne** : associez jusqu’à 5 personnes ou entreprises concernées.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, d’un message Slack, Teams, WhatsApp, Telegram ou de tout autre message accessible à The Machine. Faites une recherche par texte ou expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : appuyez sur le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur téléphone, l’icône d’appareil photo à côté permet de prendre une photo. Vous pouvez ajouter jusqu’à 5 fichiers, comme dans le chat (consultez [Ajouter des fichiers](card-chat.md#add-files)). Appuyez sur × pour retirer un fichier.

Les fichiers restent associés à la tâche et The Machine les lit lorsqu’elle s’en occupe. Vous pouvez aussi joindre uniquement des fichiers : elle remplit les informations de la tâche à partir d’un PDF ou d’un fichier texte. Une photo s’affiche sous forme de vignette. Appuyez dessus pour l’agrandir.
