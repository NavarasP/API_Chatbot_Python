# Project Name

## Description

This project is a conversational chatbot powered by the OpenAI GPT-3.5 Turbo model. It allows users to have interactive conversations with the chatbot and receive answers to their queries.

## Prerequisites

Before running the project, ensure that you have the following:

- Python (version X.X.X)
- Flask (version X.X.X)
- Flask-CORS (version X.X.X)
- OpenAI Python SDK (version X.X.X)
- Chroma (version X.X.X)

## Installation

1. Clone the repository:
```
git clone https://github.com/your-username/your-repository.git
```

3. Change into the project directory:
cd your-repository


4. Install the required dependencies using pip:


3. Install the required dependencies using pip:


## Configuration

1. Set the OpenAI API key as an environment variable:

export OPENAI_API_KEY=your_api_key


Replace `your_api_key` with your actual OpenAI API key.

2. (Optional) Enable persistence:

- To save the model to disk and reuse it for repeated queries, set the `PERSIST` variable to `True` in the `app.py` file.

## Usage

1. Start the Flask server:
   python app.py

2. Access the chatbot API using the following endpoint:
POST /api/chat


The endpoint expects a JSON payload with the following structure:

```json
{
  "query": "Your query or message"
}
Example usage with cURL:
curl -X POST -H "Content-Type: application/json" -d '{"query": "Hello"}' http://localhost:5000/api/chat

The chatbot will respond with a JSON object containing the answer:

{
  "answer": "The chatbot's response"
}


To end the conversation, you can send one of the following messages: "quit", "q", or "exit".

Troubleshooting
If you encounter any errors or issues while running the project, please ensure that you have followed the installation steps correctly and that all dependencies are installed.
If you receive a rate limit error from the OpenAI API, the chatbot will automatically retry up to three times before returning a rate limit exceeded message. You can adjust the MAX_RETRY_COUNT variable in the app.py file if needed.
License
This project is licensed under the MIT License.



