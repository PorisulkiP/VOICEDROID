import speech_recognition as sr
import os
import ffmpeg
from pocketsphinx import AudioFile, get_model_path, get_data_path
from pydub import AudioSegment

model_path = get_model_path()
data_path = get_data_path()

# PATH = 'E:\\GitHub\\Materials\\Psal\\'

PATH = 'E:\\GitHub\\VOICEROID\\audio\\'

list_dir = os.listdir(PATH)
os.chdir(PATH)

#Переименовываем и конвертируем файлы под единый формат
real_name = 'Hello.wav'
name_changes = 'Hello.wav'

q = int(input('С чем работаем?' + '\n' + '1 – Папка' + '\n' + '2 – Файл' + '\n'))

if q == 1:
	def rename_dir():
		i = 0
		a = 1
		for last_name in list_dir:
			name = name_changes + str(i) + '.mp3'
			try:
				os.rename(last_name, name)
			except NameError:
				pass
			except TypeError:
				pass
			except FileExistsError:
				pass
			except FileNotFoundError:
				pass 
			a += 1
			i += 1
	name = rename_dir() 
	
else:
	def rename_file(name_changes):
		try:
			os.rename(real_name, name_changes)
		except NameError:
			pass
		except TypeError:
			pass
		except FileExistsError:
			pass        
		except FileNotFoundError:
			pass 
	name = rename_file(name_changes)
	name = name_changes

# Конвертируем в Wav
def convert(name_convert):
	stream = ffmpeg.input(name_convert)
	stream = ffmpeg.output(stream, name_convert + '.wav')

if not name.endswith('wav'):
	convert(os.path.join(str(PATH), str(name)))

AUDIO_FILE = os.path.join(str(PATH), str(name))

r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
	audio = r.record(source) 

try:
	f = open('name_changes.txt', 'w')
	data = (r.recognize_google(audio, language="ru-RU"))
	print(data)
	f.write(data)
	f.close()
except sr.UnknownValueError:
	print("Sphinx could not understand audio")
except sr.RequestError as e:
	print("Sphinx error; {0}".format(e))

