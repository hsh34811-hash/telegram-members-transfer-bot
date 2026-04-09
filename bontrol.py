from telethon.sync import TelegramClient
import sys, time, os, random
import json
import configparser
import requests
from database import *
from texts import *
import re
import json


opreats    = ['join','check','start','finish','getusers','getuser','joining','joinPro','leaveChat','View'];
opreat      = sys.argv[1];

if opreat not in opreats:
	exit();

doneJoin     = "✅ تم الإنضمام للمجموعة بنجاح ، سيتم بدء النقل حال تخزين الأعضاء....\n⚡️ للمغادرة إرسل /leave_";
doneGet      = "✅ تم تخزين الأعضاء وعددهم ++CC++ عضو ، سيتم بدء النقل حال إرسالك للأمر /move_";
errorsText   = ["لا يوجد أخطاء","لم يستطع أي حساب مضاف أن يقوم بالدخول إلى المجموعة","لا توجد استجابة من الخادم عند محاولة الإنضمام للمجموعات","لم يستطع الحساب تخزين الأعضاء ، قد يرجع سبب ذلك إلى إخفاء أعضاء المجموعة","لا توجد استجابة من الخادم عند محاولة تخزين الأعضاء","لا يوجد لديك حسابات نشطة"];
pleasewait   = "⚡️ لحظات من فضلك .....";
move_over   = "❌ تم إلغاء النقل قبل اكتماله نظرا لنفاذ الحسابات المضافة ";
move_finish = "✅ تم إضافة ++COUNT++ عضو\n♻️»» من المجموعة : ++FROM++\n♻️«« إلى المجموعة : ++TO++\n\n♻️كان العدد المطلوب ++REQUESTED++ ♻️\n♻️بينما كان العدد الفعلي للأعضاء على سيرفراتنا ++LI++\n\n♻️ الوقت بين كل إضافة وإضافة : ++TIME++ ثانية\n\n✅ تم الإضافة بالكامل : ++SUCCESS++ ♻️\n⏳ تبقى ++STAY++ ♻️\n♻️لا يمكن إضافة  ++BLOCK++ ♻️\n\n⚡️ عدد الحسابات المستخدمة بالإضافة حتى الآن : ++ADDER++ من أصل ++TOTAL++\n♻️ عدد الحسابات التي انحظرت مؤقتا أثناء عملية الإضافة : ++BANNED++ حساب";
ADDING_TG = "♻️العدد المطلوب ++REQUESTED++ ♻️\n♻️العدد الفعلي للأعضاء على سيرفراتنا ++LI++\n\n♻️ جار إضافة++COUNT++ عضو\n♻️»» من المجموعة : ++FROM++\n♻️«« إلى المجموعة : ++TO++\n♻️ الوقت بين كل إضافة وإضافة : ++TIME++ ثانية\n\n✅ تم الإضافة حتى الآن : ++SUCCESS++ ♻️\n⏳ تبقى ++STAY++ ♻️\n♻️لا يمكن إضافة  ++BLOCK++ ♻️\n\n⚡️ عدد الحسابات المستخدمة بالإضافة حتى الآن : ++ADDER++ من أصل ++TOTAL++\n♻️ عدد الحسابات التي انحظرت مؤقتا أثناء عملية الإضافة : ++BANNED++\n\n♻️  لإيقاف العملية قم بإرسال /stop_";
TESTER	 = "✅ تم عمل الفحص بنجاح\nإجمالي عدد الحسابات على السيرفر ++ALL++\nعدد الحسابات النشطة ++SUCCESS++\nعدد الحسابات المنتهية ++AUTH++\nعدد الحسابات المحذوفة ++DELETED++\nعدد الحسابات التي تحتوي على مشاكل ++OTHER++";
TESTING	= "⚡️ يتم الفحص الآن........\nإجمالي عدد الحسابات على السيرفر ++ALL++\nعدد الحسابات النشطة ++SUCCESS++\nعدد الحسابات المنتهية ++AUTH++\nعدد الحسابات المحذوفة ++DELETED++\nعدد الحسابات التي تحتوي على مشاكل ++OTHER++";

SUPPORT   = "⚡️ جار الرشق ......\n♻️ يتم تمويل ++CH++ ب ++TOTAL++ عضو\n\n✅ تم التمويل حتى اللحظة ب ++JOINED++ عضو من أصل ++TOTAL++ عضو \nمعرف العملية كالتالي\n++ID++";
SUP_DONE = "✅ تم الرشق بنجاح\n♻️ إلى ++CH++ تم رشق ++JOINED++ عضو بنجاح من أصل ++TOTAL++ عضو";
#opreatID   =


