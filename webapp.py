from fastapi import FastAPI, File, UploadFile
from slack import Slack, BearerAuth
import os
from pydantic import Field, BaseModel


TOKEN = os.environ.get('SLACK_TOKEN')

Slacker = Slack(
    TOKEN,
    BearerAuth(TOKEN)
)


channels, _ = Slacker.get_conversations()


CHANNEL = channels['test']  # ----> for testing
# channel = channels['04-labeling-questions'] # main application channel

# CHANNEL = channels['test']  #----> for testing


class MessageModel(BaseModel):
    text: str


images = {}
messages = {}

app = FastAPI()


@app.post('/upload_message/{userID}')
async def upload_message(userID: str, message: MessageModel):
    messages[userID] = message.dict()['text']
    print(messages)
    return {'type': 'success'}


@app.post('/send_file/{userID}')
async def send_file(userID: str, file: UploadFile = File(...)):
    images[userID] = await file.read()
    Slacker.send_file(CHANNEL, images[userID], messages[userID])
    return {"filename": file.filename}


@app.get('/')
def get_something():
    return {'text': 'hello world'}
