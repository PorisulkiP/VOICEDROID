# Голосовой помощник Ариэль v0.0.1
import speech_recognition as sr
import os, pyaudio, sys, webbrowser, youtube_dl, pyttsx3, fuzzywuzzy, datetime, winsound

speak_engine = pyttsx3.init()

# Произносим
def talk(text):
	print(text)
	speak_engine.say( text )
	speak_engine.runAndWait()
	speak_engine.stop() 
	return speak_engine
# talk("Если вы намереваетесь начать со мной диалог, то первый шаг за вами...")

def speech(say_some):
	winsound.PlaySound(say_some, winsound.SND_ALIAS)

print("Здравствуйте, я голосовой помощник Ариэль")

speech('Hello.wav')

# настройки

time = ('который час','текущее время','сейчас времени','время')
name =('ари','ариэль','эй, ари','ариэлюшка','ариэлька','эй, ариэль')
tbr = ('скажи','расскажи','покажи','сколько','произнеси', 'открой'),
radio = ('включи музыку','воспроизведи радио','включи радио'),
browser = ('открой браузер','включи ютюб','включи youtube', 'скачай видео с ютюба','')


def command():
	# Включаем микрофон
	r = sr.Recognizer()
	r.energy_threshold = 4000
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
	if say.endswith(time):
		# сказать текущее время
		now = datetime.datetime.now()
		talk("Сейчас " + str(now.hour) + ":" + str(now.minute))
		pass
	if 'открой youtube' in say:
		talk("Уже открываю")
		url = 'https://www.youtube.com'
		webbrowser.open(url)
		pass
	elif 'стоп' or 'топ' or 'stop' or 'top' in say:
		talk("Да, конечно, без проблем")
		sys.exit(0)
	elif 'имя' or 'твоё имя' in say:
		winsound.PlaySound('Untitled 2.wav', winsound.SND_MEMORY)
		talk("Меня зовут Ариэль")
		pass
	elif radio in say:
		talk("Выберите радио: ")
		say = None
		say == True
		print(say)
		if 'эхо москвы' in say:
			webbrowser.open('http://ice912.echo.msk.ru:9120/24.aac', new=0, autoraise=True)
		else:
			sys.exit()
		pass
	else:
		winsound.PlaySound('Error 1.wav', winsound.SND_ALIAS)
		pass

# Записываем в файл
f = open('То, что нужно сказать.txt', 'a')

for i in range(1):
	f.write(say + '\n')
f.close()

while True:
	makeSomething(say)
