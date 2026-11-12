---
title: Heures de travail
area: settings
summary: Quand votre Machine peut vous envoyer des messages, quand reviennent les mises en attente et quand arrive le récap du matin.
code: dashboard.html, assistant.py
order: 3
keywords: quiet hours, weekend, evening, night, do not disturb, time zone
---
Dans **Paramètres**, **Notifications**, sous **Heures de travail** :

- **Jours de travail** : les tâches de travail et le travail mis en attente attendent un jour de travail.
- **Messages de** et **Jusqu’à** : rien ne vous est envoyé en dehors de ces heures, ni push, ni Telegram, ni e-mail.
- **Les mises en attente reviennent à** : quand revient une mise en attente d’un jour ou plus. Le récap du matin arrive au moins 5 minutes après, pour les inclure.
- **Récap du matin** : quand arrive le résumé du matin. Si les mises en attente reviennent plus tard, il suit.
- **Récap du soir** : l’heure du récap du soir. Il est réglé 15 minutes avant **Jusqu’à** et suit cette heure jusqu’à ce que vous en choisissiez une.
- **Fuseau horaire** : le vôtre, pour tout ce qui précède.

Appuyez sur **Enregistrer**. Par défaut, c’est du lundi au vendredi, de 08:00 à 23:00, les mises en attente à 08:00, le récap du matin à 08:30 et le récap du soir à 22:45.

Ce qui part pendant ces heures, et comment, est expliqué dans [Notifications](notifications.md).

Sur votre propre ordinateur, `assistant hours` les affiche et les modifie aussi.
