---
title: Tâches
area: cards
summary: Une tâche par élément qui nécessite votre attention, prête à être validée. Comprendre les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: e1656daff6fc566a
---
Votre Machine lit tout ce qui est nouveau et crée une tâche uniquement lorsqu’un élément nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où se trouvent les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, une dernière étape que vous avez confirmée, comme un formulaire ou un problème, a abouti pendant votre absence. Elle reste là jusqu’à ce que vous appuyiez sur **Compris**, pendant un jour maximum, et votre téléphone en est également informé.
- **Pour vous** : tout ce qui attend votre intervention, en commençant par le plus urgent. Chaque tâche indique **Préparée** (un brouillon ou un résultat est prêt, et **Faire** ou **Envoyer** permet de le finaliser), **Vous attend** (une décision ou une réponse de votre part est nécessaire ; si le travail ne peut pas avancer ou être utilisé sans une information que vous seule avez, comme un prix, un fait ou un choix, une ligne sous le titre l’indique), **En préparation…** (votre Machine s’en occupe) ou **À lire** (un récap ou un résumé, sans décision à prendre).
- **Plus anciennes** : les tâches repliées qui n’ont rien de nouveau depuis une semaine (voir ci-dessous).
- **En attente des autres** : les tâches repliées dont la prochaine étape dépend de quelqu’un d’autre (voir ci-dessous).
- **Revient plus tard** : les tâches mises en attente et celles restées sans réponse à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : ce que vous avez promis et ce que les autres vous ont promis. Voir [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec l’heure à laquelle elles ont été terminées, par exemple « Fait il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après un envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Déplacé dans Plus tard jusqu’à lun. ». Une réponse qui se contente de promettre que le travail sera fait, comme « Je l’enverrai d’ici mardi », laisse la tâche ouverte : « Envoyé. Tâche laissée ouverte. » **Ouvrir** permet d’y accéder. La recherche trouve une tâche par son titre ou par son destinataire, y compris dans Plus tard et Fait.

Dans **Pour vous**, les tâches en retard ou à échéance demain au plus tard s’affichent d’abord, suivies des questions de votre Fleet, des relances d’un tableau, puis du reste. Dans chaque groupe, les plus récentes apparaissent en premier. Une tâche garde sa place pendant que votre Machine la prépare et une fois terminée : seul son statut change. Dans les autres groupes ouverts, les tâches en retard ou à échéance demain au plus tard s’affichent d’abord, puis le reste par ordre de date, des plus récentes aux plus anciennes. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine pense que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore clôturée. **Rouvrir** la remet dans votre liste, et votre Machine en tire des enseignements. Ces tâches ne sont jamais signalées comme en retard. Si un message l’indique, elle se clôture automatiquement au bout d’un jour, avec **Annuler**. Sinon, elle attend que vous appuyiez sur **Marquer comme fait**. Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se clôture également automatiquement.

Lorsqu’un message provient d’une adresse qui ressemble à celle d’une personne que vous connaissez, comme sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche le signale clairement : « Ce n’est pas Sam Lee. » Le nom affiché est celui de l’adresse utilisée, jamais celui que la personne a indiqué. Votre Machine vérifie ce type de message auprès de la personne dont vous avez déjà l’adresse, jamais auprès de son auteur.

Une tâche qui attend toujours quelqu’un d’autre, par exemple une relecture ou une réponse, indique cette étape sous **En attente de**. Elle apparaît dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est également le cas après une question que vous avez renvoyée : la tâche réapparaît le matin précédant son échéance, à l’échéance si celle-ci tombe plus tard dans la journée, ou le lendemain matin si elle est passée. Elle indique alors la personne dont elle attend toujours une réponse.

Lorsqu’une tâche concerne un résultat que quelqu’un d’autre doit fournir, comme un contrat signé, **Détails** indique le résultat sous **Terminé quand**. Envoyer votre partie ne clôture pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se clôture automatiquement, avec **Annuler**. Si rien n’arrive avant le moment de relancer la personne, la tâche réapparaît avec **Écrivez une courte relance** dans son chat. Indiquez dans le chat ce qui compte comme terminé pour modifier ce critère.

Une tâche qui n’a rien de nouveau depuis une semaine passe de Pour vous à **Plus anciennes**, afin que les nouvelles tâches apparaissent en premier après quelques jours d’absence. Rien de nouveau signifie qu’il n’y a aucun nouveau message à son sujet et que vous n’avez rien fait, comme écrire dans le chat, modifier la tâche ou la mettre en attente. La consulter ne compte pas.

Les tâches urgentes, celles qui arrivent bientôt à échéance et celles dont l’envoi est en cours restent dans Pour vous. **Tout écarter** marque comme non nécessaires, après une seule confirmation, toutes les tâches de Plus anciennes, comme le fait **Pas nécessaire** pour une tâche à la fois, avec **Annuler**. Toute nouveauté sur une tâche la ramène dans Pour vous.

Une tâche à laquelle personne n’a touché depuis une semaine demande une fois : **Toujours utile ?** **Pas nécessaire** la clôture, avec **Annuler**. **Garder** la conserve, et elle ne vous le demandera plus. Si vous ne répondez pas pendant une semaine supplémentaire, elle est repliée dans Revient plus tard et n’est plus comptabilisée dans le nombre affiché sur l’icône de l’application ni dans le récap du matin. L’ouvrir, écrire dans le chat, la modifier, la mettre en attente ou recevoir un nouveau message la fait réapparaître.

Une fois par semaine, un projet resté inactif et sans tâche ouverte peut donner lieu à une tâche proposant une prochaine étape précise, dans la limite de trois par semaine. Voir [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine se met en veille et la liste reste vide. Pendant une vérification, elle se réveille et vous en informe. Si une vérification a échoué ou est en retard, sa ligne l’indique et propose **Vérifier maintenant**.

Les filtres **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou seulement celles d’un type. Votre téléphone et votre ordinateur appliquent le même choix. Quand Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à la liste complète. Une alerte concernant votre Machine elle-même, comme un composant qui ne cesse de redémarrer, n’est ni Travail ni Perso et apparaît uniquement sous Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre filtre : sous **Perso uniquement**, appuyez sur **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le nom de votre dernier récap du matin ou du soir et ce qu’il comptabilise, par exemple **Récap d’hier soir** · 12 terminées, 3 ouvertes. Appuyez dessus pour relire ce récap, puis sur **Copier** pour le coller où vous voulez. Une fois que vous l’ouvrez ou que vous appuyez sur son **×**, il reste accessible sur tous vos appareils jusqu’au prochain récap.

Sans récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui reste ouvert, pour Travail et Perso, ou uniquement pour le filtre sélectionné.

Une tâche associée à un projet affiche le nom du projet sous son titre. Appuyez dessus pour ouvrir le projet. **Projet**, sous **Détails**, permet de modifier le projet ou de retirer la tâche du projet. Voir [Les tâches d’un projet](projects.md#a-project-s-to-dos).

**Domaine**, sous **Détails**, déplace une tâche vers votre autre domaine. Les éléments auxquels elle peut accéder pour lire et envoyer des messages sont déplacés avec elle. **Annuler** dans la note permet de la déplacer à nouveau.

Lorsqu’une tâche doit passer dans votre autre domaine et que tous les messages dont elle provient s’y trouvent, elle y est déplacée automatiquement et peut continuer. Sinon, elle affiche **Déplacer vers Travail**, et rien ne change tant que vous n’appuyez pas dessus. Une tâche que vous avez créée sans choisir Travail ou Perso est déplacée automatiquement dès que votre Machine trouve à quel domaine elle appartient. En attendant, elle n’est classée ni dans Travail ni dans Perso, et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Si elle a besoin d’autres messages de votre autre domaine, elle le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte mail professionnelle que vous avez étiquetée Perso est considérée comme personnelle. Les e-mails destinés à une autre de vos entreprises sont associés aux tâches de cette entreprise, et une tâche concernant votre vie personnelle, comme un message de votre famille reçu sur votre adresse professionnelle, est personnelle dès le départ.

Un sujet professionnel qui vous parvient sur un compte personnel, comme un client sur WhatsApp, une commande dans votre boîte mail personnelle ou une [promesse](promises.md) concernant le travail, est professionnel dès le départ.

Une tâche que vous avez déplacée ou classée vous-même reste toujours là où vous l’avez mise. Travail ou Perso détermine où la tâche apparaît et avec qui elle est partagée, jamais où elle répond : une réponse est toujours envoyée dans la conversation d’origine, même après un déplacement, sauf si vous choisissez un autre moyen.

Une tâche personnelle de ce type répond tout de même depuis l’adresse professionnelle qui a reçu son e-mail et n’apparaît jamais dans un Fleet Travail ni dans le Graph d’équipe.

S’il y a au moins deux tâches en attente, **Passer en revue** dans l’en-tête de Pour vous les parcourt une par une, dans l’ordre de la liste, avec le brouillon complet et les options **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur un ordinateur, Entrée envoie le contenu affiché, `S` met la tâche en attente, `→` la passe et Échap arrête le parcours. L’en-tête indique le temps nécessaire à votre rythme, par exemple « environ 2 min ».

À la fin, un récapitulatif indique le nombre de tâches envoyées ou clôturées et celles qui sont encore en préparation.

Une tâche qui vous pose une question n’est incluse dans aucun des deux groupes : elle attend votre réponse, pas un appui.

## Vérifier maintenant

Votre Machine consulte chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès qu’il y en a 40 ou que le plus ancien message d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus sont traités lors de la prochaine vérification, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont quand même lus et conservés, puis traités ensemble à 06:30, afin que vos tâches soient prêtes avant votre récap du matin. Sous Connexions, la section Vérifications indique « Suspendues pour la nuit, reprise à 06:30 ». Si vous cliquez, saisissez du texte ou faites défiler l’application, écrivez dans le chat ou appuyez sur une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous soyez inactive depuis une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** consulte immédiatement toutes les sources. Si aucune tâche n’est ouverte, appuyez sur la ligne de votre Machine pour l’afficher, avec **Détails**, qui ouvre les vérifications sous Connexions. S’il y a des tâches ouvertes, l’option se trouve en haut de la liste sur un ordinateur. Une courte ligne s’affiche uniquement pendant une vérification, ou si l’une d’elles a échoué ou est en retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare suivent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans chaque source consultée, par exemple « 13 messages vérifiés à 16:11 · aucune nouvelle tâche » ou « · 2 nouvelles tâches ». Elle concerne uniquement cette vérification : les tâches déjà dans votre liste restent inchangées. Lorsqu’une nouvelle tâche attend un meilleur moment, comme votre récap du matin, la ligne indique jusqu’à quand : « 1 tâche reportée jusqu’à demain 08:30 ».

Appuyez sur la ligne pour voir chaque fil de discussion par e-mail, chat et notification, avec l’icône de sa source : l’auteur, l’objet ou les premiers mots, puis la nouvelle tâche ou la raison pour laquelle le message n’a rien nécessité, comme « Vous étiez seulement en copie, un collègue répond » ou « Réunion déjà prévue jeudi ». Un fil n’indique aucune raison si la vérification n’en a donné qu’une vague. Appuyez sur un élément pour le lire avec les messages qui l’entourent.

Les 10 premiers éléments s’affichent. Appuyez sous leur liste pour voir le reste. Le nombre après un nom, comme (3), indique combien de nouveaux messages contient ce chat. Une notification sur votre téléphone concernant un message déjà répertorié ne s’affiche qu’une fois. La ligne reste visible pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptabilisés. Vos propres réponses sont lues pour comprendre le contexte et les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que The Machine vous envoie, comme votre récap du matin ou une notification de correction, ne sont jamais lus ni répertoriés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche affiche l’étape suivante, par exemple **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Voir [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** permet d’indiquer ce qui doit changer : la façon de procéder ou, une fois le brouillon prêt, les modifications à y apporter. **Marquer comme fait** indique que la tâche est traitée : l’option est visible sur une tâche prête sans brouillon ou sur une tâche qui vous pose une question. Dans les autres cas, elle se trouve en haut du menu **…**. La tâche quitte immédiatement la liste, et la notification propose **Annuler**. Faites glisser le message pour le supprimer ou déplacez-le hors de l’écran avec la souris pour le fermer plus tôt. La modification est conservée.

Pour que la tâche soit faite autrement, dites-le dans son **Chat**. La réponse indique uniquement ce qui a changé, par exemple la mise en attente et sa durée. Si une modification est impossible, comme celle d’une échéance, votre Machine vous le dit.

Sous **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez une relecture](ask-to-review.md).
- **Répéter…** : la tâche [revient à intervalle régulier](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez préciser pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Appuyez sur le titre ou sur **Nom** sous **Détails** pour le modifier, ou demandez-le dans le chat de la tâche, par exemple « Renomme-la en… ». Le titre que vous choisissez est conservé.

**Rouvrir** fait réapparaître une tâche clôturée. Elle réapparaît également automatiquement lorsqu’un nouvel élément survient, comme un nouveau message de la personne concernée, mais pas après votre propre réponse. La tâche indique alors quand elle est revenue et est classée comme nouvelle. Son chat reprend là où il s’était arrêté, même après plusieurs semaines.

Une facture que vous devez encore régler vous-même, quel que soit le pays, devient une tâche qui indique le montant, la date d’échéance et les modalités de paiement figurant sur la facture. Les factures réglées automatiquement, par exemple par prélèvement automatique ou avec une carte enregistrée, ne deviennent pas des tâches. Lorsqu’un e-mail ultérieur confirme le paiement, par exemple un message de l’expéditeur indiquant qu’il l’a reçu, la tâche se clôture automatiquement. **Annuler** la fait réapparaître pendant un jour.

Une tâche qui n’est utile que jusqu’à une heure précise, comme une confirmation à envoyer avant une réunion, se clôture automatiquement une fois cette heure passée. Elle apparaît dans **Fait / écarté** avec la mention « N’est plus nécessaire ». **Annuler** la fait réapparaître pendant un jour.

Avant qu’un message ou un transfert destiné à quelqu’un soit indiqué comme prêt, votre Machine vérifie vos chats récents avec les personnes concernées, y compris les chats de groupe, et attend que Slack les ait lus. Si un message ultérieur montre que la tâche est déjà terminée, par exemple si la personne a été sollicitée et a répondu oui, la tâche se clôture automatiquement. **Annuler** la fait réapparaître pendant un jour.

Si quelqu’un d’autre a écrit dans la même conversation après la rédaction de votre brouillon, **Envoyer** le met en attente : « Non envoyé : nouveau message dans le fil ». La tâche affiche ce message avec **La lire** et **Refaire pour ce message**. Appuyez de nouveau sur **Envoyer** pour envoyer votre brouillon tel quel.

Lorsqu’un message plus récent modifie les plans, par exemple si une fête change de lieu ou si une réservation est annulée, The Machine met à jour ses tâches. Une tâche toujours utile suit les nouveaux plans. Si elle n’a plus rien à faire, elle passe dans **Fait / écarté** avec la mention « Pas nécessaire ». Son chat indique « Mis à jour : » et en donne la raison. **Annuler** la fait réapparaître pendant un jour.

La première fois que vous consultez vos tâches, un bref conseil présente les principales actions : **Demander des modifications** et **Pas nécessaire**, et vous rappelle que rien n’est envoyé avant que vous appuyiez sur **Envoyer**. Le conseil disparaît définitivement dès que vous utilisez son bouton ou appuyez sur ×.

Le premier jour, un message de bienvenue s’affiche en haut de Tâches et indique qui attend votre réponse depuis le plus longtemps. Cette réponse est rédigée en priorité afin d’être prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique la personne concernée, l’organisation s’il y en a une (pas simplement parce qu’une personne y travaille), le projet, Travail ou Perso, ainsi que la date de réception. Appuyez sur un nom pour ouvrir la page correspondante dans le Graph.

Un nom et une organisation affichent leur photo ou leur logo si le Graph en possède un, sinon leurs initiales. Si un logo est illisible en petit, par exemple du texte blanc sur un fond transparent ou un nom très large, l’initiale s’affiche aussi.

Une ligne discrète indique parfois les informations manquantes, par exemple « Dernier contact il y a 12 jours par e-mail ; rien depuis ». Elle s’affiche lorsque le dernier échange avec cette personne est ancien ou sans réponse, et indique les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine indique ce qu’elle ne sait pas au lieu de deviner.

Lorsqu’un canal non connecté est indiqué, **Connecter** à côté permet de le connecter.

Un titre indique ce qu’il faut faire et ne change que si cela change. Une tâche terminée conserve son titre, suivi de la façon dont elle s’est terminée, par exemple « Fait : Sam l’a signé mardi ».

Une ligne discrète au-dessus du brouillon indique le message dont il provient, avec le logo du service. Appuyez dessus pour lire le fil. Le brouillon affiche le logo de sa destination, pour voir immédiatement s’il s’agit d’une réponse Slack ou d’un e-mail.

Si le brouillon s’appuie sur la contribution d’une personne ailleurs, comme la suggestion d’un collègue dans Slack, une ligne l’indique, par exemple « Inspiré par Sam dans #ops ». Appuyez dessus pour lire le message. Cette référence disparaît lorsqu’une mise à jour remplace le brouillon.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche sous la forme d’une seule conversation, de la plus ancienne à la plus récente : les messages qui précèdent celui concerné par la tâche, puis les réponses suivantes. Dans WhatsApp, Telegram ou Signal, vos messages apparaissent à droite, comme dans l’application. Le message associé à la tâche porte la mention « Cette tâche » et s’affiche dans la conversation. **Afficher les messages précédents** ajoute les messages plus anciens. Les autres messages du fil d’un e-mail sont repliés au-dessus et en dessous du message concerné.

Un message s’ouvre de la même façon depuis la recherche, le Graph, les réponses d’Ask ou la dernière vérification. Il porte la mention « Ce message » (ou « Nouveaux messages »).

**Ouvrir dans Gmail** ouvre l’e-mail dans le compte Gmail qui l’a reçu. Sur Android, il s’ouvre dans l’application Gmail si elle est installée.

Les **Détails** d’un e-mail n’affichent que les informations absentes de son en-tête, comme les adresses complètes en copie, les adresses en copie cachée ou une adresse de réponse différente. S’il n’y a rien à ajouter, aucun détail ne s’affiche.

Une réponse dans un fil Slack affiche également les messages envoyés avant le début du fil. Le lien d’une tâche vers le message d’origine l’ouvre aussi ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet et le domaine de la tâche (appuyez sur l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de programmation. Appuyez sur son titre pour ouvrir le chat. Une tâche terminée reste compacte ; le message dont elle provient se trouve sous **Détails**.

Une tâche « En attente de » renvoie au dernier message que vous avez envoyé à la personne, celui dont vous attendez la suite : « E-mail à Pat · mar. ».

## Créer une tâche

**Nouvelle tâche** (sous **Rechercher** sur un ordinateur, **+** sur un téléphone ou `N`) permet de créer une tâche pour n’importe quel sujet. Sa création n’envoie rien. Si vous ne choisissez ni **Travail** ni **Perso**, la tâche est classée là où elle doit l’être, selon la personne et le sujet concernés. Elle retrouve également l’e-mail auquel elle fait suite, même s’il est ancien.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », y compris dans votre langue. L’icône de calendrier propose des choix rapides et **Choisir une date**.
- **Répéter** : la tâche revient à intervalle régulier. Voir [Tâches récurrentes](recurring.md).
- **Personne** : associez jusqu’à 5 personnes ou entreprises concernées.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, d’un message Slack, Teams, WhatsApp, Telegram ou de tout autre message accessible à The Machine. Recherchez par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : appuyez sur le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur un téléphone, l’icône d’appareil photo à côté permet de prendre une photo. Vous pouvez ajouter jusqu’à 5 fichiers, comme dans le chat (voir [Ajouter des fichiers](card-chat.md#add-files)). Appuyez sur × pour en retirer un.

Les fichiers restent associés à la tâche, et The Machine les lit lorsqu’elle s’en occupe. Les fichiers suffisent à eux seuls : elle crée la tâche à partir d’un PDF ou d’un fichier texte. Une photo s’affiche sous forme de petite image. Appuyez dessus pour la voir en taille réelle.
