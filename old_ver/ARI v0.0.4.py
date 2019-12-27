# Голосовой помощник Ариэль v0.0.4
import speech_recognition as sr
import os, pyaudio, sys, webbrowser, youtube_dl, pyttsx3, datetime, winsound
from fuzzywuzzy import fuzz

speak_engine = pyttsx3.init()

# Произносим
def talk(text):
	print(text)
	speak_engine.say(text)
	speak_engine.runAndWait()
	speak_engine.stop() 
	return speak_engine


def speech(say_some):
	winsound.PlaySound(say_some, winsound.SND_FILENAME)


print("Здравствуйте, я голосовой помощник Ариэль")
speech('audio/Hello.wav')

# настройки
time = ('который час','текущее время','сейчас времени','время')
name = ('как тебя зовут', 'назови своё имя', 'представься')
radio = ('включи музыку','воспроизведи радио','включи радио', 'радио')
what = ('что означает','что значит','что такое')
stop = ('стоп', 'топ', 'stop')
youtube = ('открой браузер','включи ютюб','включи youtube', 'скачай видео с ютюба', "открой youtube","включи браузер")
radio_dict = {
				'радио дача' : 'http://listen10.vdfm.ru:8000/dacha',
				'русское радио' : 'http://play.russianradio.eu/stream',
				'электронная музыка' : 'http://radio-electron.ru:8000/128',
				'эхо москвы' : 'http://ice912.echo.msk.ru:9120/24.aac',
				'классическая музыка' : 'http://stream.srg-ssr.ch/m/rsc_de/mp3_128',
				'наше радио' : 'http://nashe128.streamr.ru'
			}

print("Говорите, я жду: ")
speech('audio/Start taking.wav')
def command():
	# Включаем микрофон
	r = sr.Recognizer()
	r.energy_threshold = 10000
	m = sr.Microphone(device_index = 1)
	# Слушаем микрофоном
	with m as data:
		print('Слушаю:')
		r.adjust_for_ambient_noise(data, duration=0.2)
		audio = r.listen(data)
	# Распознаём речь
	try:
		say = r.recognize_google(audio, language="ru-RU").lower()
	except sr.RequestError:
		print("Неизвестная ошибка, проверьте интернет соединение!")
	except sr.UnknownValueError:
		talk("Я вас не поняла")
		return
	finally:
		print("Вы сказали: " + say)
	return say

say = command()

def makeSomething(say):
	if say.endswith(stop):
		talk("Да, конечно, без проблем")
		sys.exit(0)
	if say.endswith(time):
		# сказать текущее время
		now = datetime.datetime.now()
		talk("Сейчас " + str(now.hour) + ":" + str(now.minute))
		sys.exit(0)
	if say.endswith(youtube):
		talk("Уже открываю")
		url = 'https://www.youtube.com'
		webbrowser.open(url,new=0, autoraise=True)
		sys.exit(0)
	if say.endswith(name):
		speech('Presentation.wav')
		sys.exit(0)
	if say.endswith(radio):
		#Радио
		talk("Выберите радио: ")
		say = command()
		url = None
		for key in radio_dict:
			if key == say:
				print(key)
				url = radio_dict.get(key)
				webbrowser.open(url, new=0, autoraise=True)
		if url == None:
			talk('Нет такого радио')
		sys.exit(0)
	if say.startswith(what):
		webbrowser.open('https://yandex.ru/search/?lr=10735&text='+ say,new=0, autoraise=True)
		sys.exit(0)
	else:
		winsound.PlaySound('audio/Error 1.wav', winsound.SND_FILENAME)
		sys.exit(0)

# Записываем в файл
f = open('То, что нужно сказать.txt', 'a')
f.write(say + '\n')
f.close()

while True:
	makeSomething(say)