config = configparser.ConfigParser()
config.read("jello.ini")

api_id       = config['owner']['id'];
api_hash = config['owner']['hash'];
token	= config['API_KEYs']['mover'];


#keyboard    = {'inline_keyboard':''}
#oner    = {'text':'Hello', 'callback_data':'Yess'}
#keyboard['inline_keyboard'][0]     = oner;

#keyboard     = {"inline_keyboard":[[{"text":"Hello","callback_data":"yess"},{"text":"Hello 1","callback_data":"yess 1"}]]}

#import json
raw1    = [
	[
		{'text':'Hello', "callback_data": 'NotBad'}
	]
]

#seri = {"inline_keyboard":''}

#seri['inline_keyboard'] = raw1;

#print(json.dumps(seri))

#json.dumps(

def sendMessage(chat_id, text):
	URL	  = "https://api.telegram.org/bot"+token+"/sendmessage"
	PARAMS = {'chat_id': chat_id, 'text': text}
	RGET       = requests.get(url=URL, params=PARAMS);
	return json.loads(RGET.text)

def sendMessageM(chat_id, text):
	URL	  = "https://api.telegram.org/bot"+token+"/sendmessage"
	PARAMS = {'chat_id': chat_id, 'text': text,
	'parse_mode': 'MarkDown'}
	RGET       = requests.get(url=URL, params=PARAMS);
	return json.loads(RGET.text)

def sendInlineKeyboard(chat_id, text, keyboard, parse_mode):
	URL	  = "https://api.telegram.org/bot"+token+"/sendmessage"
	PARAMS = {'chat_id': chat_id, 'text': text,
	'parse_mode': parse_mode,
	'reply_markup': keyboard}
	RGET       = requests.get(url=URL, params=PARAMS);
	return json.loads(RGET.text)

def editInlineKeyboard(chat_id, text, keyboard, parse_mode, message_id):
	URL	  = "https://api.telegram.org/bot"+token+"/editMessageText"
	PARAMS = {'chat_id': chat_id, 'text': text,
	'parse_mode': parse_mode,
	'reply_markup': keyboard,
	'message_id': message_id}
	RGET       = requests.get(url=URL, params=PARAMS);
	return json.loads(RGET.text)


def replyMessage(chat_id, text, message_id):
	URL	  = "https://api.telegram.org/bot"+token+"/sendmessage"
	PARAMS = {'chat_id': chat_id, 'text': text, 'reply_to_message_id': message_id}
	RGET       = requests.get(url=URL, params=PARAMS);
	TG_RESPONSE     = False;
	try:
		TG_RESPONSE   =  json.loads(RGET);
	except:
		return TG_RESPONSE;
	return TG_RESPONSE;

def editMessage(chat_id,text,message_id):
	URL	   = "https://api.telegram.org/bot"+token+"/editMessageText";
	PARAMS  = {'chat_id': chat_id, 'text': text, 'message_id': message_id};
	RGET       = requests.get(url=URL, params=PARAMS);
	TG_RESPONSE     = False;
	try:
		TG_RESPONSE   =  json.loads(RGET);
	except:
		return TG_RESPONSE;
	return TG_RESPONSE;

sessions	      = os.listdir('sessions');
random.shuffle(sessions);
THE_SESSIONS = os.listdir('sessions');
cSessions	   = len(THE_SESSIONS);

#join Ses Owner FromG ToG Count Time

