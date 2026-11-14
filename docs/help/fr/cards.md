---
title: Tâches
area: cards
summary: Une tâche par chose qui nécessite votre attention, prête à être validée. Découvrez les différentes parties d’une tâche.
covers: tab:inbox
code: dashboard.html, assistant.py
order: 1
translated: cd59c14a7a27491d
---
The Machine lit tous les nouveaux messages et crée une tâche uniquement quand quelque chose nécessite votre attention. Une tâche par sujet, quel que soit le nombre de messages concernés.

## Où trouver les tâches

La page **Tâches** les regroupe :

- **Pour vous** : tout ce qui attend votre intervention, en commençant par le plus urgent. Chaque tâche porte l’une de ces mentions : **Préparée** (le travail est fait, et **Faire** ou **Envoyer** permet de passer à l’action), **Vous attend** (elle nécessite d’abord une décision ou une réponse de votre part) ou **En préparation…** (votre Machine s’en occupe).
- **Tout juste fait** : une dernière étape que vous avez confirmée, comme un formulaire ou un ticket, a été effectuée pendant votre absence. Elle reste affichée jusqu’à ce que vous touchiez **Compris**, pendant une journée au maximum. Votre téléphone vous en avertit aussi.
- **Revient plus tard** : les tâches mises en attente et celles auxquelles vous n’avez pas répondu à **Toujours utile ?** (voir ci-dessous).
- **Promesses** : ce que vous avez promis et ce que d’autres vous ont promis. Consultez [Promesses](promises.md).
- **Fait / écarté** : toutes les tâches terminées, des plus récentes aux plus anciennes, avec l’heure de leur clôture, par exemple « Fait il y a 5 minutes ». Les tâches qui semblent déjà terminées portent la mention **Semble fait**.

Après un envoi, un court message indique où la tâche a été déplacée, par exemple « Envoyé. Déplacé dans Fait. » ou « Envoyé. Déplacé dans Plus tard jusqu’à lundi. » **Ouvrir** vous y conduit. La recherche trouve une tâche par son titre ou par son destinataire, y compris dans Plus tard et Fait.

Dans **Pour vous**, les tâches en retard ou à échéance d’ici demain apparaissent d’abord, puis les questions de votre Fleet, puis le reste. Dans chaque groupe, les plus récentes s’affichent en premier. Une tâche garde sa place pendant que votre Machine la prépare et une fois terminée : seul son statut change. Dans les autres groupes ouverts, les tâches en retard ou à échéance d’ici demain s’affichent d’abord, puis les plus récentes. La barre latérale conserve le même ordre.

**Semble fait** signifie que votre Machine voit que la tâche est terminée, par exemple « PR #3451 fusionnée », mais qu’elle n’est pas encore clôturée. **Rouvrir** la remet dans votre liste, et votre Machine en tire des enseignements. Ces tâches ne sont jamais en retard. Au bout d’une journée, elles se clôturent automatiquement, avec **Annuler** pour revenir en arrière. Une tâche que vous avez déjà traitée vous-même, par exemple en répondant dans Gmail ou Slack, se clôture aussi automatiquement.

Si un message vient d’une adresse qui ressemble à celle d’une personne que vous connaissez, comme sam@acme-corp.example au lieu de sam@acmecorp.example, la tâche l’indique clairement : « Ce n’est pas Sam Lee. » La personne est affichée avec sa propre adresse, jamais avec le nom qu’elle a utilisé. Votre Machine vérifie ce type de message auprès de la personne dont vous avez déjà l’adresse, jamais auprès de son expéditeur.

Une tâche qui attend toujours quelqu’un d’autre, par exemple une révision ou une réponse, indique l’étape concernée à côté de **En attente de**. Elle apparaît dans **En attente des autres**, repliée au-dessus de Revient plus tard, jusqu’à ce qu’un nouveau message la fasse réapparaître. C’est aussi le cas quand vous avez posé une question : la tâche revient le matin précédant son échéance, à l’échéance si celle-ci est plus tard dans la journée, ou le lendemain matin une fois l’échéance passée. Elle indique alors qui doit encore répondre.

