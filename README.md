# infinum_chatbot

## HOW TO RUN APP IN DOCKER
### Basic guideline
To run this project, you will need an **OPENAI key**. You need to add them, in file *infinum_chatbot/backend/API.py*, on line 106, variable **my_key**. This application is running on **port 8501**.<br>

If this port is not available, you can change it in *infinum_chatbot/docker-compose.yml* on line 40. <br>

This application requires postgresql. In docker, postgresql is running on **port 5432**. You can change it on line 15 in *infinum_chatbot/backend/API.py*.<br>

**Backend** is running on **port 8000**. You can change it on line 25 in file *infinum_chatbot/docker-compose.yml*.

### Run through Docker
This project is done with docker compose. You need to run docker-compose.yml file from *infinum_chatbot/docker/docker-compose.yml*, by command *(sudo) docker-compose up --build*.
Now, docker container is running. You can open application by pasting this url: **http://localhost:8501/**. 

## HOW TO RUN ON LOCAL
This application requires postgres. To run postgres in Ubuntu, you need to run *sudo service postgresql start*. You need to change line 9 in file *infinum_chatbot/frontend/frontend.py* on 
**with open("frontend/Style/main.css", "r") as f:**. 

You need to change 'backend' to 'localhost' in file *infinum_chatbot/backend/API.py* on lines 17, 52, 96, 133.

After these changes, you can run streamlit run **infinum_chatbot/frontend/frontend.py**. 


## RESUME
Important ports

1. 8501 => Port for running frontend-app container (Main part of application)
2. 5432 => Port for running Postgresql
3. 8000 => Port for running backend-app container

these ports, you can change in the file **docker-compose.yml**.


If you are running application from local


In file **API.py**, you need to change 'backend' to 'localhost' on lines 17, 52, 96, 133.

