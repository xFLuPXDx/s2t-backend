from openai import OpenAI
from dotenv import dotenv_values



def s2tConvert(file):
  config = dotenv_values(".env")
  API_KEY = config["OPEN_AI_S2T_KEY"]

  from openai import OpenAI
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
      {"role": "system", "content": "You are a helpful assistant designed to give summary , headpoints and topics covered and also youtube urls for topic for subject related software quality designed to output JSON"},
      {"role": "user", "content": transcript}
    ]
  )
  return response.choices[0].message.content