if opreat == 'join' or opreat == 'joinPro':
	opreatID       = sys.argv[2];
	cMembers   = sys.argv[6];
	owner_id      = sys.argv[3];
	urlF		= sys.argv[4];
	urlL		= sys.argv[5];
	time_of	 = sys.argv[7];

	set(opreatID,f"{cMembers}|{owner_id}|{urlF}|{urlL}",None,"database/control.json");
	tryJoin = 0;
	success = 0;
	ERROR_CODE    = 0;
	for session in sessions:
		tryJoin		    += 1;
		RESPONSE	       = False;
		NAME_SESSION     = session.split('.')[0];
		RESPONSE	       = run_script(f"python3 addAccount.py join {NAME_SESSION} {urlF} {urlL}");
		if RESPONSE is not False:
			print("RESPONSE -- "+RESPONSE);
			RESULT      = str(RESPONSE).split("\n");
			if 'true' in RESULT:
				if RESULT[0] == 'true':
					joinfID     = RESULT[1];
					joinlID      = RESULT[2];
					success += 1;
				else:
					joinfID     = RESULT[2];
					joinlID      = RESULT[3];
				set(opreatID,'to_group_id',str(joinlID),"database/users.json");
				set(opreatID,f"{NAME_SESSION}|{joinfID}|{joinlID}",None,"database/leave.json");
				Texo      = ExtraTexts['Storing'].replace('++FROM++',str(joinfID)).replace('++TO++',str(joinlID));
				sendMessageM(owner_id,Texo);
				#sendMessage(owner_id,doneJoin+opreatID);
				print('Joined');
			else:
				ERROR_CODE    = 1;
				continue
		else:
			ERROR_CODE    = 2;
			continue
		if opreat == 'join':
			RESPONSE      = run_script(f"python3 addAccount.py getusers {NAME_SESSION} {joinfID} {joinlID} {opreatID}");
		else :
			RESPONSE      = run_script(f"python3 addAccount.py MovePro {NAME_SESSION} {joinfID} {joinlID} {cMembers} {opreatID}");
		if RESPONSE is not False:
			RESULT      = str(RESPONSE).split("\n");
			if 'true' in RESULT:
				URL_f     = URLc(urlF)[1];
				URL_l     = URLc(urlL)[1];
				
				if opreat == 'join':
					allMembers = RESULT[1];
				else :
					RESULT.reverse()
					allMembers = RESULT[1];
				
				set(opreatID,'users',allMembers,"database/users.json");
				set(opreatID,'time',time_of,"database/users.json");
				set(opreatID,'count',cMembers,"database/users.json");
				set(opreatID,'owner',str(owner_id),"database/users.json");
				set(opreatID,'from_group_link',URL_f,"database/users.json");
				set(opreatID,'to_group_link',URL_l,"database/users.json");
				tex		 = ExtraTexts['MembersStored'].replace('++C++',str(len(str(allMembers).split(','))));
				#sendMessage(owner_id,tex+opreatID);
				#sendMessage(owner_id,doneJoin+opreatID);
				#print('agroooooo');
				buttonHere   = [
					[
						{'text':extraButtons['Start'],'callback_data':f"StartMove_{opreatID}"}
					]
				]
				keyboard    = json.dumps({"inline_keyboard":buttonHere});
				
				sendInlineKeyboard(owner_id,tex,keyboard,'MarkDown');
				
				#sendMessage(owner_id,tex+opreatID);
				break;
			else:
				ERROR_CODE    = 3;
		else:
			ERROR_CODE    = 4;

	if cSessions <= 0:
		ERROR_CODE    = 5;

	if ERROR_CODE != 0:
		HRT       = errorsText[ERROR_CODE];
		sendMessage(owner_id,HRT);

def tryJoins(SS,ID,GID,f=0,e=0,newi=0):
	if SS >= cSessions:
		print ("Finishing ----");
		return ['ERROR','finish',f,e];

	rest	 = get(opreatID,'to_group_id','database/users.json');
	if newi != 0:
		newir = 0;
		reest	 = get(opreatID,'to_group_link','database/users.json');
		rees2	= get(opreatID,'from_group_link','database/users.json');
		rdf	     = reest.replace('@','https://t.me/');
		rdf2	  = rees2.replace('@','https://t.me/');
		print("RRRT ++ "+run_script(f"python3 addAccount.py join {THE_SESSIONS[SS]} {rdf} {rdf2}")+"////");
	else:
		newir = 1;
	ADDING     = run_script(f"python3 addAccount.py adduser {THE_SESSIONS[SS]} {rest} {ID}").split("\n");
	print(f"{THE_SESSIONS[SS]} {rest} {ID}");
	print(f"TT++{ADDING}=");
	CONTINUE_AI  = ['[400 USER_ALREADY_PARTICIPANT]','[400 CHAT_ADMIN_REQUIRED]','[400 PEER_ID_INVALID]','[400 USER_KICKED]','[400 USERNAME_NOT_OCCUPIED]','[400 USERNAME_INVALID]']
	if ADDING[0] == 'true':
		return ['SUCCESS',SS,f,e,newir];
	elif ADDING[0] == 'flood':
		return tryJoins(SS+1,ID,GID,f+1,e,1);
	elif ADDING[0] == 'continue':
		return ['BLOCK',SS,f,e+1];
	elif ADDING[0] == 'floodANDcontinue':
		return ['BLOCK',SS+1,f,e+1];
	elif ADDING[0] == 'deleted':
		return tryJoins(SS+1,ID,GID,f,e+1,1);
	#elif ADDING[0] == 'continues':

		#RESPONSE      = str(ADDING[0]).replace('Telegram says: ', '').split(' - ')[0];
	else:
		RESPONSE      = re.findall("(\[[a-zA-Z0-9\s\_]+\])",ADDING[0])[0];
		if RESPONSE in CONTINUE_AI:
			return ['BLOCK',SS,f,e+1];
		else :
			##sendMessage(owner_id,ADDING[0]+"$$"+RESPONSE);
			return tryJoins(SS+1,ID,GID,f+1,e+1,1);


