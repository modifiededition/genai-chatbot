# Verloop Chatbot

This chatbot leverages the OpenAI API to answer user queries based on four specific features provided by Verloop: **Smart Block**, **Spark**, **Co-Pilot**, and **AnswerFlow**. It intelligently interprets the user's intent and responds accordingly by utilizing a two-step OpenAI API call process.

## Features
The chatbot is designed to support and answer queries related to the following Verloop features:
1. **Smart Block**
2. **Spark**
3. **Co-Pilot**
4. **AnswerFlow**

## How It Works
The chatbot performs two OpenAI API calls to interpret and respond to user queries:
1. **Intent Identification**: The first API call determines the intent of the query based on both current and historical conversations, identifying which Verloop feature the user is asking about.
2. **Contextual Response**: Based on the identified feature, the chatbot updates the system prompt with relevant context for that feature, enabling it to answer the user's query accurately.

## Requirements
- **Python 3.7+**
- **OpenAI API Key** (You must have an OpenAI account and API access)

## Usage
To run the chatbot, execute the following command:

```bash
python bot.py --model_name gpt-4o
```

The chatbot has been tested with the **gpt-4o** model, which accurately captures intent based on current and historical conversations.

## History Tracking

When you stop the chatbot using a keyboard interrupt, a new folder named history is automatically created. This folder contains files tracking the conversations between the bot and the user.
