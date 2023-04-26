# Sentiment-Analysis for CSCI 5400 under Dr. Bennett. 
**Before starting, We wanted to thank Dr.Jacob Gilenwater for sharing the crash courses on HTML and FASTAPI examples. That helped alot.**
**Intallation Materals:**
1. VSCode
2. Docker
3. Python 3.x.x along with pip3(Installation details are below)

**Installation Details:**
1.Open VSCode. Open new terminal, run the command-- git clone https://github.com/udaynath1171/Sentiment-Analysis/
Open to the project directory of the cloned project and please make sure to go into the project directory in your terminal and then make sure you have python and pip installed.
You can check it using the command **python --version** . If not, Please install it using the recommendations in https://realpython.com/installing-python/#what-your-options-are 

In VSCode,Jsut make sure you already opened the project directory. All the requriment libraries will be automatically downlaoded as specified in the requirements.txt. Please make sure to have the docker extension installed and also make sure that its integrated with your docker.( You can see the docker on the left most sided on the VSCode.

Run below in project directory to build the images and bring up the containers

***docker compose up --build*** and can access the webpage with the url http://localhost:1172/ 

We have added admin module that ask you with username and password and once autheticated, it will log you to the admin module.
Username and password are hard coded.

**Username : admin**

**password: admin**

**The admin module has following functionalities:**
The average sentiment score,
The Number and Percentage of “Positive” Sentiments,
The Number and Percentage of “Negative” Sentiments,
The Number and Percentage of “Neutral” Sentiments,
Deleting a particular sentence,
Editing the sentiment of a particular sentence (e.g., from negative to positive) in the case that these are perceived to be incorrect.


***If you see 'Internal server error' when trying to acccess the webpage, Please execute below commands in your project directory:***

1. cd db       **//changes directory to db from your project directory//**

2. docker cp init.sql sentiment-analysis-db-1:/docker-entrypoint-initdb.d/       **//copies init.sql inside the docker db container//**

3. docker exec sentiment-analysis-db-1 psql -U pgsqldev4 -d Sentimental_Analysis -f docker-entrypoint-initdb.d/init.sql       **//executes the init.sql//**

***The above is because the init.sql is not copying to docker as intended by the dockerfile in the db direcory. The above workaround can manually let you copy it. Once its done, we dont need to do it multiple times. Just go ahead and refresh the webpage(Dont need to re-build the container). Please read future improvements for more details.

There is an issue with SCRAM for Mac users. https://stackoverflow.com/questions/62807717/how-can-i-solve-postgresql-scram-authentication-problem . Please run export DOCKER_DEFAULT_PLATFORM=linux/amd64 under the project directory and then start you build..!

***Also please add the line (platform: linux/amd64) under db service of docker-compose.yml file if you are a windows user.***

""Future improvements: ***Accouncement to Dr.Bennett***""

1. Change SCRAM authetication to md5. Since its not any issue in windows platforms, we dont want to ahead ahead and do it without proper research. The setting to this change can be found in postgresql.conf file under /var/lib/data/ of the db container.
2. Frontend should be done using JS intead of python. But right now, we are fresh undergrad students, and are not very familiar on JS or C# :D .We are      learning python and we implemented this application the best possible way, by learning from all the errors :) .!. We also used a little of JS and HTML in the frontend.
3. Regarding the db setup, I beleive that docker-compose.yml is not able to reference the dockerfile in db directory. We tried multiple methods to do it, but failed. We will work on it and can fix it. But for now, we want to go ahead and move to a manual workaround temporarly until we fix this bug in the coming week submissions.!
