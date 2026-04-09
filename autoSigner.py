from pyrogram import Client
from pyrogram.raw import functions
import sys, time, os, random
import asyncio
import json
import configparser
import requests

from database import *

textBanned          = "عذرا ، هذا الرقم محظور !";
retryAfter             = "عذرا ، محاولات كثيرة يرجى تبديل الرقم أو الإنتظار حتى تتمكن من تسجيل هذا الرقم ";
numberIsFalse    = "عذرا الرقم ليس صحيحا";
numberIsBanned = "عذرا ، الرقم محظور مؤقتا \n قد يرجع سبب ذلك إلى تخمين كود التحقق أو رمز التحقق بخطوتين";
doneApp                = "لقد أرسلنا لك كود التحقق إلى تطبيق تيليجرام على جهازك الآخر ، قم بتفقد آخر الرسائل";
doneSMS               = "تم إرسال كود التحقق في رسالة SMS إلى رقم هاتفك";
doneLogin             = "✅ تم تسجيل الدخول بنجاح بنجاح وتم تسجيل الخروج من كل الأجهزة الأخرى♻️";
errorCode              = "❌ كود التحقق غير صحيح ، قم بإرسال كود التحقق الذي تم إرساله لك وإلا سيتم إلغاء عملية تسجيل الدخول ";
timeOutCode        = "⏰ الكود منتهي الصلاحية ، قم بإرسال كود التحقق الجديد";
sendCodeAuth     = "♻️ هذا الحساب محمي بواسطة المصادقة الثنائية ( التحقق بخطوتين ) ولتسجيل الدخول إليه قم بإرسال كود التحقق بخطوتين ";
errorCodeAuth     = "❌ كود التحقق بخطوتين غير صحيح ، قم بإرسال كود التحقق بخطوتين الذي قمت بوضعه سابقا من الجهاز الآخر";
unknownError      = "❌ حدث خطأ غير معروف!";
timeOutSession  = "⌛ انتهت مهلة جلسة تسجيل الدخول!";
overSession         = "♻️ تم انهاء الجلسة بنجاح ✅";
doneLoginNotOut = "✅ تم تسجيل الدخول \n⌛ لكن لم يتم تسجيل الخروج من بقية الجلسات";

FIRST_NAMES     = ['محمد','علي','أحمد','سالم','سلمان','عبدالرحيم','عبدالله','أواب','مهدي','رحمة','نور','زكريا','أبو بكر','جيلو','حياة','رؤوف','درهم','ميقات','رجب','محرم','عبدالباري','حسن','كنعان','توفيق','سعيد','سهيل','بدر','أبو بدر','أمجد','أكرم','نادر','قاسم','محسن','محمود','إمام','عادل','صلاح','صالح','عبدالرزاق','عبدالعلي','عبدالعظيم','عبدالعليم','عبدالحليم','رياض','مهند','سجاد','سيف','عثمان','خليل','أنطوان','ميسور','شرف','سامي','نوح','سمير','عمر','عمرو','هشام','معد','ممدوح','محبوب','أيوب','مأمون','فارغ','خالد','نعمان','مصلح','ربيع','رمضان','زهراء','ميثاق','رعد','صفاء','نقاء','حليم','كريم','عبدالكريم','موسى','عيسى','هارون','مريم','ناصر','حوت','أمين','بدير','نجم الدين','عزالدين','مهيوب','منصور','فيصل','حسام','أسامة','رقيب','أصيل','راغب','ضياء','قصي','عميد','إيهاب','وهيب','مهيب'];
LAST_NAMES      = ['الخالدي','اليافعي','العراقي','السوري','الشامي','بن رمل','بن محمد','اليمني','المغربي','المصري','العشاري','الحميري','رأفت','باسم','علامة','الحاج','التاج','الشامخ','الرنم','خان','عميد','روؤف','السادس','كمال','البدر','الصقراوي','السروري','باعلوي','باسالم','بلفقيه','المحضار','ساري','صدام','حسين','الهيبة','الهباهبة','العمايرة','الهاشمي','الكنعاني','الصنعاني','الفقير','النرجس','الورش','نافع','الوجيه','سليم','الصنبحي','رأفت','رامي','رائد','رتبة','خبير','الحمصي','زين العابدين','مبارك','الرزيق','الرزين','السامرائي','الكلدي','اليهري','التعزي','عساج','الفهد','فهد','هيثم','الحراني','الصعيدي','البورسعيدي','هشام','رمح','جواس','ثابت','جساس','فضل','السكر','العلوي','القرشي','السعودي','الكويتي','صلالة','الرياضي','قيس','أوس','السرابي','الصحراوي','الجبلي','الحيد','البيرق','العقربي','النوكياوي','الهجام','رئيس','منصدع','عبدالعزيز','عبدالرحمن','المحاسن','ريدان','مراسل','صعيب','عمار','ياسر'];

opreat      = sys.argv[1];

if opreat != 'add':
	exit();

number    = sys.argv[2];
owner_id  = sys.argv[3];

config = configparser.ConfigParser() 
config.read("jello.ini")

api_id       = config['owner']['id'];
api_hash = config['owner']['hash'];
token        = config['API_KEYs']['signer'];
ses            = makeKey();
app            = Client(name=f"sessions/{ses}",api_id=api_id, api_hash=api_hash);
app.connect();


def sendMessage(chat_id, text):
    URL = "https://api.telegram.org/bot"+token+"/sendmessage"
    PARAMS = {'chat_id': chat_id, 'text': text, 'parse_mode': 'markdown'}
    requests.get(url=URL, params=PARAMS)


