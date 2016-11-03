# Video_player

Le plugin `video_player` joue un fichier vidéo. Ce plugin est utilisable pour la lecture de vidéo basique et nécessite le back-end `legacy`. Si vous cherchez des fonctionnalités plus avancées de lecteurs de vidéo, vous pouvez utiliser le plug-in `media_player_vlc`.

Les options suivantes sont disponibles :

- *Video file* : Une vidéo issue du groupe de fichiers. Le format supporté dépend de votre plateforme, mais la plupart des formats classiques sont généralement supportés (tels que`.avi` and `.mpeg`).
- *Resize to fit screen* : Indique s'il faut redimensionner une vidéo afin qu'elle s'adapte à la totalité de l'écran. Si ce n'est pas le cas, la vidéo sera présentée au centre de l'écran.
- *Duration* : Une durée en millisecondes, 'keypress' (pour arrêter quand une touche est pressée) ou 'mouseclick' (pour arrêter quand le bouton de la souris est cliqué).
- *Frame duration* : La durée en millisecondes d'une image unique. Cela contrôle essentiellement la vitesse de lecture. Notez que la vitesse de lecture dépend de la rapidité de votre ordinateur.

