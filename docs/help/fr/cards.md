---
title: Tâches
area: cards
summary: Une tâche par élément qui nécessite votre attention, prête à recevoir votre validation. Découvrez ce que signifient les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 91b111b2d6f2a97b
---
Votre Machine lit tout ce qui est nouveau et crée une tâche uniquement quand quelque chose nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où trouver les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, vous retrouvez une dernière étape que vous avez confirmée, comme un formulaire ou un problème, et qui a abouti pendant votre absence. Elle reste là jusqu’à ce que vous appuyiez sur **Compris**, pendant un jour maximum. Vous la voyez aussi sur votre téléphone.
- **Pour vous** : tout ce qui attend votre intervention, avec d’abord les échéances prévues d’ici demain. Chaque tâche porte l’un de ces statuts : **Préparée** (un brouillon ou un résultat est prêt, et **Faire** ou **Envoyer** permet de le finaliser), **Vous attend** (elle nécessite d’abord une décision ou une réponse de votre part ; quand le travail ne peut pas avancer ou être utilisé sans une information que vous seule avez, comme un prix, un fait ou un choix, une ligne sous le titre l’indique), **En préparation…** (votre Machine y travaille) ou **À lire** (un récap ou un résumé, sans décision à prendre).
- **Plus anciennes** : tâches repliées qui n’ont rien de nouveau depuis une semaine (voir plus bas).
- **En attente des autres** : tâches repliées dont la prochaine étape dépend de quelqu’un d’autre (voir plus bas).
- **Revient plus tard** : tâches mises en attente, messages qui [partiront plus tard](send-later.md) et tâches restées sans réponse à **Toujours utile ?** (voir plus bas).
- **Promesses** : ce que vous avez promis et ce que les autres vous ont promis. Voir [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec leur date de fin, par exemple « Terminée il y a 5 minutes ». Les tâches qui semblent déjà terminées portent le statut **Semble fait**.

Après l’envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Mis en attente jusqu’à lundi. ». Si votre réponse promet seulement que le travail sera fait, par exemple « Je l’enverrai d’ici mardi », la tâche reste ouverte : « Envoyé. La tâche reste ouverte. » **Ouvrir** vous y mène. La recherche trouve une tâche par son titre ou par son destinataire, y compris dans Revient plus tard et Fait.

Dans **Pour vous**, les tâches en retard ou dont l’échéance est demain ou avant s’affichent d’abord, puis les questions de votre Fleet, les suivis d’un tableau, et enfin le reste. Dans chaque groupe, les plus récentes s’affichent en premier. Une tâche garde sa place pendant que votre Machine la prépare et une fois terminée : seul son statut change. Dans les autres groupes ouverts, les tâches en retard ou dont l’échéance est demain ou avant s’affichent d’abord, puis les autres, de la plus récente à la plus ancienne. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore clôturée. **Rouvrir** la remet dans votre liste, et votre Machine en tire des enseignements. Ces tâches ne sont jamais en retard. Quand un message l’indique, la tâche se clôt automatiquement au bout d’un jour, avec **Annuler**. Sinon, elle attend que vous appuyiez sur **Marquer comme fait**.

Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se clôt également automatiquement. Une réponse indiquant qu’un fichier est joint alors qu’il ne l’est pas ne clôt pas la tâche.

Quand un message provient d’une adresse qui ressemble seulement à celle d’une personne que vous connaissez, par exemple sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche l’indique clairement : « Ce n’est pas Sam Lee. » Le message affiche l’adresse réelle de la personne, jamais le nom qu’elle a utilisé. Votre Machine vérifie ce type de message auprès de la personne dont vous avez déjà l’adresse, jamais auprès de son expéditeur.

Une tâche qui attend toujours quelqu’un d’autre, par exemple une révision ou une réponse, indique cette étape avec **En attente de :**. Elle apparaît dans **En attente des autres**, dans une section repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la réactive. C’est aussi le cas après que vous avez posé une question en retour : la tâche revient le matin précédant son échéance, à l’échéance si celle-ci tombe plus tard dans la journée, ou le lendemain matin si l’échéance est passée. Elle indique alors la personne dont elle dépend toujours.

Quand une tâche concerne un résultat fourni par quelqu’un d’autre, comme un contrat signé, **Détails** l’indique sous **Terminé quand**. Envoyer votre partie ne clôt pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se clôt automatiquement, avec **Annuler**. Si rien n’arrive au moment de relancer la personne, la tâche revient avec l’option **Écrivez une courte relance** dans son chat. Indiquez dans le chat ce qui permettra de considérer la tâche comme terminée.

Une tâche qui n’a rien de nouveau depuis une semaine passe de Pour vous à **Plus anciennes**, pour faire passer les tâches récentes en premier après quelques jours d’absence. Rien de nouveau signifie qu’il n’y a eu ni nouveau message ni action de votre part sur cette tâche, comme un message dans le chat, une modification ou une mise en attente. La consulter ne compte pas.

Les tâches urgentes, celles dont l’échéance approche et celles dont l’envoi est en cours restent dans Pour vous. **Tout écarter** marque toutes les tâches de Plus anciennes comme inutiles après une seule confirmation, comme le fait **Pas nécessaire** pour une tâche à la fois, avec **Annuler**. Une nouveauté sur une tâche la ramène dans Pour vous.

Une tâche laissée sans activité pendant une semaine vous demande une fois : **Toujours utile ?** **Pas nécessaire** la clôt, avec **Annuler**. **Garder** la conserve, et la question ne s’affiche plus. Sans réponse pendant une semaine de plus, elle passe dans Revient plus tard et n’est plus comptée dans le nombre affiché sur l’icône de l’app ni dans le récap du matin. L’ouvrir, envoyer un message dans le chat, la modifier, la mettre en attente ou recevoir un nouveau message la fait réapparaître.

Une fois par semaine, un projet sans activité et sans tâche ouverte peut recevoir une tâche indiquant une prochaine étape précise, dans la limite de trois par semaine. Voir [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine se met en veille et la liste reste vide. Pendant une vérification, elle se réveille et vous l’indique. Si une vérification a échoué ou a pris du retard, une ligne le précise, avec **Vérifier maintenant** en dessous.

Les filtres **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou uniquement celles d’un type. Votre téléphone et votre ordinateur utilisent le même filtre. Quand Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à l’ensemble des tâches. Une alerte sur votre Machine elle-même, comme un composant qui redémarre sans cesse, n’est ni Travail ni Perso et ne s’affiche que dans Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre filtre : dans **Perso uniquement**, appuyez sur **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le dernier récap du matin ou du soir et ce qu’il comptait, par exemple **Récap d’hier soir** · 12 terminées, 3 ouvertes. Appuyez dessus pour relire le récap, avec **Copier** pour le coller où vous voulez. Dès que vous l’ouvrez ou appuyez sur son **×**, il reste disponible sur tous vos appareils jusqu’au prochain récap.

Sans récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui reste à faire, pour Travail et Perso, ou seulement pour le filtre sélectionné.

Une tâche liée à un projet affiche le nom de celui-ci sous son titre. Appuyez dessus pour ouvrir le projet. **Projet** sous **Détails** permet de le modifier ou de retirer la tâche du projet. Voir [Les tâches d’un projet](projects.md#a-project-s-to-dos).

**Domaine** sous **Détails** permet de déplacer une tâche dans votre autre domaine. Les sources qu’elle peut consulter et les messages qu’elle peut envoyer sont déplacés avec elle. **Annuler** dans la note permet de la remettre à sa place.

Quand une tâche doit passer dans votre autre domaine pour avancer, et que tous les messages dont elle provient s’y trouvent, elle y est déplacée automatiquement et le travail continue. Sinon, l’option **Déplacer vers Travail** s’affiche, et rien ne bouge tant que vous n’appuyez pas dessus. Une tâche que vous avez créée sans choisir Travail ou Perso est déplacée automatiquement dès que son domaine est identifié. En attendant, elle n’est associée ni à Travail ni à Perso, et reste privée.

Une tâche peut toujours consulter les messages dont elle provient. Quand elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte de réception professionnelle que vous avez classée comme Perso compte comme Perso. Les e-mails destinés à une autre de vos entreprises sont associés aux tâches de cette entreprise, et une tâche concernant votre vie personnelle, comme un membre de votre famille qui écrit à votre adresse professionnelle, est classée Perso dès le départ.

Le travail qui vous parvient sur un compte personnel, comme un client sur WhatsApp, une commande dans votre boîte de réception personnelle ou une [promesse](promises.md) concernant le travail, est classé Travail dès le départ.

Une tâche que vous avez déplacée ou classée vous-même reste toujours à l’endroit où vous l’avez mise. Travail ou Perso détermine où une tâche s’affiche et avec qui elle est partagée, jamais où elle répond : une réponse est toujours envoyée dans la conversation concernée, même après un déplacement, sauf si vous choisissez une autre option.

Une tâche classée Perso répond toujours depuis l’adresse professionnelle à laquelle son e-mail a été envoyé, et n’apparaît jamais dans un Fleet Travail ni dans le Graph d’équipe.

Quand au moins deux tâches vous attendent, **Passer en revue** dans l’en-tête de Pour vous les parcourt une par une, dans l’ordre de la liste, en affichant chaque brouillon en entier, avec **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur ordinateur, Entrée envoie le contenu affiché, `S` met la tâche en attente, `→` la passe et Échap arrête le parcours. L’en-tête indique le temps nécessaire à votre rythme, par exemple « environ 2 min ».

À la fin, un récap indique ce qui a été envoyé ou clôturé et ce qui est encore en préparation.

Les tâches qui vous posent une question n’apparaissent dans aucun de ces groupes : elles attendent votre réponse, pas un clic.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès qu’il y en a 40 en attente ou que le message le plus ancien d’une personne est en attente depuis 15 minutes. Les newsletters, notifications et reçus sont traités lors de la vérification suivante, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont toujours lus et conservés, puis traités ensemble à 06:30, pour que vos tâches soient prêtes avant le récap du matin. Dans Connexions, les vérifications affichent « Suspendues pour la nuit, reprise à 06:30 ». Si vous cliquez, saisissez du texte ou faites défiler l’app, écrivez dans le chat ou appuyez sur une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous soyez inactive depuis une heure. **Vérifier maintenant** lance toujours une vérification immédiatement.

**Vérifier maintenant** lance immédiatement la vérification de toutes les sources. Si aucune tâche n’est ouverte, appuyez sur la ligne de votre Machine pour la voir, avec **Détails**, qui ouvre Vérifications sous Connexions. Si des tâches sont ouvertes, l’option se trouve en haut sur ordinateur. Une courte ligne s’affiche uniquement pendant une vérification, ou si l’une d’elles a échoué ou pris du retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare suivent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans chaque source consultée, par exemple « 13 messages vérifiés à 16:11 · aucune nouvelle tâche » ou « · 2 nouvelles tâches ». Cette ligne concerne uniquement cette vérification : les tâches déjà dans votre liste restent telles quelles. Quand une nouvelle tâche attend un moment plus propice, comme le récap du matin, la ligne indique jusqu’à quand : « 1 tâche mise en attente jusqu’à demain 08:30 ».

Appuyez sur la ligne pour voir chaque fil d’e-mails, chat et notification, accompagné de l’icône de sa source : l’expéditeur, l’objet ou les premiers mots, ainsi que la nouvelle tâche ou la raison pour laquelle le message n’a nécessité aucune action, comme « Vous étiez en copie, un collègue répond » ou « Réunion déjà prévue jeudi ». Un fil n’indique aucune raison si la vérification n’en a donné qu’une vague. Appuyez sur un élément pour le lire, avec les messages qui l’entourent.

Les 10 premiers éléments s’affichent. Appuyez dessous pour voir le reste. Le nombre après un nom, comme (3), indique combien de nouveaux messages contient ce chat. Une notification sur un téléphone concernant un message déjà affiché ne s’affiche qu’une fois. La ligne reste visible pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptés. Vos réponses sont lues pour comprendre le contexte et les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que The Machine vous envoie, comme votre récap du matin ou un avis de correctif, ne sont jamais lus ni affichés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche affiche sa prochaine étape, comme **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Voir [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** permet de préciser ce qu’il faut changer : la façon de faire ou, une fois le brouillon prêt, son contenu. Si vous laissez votre demande inachevée, elle vous attendra à votre retour ; **Annuler** la supprime.

**Marquer comme fait** indique que la tâche est traitée. Sur ordinateur, cette option se trouve avec les autres boutons quand ils tiennent sur une seule ligne. Sur téléphone, elle est visible pour une tâche prête sans brouillon ou qui vous pose une question ; sinon, elle se trouve en haut du menu **…**. La tâche quitte immédiatement la liste, avec **Annuler** dans le message. Faites glisser le message pour le fermer, ou faites-le glisser avec la souris pour le fermer plus tôt. Le changement est conservé.

Pour faire autrement, indiquez-le dans son **Chat**. La réponse précise uniquement ce qui a changé, par exemple une mise en attente et sa durée. Si un élément n’a pas pu être modifié, comme une échéance, elle vous le dit.

Dans **…** :

- **Transférer…** : attribuer la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demander une révision](ask-to-review.md).
- **Répéter…** : la tâche [revient selon une fréquence définie](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez aussi indiquer pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Appuyez sur le titre ou sur **Nom** sous **Détails** pour le modifier, ou demandez-le dans le chat de la tâche, par exemple « Renomme-la en… ». Votre titre est conservé.

**Rouvrir** rétablit une tâche clôturée. Elle réapparaît aussi automatiquement en cas de nouveauté, par exemple si la personne vous envoie un nouveau message, mais pas à la suite de votre propre réponse. La tâche indique alors qu’elle est de retour et est classée parmi les nouvelles. Son chat reprend là où il s’était arrêté, même après plusieurs semaines.

Une facture que vous devez payer vous-même, quel que soit le pays, devient une tâche indiquant le montant, la date d’échéance et les modalités de paiement fournies sur la facture. Les factures réglées automatiquement, par exemple par prélèvement ou avec une carte enregistrée, ne deviennent pas des tâches. Si un e-mail ultérieur confirme le paiement, par exemple lorsque l’expéditeur confirme avoir reçu votre règlement, la tâche se clôt automatiquement. **Annuler** permet de la rétablir pendant un jour.

Une tâche qui n’était utile que jusqu’à une heure précise, comme une confirmation à envoyer avant une réunion, se clôt automatiquement une fois cette heure passée. Elle passe dans **Fait / écarté** avec la mention « N’est plus nécessaire ». **Annuler** permet de la rétablir pendant un jour.

Avant qu’un message ou un transfert destiné à quelqu’un soit indiqué comme prêt, votre Machine vérifie vos discussions récentes avec les personnes concernées, y compris les discussions de groupe, et attend que Slack les ait lues. Si un message ultérieur montre que la tâche est déjà terminée, par exemple si la personne a été sollicitée et a accepté, la tâche se clôt automatiquement. **Annuler** permet de la rétablir pendant un jour.

Si quelqu’un d’autre a écrit dans la même conversation après la création du brouillon, **Envoyer** le met en attente : « Non envoyé : nouveau message dans le fil ». La tâche affiche ce message avec **La lire** et **Refaire pour ce message**. Appuyez de nouveau sur **Envoyer** pour envoyer le brouillon tel quel.

Quand un message plus récent change les plans, par exemple si une fête est déplacée ou si une réservation est annulée, The Machine met à jour ses tâches automatiquement. Une tâche toujours nécessaire suit les nouveaux plans. Une tâche qui n’a plus rien à faire passe dans **Fait / écarté** avec la mention « Pas nécessaire », son chat indique « Mise à jour : » suivie de la raison, et **Annuler** permet de la rétablir pendant un jour.

Lors de vos premières utilisations des tâches, une courte astuce présente les principales actions : **Demander des modifications** et **Pas nécessaire**, ainsi que le fait que rien n’est envoyé avant d’appuyer sur **Envoyer**. L’astuce disparaît définitivement dès que vous utilisez le bouton correspondant ou appuyez sur ×.

Le premier jour, le haut de la page Tâches vous souhaite la bienvenue et indique qui attend votre réponse depuis le plus longtemps. Cette réponse est préparée en premier pour être prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique les personnes concernées, l’organisation si la tâche porte sur une organisation (jamais simplement parce qu’une personne y travaille), le projet, Travail ou Perso, et la date de réception. Appuyez sur un nom pour ouvrir sa page dans le Graph.

Les noms et les organisations affichent leur photo ou leur logo si le Graph en possède un, et leurs initiales dans le cas contraire. Si un logo est illisible en petit, par exemple un logo blanc sur fond transparent ou une longue signature visuelle, les initiales s’affichent aussi.

Parfois, une ligne discrète indique ce qui est inconnu, par exemple « Dernier contact il y a 12 jours par e-mail ; rien depuis ». Elle s’affiche si le dernier échange avec cette personne remonte à longtemps ou est resté sans réponse, et indique les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine préfère dire ce qu’elle ne sait pas plutôt que de deviner.

Quand elle indique un canal qui n’est pas connecté, l’option Connecter à côté ouvre cette connexion.

Un titre indique ce qu’il faut faire et ne change que si la tâche change. Une tâche terminée conserve son titre, avec la façon dont elle s’est terminée en dessous, par exemple « Terminée : Sam l’a signée mardi ».

Au-dessus du brouillon, une ligne discrète indique le message dont il provient, avec le logo du service. Appuyez dessus pour lire le fil. Le brouillon affiche le logo de sa destination, pour voir immédiatement s’il s’agit d’une réponse Slack ou d’un e-mail.

Quand le brouillon tient compte d’une contribution d’une autre personne, par exemple la suggestion d’un collègue dans Slack, une ligne le précise, par exemple « D’après Sam dans #ops ». Appuyez dessus pour lire le message. Cette indication disparaît quand une mise à jour remplace le brouillon.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche comme une seule conversation, du plus ancien au plus récent : les messages qui précèdent celui concerné par la tâche, puis les réponses qui le suivent. Dans WhatsApp, Telegram ou Signal, vos messages s’affichent à droite, comme dans l’app. Le message lié à la tâche porte la mention « Cette tâche » et s’ouvre directement dans la conversation. **Afficher les messages précédents** ajoute les messages plus anciens. Les autres messages d’un fil d’e-mails sont repliés au-dessus et en dessous de celui concerné.

Un message s’ouvre de la même façon depuis la recherche, le Graph, les réponses d’Ask ou la dernière vérification. Il porte la mention « Ce message » (ou « Nouveaux messages »).

**Ouvrir dans Gmail** ouvre l’e-mail dans le compte Gmail qui l’a reçu. Sur Android, il s’ouvre dans l’app Gmail si elle est installée.

Les **Détails** d’un e-mail affichent uniquement les informations absentes de son en-tête, comme les adresses complètes en Cc, les destinataires en Cci ou une adresse de réponse différente. Si aucune information n’est à ajouter, cette section ne s’affiche pas.

Une réponse dans un fil Slack affiche aussi les messages échangés avant le début du fil. Le lien d’une tâche vers son propre message l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet et le domaine de la tâche (appuyez sur l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de programmation. Son titre ouvre le chat. Une tâche terminée reste succincte ; le message dont elle provient se trouve sous **Détails**.

Une tâche en attente indique un lien vers votre dernier message à la personne, celui dont vous attendez la suite : « E-mail à Pat · mar. ».

## Créer une tâche

**Nouvelle tâche** (sous **Rechercher** sur ordinateur, **+** sur téléphone ou `N`) permet d’ajouter une tâche pour n’importe quel sujet. La créer n’envoie rien. Si vous ne sélectionnez ni **Travail** ni **Perso**, elle est classée au bon endroit selon les personnes et le sujet concernés. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il est ancien.

Fermez le formulaire avant d’ajouter la tâche pour retrouver votre texte et vos choix la prochaine fois ; les fichiers, eux, ne sont pas conservés. **Supprimer** dans le message permet de les supprimer.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », y compris dans votre langue. L’icône du calendrier propose des choix rapides et **Choisir une date**.
- **Répéter** : la tâche revient selon une fréquence définie. Voir [Tâches récurrentes](recurring.md).
- **Personne** : associez jusqu’à 5 personnes ou entreprises concernées.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, d’un message Slack, Teams, WhatsApp, Telegram ou de tout autre message accessible à The Machine. Recherchez par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : appuyez sur le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur téléphone, l’appareil photo à côté permet de prendre une photo. Vous pouvez ajouter jusqu’à 5 fichiers, comme dans le chat (voir [Ajouter des fichiers](card-chat.md#add-files)). × permet de retirer un fichier.

Les fichiers restent associés à la tâche, et The Machine les lit lorsqu’elle s’en occupe. Les fichiers suffisent à eux seuls : elle remplit la tâche à partir d’un PDF ou d’un fichier texte. Une photo s’affiche sous forme de petite image ; appuyez dessus pour l’agrandir.
