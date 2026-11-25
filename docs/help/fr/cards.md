---
title: Tâches
area: cards
summary: Une tâche par sujet qui nécessite votre attention, prête à être validée. Comprenez les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: 43d9497d3a1c4a86
---
Votre Machine lit tous les nouveaux messages et ne crée une tâche que si quelque chose nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où se trouvent les tâches

La page **Tâches** les regroupe :

- **Tout juste fait** : en haut, vous retrouvez une dernière étape que vous avez confirmée, comme l’envoi d’un formulaire ou la résolution d’un problème pendant votre absence. Elle reste là jusqu’à ce que vous touchiez **Compris**, pendant une journée maximum. Votre téléphone vous en informe aussi.
- **Pour vous** : tout ce qui attend votre intervention, avec d’abord les échéances pour demain ou avant. Chaque tâche indique **Préparée** (un brouillon ou un résultat est prêt, et **Faire** ou **Envoyer** permet de le concrétiser), **Vous attend** (elle attend d’abord votre décision ou votre réponse ; si le travail ne peut pas avancer ou être utilisé sans une information que vous seul pouvez fournir, comme un prix, un fait ou un choix, une ligne sous le titre l’indique), **En préparation…** (votre Machine s’en occupe) ou **À lire** (un récap ou un bref compte rendu, sans décision à prendre).
- **Plus anciennes** : les tâches repliées qui n’ont rien de nouveau depuis une semaine (voir ci-dessous).
- **En attente des autres** : les tâches repliées dont la prochaine étape dépend de quelqu’un d’autre (voir ci-dessous).
- **Revient plus tard** : les tâches mises en attente, les messages qui [partent plus tard](send-later.md) et ceux qui n’ont pas reçu de réponse à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : les promesses que vous avez faites et celles que les autres vous ont faites. Consultez [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, des plus récentes aux plus anciennes, avec la date de fin, par exemple « Fait il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après un envoi, une courte note indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Déplacé dans Plus tard jusqu’à lun. ». Une réponse qui promet seulement de faire le travail, comme « Je l’enverrai d’ici mardi », laisse la tâche ouverte : « Envoyé. Tâche laissée ouverte. » **Ouvrir** vous y mène. La recherche trouve une tâche par son titre ou par le destinataire, y compris dans Plus tard et Fait.

Dans **Pour vous**, les tâches en retard ou à échéance demain ou avant apparaissent d’abord, suivies des questions de votre Fleet, des suivis d’un tableau, puis du reste. Dans chaque catégorie, les plus récentes s’affichent en premier. Une tâche conserve sa place pendant que votre Machine la prépare et une fois terminée : seul son statut change. Dans les autres groupes ouverts, les tâches en retard ou à échéance demain ou avant apparaissent d’abord, puis le reste, des plus récentes aux plus anciennes. La barre latérale garde le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore fermée. **Rouvrir** la remet dans votre liste, et votre Machine en tire des enseignements. Ces tâches ne sont jamais en retard. Lorsqu’un message les signale, elles se ferment automatiquement au bout d’une journée, avec **Annuler**. Sinon, elles attendent que vous choisissiez **Marquer comme fait**.

Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se ferme aussi automatiquement. Une réponse qui indique qu’un fichier est joint alors qu’il ne l’est pas ne ferme pas la tâche.

Si un message vient d’une adresse qui ressemble seulement à celle d’une personne que vous connaissez, comme sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche l’indique clairement : « Ce n’est pas Sam Lee. » La personne apparaît sous sa propre adresse, jamais sous le nom qu’elle a utilisé. Votre Machine vérifie ce type de message auprès de la personne dont vous avez déjà l’adresse, jamais auprès de son auteur.

Une tâche qui attend encore quelqu’un d’autre, par exemple une évaluation ou une réponse, indique l’étape concernée avec **En attente de :**. Elle apparaît dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la réactive. Il en va de même après que vous avez posé une question : la tâche revient le matin précédant son échéance, à l’échéance si celle-ci tombe plus tard dans la journée, ou le lendemain matin si elle est passée. Elle indique alors la personne dont elle attend toujours une réponse.

Quand une tâche porte sur un résultat fourni par quelqu’un d’autre, comme un contrat signé, **Détails** l’indique avec **Terminé quand**. Envoyer votre partie ne ferme pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se ferme automatiquement, avec **Annuler**. Si vous n’avez rien reçu au moment de relancer la personne, la tâche revient et son chat affiche **Écrivez une courte relance**. Indiquez dans le chat ce qui compte comme terminé pour modifier ce critère.

Une tâche qui n’a rien de nouveau depuis une semaine passe de Pour vous à **Plus anciennes**, pour que les nouvelles tâches apparaissent en premier après quelques jours d’absence. Rien de nouveau signifie qu’aucun nouveau message n’a été reçu et que vous n’avez rien fait dans la tâche, par exemple envoyer un message dans le chat, modifier la tâche ou la mettre en attente. Le simple fait de la consulter ne compte pas.

Les tâches urgentes, celles dont l’échéance approche et celles dont l’envoi est en cours restent dans Pour vous. **Tout écarter** marque comme non nécessaires, après une seule confirmation, toutes les tâches de Plus anciennes, comme le fait **Pas nécessaire** une tâche à la fois. **Annuler** permet de revenir en arrière. Toute nouveauté dans une tâche la remet dans Pour vous.

Une tâche à laquelle personne n’a touché depuis une semaine demande une fois : **Toujours utile ?** **Pas nécessaire** la ferme, avec **Annuler** pour revenir en arrière. **Garder** la conserve et la question ne sera plus posée. Sans réponse pendant une semaine supplémentaire, elle est repliée dans Revient plus tard, et elle n’est plus comptée sur l’icône de l’application ni dans le récap du matin. L’ouvrir, envoyer un message dans le chat, la modifier, la mettre en attente ou recevoir un nouveau message la fait revenir.

Une fois par semaine, un projet resté inactif et sans tâche ouverte peut recevoir une tâche proposant une prochaine étape précise, dans la limite de trois par semaine. Consultez [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine fait une pause et laisse la liste vide. Pendant ses vérifications, elle se réveille et vous en informe. Si une vérification a échoué ou est en retard, une ligne le signale, avec **Vérifier maintenant** en dessous.

Les filtres **Tout**, **Travail** et **Perso** en haut de la barre latérale affichent toutes les tâches ou seulement celles d’un type. Votre téléphone et votre ordinateur conservent le même choix. Lorsque Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à l’affichage complet. Une alerte concernant votre Machine elle-même, par exemple un composant qui redémarre sans cesse, n’est ni Travail ni Perso et apparaît uniquement sous Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre filtre : sous **Perso uniquement**, touchez **Travail** ou **Tout afficher**.

La ligne en haut de la liste indique le dernier récap du matin ou du soir et le nombre d’éléments qu’il contient, par exemple **Récap d’hier soir** · 12 faits, 3 ouverts. Touchez-la pour relire ce récap, avec **Copier** pour le coller où vous voulez. Dès que vous l’ouvrez ou touchez son **×**, il reste disponible sur tous vos appareils jusqu’au prochain récap.

Sans récap récent, la ligne affiche **Aujourd’hui jusqu’ici** : ce qui a été fait aujourd’hui et ce qui est encore en cours, pour Travail et Perso, ou uniquement pour le filtre sélectionné.

Une tâche associée à un projet affiche le nom du projet sous son titre. Touchez-le pour ouvrir le projet. **Projet**, dans **Détails**, permet de le modifier ou de le retirer. Consultez [Les tâches d’un projet](projects.md#a-project-s-to-dos).

**Domaine**, dans **Détails**, déplace une tâche vers votre autre domaine. Les sources qu’elle peut lire et depuis lesquelles elle peut envoyer des messages sont également déplacées. **Annuler** dans la note permet de la remettre à sa place.

Lorsqu’une tâche a besoin de votre autre domaine pour avancer et que tous les messages dont elle provient s’y trouvent, elle y est déplacée automatiquement et le travail continue. Sinon, elle affiche **Déplacer vers Travail**, et rien ne bouge tant que vous ne touchez pas cette option. Une tâche que vous avez créée sans choisir Travail ou Perso est déplacée automatiquement dès que sa catégorie est déterminée. Jusque-là, elle n’est ni Travail ni Perso et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Lorsqu’elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte mail professionnelle que vous avez classée comme Perso compte comme Perso. Les e-mails concernant une autre de vos entreprises sont associés aux tâches de cette entreprise. Une tâche concernant votre vie personnelle, comme un e-mail familial reçu à votre adresse professionnelle, est Perso dès le départ.

Un sujet professionnel qui vous parvient sur un compte personnel, comme un client sur WhatsApp, une commande reçue dans votre boîte personnelle ou une [promesse](promises.md) concernant le travail, est Travail dès le départ.

Une tâche que vous avez déplacée ou placée vous-même reste toujours là où vous l’avez mise. Travail ou Perso détermine où la tâche apparaît et avec qui elle est partagée, mais jamais où elle répond : la réponse est toujours envoyée dans la conversation d’origine, même après un déplacement, sauf si vous choisissez une autre méthode.

Une tâche Perso de ce type répond toujours depuis l’adresse professionnelle à laquelle son e-mail a été envoyé, et n’apparaît jamais dans un Fleet Travail ni dans le Graph d’équipe.

Lorsque plusieurs tâches vous attendent, **Passer en revue** dans l’en-tête de Pour vous les parcourt une à une, dans l’ordre de la liste, en affichant chaque brouillon en entier, avec **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur un ordinateur, Entrée envoie le contenu affiché, `S` le met en attente, `→` passe à la suite et Échap arrête le parcours. L’en-tête indique le temps nécessaire à votre rythme, par exemple « environ 2 min ».

À la fin, un récap indique ce qui a été envoyé ou fermé et ce qui est encore en préparation.

Les tâches qui vous posent une question sont exclues des deux catégories : elles attendent votre réponse, pas un clic.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès que 40 messages sont en attente ou que le plus ancien message d’une personne est en attente depuis 15 minutes. Les newsletters, notifications et reçus sont traités lors de la vérification suivante, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont toujours lus et conservés, puis vérifiés ensemble à 06:30, pour que vos tâches soient prêtes avant le récap du matin. Dans Connexions, la section Vérifications indique « Suspendues pour la nuit, rattrapage à 06:30 ». Si vous cliquez, saisissez du texte ou faites défiler l’application, écrivez dans le chat ou touchez une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous soyez absent depuis une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lit toutes les sources immédiatement. S’il n’y a aucune tâche ouverte, touchez la ligne de votre Machine pour la voir, avec **Détails**, qui ouvre la section Vérifications sous Connexions. S’il y a des tâches ouvertes, cette option se trouve en haut sur ordinateur. Une courte ligne apparaît uniquement pendant une vérification, ou si l’une d’elles a échoué ou est en retard. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare suivent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans toutes les sources consultées, par exemple « 13 messages vérifiés à 16:11 · aucune nouvelle tâche » ou « · 2 nouvelles tâches ». Elle ne concerne que cette vérification : les tâches déjà présentes dans votre liste restent inchangées. Si une nouvelle tâche est reportée à un moment plus opportun, comme le récap du matin, la ligne indique jusqu’à quand : « 1 tâche reportée jusqu’à demain 08:30 ».

Touchez cette ligne pour voir chaque fil d’e-mails, chat et notification, avec l’icône de sa source : l’auteur, l’objet ou les premiers mots, ainsi que la nouvelle tâche ou la raison pour laquelle le message n’a rien nécessité, par exemple « En copie seulement, un collègue répond » ou « Réunion déjà prévue jeudi ». Un fil n’indique aucune raison si la vérification n’en a trouvé qu’une de vague. Touchez un élément pour le lire avec les messages échangés autour.

Les 10 premiers éléments s’affichent. Touchez l’option en dessous pour voir le reste. Un nombre après un nom, comme (3), indique le nombre de nouveaux messages dans ce chat. Une notification Android concernant un message déjà répertorié ne s’affiche qu’une seule fois. La ligne reste visible pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptés. Vos propres réponses sont lues pour le contexte et les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que The Machine vous envoie, comme le récap du matin ou une notification de résolution, ne sont jamais lus ni répertoriés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus normalement.

## Les boutons

Une tâche indique la prochaine étape, par exemple **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Consultez [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** permet d’indiquer ce qu’il faut changer : la façon de procéder ou, une fois le brouillon prêt, son contenu. Si vous commencez à saisir une demande sans la terminer, elle vous attendra à votre retour. **Annuler** l’efface.

**Marquer comme fait** indique que la tâche est traitée. Sur ordinateur, cette option apparaît avec les autres boutons lorsqu’ils tiennent sur une seule ligne. Sur téléphone, elle est visible sur une tâche prête qui n’a pas de brouillon ou qui vous pose une question. Sinon, elle se trouve en haut du menu **…**. La tâche disparaît immédiatement de la liste, avec **Annuler** dans le message. Faites glisser le message pour le fermer, ou déplacez-le hors de l’écran avec la souris. La modification est conservée.

Pour faire la tâche autrement, dites-le dans son **Chat**. La réponse indique uniquement ce qui a changé, par exemple la mise en attente et sa durée. Si un élément n’a pas pu être modifié, comme une échéance, la réponse vous le signale.

Dans **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez à quelqu’un de la relire](ask-to-review.md).
- **Répéter…** : la tâche [revient selon une certaine fréquence](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez indiquer pourquoi : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Touchez le titre ou **Nom** dans **Détails** pour le modifier, ou demandez-le dans le chat de la tâche, par exemple « Renomme-la… ». Votre titre est conservé.

**Rouvrir** réactive une tâche fermée. Elle peut aussi revenir automatiquement lorsqu’un nouvel événement se produit, comme un nouveau message de la personne concernée, mais pas après votre propre réponse. La date de réactivation s’affiche et la tâche est classée parmi les nouvelles. Son chat reprend là où il s’était arrêté, même après plusieurs semaines.

Une facture que vous devez encore payer vous-même, quel que soit le pays, devient une tâche indiquant le montant, la date d’échéance et les informations de paiement fournies. Les factures payées automatiquement, par exemple par prélèvement automatique ou avec une carte enregistrée, ne deviennent pas des tâches. Lorsqu’un e-mail ultérieur confirme le paiement, par exemple si l’expéditeur confirme l’avoir reçu, la tâche se ferme automatiquement. **Annuler** permet de la réactiver pendant une journée.

Une tâche qui n’est utile que jusqu’à une heure précise, comme une confirmation à envoyer avant une réunion, se ferme automatiquement une fois ce moment passé. Elle est déplacée dans **Fait / écarté** avec la mention « N’est plus nécessaire ». **Annuler** permet de la réactiver pendant une journée.

Avant qu’un message ou un transfert destiné à quelqu’un apparaisse comme prêt, votre Machine vérifie vos chats récents avec les personnes concernées, y compris les chats de groupe, et attend que Slack les ait lus. Si un message ultérieur montre que la tâche est déjà terminée, par exemple si la personne a été sollicitée et a répondu oui, la tâche se ferme automatiquement. **Annuler** permet de la réactiver pendant une journée.

Si quelqu’un d’autre a écrit dans la même conversation après la création de votre brouillon, **Envoyer** le met en attente : « Non envoyé : nouveau message dans le fil ». La tâche affiche ce message avec **La lire** et **Refaire pour ce message**. Appuyez de nouveau sur **Envoyer** pour envoyer le brouillon tel quel.

Lorsqu’un message plus récent modifie le plan, par exemple si une fête est déplacée ou une réservation annulée, The Machine met elle-même à jour ses tâches. Une tâche qui reste nécessaire suit le nouveau plan. Celle qui n’a plus rien à faire est déplacée dans **Fait / écarté** avec la mention « Pas nécessaire ». Son chat indique « Mis à jour : » et la raison, et **Annuler** permet de la réactiver pendant une journée.

Lors de vos premières tâches, un court conseil présente les principales actions : **Demander des modifications** et **Pas nécessaire**, et rappelle que rien n’est envoyé avant que vous appuyiez sur **Envoyer**. Un conseil disparaît définitivement dès que vous utilisez son bouton ou appuyez sur ×.

Le premier jour, un message de bienvenue s’affiche en haut de Tâches et indique qui attend votre réponse depuis le plus longtemps. Cette réponse est préparée en premier afin d’être prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique la personne concernée, l’organisation s’il y en a une (pas uniquement parce qu’une personne y travaille), le projet, Travail ou Perso et la date de réception. Touchez un nom pour ouvrir sa page dans le Graph.

Les noms et les organisations affichent leur photo ou leur logo si le Graph en a un, et leurs initiales dans le cas contraire. Si un logo est difficile à lire en petit, par exemple parce qu’il est blanc sur fond transparent ou qu’il s’agit d’un mot-symbole large, les initiales s’affichent aussi.

Parfois, une ligne discrète indique ce qui est inconnu, par exemple « Dernier contact il y a 12 jours par e-mail, aucun échange depuis ». Elle apparaît si le dernier échange avec la personne est ancien ou sans réponse, et indique les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine indique ce qu’elle ne sait pas au lieu de faire des suppositions.

Lorsqu’un canal non connecté est indiqué, **Connecter** à côté ouvre la connexion correspondante.

Le titre indique ce qu’il faut faire et ne change que si la tâche change. Une tâche terminée conserve son titre, avec la façon dont elle s’est terminée en dessous, par exemple « Fait : Sam l’a signée mardi ».

Au-dessus du brouillon, une ligne discrète indique le message d’origine, avec le logo du service correspondant. Touchez-la pour lire le fil. Le brouillon affiche le logo du service destinataire, pour voir d’un coup d’œil s’il s’agit d’une réponse Slack ou d’un e-mail.

Si le brouillon fait suite à une contribution faite ailleurs, comme une suggestion d’un collègue dans Slack, une ligne l’indique, par exemple « D’après Sam dans #ops ». Touchez-la pour lire le message. Cette ligne disparaît lorsqu’une mise à jour remplace le brouillon.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche comme une seule conversation, de la plus ancienne à la plus récente : les messages précédant celui auquel la tâche se rapporte, puis les réponses suivantes. Dans WhatsApp, Telegram ou Signal, vos messages apparaissent à droite, comme dans l’application. Le message associé à la tâche porte la mention « Cette tâche » et s’ouvre dans la conversation. **Afficher les messages précédents** ajoute les messages plus anciens. Dans un e-mail, le reste du fil est replié au-dessus et en dessous du message concerné.

Un message s’ouvre de la même façon depuis la recherche, le Graph, les réponses d’Ask ou la dernière vérification. Il porte la mention « Ce message » ou « Nouveaux messages ».

**Ouvrir dans Gmail** ouvre l’e-mail dans le compte Gmail qui l’a reçu. Sur Android, l’e-mail s’ouvre dans l’application Gmail si elle est installée.

Les **Détails** d’un e-mail affichent uniquement les informations absentes de son en-tête, comme les adresses Cc complètes, le champ Bcc ou une autre adresse de réponse. Si rien n’est à ajouter, cette section n’apparaît pas.

Une réponse dans un fil Slack affiche aussi les messages échangés avant le début du fil. Le lien d’une tâche vers son propre message l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet et le domaine de la tâche (touchez l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de programmation. Son titre ouvre le chat. Une tâche terminée reste concise : le message à l’origine de la tâche se trouve dans **Détails**.

Une tâche « En attente de » contient un lien vers votre dernier message envoyé à la personne, celui dont vous attendez une réponse : « E-mail pour Pat · mar. »

## Créer une tâche

**Nouvelle tâche** (sous **Rechercher** sur ordinateur, **+** sur téléphone ou `N`) ajoute une tâche pour n’importe quel sujet. La création n’envoie rien. Si vous ne choisissez ni **Travail** ni **Perso**, la tâche est classée là où elle doit être, selon la personne et le sujet concernés. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il est ancien.

Si vous fermez le formulaire avant de créer la tâche, votre texte et vos choix seront là la prochaine fois, mais pas les fichiers. **Supprimer** dans le message les efface.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », y compris dans votre langue. L’icône du calendrier propose des dates rapides et **Choisir une date**.
- **Répéter** : la tâche revient selon une certaine fréquence. Consultez [Tâches récurrentes](recurring.md).
- **Personne** : associez les personnes ou les entreprises concernées, jusqu’à 5.
- Icône de message : joignez le message concerné, qu’il s’agisse d’un e-mail, d’un message Slack, Teams, WhatsApp, Telegram ou de tout autre message auquel The Machine a accès. Faites une recherche par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : touchez le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur téléphone, l’appareil photo à côté permet de prendre une photo. Vous pouvez ajouter jusqu’à 5 fichiers, comme dans le chat (consultez [Ajouter des fichiers](card-chat.md#add-files)). × retire un fichier.

Les fichiers restent associés à la tâche, et The Machine les lit lorsqu’elle s’en occupe. Les fichiers suffisent à créer une tâche : elle extrait les informations d’un PDF ou d’un fichier texte. Une photo s’affiche sous forme de petite image. Touchez-la pour la voir en taille réelle.
