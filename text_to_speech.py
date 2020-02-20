from gtts import gTTS
import vlc
from playsound import playsound
'''
install playsound using pip install playsound
install gtts using pip install gTTS
tested on linux
'''
file_path = <FILE_PATH>
tts = gTTS(text="Hi Python, lets rock", lang="en")
tts.save(file_path)
playsound(file_path)

