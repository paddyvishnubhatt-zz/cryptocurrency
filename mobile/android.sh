DEVICE_TOKEN="fWgvy6LxaD4:APA91bGQVH7xgRnMBynPKYzWI7yeG88lDghNM5jhHZmUJFhDD3_wV70Ga8t095yPIoEEhwx5dqfUUFpMERMSz96pSb0QohlymVOF_hX3U0oqPdtVpmOxrfLNcVlDiCHLLXgTNLwCvrGT"

curl -X POST --header "Authorization: key=AIzaSyDxwE1m7WjI6400WD9GadNJqoZfJvBmjGs" \
       --header "Content-Type:application/json" \
       https://fcm.googleapis.com/fcm/send \
	-d "{\"to\":\"$DEVICE_TOKEN\",\"notification\":{\"title\": \"Dar title\", \"body\":\"Dar Message\"},\"priority\":\"high\"}"
