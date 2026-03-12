# Simple telegram bot (STB)
___

A simple Telegram bot demonstrtes core features which is powered by the aiogram Telegram framework and Mistral LLM. By using Redis database STB keeps track of user conversation history. For interaction with Mistral LLM used Pydantic AI.

## Built With
- [aiogram](https://docs.aiogram.dev/) - Async Telegram bot framework
- [Mistral AI](https://mistral.ai/) - Large Language Model
- [Pydantic AI](https://ai.pydantic.dev/) - AI interaction layer
- [Redis](https://redis.io/) - Conversation history storage
- [Logfire](https://logfire.pydantic.dev/) - Logging and monitoring

## How to use it:
 - /help - shows you interactive commands
 - /send_photo - send nice picture of black kitty
 - /promo - get your discount for evening
 - /start - say hello to bot
 - or ask whatever you like, and STB will ask Mistral LLM for you:)



## Instructions to run STB:
 - Create [Telegram Bot](https://core.telegram.org/bots/tutorial).
 - Install [Docker](https://www.docker.com/) for running Redis server.
 - Get API key on [Mistral AI](https://mistral.ai/Mistral) .
 - Get API key on [Logfire](https://logfire.pydantic.dev/).

