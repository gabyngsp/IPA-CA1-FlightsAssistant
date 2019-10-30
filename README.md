# SECTION 1 : PROJECT TITLE
### Flights Assistant
![logo](resources/Airplane.jpg)

# SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT
Flight Assistant Chatbot (via WeChat app) to help monitor flight deal based on users' request and send daily updates on flight deals they are looking for to their WeChat account. User can click on the hyperlink associated to the deal to access the deal and make the booking.


# SECTION 3 : CREDITS / PROJECT CONTRIBUTION
| Official Full Name | Student ID (MTech Applicable)| Work Items (Who Did What) | Email (Optional) |
| :---: | :---: | :---: | :---: |
| GONG YIFEI | A0198495E  | WeChat Bot (Receive Request, Send Result), Speech-to-Text | e0402036@u.nus.edu |
| JIANG YANNI | A0201097M  | RPA (Extract Flight Deals, Compare and generate final deals) | e0409752@u.nus.edu |
| NG SIEW PHENG | A0198525R  | RPA (Search Flight Deals, Export Search Result), Database functions | e0402066@u.nus.edu |


# SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO


# SECTION 5 : USER GUIDE
1. add chatbot as your wechat friend
2. send a flight searching request, can use both text message and audio message

Some examples of request:
- I want to book a flight from Dalian to Shanghai on January 3rd and returning on January 5th for 1 adult and 2 children age 2 and 3
- I would like to book a flight from singapore to beijing on November 1st for 2 adults.
- Book a flight from Edinburgh to Dalian on December 10th, Dalian to Tokyo on December 15th, Tokyo to Osaka on December 20th


# SECTION 6 : INSTALLATION GUIDE
## Database
Install Mongo DB by following the instruction here https://docs.mongodb.com/manual/administration/install-community/

## Conda Environment
To set up the environment
1. git clone https://github.com/gabyngsp/IPA-CA1-FlightsAssistant/
2. cd IPA-CA1-FlightsAssistant
3. conda env create --file environment.yaml
4. conda activate FlightsAssistant
5. conda install -c conda-forge ffmpeg
6. python -m spacy download en_core_web_sm


## Start WeChat Bot
1. python thread.py
2. Open WeChat app and scan QR code generated







