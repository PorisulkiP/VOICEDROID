# Голосовой помощник Ариэль v0.0.2
import speech_recognition as sr
import os, pyaudio, sys, webbrowser, youtube_dl, pyttsx3, fuzzywuzzy, datetime, winsound

speak_engine = pyttsx3.init()

# Произносим
def talk(text):
	print(text)
	speak_engine.say(text)
	speak_engine.runAndWait()
	speak_engine.stop() 
	return speak_engine
# talk("Если вы намереваетесь начать со мной диалог, то первый шаг за вами...")

def speech(say_some):
	winsound.PlaySound(say_some, winsound.SND_FILENAME)

print("Здравствуйте, я голосовой помощник Ариэль")

speech('Hello.wav')

# настройки
time = ('который час','текущее время','сейчас времени','время')
name = ('как тебя зовут', 'назови своё имя', 'представься')
radio = ('включи музыку','воспроизведи радио','включи радио', 'радио')
what = ('что означает','что значит','что такое')
stop = ('стоп', 'топ', 'stop')
youtube = ('открой браузер','включи ютюб','включи youtube', 'скачай видео с ютюба', "открой youtube","включи браузер")

def command():
	# Включаем микрофон
	r = sr.Recognizer()
	r.energy_threshold = 8000
	r.dynamic_energy_adjustment_damping = 0.15
	r.pause_threshold = 0.5
	m = sr.Microphone(device_index = 1)
	# Слушаем микрофоном
	with m as data:
		print("Говорите, я жду: ")
		speech('Start taking.wav')
		r.adjust_for_ambient_noise(data, duration=1)
		audio = r.listen(data)
	# Распознаём речь
	try:
		say = r.recognize_google(audio, language="ru-RU").lower()
		print("Вы сказали: " + say)
	except sr.UnknownValueError:
		talk("Я вас не поняла")
		say = command()
	return say
	
say = command()

def makeSomething(say):
	print(say)

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
		talk("Выберите радио: ")
		say = command()
		if say.endswith('эхо москвы' or 'москвы' or 'эхо'):
			url = 'http://ice912.echo.msk.ru:9120/24.aac'
			webbrowser.open(url, new=0, autoraise=True)

		if say.endswith('русское радио ' or 'русское'):
			url = 'http://play.russianradio.eu/stream'
			webbrowser.open(url, new=0, autoraise=True)

		if say.endswith('электронная музыка' or 'электронная'):
			url = 'http://radio-electron.ru:8000/128'
			webbrowser.open(url, new=0, autoraise=True)

		if say.endswith('классическая музыка' or 'классическая'):
			url = 'http://stream.srg-ssr.ch/m/rsc_de/mp3_128'
			webbrowser.open(url, new=0, autoraise=True)

		if say.endswith('наше радио' or 'наше'):
			url = 'http://nashe128.streamr.ru'
			webbrowser.open(url, new=0, autoraise=True)

		if say.endswith('радио дача' or 'дача'):
			url = 'http://listen10.vdfm.ru:8000/dacha'
			webbrowser.open(url, new=0, autoraise=True)
		else:
			sys.exit(0)
	if say.startswith(what):
		webbrowser.open('https://yandex.ru/search/?lr=10735&text='+ say[2],new=0, autoraise=True)
		sys.exit(0)
	else:
		winsound.PlaySound('Error 1.wav', winsound.SND_FILENAME)
		sys.exit(0)

# Записываем в файл
f = open('То, что нужно сказать.txt', 'a')

for i in range(1):
	f.write(say + '\n')
f.close()

while True:
	makeSomething(say)
