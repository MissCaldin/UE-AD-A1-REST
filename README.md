# UE-AD-A1-REST

## Service de réservations de films avec des micro-sevices REST

### Description

Ce projet permet aux utilisateurs d'accéder à la liste des films disponibles ainsi qu'à leur date de projection, et de réserver une séance.

### Installation

Pour installer le projet, vous devez cloner le projet puis installer les dépendances nécessaires. Pour cela, utilisez :

```pip install -r .\requirements.txt```

### Utilisation
Depuis le path de chaque micro-service, exécutez le micro-service (user, booking, showtime et movies). Puis vous pouvez commencer à faire vos requêtes en suivant la documentation Open API.

### Structure

- Le micro-service movies contient et permet l'accès aux informations des films, c'est à dire leur titre, leur note et leur directeur.
- Le micro-service showtimes permet d'accéder aux séances, qui sont composés de la date de projection et du film projeté.
- Le micro-service booking contient les réservations, qui sont composées de l'utilisateur et du créneau réservé. Il fait appel au micro-service showtimes.
- Le micro-service user contient les informations de l'utilisateur, comme son nom. Il fait appel aux micro-services movies et booking.