async def signAccount():
	
	try:
		send   = await app.send_code(phone_number=number);
		trueF   = True;
	except Exception as Errors:
		try:
			os.remove(f"sessions/{ses}.session");
		except:
			pass
		print(Errors);
		
		RESPONSE      = str(Errors).replace('Telegram says: ', '').split(' - ')[0];
		
		if RESPONSE == '[400 PHONE_NUMBER_BANNED]':
			delete(owner_id);
			sendMessage(owner_id,textBanned);
			return
		elif RESPONSE == '[420 FLOOD_WAIT_X]':
			delete(owner_id);
			sendMessage(owner_id,retryAfter);
			return
		elif RESPONSE == '[406 PHONE_NUMBER_INVALID]':
			delete(owner_id);
			sendMessage(owner_id,numberIsFalse);
			return
		elif RESPONSE == '[406 PHONE_PASSWORD_FLOOD]':
			delete(owner_id);
			sendMessage(owner_id,numberIsBanned);
			return
	success   = json.loads(str(send));
	
	if success['_'] == 'SentCode':
		if success['type'] == 'SentCodeType.APP' or success['type'] == 'app':
			METHOD   = 'APP';
			sendMessage(owner_id,doneApp);
		else:
			METHOD         = 'SMS';
			sendMessage(owner_id,doneSMS);
		CODE_HASH   = success['phone_code_hash'];
		set(owner_id,"status","verfiry");
		set(owner_id,"code_hash",CODE_HASH);
		set(owner_id,"method",METHOD);
		time.sleep(5);
		
	counter     = 0;
	while trueF:
		
		status      = get(owner_id,"status");
		code         = get(owner_id,"code");
		counter  += 1;
		
		
		
		if code is False and counter <= 12:
			time.sleep(10);
		
		
		if status == "verfiry" and code is not False and code != '':
			code_hash   = get(owner_id,"code_hash");
			method         = get(owner_id,"method");
			
			if method == 'APP':
				try:
					await app.sign_in(number, code_hash, str(code));
					#try:
						#await app.invoke(functions.auth.ResetAuthorizations(#));
						#sendMessage(owner_id,doneLogin);
					#except:
					sendMessage(owner_id,doneLoginNotOut);
					
					delete(owner_id);
					exit();
					break;
					return
				except Exception as ERROR_DATA:
					RESPONSE      = str(ERROR_DATA).replace('Telegram says: ', '').split(' - ')[0];
					if RESPONSE == '[400 PHONE_CODE_INVALID]':
						sendMessage(owner_id,errorCode);
						delete(owner_id,"code");
					elif RESPONSE == '[400 PHONE_CODE_EXPIRED]':
						sendMessage(owner_id,timeOutCode);
						delete(owner_id,"code");
					elif RESPONSE == '[401 SESSION_PASSWORD_NEEDED]':
						sendMessage(owner_id,sendCodeAuth);
						delete(owner_id,"code");
						set(owner_id,"status","auth");
					else:
						sendMessage(owner_id,sendCodeAuth);
						delete(owner_id);
						os.remove(f"sessions/{ses}.session");
						exit();
						break;
						return
					pass
			elif method == 'SMS':
				try:
					try :
						
						await app.sign_up(phone_number=number, phone_code_hash = code_hash, first_name= random.choice(FIRST_NAMES), last_name = random.choice(LAST_NAMES));
						sendMessage(owner_id,doneLogin);
						delete(owner_id);
						exit();
						break;
						return
					except Exception as hj:
						print(hj);
						
					await app.sign_in(number, code_hash, str(code));
				except Exception as ERROR_DATA:
					print(ERROR_DATA);
					RESPONSE      = str(ERROR_DATA).replace('Telegram says: ', '').split(' - ')[0];
					if RESPONSE == '[400 PHONE_CODE_INVALID]':
						sendMessage(owner_id,errorCode);
						delete(owner_id,"code");
					elif RESPONSE == '[400 PHONE_CODE_EXPIRED]':
						sendMessage(owner_id,timeOutCode);
						delete(owner_id,"code");
					elif RESPONSE == '[401 SESSION_PASSWORD_NEEDED]':
						sendMessage(owner_id,sendCodeAuth);
						delete(owner_id,"code");
						set(owner_id,"status","auth");
					else:
						sendMessage(owner_id,unknownError);
						delete(owner_id);
						os.remove(f"sessions/{ses}.session");
						exit();
						break;
						return
					pass 
			pass
		if status == "auth" and code is not False and code != '':
			try:
				await app.check_password(code);
				sendMessage(owner_id,doneLogin);
				#try:
					#await app.invoke(functions.auth.ResetAuthorizations());
					#sendMessage(owner_id,doneLogin);
				#except:
				sendMessage(owner_id,doneLoginNotOut);
				delete(owner_id);
				set(ses,'password',str(code),'database/passwords.json');
				exit();
				break;
				return
			except Exception as ERROR_AUTH:
				sendMessage(owner_id,errorCodeAuth);
				delete(owner_id,"code");
				print(ERROR_AUTH);
				
		## Check Time Out '___' ##
		if counter > 12:
			sendMessage(owner_id,timeOutSession);
			delete(owner_id);
			await app.disconnect();
			os.remove(f"sessions/{ses}.session");
			exit();
			break;
			return
		time.sleep(10);

asyncio.get_event_loop().run_until_complete(signAccount());