Quand une tâche dépend d’un résultat fourni par quelqu’un d’autre, comme un contrat signé, **Détails** indique ce résultat à côté de **Terminé quand**. L’envoi de votre partie ne clôture pas la tâche : elle reste dans **En attente des autres** jusqu’à ce qu’un message confirme le résultat, puis se clôture automatiquement, avec **Annuler** pour revenir en arrière. Si rien n’arrive avant le moment où il faut relancer la personne, la tâche réapparaît avec **Écris une courte relance** dans son chat. Dites dans le chat ce qui compte comme un résultat terminé pour modifier ce critère.

Si personne ne touche à une tâche pendant une semaine, elle demande une fois : **Toujours utile ?** **Pas nécessaire** la clôture, avec **Annuler** pour revenir en arrière. **Garder** la conserve, et elle ne posera plus la question. Si vous ne répondez pas dans la semaine qui suit, elle est repliée dans Revient plus tard, et elle n’est plus comptabilisée sur l’icône de l’application ni dans le récap du matin. Le fait de l’ouvrir, d’envoyer un message dans le chat, de la modifier, de la mettre en attente ou de recevoir un nouveau message la fait réapparaître.

Une fois par semaine, un projet resté sans activité et sans tâche ouverte peut générer une tâche avec une prochaine étape précise, dans la limite de trois par semaine. Consultez [Projets](projects.md).

Quand rien ne nécessite votre attention, votre Machine se repose et la liste reste vide. Pendant une vérification, elle se réveille et vous le signale. Si une vérification a échoué ou tarde, elle l’indique, avec **Vérifier maintenant** en dessous.

Les filtres **Tout**, **Travail** et **Perso**, en haut de la barre latérale, affichent toutes les tâches ou uniquement celles d’un type donné. Le téléphone et l’ordinateur affichent le même filtre. Quand Travail ou Perso est sélectionné, **Tout afficher** permet de revenir à la liste complète. Une alerte concernant votre Machine, par exemple un élément qui ne cesse de redémarrer, n’est ni Travail ni Perso et s’affiche uniquement dans Tout.

La ligne en haut de la liste permet aussi de passer directement à l’autre filtre : **Perso uniquement · Travail · Tout afficher**.

La première ligne de la liste indique le dernier récap du matin ou du soir et ce qu’il comptabilise, par exemple **Récap d’hier soir** · 12 terminées, 3 ouvertes. Touchez-la pour relire ce récap, et **Copier** pour le coller où vous voulez. Une fois le récap ouvert ou son **×** touché, il reste affiché sur tous vos appareils jusqu’au prochain récap.

Si aucun récap récent n’est disponible, la ligne affiche **Aujourd’hui jusqu’ici** : les tâches terminées aujourd’hui et celles qui sont toujours ouvertes, pour Travail et Perso ou uniquement pour le filtre sélectionné.

