---
title: Heures de travail
area: settings
summary: Quand votre Machine peut vous contacter, quand les mises en attente reviennent et quand arrivent les récapitulatifs du matin et du soir.
code: dashboard.html, assistant.py
order: 3
keywords: quiet hours, weekend, evening, night, do not disturb, time zone
translated: 062ccef1310f228a
---
Choisissez quand votre Machine peut vous contacter. Dans **Paramètres**, **Notifications**, sous **Heures de travail** :

- **Jours de travail** : les tâches professionnelles et les tâches professionnelles mises en attente attendent un jour de travail.
- **Messages de** et **Jusqu’à** : rien ne vous parvient en dehors de ces heures, ni notification, ni message Telegram, ni e-mail.
- **Les mises en attente reviennent à** : indique l’heure à laquelle les mises en attente d’un jour ou plus reviennent. Le récap du matin arrive au moins 5 minutes plus tard, pour qu’elles y figurent.
- **Récap du matin** : indique l’heure à laquelle arrive le récap du matin. Si vous décalez l’heure des mises en attente, le récap se décale aussi.
- **Récap du soir** : indique l’heure à laquelle arrive le récap du soir. Il est prévu 15 minutes avant l’heure indiquée dans **Jusqu’à**, puis suit cet horaire jusqu’à ce que vous choisissiez une autre heure.
- **Fuseau horaire** : le vôtre, pour tous les horaires ci-dessus.

Appuyez sur **Enregistrer**. Par défaut, les jours de travail vont du lundi au vendredi, de 08:00 à 23:00. Les mises en attente reviennent à 08:00, le récap du matin arrive à 08:30 et celui du soir à 22:45.

Pour savoir ce qui est envoyé pendant ces heures et comment, consultez [Notifications](notifications.md).

Sur votre propre ordinateur, `assistant hours` les affiche et permet de les modifier dans un terminal.
