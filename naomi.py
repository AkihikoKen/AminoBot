### Bot Amino Naomi version 0.6 by Akihiko Ken 
import amino
import random
import datetime
from gtts import gTTS
import nekos
import requests
import os

client = amino.Client()
client.login(email="secret", password="secret") #вводим пароль и почту от аккаунта бота
sub_client = amino.SubClient(comId='secret', profile=client.profile) #вместо "id" введите айди сообщества, в котором будет работать чат
ban = 0
tim = 1
hm = [0]
av = []
nom = 0
ANTI_SPAM = {}


def on_message(data):
	global ban
	global tim
	global nom
	userid = data.message.author.userId
	chatId = data.message.chatId
	nickname = data.message.author.nickname
	content = data.message.content
	message_time = str(data.message.createdTime[11:19])
	id = data.message.messageId

	def hentai(a):
		url = nekos.img(str(a))
		response = requests.get(url, stream=True)
		name = url.split('/')[-1]
		file = open(name, 'bw') #Бинарный режим, изображение передається байтами
		for chunk in response.iter_content(4096): # Записываем в файл по блочно данные
			file.write(chunk)
		with open(name, "rb") as file:
			sub_client.send_message(chatId=chatId, file=file, fileType="image")
		os.remove(str(name))

	print(f"{nickname}: {content}: {chatId} : {ban}: {data.message.type}") # вывод в консоль сообщений и автора этих сообщений
	lis = ['Думаю, да', 'Думаю что нет']
	
	content = str(content).split(" ")
	if content[0][0] == "!" and content[0][1:].lower() == "инфа":
		sub_client.send_message(message="Привет! Меня зовут Наоми. Вот мои команды:", chatId=chatId)
	if content[0][0] == "?":
		sub_client.send_message(message=str(random.choice(lis)), chatId=chatId, replyTo=id)
	if content[0][0] == "!" and content[0][1:].lower() == "love":
		sub_client.send_message(message=(f"Вероятность любви между {content[1]} и {content[3]} равна {random.randint(0,100)}%"), chatId=chatId, replyTo=id)
	if content[0][0] == "!" and content[0][1:].lower() == "гс":
		myobj = gTTS(text=data.message.content[4:], lang='ru', slow=False)
		myobj.save("gs.mp3")
		with open("gs.mp3", "rb") as file:
			sub_client.send_message(chatId=chatId, file=file, fileType="audio")
	if content[0][0] == "!" and content[0][1:].lower() == "on":
		tim = -tim
	if content[0][0] == "!" and content[0][1:].lower() == "хентыч":
		if content[1] == "юри":
			hentai("yuri")
		if content[1] == "ножки":
			hentai("feet")
		if content[1] == "трап":
			hentai("trap")
		if content[1] == "тить":
			hentai("tits")
		if content[1] == "эротиш":
			hentai("ero")

	##################################Защита чата##################################################
	global nazvan
	global opisan
	global fonsss

	if content[0][0] == "!":
		if content[0][1:].lower() == "save":
			nazvan = sub_client.get_chat_thread(chatId=data.message.chatId).title
			opisan = sub_client.get_chat_thread(chatId=data.message.chatId).content
			fonsss = sub_client.get_chat_thread(chatId=data.message.chatId).backgroundImage
			sub_client.send_message(message='Усё', chatId=data.message.chatId)
		if content[0][1:].lower() == "go":
			sub_client.edit_chat(chatId=data.message.chatId, title=str(nazvan), content=str(opisan))
			try:
				sub_client.edit_chat(chatId=data.message.chatId, backgroundImage=str(fonsss))
			except:
				sub_client.send_message(message='Восстановление прошло успешно!', chatId=data.message.chatId)
		if content[0][1:].lower() == "a" and sub_client.get_chat_thread(chatId).author.userId:
			sub_client.invite_to_chat(userId=str(client.get_from_code(str(content[1][:])).objectId), chatId=chatId)
			nom = 1

	 if ANTI_SPAM.get(userid) is None:
               ANTI_SPAM[userid] = {"warns": 1, "last_time": message_time}
         else:
               now = datetime.datetime.now(tz=pytz.timezone("Europe/London"))
               last_message = str(ANTI_SPAM[userid]["last_time"]).split(":")
               difference = datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second) - datetime.timedelta(hours=int(last_message[0]), minutes=int(last_message[1]), seconds=int(last_message[2]))
               if difference.seconds <= 1:
                   ANTI_SPAM[userid]["last_time"] = message_time
                   ANTI_SPAM[userid]["warns"] += 1
                   if ANTI_SPAM[userid]["warns"] >= 3:
                       ANTI_SPAM[userid]["warns"] = 1
                       ANTI_SPAM[userid]["last_time"] = message_time
                       sub_client.kick(userId=userid, chatId=chatId)
               else:
                   ANTI_SPAM[userid]["warns"] = 1
                   ANTI_SPAM[userid]["last_time"] = message_time

	if data.message.content != None and data.message.type in [1, 50, 58, 57, 59, 100, 101, 102, 103, 104, 105, 106, 107, 109, 110, 113, 114, 115, 116, 124, 125, 126]:
		sub_client.send_message(message='Рейдеры пошлены нахуй11!', chatId=data.message.chatId)
		sub_client.kick(userId=data.message.author.userId, chatId=data.message.chatId, allowRejoin = True)
	if data.message.type == 101 and nom == 0 and data.message.content == None:
		sub_client.send_message(message='Рейдеры пошлены нахуй!', chatId=data.message.chatId)
		sub_client.kick(userId=data.message.author.userId, chatId=data.message.chatId, allowRejoin = True)
		nom = 0
methods = []
for x in client.callbacks.chat_methods:
	methods.append(client.callbacks.event(client.callbacks.chat_methods[x].__name__)(on_message))
