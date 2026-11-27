---
title: Tâches
area: cards
summary: Une tâche par élément qui nécessite votre intervention, prête à recevoir votre accord. Découvrez ce que signifient les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: b218e3423a2162c5
---
Votre Machine lit chaque nouveauté et crée une tâche uniquement si quelque chose nécessite votre intervention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où se trouvent les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, une dernière étape que vous avez confirmée, comme un formulaire ou un ticket, a abouti pendant votre absence. Elle reste affichée jusqu’à ce que vous touchiez **Compris**, pendant un jour maximum, et votre téléphone en est aussi informé.
- **Pour vous** : tout ce qui attend votre intervention, en commençant par ce qui est dû au plus tard demain. Chaque tâche indique **Préparée** (un brouillon ou un résultat est prêt, et **Faire** ou **Envoyer** permet de le finaliser), **Vous attend** (une décision ou une réponse est d’abord nécessaire ; si le travail ne peut pas avancer ou être utilisé sans une information que vous seule avez, comme un prix, un fait ou un choix, une ligne sous le titre l’indique), **En préparation…** (votre Machine travaille dessus) ou **À lire** (un récap ou un compte rendu, sans décision à prendre).
- **Plus anciennes** : les tâches repliées qui n’ont rien de nouveau depuis une semaine (voir ci-dessous).
- **En attente des autres** : les tâches repliées dont la prochaine étape revient à quelqu’un d’autre (voir ci-dessous).
- **Revient plus tard** : les tâches mises en attente, les messages qui [arrivent plus tard](send-later.md) et celles restées sans réponse à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : ce que vous avez promis et ce que d’autres vous ont promis. Consultez [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec la date de fin, par exemple « Fait il y a 5 min ». Les tâches qui semblent déjà terminées sont marquées **Semble fait**.

Après un envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Déplacé dans Plus tard jusqu’à lun. ». Une réponse qui promet seulement de faire le travail, comme « Je l’enverrai d’ici mardi », ne ferme pas la tâche : « Envoyé. Tâche conservée. » **Ouvrir** permet d’y accéder. La recherche trouve une tâche par son titre ou par le destinataire, y compris dans Plus tard et Fait.

**Pour vous** affiche d’abord les tâches en retard ou dues au plus tard demain, puis les questions de votre Fleet, les suivis d’un tableau et le reste. Dans chaque groupe, les plus récentes apparaissent en premier. Une tâche garde sa place pendant que votre Machine la prépare et une fois terminée : seul son statut change. Dans les autres groupes ouverts, les tâches en retard ou dues au plus tard demain apparaissent d’abord, puis les plus récentes. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore fermée. **Rouvrir** la remet dans votre liste et votre Machine en tient compte. Ces tâches ne sont jamais signalées comme en retard. Quand un message l’indique, la tâche se ferme automatiquement après un jour, avec **Annuler**. Sinon, elle attend que vous choisissiez **Marquer comme fait**.

Une tâche que vous avez déjà réglée vous-même, par exemple en répondant dans Gmail ou Slack, se ferme aussi automatiquement. Une réponse qui indique qu’un fichier est joint alors qu’il ne l’est pas ne ferme pas la tâche.

Si un message vient d’une adresse qui ressemble seulement à celle d’une personne que vous connaissez, comme sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche l’indique clairement : « Ce n’est pas Sam Lee. » Le nom affiché est celui de l’adresse réelle, jamais celui indiqué par l’expéditeur. Votre Machine vérifie ce type de message auprès de la personne dont vous avez déjà l’adresse, jamais auprès de l’expéditeur.

Une tâche qui attend toujours quelqu’un d’autre, par exemple une révision ou une réponse, indique l’étape avec **En attente de :**. Elle apparaît dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est aussi le cas après que vous avez posé une question : la tâche revient le matin précédant son échéance, à l’échéance si elle tombe plus tard dans la journée, ou le lendemain matin si elle est dépassée. Elle indique alors la personne dont elle attend toujours la réponse.

Quand une tâche porte sur un résultat que quelqu’un d’autre doit fournir, comme un contrat signé, **Détails** l’indique sous **Terminé quand**. Envoyer votre partie ne ferme pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat. Elle se ferme alors automatiquement et affiche le résultat et **Annuler**. Si rien n’arrive au moment de relancer la personne, la tâche réapparaît avec **Écrivez une courte relance** dans son chat. Pour modifier ce qui compte comme terminé, indiquez-le dans le chat.

Avant de fermer la tâche, votre Machine compare le résultat avec ce qui a été convenu dans le fil, comme le prix, le texte ou le lien que vous avez envoyé. Elle ne ferme la tâche que si tout correspond, et indique ce qu’elle a vérifié. Si un élément diffère, si votre accord n’a pas été demandé ou si votre partie d’un échange n’est pas encore terminée, la tâche réapparaît et l’indique.

Si le résultat doit apparaître sur une page Web publique mentionnée dans les messages, comme un article qui doit vous citer, votre Machine consulte cette page au moment de relancer la personne. Si le résultat y figure et qu’il n’y figurait pas au début de l’attente, il est vérifié de la même manière avant la fermeture de la tâche. Votre Machine consulte seulement la page, comme n’importe quel visiteur, et n’envoie jamais rien.

Si le résultat n’apparaît pas sur la page et que l’échéance n’est pas encore passée, votre Machine consulte la page une fois de plus le matin suivant l’échéance. Sinon, la tâche réapparaît comme avant, avec « Vérifié » ou « Impossible à ouvrir » et la page dans son chat.

Après une semaine sans nouveauté, une tâche passe de Pour vous à **Plus anciennes**, pour que les nouvelles tâches s’affichent en premier après quelques jours d’absence. Il n’y a rien de nouveau lorsqu’il n’y a pas de nouveau message ni d’action de votre part sur la tâche, comme un message dans le chat, une modification ou une mise en attente. Le simple fait de la consulter ne compte pas.

Les tâches urgentes, bientôt dues et dont l’envoi est en cours restent dans Pour vous. **Tout écarter** marque toutes les tâches de Plus anciennes comme non nécessaires après une seule confirmation, comme le fait **Pas nécessaire** pour une tâche à la fois, avec **Annuler**. Toute nouveauté sur une tâche la remet dans Pour vous.

Une tâche à laquelle personne n’a touché depuis une semaine demande une fois : **Toujours utile ?** **Pas nécessaire** la ferme, avec **Annuler**. **Garder** la conserve et la question ne sera plus posée. Sans réponse la semaine suivante, elle est repliée dans Revient plus tard, et elle n’est plus comptabilisée dans le nombre affiché sur l’icône de l’application ni dans le récap du matin. La consulter, envoyer un message dans son chat, la modifier, la mettre en attente ou recevoir un nouveau message la fait réapparaître.

Une fois par semaine, un projet sans activité et sans tâche ouverte peut recevoir une tâche avec une prochaine étape précise, dans la limite de trois par semaine. Consultez [Projets](projects.md).

Quand rien ne nécessite votre intervention, votre Machine se repose et la liste reste vide. Pendant une vérification, elle se réveille et vous le signale. Si une vérification a échoué ou est en retard, sa ligne l’indique et affiche **Vérifier maintenant**.

Les options **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou uniquement celles d’un type. Le même choix s’applique sur votre téléphone et votre ordinateur. Lorsque Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à l’ensemble des tâches. Une alerte concernant votre Machine elle-même, comme un composant qui redémarre sans cesse, n’est ni liée au Travail ni personnelle et apparaît uniquement sous Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre option : sous **Perso uniquement**, touchez **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le titre de votre dernier récap du matin ou du soir et le nombre d’éléments qu’il contient, par exemple **Récap d’hier soir** · 12 terminés, 3 ouverts. Touchez-la pour relire ce récap, puis **Copier** pour le coller où vous voulez. Dès que vous l’ouvrez ou que vous touchez son **×**, il est disponible sur tous vos appareils jusqu’au prochain récap.

Sans récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : ce qui a été terminé aujourd’hui et ce qui est encore en cours, pour Travail et Perso ou uniquement pour l’option sélectionnée.

Une tâche liée à un projet affiche le nom du projet sous son titre. Touchez-le pour ouvrir le projet. **Projet** sous **Détails** permet de le modifier ou de le retirer. Consultez [Les tâches d’un projet](projects.md#a-project-s-to-dos).

**Domaine** sous **Détails** permet de déplacer une tâche dans votre autre domaine. Les éléments qu’elle peut lire et envoyer sont déplacés avec elle. **Annuler** dans la note permet de la remettre à son emplacement initial.

Lorsqu’une tâche a besoin de votre autre domaine pour continuer et que tous les messages dont elle provient s’y trouvent, elle y est déplacée automatiquement et reprend son cours. Sinon, elle affiche **Déplacer vers Travail** et rien ne change avant que vous la touchiez. Une tâche que vous avez ajoutée sans choisir Travail ou Perso est déplacée automatiquement dès que son domaine est déterminé. En attendant, elle n’est associée ni à Travail ni à Perso, et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Si elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte mail professionnelle que vous avez définie comme personnelle compte comme Perso. Les e-mails destinés à une autre de vos entreprises sont associés aux tâches de cette entreprise. Une tâche qui concerne votre vie personnelle, comme un message d’un membre de votre famille reçu sur votre adresse professionnelle, est personnelle dès le départ.

Le travail qui arrive sur un compte personnel, comme un client sur WhatsApp, une commande dans votre boîte mail personnelle ou une [promesse](promises.md) concernant le travail, est associé à Travail dès le départ.

Une tâche que vous avez déplacée ou classée vous-même reste toujours là où vous l’avez mise. Travail ou Perso détermine où la tâche s’affiche et avec qui elle est partagée, jamais où elle répond : une réponse est toujours envoyée dans la conversation d’origine, même après un déplacement, sauf si vous choisissez une autre option.

Une tâche personnelle de ce type répond quand même depuis l’adresse professionnelle qui a reçu l’e-mail et n’apparaît jamais dans un Fleet Travail ni dans le Graph d’équipe.

S’il y a au moins deux tâches en attente, **Passer en revue** dans l’en-tête de Pour vous les parcourt une par une, dans l’ordre de la liste, en affichant chaque brouillon en entier, avec **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur ordinateur, Entrée envoie le contenu affiché, `S` met en attente, `→` ignore et Échap arrête. L’en-tête indique le temps nécessaire à votre rythme, par exemple « environ 2 min ».

À la fin, un bilan indique le nombre d’éléments envoyés ou fermés et ceux qui sont encore en préparation.

Les tâches qui vous posent une question ne sont pas incluses : elles attendent votre réponse, pas un toucher.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès qu’il y en a 40 en attente ou que le plus ancien message d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus sont vérifiés lors du prochain contrôle, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont toujours lus et conservés, puis vérifiés ensemble à 06:30, afin que vos tâches soient prêtes avant votre récap du matin. Dans Connexions, la ligne de vérification indique « Suspendues pour la nuit, reprise à 06:30 ». Si vous cliquez, écrivez ou faites défiler l’application, écrivez dans le chat ou touchez une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous soyez restée inactive pendant une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit immédiatement toutes les sources. Si aucune tâche n’est ouverte, touchez la ligne de votre Machine pour l’afficher, avec **Détails**, qui ouvre Vérifications dans Connexions. Si des tâches sont ouvertes, cette option se trouve en haut sur ordinateur. Une courte ligne s’affiche uniquement pendant une vérification, ou si l’une d’elles a échoué ou est en retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare gardent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans chaque source consultée, par exemple « 13 messages vérifiés à 16:11 · aucune nouvelle tâche » ou « · 2 nouvelles tâches ». Cette ligne concerne uniquement cette vérification : les tâches déjà présentes dans votre liste restent inchangées. Si une nouvelle tâche attend le bon moment, comme votre récap du matin, la ligne indique jusqu’à quand : « 1 tâche retenue jusqu’à demain 08:30 ».

Touchez la ligne pour afficher chaque fil d’e-mails, chat et notification avec l’icône de sa source : le nom de l’expéditeur, l’objet ou les premiers mots, ainsi que la nouvelle tâche ou la raison pour laquelle le message n’a rien nécessité, par exemple « En copie seulement, un collègue répond » ou « Réunion déjà prévue jeudi ». Un fil n’indique aucune raison si la vérification n’a fourni qu’une explication vague. Touchez un élément pour le lire avec les messages qui l’entourent.

Les 10 premiers éléments s’affichent. Touchez en dessous pour voir le reste. Le nombre après un nom, comme (3), indique le nombre de nouveaux messages dans ce chat. Sur Android, une notification concernant un message déjà affiché n’apparaît qu’une fois. La ligne reste visible pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptabilisés. Vos propres réponses sont lues pour le contexte et les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que votre Machine vous envoie, comme votre récap du matin ou un avis de résolution, ne sont jamais lus ni répertoriés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche affiche sa prochaine étape, par exemple **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Consultez [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** permet de préciser ce qui doit changer : la manière de procéder ou, une fois le brouillon prêt, les éléments à modifier. Si vous commencez à écrire sans terminer, votre texte vous attendra à votre retour. **Annuler** le supprime.

**Marquer comme fait** signifie que la tâche est réglée. Sur ordinateur, cette option apparaît avec les autres boutons lorsqu’ils tiennent sur une ligne. Sur téléphone, elle est visible pour une tâche prête sans brouillon ou pour une tâche qui vous pose une question. Sinon, elle se trouve en haut de **…**. La tâche disparaît aussitôt de la liste et le message affiche **Annuler**. Faites glisser le message pour le fermer ou faites-le glisser avec la souris pour le fermer plus tôt. La modification est conservée.

Pour procéder autrement, dites-le dans le **Chat** de la tâche. La réponse indique uniquement ce qui a changé, par exemple la mise en attente et sa durée. Si une modification n’a pas pu être effectuée, comme celle de l’échéance, votre Machine vous le dit.

Sous **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez à quelqu’un de la réviser](ask-to-review.md).
- **Répéter…** : la tâche [revient à intervalles réguliers](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez préciser pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tient compte.

Touchez le titre ou **Nom** sous **Détails** pour le modifier, ou demandez-le dans le chat, par exemple « Renomme-la en… ». Votre titre est conservé.

**Rouvrir** fait réapparaître une tâche fermée. Elle réapparaît aussi automatiquement quand quelque chose de nouveau se produit, comme un nouveau message de leur part, mais pas après votre propre réponse. La date de réapparition s’affiche alors et la tâche est considérée comme nouvelle pour le tri. Son chat reprend là où il en était, même après plusieurs semaines.

Une facture que vous devez encore payer vous-même, quel que soit le pays, devient une tâche avec le montant, l’échéance et les détails de paiement indiqués sur la facture. Ce n’est pas le cas des factures payées automatiquement, par exemple par prélèvement automatique ou avec une carte enregistrée. Si un e-mail ultérieur confirme le paiement, par exemple un message de l’expéditeur indiquant qu’il l’a reçu, la tâche se ferme automatiquement. **Annuler** permet de la rétablir pendant un jour.

Une tâche qui n’était utile que jusqu’à une heure donnée, comme une confirmation à envoyer avant une réunion, se ferme automatiquement une fois cette heure passée. Elle est déplacée dans **Fait / écarté** avec le statut « N’est plus nécessaire ». **Annuler** permet de la rétablir pendant un jour.

Avant qu’un message ou un transfert destiné à quelqu’un soit prêt, votre Machine vérifie vos chats récents avec les personnes concernées, y compris les chats de groupe, et attend que Slack les ait lus. Si un message ultérieur montre que la tâche est déjà terminée, par exemple si la personne a été sollicitée et a répondu oui, la tâche se ferme automatiquement. **Annuler** permet de la rétablir pendant un jour.

Si quelqu’un d’autre a écrit dans la même conversation après la création de votre brouillon, **Envoyer** le met en attente : « Non envoyé : nouveau message dans le fil ». La tâche affiche le message avec **La lire** et **Refaire pour ce message**. Appuyez à nouveau sur **Envoyer** pour envoyer le brouillon tel quel.

Quand un message plus récent modifie le plan, par exemple si une fête est déplacée ou une réservation annulée, The Machine met elle-même à jour ses tâches. Une tâche qui reste utile suit le nouveau plan. Si rien ne reste à faire, elle est déplacée dans **Fait / écarté** avec la mention « Pas nécessaire ». Son chat indique « Mise à jour : » et la raison, et **Annuler** permet de la rétablir pendant un jour.

La première fois que vous consultez vos tâches, une courte astuce présente les principales actions : **Demander des modifications** et **Pas nécessaire**, et précise que rien n’est envoyé avant que vous appuyiez sur **Envoyer**. L’astuce disparaît définitivement dès que vous utilisez son bouton ou appuyez sur ×.

Le premier jour, le haut de la page Tâches vous souhaite la bienvenue et indique qui attend votre réponse depuis le plus longtemps. Cette réponse est rédigée en priorité pour être prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique la personne concernée, l’organisation si la tâche porte sur une organisation, mais jamais seulement parce que quelqu’un y travaille, le projet, Travail ou Perso, et la date de réception. Touchez un nom pour ouvrir sa page dans Graph.

Si Graph dispose d’une photo ou d’un logo, le nom et l’organisation l’affichent. Sinon, leurs initiales apparaissent. Un logo difficile à lire à cette taille, comme du texte blanc sur fond transparent ou un long nom stylisé, est aussi remplacé par l’initiale.

Une ligne discrète indique parfois ce qui est inconnu, par exemple « Dernier contact par e-mail il y a 12 jours, sans réponse depuis ». Elle apparaît lorsque le dernier échange avec cette personne est ancien ou sans réponse, et précise les canaux non connectés, comme WhatsApp. Votre Machine indique ce qu’elle ne sait pas au lieu de faire des suppositions.

Lorsqu’un canal non connecté est indiqué, **Connecter** à côté ouvre la connexion correspondante.

Le titre indique ce qu’il faut faire et ne change que si la tâche change. Une tâche terminée garde son titre, avec la manière dont elle s’est terminée en dessous, par exemple « Terminé : Sam a signé mardi ».

Au-dessus du brouillon, une ligne discrète indique le message dont il provient, avec le logo du service. Touchez-la pour lire le fil. Le brouillon affiche le logo de sa destination, ce qui permet de voir tout de suite s’il s’agit d’une réponse Slack ou d’un e-mail.

Si le brouillon s’appuie sur une contribution faite ailleurs, comme une suggestion d’un collègue dans Slack, une ligne l’indique, par exemple « Selon Sam dans #ops ». Touchez-la pour lire le message. Elle disparaît lorsqu’une mise à jour remplace le brouillon.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche sous la forme d’une seule conversation, du plus ancien au plus récent : les messages précédant celui auquel la tâche se rapporte, puis les réponses reçues ensuite. Dans WhatsApp, Telegram ou Signal, vos messages s’affichent à droite, comme dans l’application. Le message concerné par la tâche porte la mention « Cette tâche » et s’ouvre directement à l’écran. **Afficher les messages précédents** ajoute les messages plus anciens. Le reste d’un fil d’e-mails apparaît replié au-dessus et au-dessous du message concerné.

Un message s’ouvre de la même manière depuis la recherche, Graph, les réponses d’Ask ou la dernière vérification, avec la mention « Ce message » ou « Nouveaux messages ».

**Ouvrir dans Gmail** ouvre l’e-mail dans le compte Gmail qui l’a reçu. Sur Android, il s’ouvre dans l’application Gmail si vous l’avez installée.

Les **Détails** d’un e-mail affichent uniquement les éléments absents de son en-tête, comme les adresses complètes en Cc, en Cci ou une autre adresse de réponse. S’il n’y a rien à ajouter, cette section n’apparaît pas.

Une réponse dans un fil Slack affiche aussi les messages échangés avant le début du fil. Le lien d’une tâche vers son propre message l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche son nom, son projet et son domaine, que vous pouvez toucher pour les modifier, ainsi que votre dernière note et le résultat d’un agent de programmation. Son titre ouvre le chat. Une tâche terminée reste brève : le message dont elle provient se trouve sous **Détails**.

Une tâche « En attente de » contient un lien vers votre dernier message à la personne, celui dont vous attendez la suite : « E-mail à Pat · mar. ».

## Créer une tâche

**Nouvelle tâche** (sous **Rechercher** sur ordinateur, **+** sur téléphone ou `N`) permet de créer une tâche pour n’importe quel élément. Sa création n’envoie rien. Si vous ne choisissez ni **Travail** ni **Perso**, la tâche est classée selon la personne et le sujet concernés. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il est ancien.

Si vous fermez la fenêtre avant de l’ajouter, votre texte et vos choix seront toujours là la prochaine fois, mais pas les fichiers. **Supprimer** dans le message les retire.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », également dans votre langue. L’icône du calendrier propose des choix rapides et **Choisir une date**.
- **Répéter** : la tâche revient à intervalles réguliers. Consultez [Tâches récurrentes](recurring.md).
- **Personne** : associez les personnes ou les entreprises concernées, jusqu’à 5.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, d’un message Slack, Teams, WhatsApp, Telegram ou de tout autre message accessible à The Machine. Faites une recherche par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : touchez le trombone, collez une capture d’écran ou déposez des fichiers sur le formulaire. Sur téléphone, l’appareil photo à côté permet de prendre une photo. Jusqu’à 5 fichiers, comme dans le chat (consultez [Ajouter des fichiers](card-chat.md#add-files)). Touchez × pour en retirer un.

Les fichiers restent associés à la tâche et The Machine les lit lorsqu’elle travaille dessus. Vous pouvez joindre uniquement des fichiers : elle crée la tâche à partir d’un PDF ou d’un fichier texte. Une photo s’affiche sous forme de petite image. Touchez-la pour la voir en taille réelle.
