# Fake Spreader

## About

This project was developed in due course of Hack Cambridge 2022 which was dedicated to development in (ESG)[https://www.investopedia.com/terms/e/environmental-social-and-governance-esg-criteria.asp].  
The hackathon submission is published on (Devpost)[https://devpost.com/software/fakespreader]

## Inspiration

We have been inspired by the Shazam application allowing individuals to scan for sound patterns to see what music is played. We came up with an idea to create a similar tool to fight disinformation, by allowing us to check if the person we are listening to is spreading fake information, sharing rumours, or being biased by its stance if at all being friendly in the first place.

## What it does

Our tool uses text input (also obtainable from speech recognition and translation into text) to perform different analyses and present information in a dashboard. In particular, we check the sentiment of the statement (objective claims usually imply neutral sentiment), check against the available fact-checking database, provide recent news updates based on the query, and provide a prediction from a machine learning model to guess whether the statement is fake or true.

## Project structure

In our repo you can see two representations we have worked on:
 - CLI app showcasing logic of our backend to classify the sentiment of the statement and search the database for fact-checking.
 - Proper front-end representation, and the ability to submit URL for an audio file to call Deepgram API.

## Challenges we ran into

Availability of APIs to existing fact-checking resources is limited. Google API implementation served severe challenges; Full Fact API that we considered as an alternative is available only after license with Full Fact organization. On the other side, the Deepgram tool at the moment does not analyse real-time audio inputs, which require recording audio input.

## Accomplishments that we're proud of

Working as a mixed team and being able to coordinate in order to deal with challenges effectively - for all of us this was a new field with a lot of investigation to be made.

## What we learned

There are many NLP applications that could serve retail investors, journalists or laypeople in building an immune system against fake news. At the same time, people do not have tools to protect themselves at their fingertips.

## What's next for FakeSpreader

While proving that the way to tackle fact-checking, rumour spreading and stance association is possible, we wanted to check the capabilities of technology. With this success, we are confident that a tool to analyse fact chacking about companies, reviewing both audio and text inputs from real life or web, would be possible. Verifiability of claims about listed companies, that would be checked against their annual, quarterly reports or news statements would prevent people from emotional decisions on their investments and money in general. In the future, we would also like to develop tool matching language from the news with the volume of stock trading and social media mentions measuring 'pressure' under which company is and indicate a warning sign to investors or customers about the existence and nature of the issue that company is going through.

## Try it for yourself!

To test out the suite you need to obtain API keys from (Monkeylearn)[https://monkeylearn.com/] and (NewsAPI)[https://newsapi.org/], since they are used for sentiment analysis and the recent news based on the search query. Once obtained, set environmental variables `APIKEY_MONKEYLEARN` and `APIKEY_NEWSAPI`, and run
```
./spreader.py -s "<query>"
```
to get the dashboard output in your terminal.

