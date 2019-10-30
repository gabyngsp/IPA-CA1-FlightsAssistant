# SECTION 1 : PROJECT TITLE
### Flights Assistant
![logo](resources/Airplane.jpg)

# SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT
Flight Assistant Chatbot (via WeChat app) to help monitor flight deal based on users' request and send daily updates on flight deals they are looking for to their WeChat account. User can click on the hyperlink associated to the deal to access the deal and make the booking.


# SECTION 3 : CREDITS / PROJECT CONTRIBUTION
| Official Full Name | Student ID (MTech Applicable)| Work Items (Who Did What) | Email (Optional) |
| :---: | :---: | :---: | :---: |
| GONG YIFEI | A0198495E  | WeChat Bot (Receive Request, Send Result), Speech-to-Text |  |
| JIANG YANNI | A0201097M  | RPA (Extract Flight Deals, Compare and generate final deals) |  |
| NG SIEW PHENG | A0198525R  | RPA (Search Flight Deals, Export Search Result), Database functions | e0402066@u.nus.edu |


# SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO


# SECTION 5 : USER GUIDE

# SECTION 6 : DEVELOPER GUIDE
## Database
Install Mongo DB by following the instruction here https://docs.mongodb.com/manual/administration/install-community/

## Conda Environment
To set up the environment
1. git clone https://github.com/gabyngsp/IPA-CA1-FlightsAssistant/
2. cd IPA-CA1-FlightsAssistant
3. conda create -n FlightsAssistant --file environment.yaml
4. conda activate FlightsAssistant
5. conda install -c conda-forge ffmpeg
6. python -m spacy download en_core_web_sm


## Start WeChat Bot
1. python thread.py
2. Open WeChat app and scan QR code generated







