from fastapi import FastAPI, Request, Response, Depends
from fastapi.responses import PlainTextResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
import json
import openai
import os
import configargparse
import uvicorn
from jinja2 import Template

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="some-secret-key")  # You should use a more secure secret key in production.

openai.api_key = os.environ["OPENAI_API_KEY"]
if not openai.api_key:
    raise ValueError("Please provide an API key in the environment variable OPENAI_API_KEY")

def load_config():
    parser = configargparse.ArgParser(default_config_files=['assistant_config.ini'])
    parser.add('-c', '--config', is_config_file=True, help='config file path')
    parser.add('--model_name', default=None, help='OpenAI Model Name')
    parser.add('--assistant_name', default=None, help='Name of the assistant')
    parser.add('--description', default=None, help='description of the assistant')
    return parser.parse_args()

def get_session(request: Request):
    return request.session

@app.get("/")
async def index(request: Request):
    with open("templates/index.html") as file:
        content = file.read()
    template = Template(content)
    rendered_content = template.render(assistant_name=config.assistant_name)
    return Response(content=rendered_content, media_type='text/html')


@app.post("/send_prompt", response_class=PlainTextResponse)
async def send_prompt(request: Request, session: dict = Depends(get_session)):
    user_input = (await request.json())['prompt']

    # Retrieve messages from session or initialize if not present
    messages = session.get("messages", [
        {
            "role": "system",
            "content": config.description
        },
        {
            "role": "assistant",
            "content": "Hello, how can I help you?"
        },
    ])
    
    # Append the new user message
    messages.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model=config.model_name,
        messages=messages,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    # Append the assistant's response to the messages
    messages.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
    
    # Save messages to session
    session["messages"] = messages

    return response['choices'][0]['message']['content']


if __name__ == '__main__':
    config=load_config()
    uvicorn.run(app, host='0.0.0.0', port=8000)
