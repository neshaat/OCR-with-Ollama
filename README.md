# Receipt OCR with Ollama + Gemma3:4B

This project demonstrates a lightweight **LLM-based OCR system** that extracts text from receipt images using **Gemma3:4B running on Ollama**.

The system runs in **Google Colab** and uses **ngrok** to expose the local Ollama API, allowing external requests to send receipt images and receive extracted text.

This project is designed as a simple and practical experiment showing how **Large Language Models can be used for OCR-like tasks**.

---

## Architecture

The pipeline works as follows:

Receipt Image  
↓  
Upload to Colab Interface  
↓  
Send Request to Ollama (Gemma3:4B)  
↓  
Image → Text Extraction  
↓  
Return Extracted Receipt Text  

To make the local model accessible externally, **ngrok** creates a public endpoint.

---

## Technologies Used

- Ollama
- Gemma3:4B
- Google Colab
- ngrok
- Python
- LLM-based OCR

---

## Features

- Upload receipt images
- Extract text using Gemma3:4B
- Run fully on a local LLM (via Ollama)
- Public API access through ngrok
- Simple accuracy checking for extracted text

---

## Installation

### 1 Install Ollama
Follow the instructions from the official website:

https://ollama.com

---

### 2 Pull the Gemma model

```bash
ollama pull gemma3:4b
