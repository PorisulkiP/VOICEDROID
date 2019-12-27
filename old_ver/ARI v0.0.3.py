# Голосовой помощник Ариэль v0.0.3
import speech_recognition as sr
import os, pyaudio, sys, webbrowser, youtube_dl, pyttsx3, fuzzywuzzy, datetime, winsound

speak_engine = pyttsx3.init()

#Определение рабочего микрофона на устройстве
"""
for index, name in enumerate(sr.Microphone.list_microphone_names()):
	print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
"""

#Если вы богатый и у вас есть подписка на Yandex SpeechKit
"""
URL = 'https://tts.voicetech.yandex.net/generate?text=' + f + '&format=wav&lang=ru-RU&speaker=ermil&key=b1gs5er9aprbc9suf92h&speed=1&emotion=good'
response=requests.get(URL)
if response.status_code==200:
	with open(speech_file_name,'wb') as file:
		file.write(response.content)
"""
#Для любителей pocketsphinx
"""
from pocketsphinx import LiveSpeech

speech = LiveSpeech(
	verbose=False,
	sampling_rate=8000,
	buffer_size=2048,
	no_search=False,
	full_utt=False,
	hmm=os.path.join(model_path, 'zero_ru.cd_cont_4000'),
	lm=os.path.join(model_path, 'ru.lm'),
	dic=os.path.join(model_path, 'ru.dic')
)
"""
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
radio_list = {
	'name1' : 'радио дача', 'url1' : 'http://listen10.vdfm.ru:8000/dacha',
	'name2' : 'русское радио', 'url2'  : 'http://play.russianradio.eu/stream',
	'name3' : 'электронная музыка', 'url3'  : 'http://radio-electron.ru:8000/128',
	'name4' : 'эхо москвы', 'url4'  : 'http://ice912.echo.msk.ru:9120/24.aac',
	'name5' : 'классическая музыка', 'url5'  : 'http://stream.srg-ssr.ch/m/rsc_de/mp3_128',
	'name6' : 'наше радио', 'url6'  : 'http://nashe128.streamr.ru'
}

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
		# pyaudio.Stream.read(r'C:\Users\Алексей\Desktop\project\Аудио\Untitled 2.wav')
		# os.startfile(r'C:\Users\Алексей\Desktop\project\Аудио\Untitled 2.wav')
		speech('Presentation.wav')
		sys.exit(0)
	if say.endswith(radio):

		talk("Выберите радио: ")
		
		say = command()

		# for i in radio_list:
		# 	if radio_list[i][say] == radio_list:
		# 		print(radio_list[i]['url'])
		# 		url = (radio_list[i]['url'])
		# 		webbrowser.open(url, new=0, autoraise=True)
		# 	else:
		# 		talk('нет такого радио')
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

# Читаем
# f = open('То, что нужно сказать.txt')
# a = f.read()
# talk(a)

while True:
	makeSomething(say)

# def callback(recognizer, audio):
#     try:
#         voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
#         print("Распознано: " + voice)
   
#         if voice.startswith(opts["alias"]):
#             # обращение к Ариэль
#             cmd = voice
 
#             for x in opts['alias']:
#                 cmd = cmd.replace(x, "").strip()
		   
#             for x in opts['tbr']:
#                 cmd = cmd.replace(x, "").strip()
		   
#             # распознаем и выполняем команду
#             cmd = recognize_cmd(cmd)
#             execute_cmd(cmd['cmd'])
 
#     except sr.UnknownValueError:
#         print("Голос не распознан!")
#     except sr.RequestError as e:
#         print("Неизвестная ошибка, проверьте интернет соединение!")
 
# def recognize_cmd(cmd):
#     RC = {'cmd': '', 'percent': 0}
#     for c,v in opts['cmds'].items():
 
#         for x in v:
#             vrt = fuzz.ratio(cmd, x)
#             if vrt > RC['percent']:
#                 RC['cmd'] = c
#                 RC['percent'] = vrt
   
#     return RC
 
# def execute_cmd(cmd): 
#     if cmd == 'ctime':
#         # сказать текущее время
#         now = datetime.datetime.now()
#         speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
   
#     elif cmd == 'radio':
#         # воспроизвести радио
#         speak("Выберите радио: ")
#         say = microphone()
#         print(say)
#         if say == "эхо москвы":
#             url = "http://ice912.echo.msk.ru:9120/24.aac" 
#         webbrowser.open(url, new=0, autoraise=True)
   
#     elif cmd == 'browser':
#         pass
#         # # обратиться к браузеру
#         # speak("")
   
#     else:
#         print('Команда не распознана, повторите!')




# def microphone():
#         # Слушаем микрофоном
#         with m as data:
#             print('Говорите: ')
#             r.adjust_for_ambient_noise(data, duration=1)
#             audio = r.listen(data)
#         # Распознаём речь
#         say = r.recognize_google(audio, language="ru-RU")
#         return say
#     return say