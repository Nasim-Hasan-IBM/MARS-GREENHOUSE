# SMART MARS GREENHOUSE:
A Smart Greenhouse system for Mars combining the **Artificial Intelligence (AI)**, **Internet of Things (IoTs)** and **Space Exploration** for the IBM's AI Builders' **August 2026** challenge.

# Background:
**National Aeronautics & Space Administration (NASA):https://www.nasa.gov/** through its **Mars Exploration Program (MEP):https://en.wikipedia.org/wiki/Mars_Exploration_Program** is trying to establish human inhabitants in Mars. In order to make it suitable for living, the key focused areas will be farming/cultivation of corps, possible detection of diseases and energy utilization. As, the weather & climate of Mars are different from the Earth, that's why, a special effort (greenhouse) is required for the farming/cultivation of corps. disease detection & energy optimization in Mars. For this reason, various statistical predictions are required for the Mars' environment related data, such as: atmospheric temperature, surrounding atmospheric pressure, compass degree, season etc. 

# Problem Statement:
The distance between the Earth and Mars is on average 140 million miles (225 million kilometers). As the distance is so huge, that's why, it will take a long time to oversee the greenhouse program in Mars from the Earth.

# Our Solution:
**SMART MARS GREENHOUSE** is a combined **Artificial Intelligence (AI)** and **Internet of Things (IoTs)** based approach for the real time analysis of the environment related data aiming to overcome/reduce the overseeing delay from the Earth.   

# High Level (HL) Architecture:

                  +-----------------------------+
                  |   Smart Mars Greenhouse     |
                  |-----------------------------|
                  | Temperature Sensor          |
                  | Pressure Sensor             |
                  | Season Detection            |
                  | Wind Direction              |
                  +-------------+---------------+
                                |
                        IoT Gateway
                        (ESP32/Raspberry Pi)
                                |
                        NASA's InSight MARS API
                                |
        -------------------------------------------------
                            IBM Cloud
        -------------------------------------------------
                                |
                            IBM Cloud Functions
                                |
            +-------------------+------------------+
            |                                      |
         IBM Cloudant                            OpenAI
      Sensor Data Storage                     GPT-4o AI Models
            |                                      |
            +-------------------+------------------+
                                |
                        AI Decision Engine
         ----------------------------------------------
                        Predict Irrigation
                        Disease Detection
                        Energy Optimization
        ----------------------------------------------
                   
# Operation Flow/Sequence:

Sense => Analyse => Decide => Report

# Tech Stack:
- **1. Programming Language:** Python Version#:3.13.5. Hyper Text Markup Language (HTML), Java Script (JS)
- **2. Artificial Intelligence (AI) Model:** OpenAI GPT-4o Model
- **3. Integrated Development Environment (IDE):** IBM Bob 

# Project's (MARS-GREENHOUSE) Folder Structure:

```
MARS-GREENHOUSE/
├── templates/
│   └── index.html               # Frontend template referenced in Flask route '/'
├── .gitignore                   # Version control exclusions[cite: 1]
├── app.py                       # Main Flask/FastAPI application logic & routes
├── README.md                    # Project documentation & architecture overview[cite: 3]
├── requirements.txt             # Project dependencies[cite: 4]
└── Secrets.env                  # Environment variables & API credentials
```

# IBM Bob's Role:
In this project, IBM's Bob played the role of an **Artificial Intelligence (AI) Assistant** to design, plan and implement the whole system by switching to the **Ask**, **Plan** and **Agent** modes respectively. The summary of Bob's role is mentioned below:

| Phase | Bob’s Mode | Bob’s Activities | Remarks
|---|---|---|---|
| Designing | Ask | Drew the High Level (HL) Architecture, Operation Flow/Sequence & Project’s Folder Structure | Inspected Bob’s output and performed the re-prompting where necessary|
| Planning | Plan | Divided the whole project into the smaller implementable sub-tasks based on the requirements | Approved the sub-tasks’ implementation plans of Bob through modification and re-prompting|
| Implementation | Agent | Generated the source codes for the back-end (Python) & front-end (HTML+JS) scripts | Audited the output of the source codes for both ends (back + front) and conducted the necessary changes for the successful local & production systems’ running |

# Local Setup:
The local setup of this project is very simple. You will need to follow the below mentioned steps chronologically:
- **1.** Install the Python Version#:3.13.5.
- **2.** Run the command **pip install -r requirements.txt** to install the Python's required packages/dependencies for this project.
- **3.** Install/Configure the **Apache** or any other webserver in the local system.
- **4.** Hit the **URL:http://localhost/templates/index.html** from a browser to land into the User Interface (UI) of this project. 

- **Note:** You will need to configure the port number properly in both ends (front + back) for establishing the communication.

# Production Deployment:
The whole project has been deployed in the **Render(https://www.render.com)**, which is a free hosting site and the production's **URL:https://mars-greenhouse.onrender.com/**  

# Demo Video URL:
The URL for our project's demo video is: **https://youtu.be/U1l60m0PFIg**









