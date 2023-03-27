# Sentiment-Analysis

Go to the project directory and please sure you have python3 latest version which is Python 3.9.6 and then run the below:

docker compose up --build and can access the webpage with the url http://localhost:1172/ 

There is an issue with SCRAM for Mac users. https://stackoverflow.com/questions/62807717/how-can-i-solve-postgresql-scram-authentication-problem . Please use export DOCKER_DEFAULT_PLATFORM=linux/amd64 and then start you build. 

Also please remove the line platform: linux/amd64 under db service if you are a windows user.

""Future improvements: ***Accouncement to Dr.Bennett****""

1. Change SCRAM authetication to md5.
2. Frontend should be done using JS intead of python. But right now, we are fresh undergrad students, and we are not knowledgeable on JS or C# :D .We are      learning python for now and we implemented this application the best possible way, by learning from all the errors :) .!. We also used a little of JS      and HTML in the frontend.