if opreat == 'joining':
	opreatID       = sys.argv[2];
	try :
		owner_id     = get(opreatID,'owner','database/support.json');
		requested    = int(get(opreatID,'requested_count','database/support.json'));
		user_name  = get(opreatID,'supported_username','database/support.json');
	except :
		pass
	#sendMessage(owner_id,pleasewait);
	
	SUCCESS     = 0;
	REQUESTED     = requested;
	if requested >= cSessions:
		REQUESTED   = cSessions;
	
	
	EM_ID	 = sendMessage(owner_id,pleasewait);
	try:
		M_ID = EM_ID['result']['message_id']
	except:
		M_ID = 4;
	LOOPS   = 0;
	IDU          = 'False';
	while True:
		LOOPS   += 1;
		
		if LOOPS > cSessions or SUCCESS >= REQUESTED:
			TEXT      = SUP_DONE.replace('++CH++',str(user_name)).replace('++JOINED++',str(SUCCESS)).replace('++TOTAL++',str(REQUESTED));
			sendMessage(owner_id,TEXT);
			exit();
			break;
		
		try :
			JOINED_SESSIONS    = get(IDU,'joined').split(',');
		except :
			JOINED_SESSIONS     = [];
		
		SESSION_AT  = sessions[LOOPS - 1].split('.')[0];
		if SESSION_AT in JOINED_SESSIONS:
			continue;
		
		JOIN                = run_script(f"python3 addAccount.py joining {SESSION_AT} {user_name}");
		try:
			pales      = re.findall("\[\'true\'\,\s\-(\d+)",JOIN);
			if len(pales) > 0:
				IDU      = '-'+str(pales[0]);
				SUCCESS     += 1;
				ERROR = "\n ___TRUE____";
				set(IDU,'joined',get(IDU,'joined')+SESSION_AT+',');
			else:
				ERROR = f"\n {JOIN}";
		except Exception as Jello:
			ERROR = f"\n {Jello}";
		
		TEXT      = SUPPORT.replace('++CH++',user_name).replace('++JOINED++',str(SUCCESS)).replace('++TOTAL++',str(REQUESTED)).replace('++ID++',IDU);
		editMessage(owner_id,TEXT+ERROR,M_ID);
		
		
		
