
# Utility Rasa ChatBot

A Utility Based ChatBot built using Rasa. 

The features which has been added in it:

- Greets the client
- Shows a picture in response to client regarding his mood
- Remembers the location of the client as described
- Gets the current time based on the location of the client
- Shows the time difference between a new location and the residential location mentioned by the user




## Installation

Steps to install this project and run in Windows:

### Step-up new Environment for Rasa
```bash
  conda create --name rasa python==3.8
  conda activate rasa
```
### Install dependencies and packages
```bash
  conda install ujson
  conda install tensorflow
  pip install rasa
```
### Clone the repository
```bash
  git clone https://github.com/SarveshSridhar/Utility-Rasa-ChatBot.git
```
### Train the model
```bash
  rasa train
```
### Run the chatbot in Interactive Mode
```bash
  rasa interactive
```
### Run the chatbot in Shell Mode
```bash
  rasa shell
```
## Screenshots

![App Screenshot](https://github.com/SarveshSridhar/Utility-Rasa-ChatBot/blob/master/chatbot.PNG)
