---
title: Tâches
area: cards
summary: Une tâche par élément qui nécessite votre attention, prête à être validée. Voici ce que signifient les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 51db64e67403d2ea
---
Votre Machine lit tous les nouveaux messages et crée une tâche uniquement quand quelque chose nécessite votre attention. Une tâche par sujet, même s’il s’étend sur plusieurs messages.

## Où se trouvent les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, vous voyez la dernière étape que vous avez validée, comme l’envoi d’un formulaire ou le traitement d’un problème pendant votre absence. Elle reste affichée jusqu’à ce que vous touchiez **Compris**, pendant un jour maximum. Votre téléphone en est également informé.
- **Pour vous** : tout ce qui attend votre intervention, par ordre d’urgence. Chaque tâche porte l’un de ces statuts : **Préparée** (un brouillon ou un résultat est prêt, et **Faire** ou **Envoyer** permet de le valider), **Vous attend** (elle nécessite d’abord une décision ou une réponse de votre part ; si le travail est bloqué par une information que vous seul pouvez fournir, comme un fait, une connexion ou un choix, une ligne sous le titre vous l’indique), **En préparation…** (votre Machine s’en occupe) ou **À lire** (un récap ou un résumé, sans décision à prendre).
- **Plus anciennes** : les tâches repliées qui n’ont rien de nouveau depuis une semaine (voir ci-dessous).
- **En attente des autres** : les tâches repliées dont la prochaine étape dépend de quelqu’un d’autre (voir ci-dessous).
- **Revient plus tard** : les tâches mises en attente et celles qui n’ont pas reçu de réponse à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : ce que vous avez promis et ce que les autres vous ont promis. Voir [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, de la plus récente à la plus ancienne, avec leur date de fin, par exemple « Fait il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après un envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Déplacé dans Plus tard jusqu’à lun. ». Une réponse qui promet seulement de faire le travail, comme « Je l’enverrai d’ici mardi », laisse la tâche ouverte : « Envoyé. Tâche laissée ouverte. » **Ouvrir** vous y mène. La recherche trouve une tâche par son titre ou par son destinataire, y compris dans Plus tard et Fait.

Dans **Pour vous**, les tâches en retard ou à échéance d’ici demain s’affichent d’abord, suivies des questions de votre Fleet, des suivis d’un tableau, puis du reste. Dans chaque groupe, les plus récentes apparaissent en premier. Une tâche garde sa place pendant que votre Machine s’en occupe et une fois terminée : seul son statut change. Dans les autres groupes ouverts, les tâches en retard ou à échéance d’ici demain apparaissent d’abord, puis le reste, des plus récentes aux plus anciennes. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore clôturée. **Rouvrir** la remet dans votre liste et permet à votre Machine d’en tirer des enseignements. Ces tâches ne sont jamais indiquées comme en retard. Quand un message indique que la tâche est terminée, elle se clôture automatiquement au bout d’un jour, avec **Annuler**. Sinon, elle attend que vous la **Marquiez comme faite**. Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se clôture également automatiquement.

Si un message provient d’une adresse qui ressemble à celle d’une personne que vous connaissez, comme sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche l’indique clairement : « Ce n’est pas Sam Lee. » La personne apparaît sous sa véritable adresse, jamais sous le nom qu’elle a utilisé. Votre Machine vérifie ce type de message auprès de la personne dont vous avez déjà l’adresse, jamais auprès de son expéditeur.

Une tâche qui attend encore une autre personne, par exemple pour une relecture ou une réponse, indique l’étape en **En attente de**. Elle apparaît dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est aussi le cas après que vous avez posé une question : la tâche revient le matin précédant son échéance, à l’échéance si elle tombe plus tard dans la journée, ou le lendemain matin si l’échéance est passée. Elle indique alors la personne dont elle attend toujours une réponse.

Quand une tâche dépend d’un résultat fourni par quelqu’un d’autre, comme un contrat signé, **Détails** indique ce résultat sous **Terminé quand**. L’envoi de votre partie ne clôture pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se clôture automatiquement, avec **Annuler**. Si rien n’arrive au moment de relancer la personne, la tâche réapparaît avec **Écrivez une courte relance** dans son chat. Indiquez dans le chat ce qui compte comme terminé pour modifier ce critère.

Une tâche sans nouveauté depuis une semaine passe de Pour vous à **Plus anciennes**, pour que les nouvelles apparaissent en premier après quelques jours d’absence. Une nouveauté désigne un nouveau message dans la tâche ou une action de votre part, comme un message dans le chat, une modification ou une mise en attente. Le simple fait de la consulter ne compte pas.

Les tâches urgentes, bientôt à échéance et celles dont un envoi est en cours restent dans Pour vous. **Tout écarter** marque comme non nécessaires, après une confirmation, toutes les tâches de Plus anciennes, comme le fait **Pas nécessaire** pour une tâche à la fois, avec **Annuler**. Toute nouveauté dans une tâche la fait revenir dans Pour vous.

Une tâche restée sans intervention pendant une semaine demande une fois : **Toujours utile ?** **Pas nécessaire** la clôture, avec **Annuler**. **Garder** la conserve et la question ne sera plus posée. Sans réponse pendant une autre semaine, elle est repliée dans Revient plus tard et n’est plus comptée sur l’icône de l’application ni dans le récap du matin. Son ouverture, un message dans le chat, une modification, une mise en attente ou un nouveau message la fait réapparaître.

Une fois par semaine, un projet inactif qui n’a aucune tâche ouverte peut donner lieu à une tâche avec une prochaine étape précise, dans la limite de trois par semaine. Voir [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine se met en veille et la liste reste vide. Pendant ses vérifications, elle se réveille et vous en informe. Si une vérification a échoué ou a pris du retard, une ligne vous l’indique, avec **Vérifier maintenant** en dessous.

Les vues **Tout**, **Travail** et **Perso**, en haut de la barre latérale, affichent toutes les tâches ou uniquement celles d’une catégorie. Votre téléphone et votre ordinateur conservent le même choix. Quand Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à la vue complète. Une alerte concernant votre Machine, comme un composant qui ne cesse de redémarrer, n’est ni Travail ni Perso et apparaît uniquement dans Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre vue : dans **Perso uniquement**, touchez **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le nom de votre dernier récap du matin ou du soir et ce qu’il comptabilise, par exemple **Récap d’hier soir** · 12 terminées, 3 ouvertes. Touchez-la pour relire le récap, avec **Copier** pour le coller où vous voulez. Une fois ouvert ou après avoir touché son **×**, il reste disponible sur tous vos appareils jusqu’au prochain récap.

Sans récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui reste à faire, pour Travail et Perso ou uniquement pour la catégorie sélectionnée.

Une tâche associée à un projet affiche le nom du projet sous son titre. Touchez-le pour ouvrir le projet. **Projet**, sous **Détails**, permet de modifier ou de retirer le projet. Voir [Les tâches d’un projet](projects.md#a-project-s-to-dos).

**Domaine**, sous **Détails**, permet de déplacer une tâche vers votre autre domaine. Les éléments qu’elle peut lire et envoyer sont déplacés avec elle. **Annuler**, dans le message, permet de la remettre à sa place.

Quand une tâche doit passer dans votre autre domaine pour avancer et que les messages dont elle provient s’y trouvent tous, elle y est déplacée automatiquement et se poursuit. Sinon, elle affiche **Déplacer vers Travail**, et rien ne bouge tant que vous ne l’avez pas touché. Une tâche que vous avez créée sans choisir Travail ou Perso est déplacée automatiquement dès qu’elle trouve sa place. En attendant, elle n’est associée ni à Travail ni à Perso et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Si elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte de réception professionnelle que vous avez classée dans Perso est considérée comme personnelle. Les e-mails destinés à une autre de vos entreprises sont associés aux tâches de cette entreprise. Une tâche liée à votre vie personnelle, comme un message de votre famille envoyé à votre adresse professionnelle, est personnelle dès le départ.

Le travail qui arrive sur un compte personnel, comme un client sur WhatsApp ou une commande dans votre boîte de réception personnelle, est considéré comme professionnel dès le départ. Une tâche que vous avez déplacée ou classée vous-même reste toujours à l’endroit choisi. Travail ou Perso détermine où la tâche apparaît et avec qui elle est partagée, jamais l’adresse à laquelle elle répond : la réponse est toujours envoyée dans la conversation d’origine, même après un déplacement, sauf si vous choisissez un autre moyen.

Une tâche personnelle de ce type répond quand même depuis l’adresse professionnelle qui a reçu son e-mail. Elle n’apparaît jamais dans un Fleet Travail ni dans le Graph d’équipe.

Quand au moins deux tâches vous attendent, **Passer en revue**, dans l’en-tête de Pour vous, les parcourt une par une, dans l’ordre de la liste. Chaque brouillon s’affiche en entier, avec **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur un ordinateur, Entrée envoie ce qui est affiché, `S` met la tâche en attente, `→` l’ignore et Échap arrête le parcours. L’en-tête indique le temps nécessaire à votre rythme, par exemple « environ 2 min ».

À la fin, un récapitulatif indique ce qui a été envoyé ou clôturé, et ce qui est encore en préparation.

Les tâches qui vous posent une question ne sont pas incluses : elles attendent votre réponse, pas un toucher.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès qu’il y en a 40 ou que le plus ancien message d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus sont traités lors de la vérification suivante, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont quand même lus et conservés, puis traités ensemble à 06:30, pour que vos tâches soient prêtes avant votre récap du matin. Dans Connexions, la ligne des vérifications indique « Suspendues pour la nuit, reprise à 06:30 ». Si vous cliquez, saisissez du texte ou faites défiler l’application, écrivez dans le chat ou touchez une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous vous absentiez pendant une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit toutes les sources immédiatement. Si aucune tâche n’est ouverte, touchez la ligne de votre Machine pour afficher ses informations, avec **Détails**, qui ouvre la page des vérifications dans Connexions. S’il y a des tâches ouvertes, le bouton se trouve en haut de la liste sur un ordinateur. Une courte ligne s’affiche uniquement pendant une vérification, ou si elle a échoué ou pris du retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare suivent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans chaque source consultée, par exemple « 13 messages vérifiés à 16:11 · aucune nouvelle tâche » ou « · 2 nouvelles tâches ». Elle concerne uniquement cette vérification : les tâches déjà présentes dans votre liste restent inchangées. Si une nouvelle tâche attend un moment plus propice, comme votre récap du matin, la ligne indique jusqu’à quand : « 1 tâche reportée à demain 08:30 ».

Touchez la ligne pour afficher chaque fil d’e-mails, chat et notification, avec l’icône de sa source : l’auteur, l’objet ou les premiers mots du message, ainsi que la tâche créée ou la raison pour laquelle aucune tâche n’était nécessaire, par exemple « En copie seulement, un collègue répond » ou « Réunion déjà prévue jeudi ». Un fil n’indique aucune raison si la vérification n’en a donné qu’une vague. Touchez un élément pour le lire.

Les 10 premiers éléments s’affichent. Touchez en dessous pour voir le reste. Un nombre après un nom, comme (3), indique le nombre de nouveaux messages dans ce chat. Une notification du téléphone concernant un message déjà répertorié n’apparaît qu’une fois. La ligne reste affichée pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptabilisés. Vos réponses sont lues pour leur contexte et les promesses qu’elles contiennent, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que The Machine vous envoie, comme votre récap du matin ou une notification de correction, ne sont jamais lus ni répertoriés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche affiche sa prochaine étape, comme **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Voir [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** vous permet de préciser ce qu’il faut changer : la façon de procéder ou, une fois le brouillon prêt, ce qu’il faut modifier dans celui-ci. **Marquer comme fait** indique que la tâche est traitée : cette option est visible sur une tâche prête sans brouillon ou une tâche qui vous pose une question. Dans les autres cas, elle se trouve en haut du menu **…**. La tâche quitte aussitôt la liste, et le message qui s’affiche propose **Annuler**. Faites glisser le message pour le faire disparaître, ou déplacez-le hors de l’écran avec la souris, pour le fermer plus vite. La modification est conservée.

Pour procéder autrement, dites-le dans le **Chat** de la tâche. La réponse indique uniquement ce qui a changé, par exemple la mise en attente et sa durée. Si un élément n’a pas pu être modifié, comme une échéance, elle vous le précise.

Dans **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez à quelqu’un de la relire](ask-to-review.md).
- **Répéter…** : la tâche [revient à intervalles réguliers](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez indiquer pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Touchez le titre ou **Nom**, sous **Détails**, pour le modifier. Vous pouvez aussi le demander dans le chat de la tâche, par exemple « Renomme-la … ». Votre titre reste inchangé.

**Rouvrir** rétablit une tâche clôturée. Elle réapparaît aussi automatiquement en cas de nouveauté, comme un nouveau message de la personne concernée, mais pas après votre propre réponse. La tâche indique alors quand elle est réapparue et est considérée comme nouvelle dans le tri. La conversation du chat reprend là où elle en était, même après plusieurs semaines.

Une facture que vous devez payer vous-même, quel que soit le pays, devient une tâche avec le montant, la date d’échéance et les modalités de paiement indiquées sur la facture. Les factures payées automatiquement, par exemple par prélèvement automatique ou avec une carte enregistrée, ne créent pas de tâche. Lorsqu’un e-mail ultérieur confirme le paiement, par exemple un message de l’expéditeur indiquant qu’il a reçu votre paiement, la tâche se clôture automatiquement. **Annuler** permet de la rétablir pendant un jour.

Une tâche qui n’a d’utilité que jusqu’à une heure précise, comme une confirmation à envoyer avant une réunion, se clôture automatiquement une fois ce délai passé. Elle passe dans **Fait / écarté** avec la mention « N’est plus nécessaire ». **Annuler** permet de la rétablir pendant un jour.

Avant d’indiquer qu’un message ou un transfert destiné à quelqu’un est prêt, votre Machine vérifie vos échanges récents avec les personnes concernées, y compris dans les chats de groupe, et attend que Slack les ait lus. Si un message ultérieur montre que la tâche est déjà terminée, par exemple si quelqu’un a été sollicité et a répondu oui, elle se clôture automatiquement. **Annuler** permet de la rétablir pendant un jour.

Si une autre personne a écrit dans la même conversation après la création de votre brouillon, **Envoyer** le met en attente : « Non envoyé : nouveau message dans le fil ». La tâche affiche ce message avec **La lire** et **Refaire pour ce message**. Appuyez de nouveau sur **Envoyer** pour envoyer le brouillon tel quel.

Lorsqu’un nouveau message modifie les plans, par exemple si une fête change de lieu ou qu’une réservation est annulée, The Machine met elle-même à jour ses tâches. Une tâche qui reste utile tient compte des nouveaux plans. Une tâche qui n’a plus rien à faire passe dans **Fait / écarté** avec la mention « Pas nécessaire ». Son chat indique « Mis à jour : » et explique pourquoi. **Annuler** permet de la rétablir pendant un jour.

La première fois que vous consultez vos tâches, une courte astuce présente les principales actions : **Demander des modifications** et **Pas nécessaire**, et précise que rien n’est envoyé tant que vous n’appuyez pas sur **Envoyer**. L’astuce disparaît définitivement dès que vous utilisez son bouton ou appuyez sur ×.

Le premier jour, un message de bienvenue apparaît en haut de la page Tâches et indique qui attend votre réponse depuis le plus longtemps. Cette réponse est rédigée en premier pour être prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique la personne concernée, l’organisation s’il y en a une (pas uniquement parce que la personne y travaille), le projet, Travail ou Perso, ainsi que la date de réception. Touchez un nom pour ouvrir sa page dans le Graph.

Une personne ou une organisation affiche sa photo ou son logo si le Graph en a un, et ses initiales dans le cas contraire. Si un logo est illisible en petit, par exemple parce qu’il est blanc sur fond transparent ou qu’il s’agit d’un mot-symbole horizontal, les initiales s’affichent à la place.

Une ligne discrète indique parfois ce qui n’est pas connu, par exemple « Dernier contact il y a 12 jours par e-mail ; rien depuis ». Elle apparaît lorsque le dernier échange avec cette personne date ou qu’il n’a pas reçu de réponse. Elle indique aussi les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine indique ce qu’elle ne sait pas au lieu de faire des suppositions.

Lorsqu’un canal non connecté est indiqué, **Connecter**, à côté de son nom, ouvre la connexion correspondante.

Le titre indique ce qu’il faut faire et ne change que si la tâche change. Une tâche terminée conserve son titre et indique en dessous comment elle s’est terminée, par exemple « Terminée : Sam l’a signée mardi ».

Une ligne discrète au-dessus du brouillon indique le message d’origine, avec le logo du service correspondant. Touchez-la pour lire le fil. Le brouillon affiche le logo du service auquel il est destiné, pour voir d’un coup d’œil s’il s’agit d’une réponse dans Slack ou d’un e-mail.

Si le brouillon tient compte d’une information fournie ailleurs, comme la suggestion d’un collègue dans Slack, une ligne l’indique, par exemple « D’après Sam dans #ops ». Touchez-la pour lire le message.

Une conversation dans un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche en entier, de la plus ancienne à la plus récente : les messages précédant celui qui concerne la tâche, puis les réponses. Dans WhatsApp, Telegram ou Signal, vos messages apparaissent à droite, comme dans l’application. Le message associé à la tâche porte la mention « Cette tâche » et s’affiche directement. **Afficher les messages précédents** ajoute les messages plus anciens. Un e-mail affiche le reste du fil, replié au-dessus et en dessous.

**Ouvrir dans Gmail** ouvre l’e-mail dans le compte Gmail qui l’a reçu. Sur Android, il s’ouvre dans l’application Gmail si elle est installée.

Les **Détails** d’un e-mail affichent uniquement les informations absentes de son en-tête, comme toutes les adresses en Cc, en Cci ou une autre adresse de réponse. S’il n’y a rien à ajouter, cette section n’apparaît pas.

Une réponse dans un fil Slack affiche aussi les messages envoyés avant le début du fil. Le lien d’une tâche vers son propre message l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet et le domaine de la tâche (touchez l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de programmation. Le titre ouvre le chat. Une tâche terminée reste concise : son message d’origine se trouve dans **Détails**.

Une tâche en attente indique le lien vers votre dernier message à la personne concernée et vers le message que vous attendez : « E-mail à Pat · mar. »

## Créer une tâche

**Nouvelle tâche** (sous **Rechercher** sur un ordinateur, **+** sur un téléphone ou `N`) permet de créer une tâche pour n’importe quel sujet. La création n’envoie rien. Si vous ne choisissez ni **Travail** ni **Perso**, la tâche est classée au bon endroit en fonction de la personne et du sujet. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il est ancien.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », également dans votre langue. L’icône du calendrier propose des dates rapides et **Choisir une date**.
- **Répéter** : la tâche revient à intervalles réguliers. Voir [Tâches récurrentes](recurring.md).
- **Personne** : associez les personnes ou les entreprises concernées, jusqu’à 5.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, d’un message Slack, Teams, WhatsApp, Telegram ou de tout autre message accessible à The Machine. Recherchez par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : touchez le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur un téléphone, l’icône de l’appareil photo permet de prendre une photo. Vous pouvez ajouter jusqu’à 5 fichiers, comme dans le chat (voir [Ajouter des fichiers](card-chat.md#add-files)). Touchez × pour en retirer un.

Les fichiers restent associés à la tâche et The Machine les lit lorsqu’elle s’en occupe. Vous pouvez aussi ajouter uniquement des fichiers : elle crée la tâche à partir d’un fichier PDF ou texte. Une photo s’affiche en petit : touchez-la pour l’agrandir.