# start ID
if opreat == 'start':
	#cMembers   = sys.argv[5];
	#owner_id      = sys.argv[3];
	#urlF		= sys.argv[4];
	opreatID       = sys.argv[2]
	#time_of	 = sys.argv[7];

	SUCCESS   = 0;
	BANED	= 0;
	CLOSED      = 0;
	STAY	    = 0;
	BLOCK	 = 0;
	USED	    = 1;

	SESSIONS_ALLOW  = cSessions;
	LIST_USERS	      = get(opreatID,'users','database/users.json').split(',');
	FROM_GROUP	  = get(opreatID,'from_group_link','database/users.json');
	TO_GROUP		= get(opreatID,'to_group_link','database/users.json');
	GROUP_ID		 = get(opreatID,'to_group_id','database/users.json');
	TIME_ADD		 = get(opreatID,'time','database/users.json');

	cMembers	  = get(opreatID,'count','database/users.json');
	owner_id	     = get(opreatID,'owner','database/users.json');


	EM_ID	 = sendMessage(owner_id,pleasewait);
	try:
		M_ID = EM_ID['result']['message_id']
	except:
		M_ID = 4;

	stored       = len(LIST_USERS);

	if stored >=  int(cMembers):
		requested    = cMembers;
	else:
		requested     = stored;


	counter   = 0;
	ses_key   = 0;
	NN = 1;
	xxdf    = 0;
	while True:
		
		if xxdf >= int(get(opreatID,'time','database/users.json')):
			TEXT      = AdderTexts['MovingStopped'].replace('++COUNT++',str(stored)).replace('++REQ++',str(cMembers)).replace('++STATUS++',str(TIME_ADD));
			TEXT      = TEXT.replace('++FROM++',FROM_GROUP).replace('++TO++',TO_GROUP).replace('++TIME++',str(TIME_ADD));
			TEXT      = TEXT.replace('++ADDED++',str(SUCCESS)).replace('++DASH++',str(STAY)).replace('++DONT++',str(BLOCK));
			TEXT      = TEXT.replace('++USED++',str(USED)).replace('++ALL++',str(SESSIONS_ALLOW)).replace('++BTIME++',str(BANED));
			buttonHere   = [
				[
					{'text':extraButtons['Back'],'callback_data':"Back"}
				]
			]
			keyboard    = json.dumps({"inline_keyboard":buttonHere});
				
			editInlineKeyboard(owner_id,TEXT,keyboard,'MarkDown',M_ID);
			break;
		if get(opreatID,'time','database/users.json') == False :
			TEXT      = AdderTexts['MovingStopped'].replace('++COUNT++',str(stored)).replace('++REQ++',str(cMembers)).replace('++STATUS++',str(TIME_ADD));
			TEXT      = TEXT.replace('++FROM++',FROM_GROUP).replace('++TO++',TO_GROUP).replace('++TIME++',str(TIME_ADD));
			TEXT      = TEXT.replace('++ADDED++',str(SUCCESS)).replace('++DASH++',str(STAY)).replace('++DONT++',str(BLOCK));
			TEXT      = TEXT.replace('++USED++',str(USED)).replace('++ALL++',str(SESSIONS_ALLOW)).replace('++BTIME++',str(BANED));
			buttonHere   = [
				[
					{'text':extraButtons['Back'],'callback_data':"Back"}
				]
			]
			keyboard    = json.dumps({"inline_keyboard":buttonHere});
				
			editInlineKeyboard(owner_id,TEXT,keyboard,'MarkDown',M_ID);
			break;
		

		TEXT      = AdderTexts['Moving'].replace('++COUNT++',str(stored)).replace('++REQ++',str(cMembers)).replace('++STATUS++',str(TIME_ADD));
		TEXT      = TEXT.replace('++FROM++',FROM_GROUP).replace('++TO++',TO_GROUP).replace('++TIME++',str(TIME_ADD));
		TEXT      = TEXT.replace('++ADDED++',str(SUCCESS)).replace('++DASH++',str(STAY)).replace('++DONT++',str(BLOCK));
		TEXT      = TEXT.replace('++USED++',str(USED)).replace('++ALL++',str(SESSIONS_ALLOW)).replace('++BTIME++',str(BANED));
		#TEXT   += opreatID;
		
		buttonHere   = [
			[
				{'text':extraButtons['Stop'],'callback_data':f"StopMove_{opreatID}"}
			]
		]
		keyboard    = json.dumps({"inline_keyboard":buttonHere});
				
		editInlineKeyboard(owner_id,TEXT,keyboard,'MarkDown',M_ID);

		#editMessage(owner_id,TEXT,M_ID);
		counter    += 1;

		if SUCCESS >= int(cMembers):
			replyMessage(owner_id,"Done ✅",M_ID);
			exit();
			break;
			#return
		ADDING       = tryJoins(ses_key,LIST_USERS[counter-1],GROUP_ID,0,0,1);
		if ADDING[0] == 'SUCCESS':
			SUCCESS     += 1;
			ses_key	  = ADDING[1];
			BANED	  += ADDING[2];
			CLOSED	+= ADDING[3];
		if ADDING[0] == 'BLOCK':
			BLOCK       += 1;
			ses_key	  = ADDING[1];
			BANED	  += ADDING[2];
			CLOSED	+= ADDING[3];
			USED	       += ADDING[2];
		if ADDING[0] == 'ERROR':
			ses_key	  = ADDING[1];
			replyMessage(owner_id,move_over,M_ID);
			delete(opreatID,None,'database/users.json');
			exit();
			break;
			#return
		STAY      = int(requested) - int(SUCCESS);

		TEXT      = AdderTexts['Moving'].replace('++COUNT++',str(stored)).replace('++REQ++',str(cMembers)).replace('++STATUS++',str(TIME_ADD));
		TEXT      = TEXT.replace('++FROM++',FROM_GROUP).replace('++TO++',TO_GROUP).replace('++TIME++',str(TIME_ADD));
		TEXT      = TEXT.replace('++ADDED++',str(SUCCESS)).replace('++DASH++',str(STAY)).replace('++DONT++',str(BLOCK));
		TEXT      = TEXT.replace('++USED++',str(USED)).replace('++ALL++',str(SESSIONS_ALLOW)).replace('++BTIME++',str(BANED));
		#TEXT   += opreatID;
		#sendMessage(owner_id,TEXT);


		if SUCCESS >= int(requested):
			TEXT      = AdderTexts['Moving'].replace('++COUNT++',str(stored)).replace('++REQ++',str(cMembers)).replace('++STATUS++',str(TIME_ADD));
			TEXT      = TEXT.replace('++FROM++',FROM_GROUP).replace('++TO++',TO_GROUP).replace('++TIME++',str(TIME_ADD));
			TEXT      = TEXT.replace('++ADDED++',str(SUCCESS)).replace('++DASH++',str(STAY)).replace('++DONT++',str(BLOCK));
			TEXT      = TEXT.replace('++USED++',str(USED)).replace('++ALL++',str(SESSIONS_ALLOW)).replace('++BTIME++',str(BANED));
			buttonHere   = [
				[
					{'text':extraButtons['Stop'],'callback_data':f"StopMove_{opreatID}"}
				]
			]
			keyboard    = json.dumps({"inline_keyboard":buttonHere});
				
			editInlineKeyboard(owner_id,TEXT,keyboard,'MarkDown',M_ID);
			replyMessage(owner_id,"Done ✅",M_ID);
			delete(opreatID,None,'database/users.json');
			exit();
			break;

		if int(TIME_ADD) > 0:
			time.sleep(int(TIME_ADD));


			#for willAdd in LIST_USERS:
				#ADDING     = run_script(f"python3 addAccount.py adduser {THE_SESSIONS[ses_key]} {GROUP_ID} {willAdd}").split("\n");
				#if ADDING[0] == 'Flood':
					#while True:
						#ses_key   += 1;
						#ADDING     = run_script(f"python3 addAccount.py adduser {THE_SESSIONS[ses_key]} {GROUP_ID} (willAdd}").split("\n");
						#if ADDING[0] == 'True':
							#SUCCESS += 1;

