# infinum_chatbot

## HOW TO RUN APP IN DOCKER
### Basic guideline
To run this project, you will need an **OPENAI key**. You need to add them, in file *infinum_chatbot/backend/API.py*, on line 106, variable **my_key**. This application is running on **port 8501**.
If this port is not avaailable, you can change it in *infinum_chatbot/docker-compose.yml* on line 40. 
This application requires postgresql. In docker, postgresql is running on **port 5432**. You can change it on line 15 in *infinum_chatbot/backend/API.py*.
**Backend** is running on **port 8000**. You can change it on line 25 in file *infinum_chatbot/docker-compose.yml*.

### Through Docker
This project is done with docker compose. You need to run docker-compose.yml file from *infinum_chatbot/docker/docker-compose.yml*, by command *(sudo) docker-compose up --build*.
Now, docker container is running. You can open application by pasting this url: **http://localhost:8501/**. 

## HOW TO RUN ON LOCAL
