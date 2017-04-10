DEVICE_TOKEN="e18v5k8ayyg:APA91bGswYiHOCUMA2NAM0La0DCPZGx14_JbkqXzFB-XP5bYpbqoImmmI5e-q9Ro6s_l45xtH2r4qkNfdGqLJO9sYVat8wl_g50ctzup7hLE7Qbfs0EoQfL7eopCl-YpP1x5l_M252r_"
curl -X POST --header "Authorization: key=AIzaSyDxwE1m7WjI6400WD9GadNJqoZfJvBmjGs" \
       --header "Content-Type:application/json" \
       https://fcm.googleapis.com/fcm/send \
	-d "{\"priority\":\"high\", \"data\":{\"name\":\"shenba\"}, \"to\":\"$DEVICE_TOKEN\", \"notification\":{ \"badge\":\"1\",\"sound\":\"default\", \"title\": \"Dar title\", \"body\":\"Dar is Great\"}}"

