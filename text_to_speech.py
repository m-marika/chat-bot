import gtts
import speech_recognition as sr
from pydub import AudioSegment

def text_to_speech(msg):
  tts = gtts.gTTS(msg, lang='en')
  tts.save('text_to_speech.mp3')


def ogg2wav(ofn):
  wfn = ofn.replace('.ogg', '.wav')
  segment = AudioSegment.from_file(ofn)
  segment.export(wfn, format='wav')


def speech_to_text():
  ogg2wav('voice.ogg')
  r = sr.Recognizer()
  with sr.AudioFile('voice.wav') as source:
    audio = r.record(source)
    text = r.recognize_google(audio_data=audio)
    return text