Une tâche liée à un projet affiche son nom sous le titre. Touchez-le pour ouvrir le projet. **Projet**, sous **Détails**, permet de le modifier ou de retirer la tâche du projet. Consultez [Les tâches d’un projet](projects.md#a-projects-to-dos).

**Domaine**, sous **Détails**, déplace une tâche vers votre autre domaine. Les messages qu’elle peut lire et envoyer sont également déplacés. **Annuler** dans le message la remet à sa place initiale.

Quand une tâche nécessite l’accès à votre autre domaine et que tous les messages dont elle provient s’y trouvent, elle s’y déplace et continue automatiquement. Sinon, elle affiche **Déplacer vers Travail** et rien ne bouge tant que vous ne touchez pas ce bouton. Une tâche créée sans choisir Travail ou Perso se déplace automatiquement dès que son domaine est déterminé. En attendant, elle n’est ni Travail ni Perso et reste privée.

Une tâche peut toujours lire les messages dont elle provient. Si elle a besoin d’autres messages de votre autre domaine, elle vous le demande avec **Utiliser cet e-mail pour cette tâche**. Une boîte de réception professionnelle que vous avez classée dans Perso est considérée comme personnelle. Les e-mails destinés à une autre de vos entreprises sont associés aux tâches de cette entreprise. Une tâche liée à votre vie personnelle, comme un message familial envoyé à votre adresse professionnelle, est classée dans Perso dès le départ.

Le travail qui arrive sur un compte personnel, comme un message d’un client sur WhatsApp ou une commande dans votre boîte personnelle, est classé dans Travail dès le départ. Une tâche que vous avez déplacée ou classée vous-même reste toujours à l’endroit choisi. Travail ou Perso détermine où la tâche s’affiche et avec qui elle est partagée, jamais où elle répond : la réponse est toujours envoyée dans la conversation concernée, même après un déplacement, sauf si vous choisissez une autre méthode.

Une tâche personnelle de ce type répond tout de même depuis l’adresse professionnelle qui a reçu l’e-mail, et n’apparaît jamais dans un Fleet professionnel ni dans le Graph de l’équipe.

Quand plusieurs tâches sont en attente, **Passer en revue** dans l’en-tête de Pour vous permet de les traiter une par une, dans l’ordre de la liste, avec chaque brouillon affiché en entier et les boutons **Envoyer** ou **Faire**, **Demander des modifications**, **Mettre en attente** et **Ignorer**. Sur ordinateur, Entrée envoie ce qui est affiché, `S` met en attente, `→` ignore et Échap arrête. Sous le titre, l’en-tête indique aussi le temps nécessaire à votre rythme, par exemple « environ 2 min ».

Une tâche qui vous pose une question n’apparaît dans aucune de ces deux listes : elle attend votre réponse, pas un clic.

## Vérifier maintenant

Votre Machine lit chaque source toutes les quelques minutes, jour et nuit. Elle vérifie les nouveaux messages dès qu’il y en a 40 en attente ou que le plus ancien message d’une personne attend depuis 15 minutes. Les newsletters, notifications et reçus sont pris en compte lors de la prochaine vérification, dans l’heure.

La nuit, de 00:00 à 06:30, les vérifications sont suspendues : les nouveaux messages sont toujours lus et conservés, puis vérifiés ensemble à 06:30, afin que vos tâches soient prêtes avant le récap du matin. Dans Connexions, la section Vérifications indique « En pause pour la nuit, rattrapage à 06:30 ». Si vous ouvrez l’application, écrivez dans le chat ou touchez une tâche pendant la nuit, les vérifications reprennent normalement jusqu’à ce que vous soyez absent depuis une heure. **Vérifier maintenant** lance toujours une vérification immédiate.

**Vérifier maintenant** lance immédiatement une vérification de toutes les sources. Si aucune tâche n’est ouverte, touchez la ligne de votre Machine pour l’afficher, avec **Détails**, qui ouvre les vérifications dans Connexions. Si des tâches sont ouvertes, l’option se trouve tout en haut sur ordinateur. Une courte ligne s’affiche uniquement pendant une vérification ou si l’une d’elles a échoué ou tarde. Vous pouvez aussi le demander dans le chat.

LinkedIn, X et Salesflare suivent leur propre rythme.

## Dernière vérification

Après une vérification qui a lu de nouveaux messages, une ligne au-dessus de vos tâches indique ce qu’elle a trouvé dans chaque source consultée, par exemple « 13 messages vérifiés à 16:11 · rien ne nécessite votre attention » ou « · 2 nouvelles tâches ». Lorsqu’une nouvelle tâche est reportée à un moment plus opportun, par exemple au récap du matin, la ligne indique jusqu’à quand : « 1 tâche reportée jusqu’à demain 08:30 ».

Touchez la ligne pour voir chaque fil d’e-mails, chat et notification, avec l’icône de sa source : l’expéditeur, l’objet ou les premiers mots, ainsi que la nouvelle tâche ou la raison pour laquelle le message n’a nécessité aucune action, par exemple « Vous étiez en copie, un collègue répond » ou « Réunion déjà prévue pour jeudi ». Un fil n’indique aucune raison si la vérification n’en a donné qu’une vague. Touchez un élément pour le lire.

Les 10 premiers éléments s’affichent. Touchez le bouton en dessous pour voir le reste. Le nombre après un nom, par exemple (3), indique le nombre de nouveaux messages dans ce chat. Une notification sur téléphone concernant un message déjà répertorié ne s’affiche qu’une fois. La ligne reste visible pendant 12 heures après la vérification.

Seuls les e-mails qui vous sont adressés sont comptabilisés. Vos réponses sont lues pour le contexte et les promesses, mais ne sont pas considérées comme de nouveaux e-mails. Les e-mails que The Machine vous envoie, comme le récap du matin ou un avis de résolution, ne sont jamais lus ni répertoriés. Les e-mails concernant la facturation, votre période d’essai ou une invitation sont lus comme d’habitude.

## Les boutons

Une tâche indique l’étape suivante, par exemple **Faire** ou **Vérifier et envoyer**, avec **Mettre en attente** à côté. Consultez [Faire](do-it.md) et [Mettre en attente](snooze.md).

**Demander des modifications** permet de préciser ce qu’il faut changer : la manière de faire ou, une fois le brouillon prêt, ce qu’il faut y modifier. **Marquer comme fait** signifie que la tâche est traitée : le bouton reste visible sur une tâche prête sans brouillon, et se trouve sinon en haut de **…**, y compris pour une tâche qui nécessite votre décision. La tâche quitte immédiatement la liste, avec **Annuler** dans le message. Balayez le message pour le faire disparaître ou faites-le glisser hors de la liste avec la souris pour le fermer plus tôt. La modification est conservée.

Pour que la tâche soit effectuée autrement, dites-le dans son **Chat**.

Sous **…** :

- **Transférer…** : confiez la tâche à un collègue, à [Claude Code ou Codex](hand-to-agent.md), ou [demandez une révision](ask-to-review.md).
- **Répéter…** : la tâche [revient selon une certaine fréquence](recurring.md).
- **Pas nécessaire** : la tâche disparaît. Vous pouvez choisir un motif : **Pas pertinent**, **Faits erronés** ou **Déjà traité**. Votre Machine en tire des enseignements.

Touchez le titre ou **Nom**, sous **Détails**, pour renommer la tâche. Votre titre est conservé.

**Rouvrir** rétablit une tâche clôturée. Elle réapparaît aussi automatiquement si un nouvel événement survient, comme un nouveau message de la personne, mais pas si vous lui répondez vous-même.

Une facture que vous devez payer vous-même, quel que soit le pays, devient une tâche indiquant son montant, son échéance et les informations de paiement qu’elle contient. Ce n’est pas le cas des factures payées automatiquement, par exemple par prélèvement automatique ou avec une carte enregistrée. Si un e-mail ultérieur indique que la facture a été payée, par exemple si l’expéditeur confirme avoir reçu votre paiement, la tâche se clôture automatiquement. **Annuler** la rétablit pendant une journée.

Une tâche qui n’est utile que jusqu’à une heure précise, comme une confirmation à fournir avant une réunion, se clôture automatiquement après cette heure. Elle est déplacée dans **Fait / écarté** avec la mention « N’est plus nécessaire ». **Annuler** la rétablit pendant une journée.

Avant qu’un message ou un transfert destiné à quelqu’un soit marqué comme prêt, votre Machine vérifie vos conversations récentes avec les personnes concernées, y compris les chats de groupe, et attend que Slack les ait lus. Si un message ultérieur montre que la tâche est déjà terminée, par exemple si la personne a été sollicitée et a répondu oui, la tâche se clôture automatiquement. **Annuler** la rétablit pendant une journée.

Quand un message plus récent modifie le plan, par exemple si une fête est déplacée ou une réservation annulée, The Machine met elle-même à jour ses tâches. Une tâche toujours utile suit le nouveau plan. Si elle n’a plus rien à faire, elle est déplacée dans **Fait / écarté** avec la mention « Pas nécessaire ». Son chat indique « Mise à jour : » et la raison. **Annuler** la rétablit pendant une journée.

Lors de vos premières tâches, un bref conseil vous présente les actions principales : **Demander des modifications** et **Pas nécessaire**, et vous rappelle que rien n’est envoyé tant que vous n’avez pas appuyé sur **Envoyer**. Le conseil disparaît définitivement dès que vous utilisez son bouton ou appuyez sur ×.

Le premier jour, un message de bienvenue s’affiche en haut de Tâches et indique qui attend votre réponse depuis le plus longtemps. Cette réponse est préparée en premier, pour être prête à votre arrivée.

Chaque tâche commence par son titre. La ligne en dessous indique de qui ou de quoi elle parle, l’organisation si elle est concernée (pas seulement parce qu’une personne y travaille), le projet, Travail ou Perso, et la date de réception. Touchez un nom pour ouvrir sa page dans le Graph.

Les noms et les organisations affichent leur photo ou leur logo si le Graph en contient un, sinon leurs initiales. Si un logo est illisible en petit format, par exemple parce qu’il est blanc sur fond transparent ou qu’il s’agit d’un long nom stylisé, l’initiale s’affiche aussi.

Parfois, une discrète ligne indique ce qui est inconnu, par exemple « Dernier contact il y a 12 jours par e-mail, rien depuis ». Elle apparaît si le dernier échange avec cette personne date ou n’a pas reçu de réponse, et indique les canaux qui ne sont pas connectés, comme WhatsApp. Votre Machine précise ce qu’elle ne sait pas au lieu de faire des suppositions.

Quand un canal non connecté est mentionné, l’option Connecter à côté ouvre la connexion correspondante.

Un titre indique ce qu’il faut faire et ne change que si la tâche change. Une tâche terminée conserve son titre et indique en dessous comment elle s’est terminée, par exemple « Fait : Sam l’a signé mardi ».

Au-dessus du brouillon, une ligne discrète indique le message dont il provient, avec le logo du service concerné. Touchez-la pour lire le fil. Le brouillon affiche le logo de sa destination, afin de voir immédiatement s’il s’agit d’une réponse Slack ou d’un e-mail.

Si le brouillon tient compte de l’avis d’une personne dans un autre espace, par exemple d’une suggestion d’un collègue dans Slack, une ligne le précise, par exemple « Basé sur le message de Sam dans #ops ». Touchez-la pour lire ce message.

Un chat (Slack, WhatsApp, Telegram, Intercom…) s’affiche comme une seule conversation, du plus ancien au plus récent : les messages qui précèdent celui concerné par la tâche, puis les réponses qui le suivent. Dans WhatsApp, Telegram ou Signal, vos messages apparaissent à droite, comme dans l’application. Le message concerné est marqué « Cette tâche » et s’ouvre directement dans la conversation. **Afficher les messages précédents** ajoute les messages plus anciens. Le reste d’un fil d’e-mails est replié au-dessus et en dessous du message concerné.

Les **Détails** d’un e-mail affichent uniquement les informations absentes de son en-tête, comme les adresses complètes en Cc, les destinataires en Cci ou une autre adresse de réponse. Si rien n’est à ajouter, cette section est vide.

Une réponse dans un fil Slack affiche aussi les messages échangés avant le début du fil. Le lien d’une tâche vers son propre message l’ouvre également ici, avec **Ouvrir dans Slack** en bas.

**Détails** affiche le nom, le projet et le domaine de la tâche (touchez l’un d’eux pour le modifier), votre dernière note et le résultat d’un agent de programmation. **Chat ›** ouvre le chat. Une tâche terminée reste succincte ; le message dont elle provient se trouve sous **Détails**.

Une tâche « En attente de » contient un lien vers votre dernier message à la personne, celui auquel vous attendez une réponse : « E-mail à Pat · mar. »

## Créer une tâche soi-même

**Nouvelle tâche** (sous **Rechercher** sur ordinateur) permet de créer une tâche pour n’importe quel sujet. Sa création n’envoie rien. Si vous ne sélectionnez ni Travail ni Perso, elle est classée selon la personne et le sujet concernés. Elle retrouve aussi l’e-mail auquel elle fait suite, même s’il est ancien.

- **Échéance** : saisissez un jour ou une heure, par exemple « demain », « ven. prochain », « 3 nov. », « 14 h » ou « dans 2 heures », dans votre langue. L’icône de calendrier propose des choix rapides et **Choisir une date**.
- **Message** : joignez le message concerné : un e-mail, un message Slack, Teams, WhatsApp, Telegram ou tout autre message auquel The Machine a accès. Recherchez par texte ou par expéditeur. Chaque résultat indique sa source, son expéditeur et sa date.
- **Fichiers** : touchez le trombone, collez une capture d’écran ou déposez des fichiers dans le formulaire. Sur un téléphone, l’appareil photo à côté permet de prendre une photo. Vous pouvez ajouter jusqu’à 5 fichiers, comme dans le chat (voir [Ajouter des fichiers](card-chat.md#add-files)). Touchez × pour en retirer un.

Les fichiers restent associés à la tâche, et The Machine les lit lorsqu’elle s’en occupe. Vous pouvez joindre uniquement des fichiers : elle crée la tâche à partir d’un PDF ou d’un fichier texte. Une photo s’affiche sous forme de petite image. Touchez-la pour l’agrandir.
