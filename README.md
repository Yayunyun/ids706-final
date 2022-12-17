# IDS706-Final-Project
# Movie Recommender Microservice via Azure & Streamlit

[![Testing and Linting with Github Actions](https://github.com/Yayunyun/ids706-final/actions/workflows/main.yml/badge.svg)](https://github.com/Yayunyun/ids706-final/actions/workflows/main.yml)

[![Python application test with Github Actions](https://github.com/nogibjj/fastapi_news/actions/workflows/main.yml/badge.svg)](https://github.com/nogibjj/fastapi_news/actions/workflows/main.yml) 

# Final Project Workflow diagram
![Final_Proct_workflow](https://user-images.githubusercontent.com/112578755/208226954-fea32706-0883-4f95-96e1-02f59e2e3fc0.jpg)

# Project purpose:

The project aims to build a web app that is able to reuturn movie recommendations, we used Cosine Similarity as the algorithic rationale to design the recommender and perform Continuous Integration through Github Actions and configure Build Server to deploy changes on build (Continuous Deployment) using Azure, Streamlit and Github. The data is retrieved from IMDB. 

# Project process: Containerized Streamlit in Azure

#Follow the commands below

`docker build .`

`docker image ls`

`docker tag <imageid> movierecommender.azurecr.io/recommender:latest`

`docker push movierecommender.azurecr.io/recommender:latest`

`docker run -p 8501:8501 movierecommender.azurecr.io/recommender:latest`

1. Streamlit was leveraged to display the movie recommendations
2. Using Codespace as the environment, the microservice was containerized in Azure Registry and pushed to production using Streamlit
3. Continuous Delivery was performed using Azure Docker.
4. Continous Integration was enabled via Github Actions.


# Deployed domain 
`https://recommender-movie.azurewebsites.net`

# Example Output

<img width="775" alt="Example_Output" src="https://user-images.githubusercontent.com/112578755/208225518-11e2c62c-3b7b-467b-a001-e0d520ea34af.png">