if opreat == 'View':
	UN        = str(sys.argv[2]);
	IDM       = int(sys.argv[3]);
	CNT       = int(sys.argv[4]);
	zero       = 0;
	for session in sessions:
		if zero >= CNT :
			break;
		zero    += 1;
		NAME_SESSION     = session.split('.')[0];
		RESPONSE	       = run_script(f"python3 addAccount.py View {NAME_SESSION} {UN} {IDM}");

if opreat == 'leaveChat':
	IDleave     = int(sys.argv[2]);
	for session in sessions:
		NAME_SESSION     = session.split('.')[0];
		RESPONSE	       = run_script(f"python3 addAccount.py left {NAME_SESSION} {IDleave} {IDleave}");


if opreat == 'check':
	owner_id  = int(sys.argv[2]);
	SUCCESS = 0;
	DELETED = 0;
	AUTH	= 0;
	OTHER      = 0;
	STATUS     = False;
	ALL	     = 0;
	EM_EID	 = sendMessage(owner_id,'Waiiiiit');
	try:
		M_ID = EM_EID['result']['message_id']
	except:
		M_ID = 4;
	for session in sessions:
		ALL			  += 1;
		RESPONSE	       = False;
		NAME_SESSION     = session.split('.')[0];
		RESPONSE	       = run_script(f"python3 addAccount.py check {NAME_SESSION}");
		if RESPONSE is not False:
			STATUS     = True;
			RESULT     = RESPONSE.split("\n");
			if 'true' in RESULT:
				SUCCESS   += 1;
			elif 'false' in RESULT:
				AUTH	  += 1;
			elif 'deleted' in RESULT:
				DELETED     += 1;
			else:
				OTHER	  += 1;
		DSR      = TESTING.replace('++ALL++',str(ALL)).replace('++SUCCESS++',str(SUCCESS)).replace('++AUTH++',str(AUTH)).replace('++DELETED',str(DELETED)).replace('++OTHER++',str(OTHER));
		editMessage(owner_id,DSR,M_ID);
	DSS      = TESTER.replace('++ALL++',str(ALL)).replace('++SUCCESS++',str(SUCCESS)).replace('++AUTH++',str(AUTH)).replace('++DELETED',str(DELETED)).replace('++OTHER++',str(OTHER));
	sendMessage(owner_id,DSS);



