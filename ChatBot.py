# chatbot.py
# A simple Gradio app to chat with a local Ollama model
# Make sure you have Ollama running locally with the desired model.
# Install required packages: pip install gradio requests
# Run the app: python chatbot.py
# Access the app at http://127.0.0.1:7860
# Ensure Ollama is running: ollama serve
# Example Ollama command to run a model: ollama run tinydolphin:1.1b
# Adjust model name as needed.
# Note: This example assumes you have a model named "tinydolphin:1.1b" available locally.
# Adjust the model name in the code if necessary.

# Import necessary libraries
import gradio as gr
import requests

# Define the Ollama API endpoint
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

# Function to send a message to the Ollama model and get a response
def chat(message, model, lang):
    '''Send a message to the Ollama model and get a response.'''
    
    # Construct the prompt based on the selected language
    prompt = message

    # Send the request to the Ollama API
    try:
        r = requests.post(OLLAMA_URL, json={
            "model": model, # e.g., "tinydolphin:1.1b"
            "prompt": prompt, # The prompt to send to the model
            "stream": False # Set to True if you want streaming responses
        }, timeout=60) # Increase timeout if necessary

        # Check for errors in the response
        if r.status_code != 200:
            return f"Error: {r.status_code} - {r.text}" # Return error message if status code is not 200
        # Return the model's response
        return r.json().get("response", "No response from model.")
    # Catch exceptions and return the error message
    except Exception as e:
        return f"Exception: {str(e)}"
    
# Create the Gradio interface
with gr.Blocks(title="Local Tiny Chat") as demo: # Set the title of the app
    gr.Markdown("Local Tiny Chat with Ollama and Gradio") # App description
    lang = gr.Dropdown(choices=["English(en)"], label="Select Language", value="English(en)") # Language selection dropdown
    model = gr.Dropdown(choices=["tinydolphin:1.1b"], label="Select Model", value="tinydolphin:1.1b") # Model selection dropdown
    message = gr.Textbox(label="Enter your message") # Input textbox for user message
    output = gr.Textbox(label="Reply", lines=6) #increase lines for better visibility
    submit = gr.Button("Submit") # Submit button
    submit.click(fn=chat, inputs=[message, model, lang], outputs=output) # Define the button click action

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False) # Launch the app on localhost without sharing
    
""" 
This Python project creates a simple web-based chatbot using the Gradio library to build the user interface and the Ollama service to power the AI model. 
It allows you to chat with a large language model (LLM) running locally on your computer, specifically using the **tinydolphin:1.1b** model as an example.

---

## Key Components

### 1. Gradio
This library creates a simple web interface for the chatbot. 
It handles all the visual elements, like the text boxes for input and output, the dropdown menus to select the language and model, and the submit button. 
It makes it easy to turn a Python function into a shareable web app.

### 2. Ollama
Ollama is a service that lets you run open-source large language models (LLMs) on your own machine. 
Instead of relying on an external API like OpenAI, this project communicates with a local Ollama server. 
This means your conversations and data don't leave your computer, offering better privacy. 
You need to have Ollama running in the background with a model like **tinydolphin:1.1b** downloaded before you can use this app.

### 3. The `requests` library
This library is used to send HTTP requests to the Ollama server.
When you type a message and click "Submit," the `chat` function uses `requests.post` to send your message to the Ollama API, which is running at `http://127.0.0.1:11434/api/generate`.

---

## How It Works

1.  **User Input**: You type a message into the text box and click the "Submit" button on the Gradio interface.
2.  **Function Call**: Clicking the button triggers the `chat` function in the Python code. This function takes your message, the selected model, and the selected language as inputs.
3.  **API Request**: The `chat` function creates a JSON object with your message and the model name, then uses `requests` to send this data to the Ollama API endpoint.
4.  **Ollama Processing**: The Ollama service receives the request, processes your message using the specified **tinydolphin:1.1b** model, and generates a response.
5.  **Response Handling**: The `requests` library gets the response from Ollama. The `chat` function extracts the AI's reply from the response and sends it back to the Gradio interface.
6.  **Display Output**: Gradio displays the AI's reply in the output text box for you to read.

In essence, the project is a bridge between a friendly web interface (Gradio) and a powerful, locally-run AI model (Ollama). 
It makes it simple to interact with a local LLM without needing to use the command line.

"""