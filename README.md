# HAI Coursework 1: AN INTERACTIVE NLP-BASED AI SYSTEM

## Project Title: Wikipedia Information Retrieval Chatbot

20204134 Chuang Caleb hcycc2

BSc Hons Computer Science with Artificial Intelligence

## Overview

---

KiwiBot is a simple chatbot that offers basic summaries about any given topic. It is a "knowledge base information retrieval system", except that rather than a small, static, local knowledge base, it instead uses the `wikipedia` python package to search the massive, dynamic, online knowledge base that is wikipedia.

The python package would simplify a lot of the query-searching aspect of the program, so more focus can be placed on the chat user interface aspect. Besides that, pulling data from a large dataset can give the illusion of a more knowledgeable, personal and realistic chatbot.

This project was part of the Humans-AI Interactions Module.

The report for this project can be found [here](https://docs.google.com/document/d/1E2wGUxfbE8L4w1zS6fW0pPOgOymix8UhWyN-zHXxaaQ/edit?usp=sharing).

## Features

---

- Identity Management
- Context Switching
- Knowledge Base Question Answering

## Using the chabot

---

### 1. Dependencies

Ensure you have the following non-standard python libraries installed in your environment:

- `nltk`
- `numpy`
- `scipy`
- `wikipedia`

### 2. Building

Before the chabot can operate, first build and train the model by running

```python
python build.py
```

This will read `intents.json` and create a `.pickle` file, which will be our trained model.

### 3. Running

Now you can run the command-line chatbot by executing in a terminal of your choice:

```python
python main.py
```
