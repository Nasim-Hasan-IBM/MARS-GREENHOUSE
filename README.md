# SMART MARS GREENHOUSE:
A Smart Greenhouse system for Mars combining the **Artificial Intelligence (AI)**, **Internet of Things (IoTs)** and **Space Exploration** for the IBM's AI Builders' **August 2026** challenge.

# Background:
National Aeronautics & Space Administration (NASA):https://www.nasa.gov/ through its Mars 
Exploration Program (MEP):https://en.wikipedia.org/wiki/Mars_Exploration_Program is trying to establish human inhabitants in Mars. In order to make it suitable for living, one of the
key focused areas will be farming/cultivation of corps. As, the weather & climate of Mars are different from the Earth, that's why, a special effort (greenhouse) is required for the farming/cultivation of corps in Mars. For this reason, various statistical predictions are required for the Mars' environment related data, such as: temperature, humidity, energy optimization & consumption etc. 

# Problem Statement:
The distance between the Earth and Mars is on average 140 million miles (225 million kilometers). As the distance is so huge, that's why, it will take a long time to oversee the greenhouse program in Mars from the Earth.

# Our Solution:
**SMART MARS GREENHOUSE** is a combined **Artificial Intelligence (AI)** and **Internet of Things (IoTs)** based approach for the real time analysis of the environment related data aiming to overcome/reduce the overseeing delay from the Earth.   

# High Level (HL) Architecture:

                  +-----------------------------+
                  |   Mars Greenhouse           |
                  |-----------------------------|
                  | Temperature Sensor          |
                  | Humidity Sensor             |
                  | Soil Moisture Sensor        |
                  | CO₂ Sensor                  |
                  | Light Sensor                |
                  | pH Sensor                   |
                  +-------------+---------------+
                                |
                        IoT Gateway
                        (ESP32/Raspberry Pi)
                                |
                    MQTT / HTTPS / Wi-Fi
                                |
        -------------------------------------------------
                        IBM Cloud
        -------------------------------------------------
                    IBM Event Streams
                       (MQTT Broker)
                                |
                 IBM Cloud Functions
                                |
            +-------------------+------------------+
            |                                      |
      IBM Db2 / Cloudant                   IBM watsonx.ai
      Sensor Data Storage                 Granite AI Models
            |                                      |
            +-------------------+------------------+
                                |
                    AI Decision Engine
     ----------------------------------------------
     Predict Irrigation
     Predict Temperature
     Predict Humidity
     Disease Detection
     Growth Prediction
     Energy Optimization
     ----------------------------------------------
                                |
                     Automation Controller
            ---------------------------------
            Water Pump
            LED Grow Lights
            Heater
            Cooling Fan
            CO₂ Injector
            Nutrient Pump
            ---------------------------------
                                |
                        Greenhouse

# Operation Flow/Sequence:

Sense => Analyse => Decide => Act => Report

# Tech Stack:
**1. Programming Language:** Python Version#:3.13.5
**2. Artificial Intelligence (AI) Model:** IBM Granite-4-H-Small
**3. Integrated Development Environment (IDE):** IBM Bob 


