# Sentiment-Analysis for CSCI 5400

Go to the project directory and please sure you have python3 latest version which is Python 3.9.6 and then run the below:

***docker compose up --build*** and can access the webpage with the url http://localhost:1172/ 

***If you see Internal server error when trying to acccess the webpage, Please execute below commands in your project directory:

1. cd db **//changes directory to db from your project directory//

2. docker cp init.sql sentiment-analysis-db-1:/docker-entrypoint-initdb.d/  **//copies init.sql inside the docker db container//

3. docker exec sentiment-analysis-db-1 psql -U pgsqldev4 -d Sentimental_Analysis -f docker-entrypoint-initdb.d/init.sql  **//executes the init.sql//

***The above is because the init.sql is not copying to docker as intended by the dockerfile in the db direcory. The above workaround can manually let you copy it. Once its done, we dont need to do it multiple times. Just go ahead and refresh the website. Please read future improvements for more details.

There is an issue with SCRAM for Mac users. https://stackoverflow.com/questions/62807717/how-can-i-solve-postgresql-scram-authentication-problem . Please use export DOCKER_DEFAULT_PLATFORM=linux/amd64 under the project directory and then start you build.

***Also please add the line (platform: linux/amd64) under db service of docker-compose.yml file if you are a windows user.***

""Future improvements: ***Accouncement to Dr.Bennett***""

1. Change SCRAM authetication to md5.
2. Frontend should be done using JS intead of python. But right now, we are fresh undergrad students, and are not very familiar on JS or C# :D .We are      learning python and we implemented this application the best possible way, by learning from all the errors :) .!. We also used a little of JS and HTML in the frontend.
3. Regarding the db setup, I beleive that docker-compose.yml is not able to reference the dockerfile in db directory. We tried multiple methods to do it, but failed. We will work on it and can fix it. But for now, we want to go ahead and move to a manual workaround temporarly until we fix this bug in the coming week submissions.!
