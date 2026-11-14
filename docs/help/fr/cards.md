---
title: Tâches
area: cards
summary: Une tâche pour chaque chose qui nécessite votre attention, prête à recevoir votre accord. Voici ce que signifient les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 12be97d431968927
---
Votre Machine lit tout ce qui est nouveau et crée une tâche uniquement quand quelque chose nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où se trouvent les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, une dernière étape que vous avez confirmée, comme un formulaire ou un problème, a abouti pendant votre absence. Elle reste affichée jusqu’à ce que vous touchiez **Compris**, pendant un jour maximum, et votre téléphone vous en informe aussi.
- **Pour vous** : tout ce qui attend votre intervention, par ordre d’urgence. Chaque tâche indique **Préparée** (le travail est terminé, et **Faire** ou **Envoyer** permet de l’effectuer), **Vous attend** (elle nécessite d’abord votre décision ou une réponse), **En préparation…** (votre Machine est en train de s’en occuper) ou **À lire** (un récap ou un résumé, sans décision à prendre).
- **En attente des autres** : les tâches repliées dont la prochaine étape revient à quelqu’un d’autre (voir ci-dessous).
- **Revient plus tard** : les tâches mises en attente, ainsi que celles pour lesquelles vous n’avez pas répondu à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : ce que vous avez promis et ce que d’autres vous ont promis. Consultez [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec l’heure de fin, par exemple « Fait il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après l’envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé vers Fait. » ou « Envoyé. Déplacé vers Plus tard jusqu’à lundi. » **Ouvrir** vous y conduit. La recherche permet de trouver une tâche par son titre ou son destinataire, y compris dans Plus tard et Fait.

**Pour vous** affiche d’abord les tâches en retard ou à échéance demain au plus tard, puis les questions de votre Fleet, ensuite les suivis d’un tableau, et enfin le reste. Dans chaque groupe, les plus récentes apparaissent en premier. Une tâche garde sa place pendant que votre Machine la prépare et une fois terminée : seul son indicateur change. Dans les autres groupes ouverts, les tâches en retard ou à échéance demain au plus tard apparaissent d’abord, puis les plus récentes. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 a été fusionnée », mais qu’elle n’est pas encore clôturée. **Rouvrir** la remet dans votre liste, et votre Machine en tient compte pour la suite. Ces tâches ne sont jamais considérées en retard. Au bout d’un jour, elles se clôturent automatiquement, avec la possibilité d’**Annuler**. Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se clôture également automatiquement.

Quand un message provient d’une adresse qui ressemble à celle d’une personne que vous connaissez, par exemple sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche le signale clairement : « Ce n’est pas Sam Lee. » La personne apparaît avec sa propre adresse, jamais sous le nom qu’elle a utilisé. Votre Machine vérifie ce type de message auprès de la personne correspondant à l’adresse que vous avez déjà, jamais auprès de son expéditeur.

Une tâche toujours en attente de quelqu’un d’autre, par exemple pour une révision ou une réponse, indique **En attente de** et l’étape concernée. Elle apparaît dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est aussi le cas après que vous avez posé une question en retour : la tâche revient le matin précédant son échéance, à l’échéance si celle-ci tombe plus tard dans la journée, ou le lendemain matin une fois l’échéance passée. Elle indique alors qui doit encore vous répondre.

Quand une tâche porte sur un résultat fourni par quelqu’un d’autre, comme un contrat signé, **Détails** l’indique sous **Terminé quand**. Envoyer votre partie ne clôture pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se clôture automatiquement. Vous pouvez **Annuler**. Si rien n’arrive au moment de relancer la personne, la tâche réapparaît avec **Écris une courte relance** dans son chat. Indiquez dans le chat ce qui compte comme terminé pour modifier ce critère.

Si personne ne s’est occupé d’une tâche pendant une semaine, elle demande une seule fois : **Toujours utile ?** **Pas nécessaire** la clôture, avec la possibilité d’**Annuler**. **Garder** la conserve, et elle ne posera plus la question. Sans réponse pendant une semaine de plus, elle est repliée dans Revient plus tard, et elle n’est plus comptée sur l’icône de l’application ni dans le récap du matin. Si vous l’ouvrez, envoyez un message dans son chat, la modifiez, la mettez en attente ou recevez un nouveau message, elle réapparaît.

Une fois par semaine, un projet inactif sans tâche ouverte peut donner lieu à une tâche indiquant une prochaine étape précise, dans la limite de trois par semaine. Consultez [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine se met en veille et affiche une liste vide. Pendant une vérification, elle se réveille et vous le signale. Si une vérification a échoué ou est en retard, sa ligne l’indique et propose **Vérifier maintenant**.

**Tout**, **Travail** et **Perso**, en haut de la barre latérale, permettent d’afficher toutes les tâches ou seulement celles d’un type. Votre téléphone et votre ordinateur conservent le même choix. Lorsque Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à l’affichage complet. Une alerte concernant votre Machine elle-même, comme un composant qui redémarre sans cesse, n’est ni Travail ni Perso et apparaît uniquement sous Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre affichage : **Perso uniquement · Travail · Tout afficher**.

La ligne en haut de la liste indique le titre de votre dernier récap du matin ou du soir et le nombre d’éléments qu’il comptait, par exemple **Récap d’hier soir** · 12 terminés, 3 ouverts. Touchez-la pour relire ce récap. **Copier** permet de le coller où vous voulez. Dès que vous l’ouvrez ou touchez son **×**, il reste disponible sur tous vos appareils jusqu’au prochain récap.

Sans récap récent, la ligne indique **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui est encore en cours, pour Travail et Perso, ou uniquement pour le filtre sélectionné.

Une tâche associée à un projet affiche le nom du projet sous son titre. Touchez-le pour ouvrir le projet. **Projet**, sous **Détails**, permet de le modifier ou de le retirer. Consultez [les tâches d’un projet](projects.md#a-project-s-to-dos).

**Domaine**, sous **Détails**, permet de déplacer une tâche vers votre autre domaine. Les éléments qu’elle peut lire et envoyer changent avec elle. **Annuler**, dans la note, permet de la remettre à sa place.

Quand une tâche nécessite votre autre domaine et que tous les messages dont elle provient s’y trouvent, elle y est déplacée automatiquement et se poursuit. Sinon, elle affiche **Déplacer vers Travail** et rien ne bouge tant que vous ne touchez pas cette option. Une tâche que vous avez ajoutée sans choisir Travail ou Perso est déplacée automatiquement dès que votre Machine trouve où elle appartient. D’ici là, elle n’est associée ni à Travail ni à Perso, et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Quand elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte de réception professionnelle que vous avez classée dans Perso compte comme Perso. Les e-mails concernant une autre de vos entreprises vont dans les tâches de cette entreprise. Une tâche portant sur votre vie personnelle, par exemple un membre de votre famille qui écrit à votre adresse professionnelle, est classée dans Perso dès le départ.

Le travail qui arrive sur un compte personnel, comme un client sur WhatsApp ou une commande dans votre boîte de réception personnelle, est classé dans Travail dès le départ. Une tâche que vous avez déplacée ou classée vous-même reste toujours là où vous l’avez mise. Travail ou Perso détermine où une tâche apparaît et avec qui elle est partagée, mais jamais l’endroit d’où elle répond : la réponse est toujours envoyée dans la conversation d’origine, même après un déplacement, sauf si vous choisissez une autre méthode.

Une tâche Perso de ce type répond quand même depuis l’adresse professionnelle à laquelle son e-mail est arrivé, et n’apparaît jamais dans une Fleet Travail ni dans le Graph de l’équipe.

Quand au moins deux tâches attendent votre attention, **Passer en revue**, dans l’en-tête de Pour vous, permet de les parcourir une par une, dans l’ordre de la liste. Chaque brouillon s’affiche en entier, avec **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur ordinateur, Entrée envoie ce qui est affiché, `S` met en attente, `→` ignore et Échap arrête le parcours. Sous le titre, l’en-tête indique aussi le temps nécessaire à votre rythme, par exemple « environ 2 min ».

Une tâche qui vous pose une question n’est incluse dans aucun des deux groupes : elle attend une réponse de votre part, pas un clic.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès qu’il y en a 40 ou que le plus ancien message d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus sont pris en compte à la prochaine vérification, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications s’interrompent : les nouveaux messages sont quand même lus et conservés, puis vérifiés ensemble à 06:30, pour que vos tâches soient prêtes avant le récap du matin. Dans Connexions, la section Vérifications indique « En pause pour la nuit, rattrapage à 06:30 ». Si vous ouvrez l’application, écrivez dans le chat ou touchez une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous vous absentiez pendant une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit immédiatement toutes les sources. Si aucune tâche n’est ouverte, touchez la ligne de votre Machine pour la voir, avec **Détails**, qui ouvre la section Vérifications dans Connexions. S’il y a des tâches ouvertes, cette ligne apparaît en haut sur ordinateur. Une courte ligne s’affiche uniquement pendant une vérification, ou si l’une d’elles a échoué ou est en retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare suivent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans chaque source consultée, par exemple « 13 messages vérifiés à 16:11 · rien ne nécessite votre attention » ou « · 2 nouvelles tâches ». Lorsqu’une nouvelle tâche attend un moment plus approprié, comme le récap du matin, la ligne indique jusqu’à quand : « 1 tâche mise de côté jusqu’à demain 08:30 ».

Touchez cette ligne pour voir chaque fil d’e-mails, chat et notification, avec l’icône de sa source : l’expéditeur, l’objet ou les premiers mots, ainsi que la nouvelle tâche ou la raison pour laquelle le message n’a rien nécessité, par exemple « En copie seulement, un collègue répond » ou « Réunion déjà prévue jeudi ». Un fil n’indique aucune raison si la vérification n’en a donné qu’une de vague. Touchez un élément pour le lire.

Les 10 premiers éléments s’affichent. Touchez en dessous pour voir le reste. Le nombre après un nom, par exemple (3), indique combien de nouveaux messages ce chat contient. Une notification de téléphone pour un message déjà affiché n’apparaît qu’une fois. La ligne reste affichée pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptés. Vos propres réponses sont lues pour leur contexte et les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails envoyés par The Machine, comme votre récap du matin ou une notification de correction, ne sont jamais lus ni répertoriés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche affiche la prochaine étape, par exemple **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Consultez [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** permet d’indiquer ce qui doit changer : la façon de procéder ou, lorsqu’un brouillon est prêt, les modifications à y apporter. **Marquer comme fait** indique que la tâche est traitée. L’option apparaît directement sur une tâche prête sans brouillon, sinon en haut du menu **…**, y compris pour une tâche qui nécessite votre décision. La tâche disparaît aussitôt de la liste, avec **Annuler** dans le message. Balayez le message ou faites-le glisser hors de la liste avec la souris pour le fermer plus vite. La modification est conservée.

Pour qu’elle soit effectuée autrement, dites-le dans son **Chat**.

Dans **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez une révision](ask-to-review.md).
- **Répéter…** : la tâche [revient à intervalles réguliers](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez éventuellement indiquer pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tient compte pour la suite.

Touchez le titre ou **Nom**, sous **Détails**, pour renommer la tâche. Le titre que vous choisissez est conservé.

**Rouvrir** fait réapparaître une tâche clôturée. Elle réapparaît aussi automatiquement lorsqu’un nouvel événement survient, comme un nouveau message de la personne concernée, mais pas après votre propre réponse.

Une facture que vous devez payer vous-même, quel que soit le pays, devient une tâche avec le montant, la date d’échéance et les coordonnées de paiement indiqués sur la facture. Ce n’est pas le cas des factures payées automatiquement, comme un prélèvement ou un paiement effectué avec une carte enregistrée. Lorsqu’un e-mail ultérieur indique que la facture a été payée, par exemple si l’expéditeur confirme la réception de votre paiement, la tâche se clôture automatiquement. **Annuler** permet de la rétablir pendant un jour.

Une tâche qui n’est pertinente que jusqu’à une heure précise, comme une confirmation à envoyer avant une réunion, se clôture automatiquement une fois cette heure passée. Elle est déplacée dans **Fait / écarté** avec la mention « N’est plus nécessaire ». **Annuler** permet de la rétablir pendant un jour.

Avant qu’un message ou un transfert destiné à quelqu’un soit indiqué comme prêt, votre Machine vérifie vos chats récents avec les personnes concernées, y compris les discussions de groupe, et attend que Slack les ait lus. Si un message ultérieur montre que la tâche est déjà terminée, par exemple si la personne a été sollicitée et a répondu oui, la tâche se clôture automatiquement. **Annuler** permet de la rétablir pendant un jour.

Quand un message plus récent modifie les plans, par exemple si une fête est déplacée dans un autre lieu ou si une réservation est annulée, The Machine met elle-même à jour ses tâches. Une tâche qui reste pertinente suit les nouveaux plans. S’il n’y a plus rien à faire, elle est déplacée dans **Fait / écarté** avec la mention « Pas nécessaire ». Son chat indique « Mis à jour : » et la raison. **Annuler** permet de la rétablir pendant un jour.

Pour vos premières tâches, une courte astuce présente les actions clés : **Demander des modifications** et **Pas nécessaire**, et précise que rien n’est envoyé tant que vous n’appuyez pas sur **Envoyer**. Une astuce disparaît définitivement dès que vous utilisez son bouton ou appuyez sur ×.

Le premier jour, le haut de la page Tâches vous souhaite la bienvenue et indique qui attend votre réponse depuis le plus longtemps. Cette réponse est préparée en premier pour être prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique la personne concernée, son organisation si la tâche porte sur une organisation (et non simplement parce que la personne y travaille), le projet, Travail ou Perso, et la date d’arrivée. Touchez un nom pour ouvrir sa page dans le Graph.

Un nom et une organisation affichent leur photo ou leur logo si le Graph en possède un, sinon leurs initiales. Si un logo est difficile à lire en petit format, par exemple s’il est blanc sur fond transparent ou s’il s’agit d’un long nom stylisé, les initiales s’affichent aussi.

Une ligne discrète indique parfois ce qui n’est pas connu, par exemple « Dernier contact il y a 12 jours par e-mail ; rien depuis ». Elle apparaît lorsque le dernier échange avec cette personne remonte à longtemps ou est resté sans réponse, et mentionne les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine indique ce qu’elle ne sait pas au lieu de faire des suppositions.

Si elle mentionne un canal qui n’est pas connecté, l’option Connecter à côté ouvre la connexion correspondante.

Le titre indique ce qu’il faut faire et ne change que si la tâche elle-même change. Une tâche terminée conserve son titre, avec la façon dont elle s’est terminée en dessous, par exemple « Fait : Sam l’a signé mardi ».

Une ligne discrète au-dessus du brouillon indique le message dont il provient, avec le logo du service concerné. Touchez-la pour lire le fil. Le brouillon affiche le logo du service auquel il est destiné, pour voir tout de suite s’il s’agit d’une réponse Slack ou d’un e-mail.

Si le brouillon tient compte d’une contribution faite ailleurs, par exemple une suggestion d’un collègue sur Slack, une ligne l’indique, par exemple « Selon Sam dans #ops ». Touchez-la pour lire le message.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche comme une seule conversation, de la plus ancienne à la plus récente : les messages qui précèdent celui auquel la tâche se rapporte, puis les réponses qui le suivent. Dans WhatsApp, Telegram ou Signal, vos messages apparaissent à droite, comme dans l’application. Le message à l’origine de la tâche porte la mention « Cette tâche » et s’ouvre directement. **Afficher les messages précédents** ajoute les messages plus anciens. Dans un e-mail, le reste du fil est replié au-dessus et en dessous.

Les **Détails** d’un e-mail n’affichent que les informations absentes de son en-tête, comme les adresses complètes en copie, les adresses en copie cachée ou une autre adresse de réponse. Si rien n’est à ajouter, aucun détail ne s’affiche.

Une réponse dans un fil Slack affiche aussi les messages précédant le début du fil. Le lien d’une tâche vers son propre message l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet, le domaine (touchez l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de codage. **Chat ›** ouvre le chat. Une tâche terminée reste succincte : le message à son origine se trouve sous **Détails**.

Une tâche « En attente de » renvoie à votre dernier message à la personne, celui auquel vous attendez une réponse : « E-mail à Pat · mar. »

## Créer une tâche vous-même

**Nouvelle tâche** (sous **Rechercher** sur ordinateur, **+** sur téléphone ou `N`) permet de créer une tâche pour n’importe quoi. Sa création n’envoie rien. Si vous ne sélectionnez ni **Travail** ni **Perso**, elle est classée au bon endroit selon la personne et le sujet concernés. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il est ancien.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », dans votre langue aussi. L’icône du calendrier propose des choix rapides et l’option **Choisir une date**.
- **Répéter** : la tâche revient à intervalles réguliers. Consultez [Tâches récurrentes](recurring.md).
- **Personne** : associez les personnes ou les entreprises concernées, jusqu’à 5.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, d’un message Slack, Teams, WhatsApp, Telegram ou de tout autre message auquel The Machine a accès. Effectuez une recherche par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : touchez le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur téléphone, l’appareil photo à côté permet de prendre une photo. Vous pouvez joindre jusqu’à 5 fichiers, comme dans le chat (consultez [Ajouter des fichiers](card-chat.md#add-files)). × permet d’en retirer un.

Les fichiers restent associés à la tâche, et The Machine les lit lorsqu’elle s’en occupe. Les fichiers suffisent à eux seuls : elle remplit la tâche à partir d’un PDF ou d’un fichier texte. Une photo s’affiche en petit : touchez-la pour la voir en taille réelle.
