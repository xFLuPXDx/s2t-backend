from openai import OpenAI
from dotenv import dotenv_values
import json



def s2tConvert(file):
  config = dotenv_values(".env")
  API_KEY = config["OPEN_AI_S2T_KEY"]

  client = OpenAI(api_key=API_KEY)
  audio_file = open(file, "rb")
  transcript = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file, 
    response_format="text"
  )
 
  response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
      {"role": "system", "content": "You are a helpful assistant who give summary and headpooints from the given content and gives the output JSON"},
      {"role": "user", "content": transcript},
      {"role": "system", "content": "make sure to include these keys in json summary and headpoints "}
    ]
  )
  
  return json.loads(response.choices[0].message.content)