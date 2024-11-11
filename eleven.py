from elevenlabs import play
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
  api_key="sk_ad250103a293862c41ea0cc893c1c85b5cfb71b178e222ce", # Defaults to ELEVEN_API_KEY
)

audio = client.generate(
  text="Yash likes cat",
  
  voice="EXAVITQu4vr4xnSDxMaL",
  model="eleven_multilingual_v2"
)
play(audio)
