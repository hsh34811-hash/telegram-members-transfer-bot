# =============================================
# Developer : ✘ 𝙍𝘼𝙑𝙀𝙉
# Telegram  : @P_X_24
# =============================================

from telethon.sync import TelegramClient
from telethon import events, Button
import json
import configparser
import subprocess
import telethon
import os, sys
import re
from database import *
from texts import *

welcome            = "أهلا وسهلا عزيزي المشرف في لوحة التحكم\n\nلبدء عملية نقل عادية ارسل /copy\n\nلبدء عملية نقل متطورة ( للجروبات المقفولة ) ارسل /MovePro\n\n\nللفحص وعرض عدد الحسابات /check"
to_cancle           = "\nللإلغاء ارسل /cancle"
send_f_url          = "قم بإرسال الرابط الخاص أو العام للمجموعة التي سيتم نقل الأعضاء منها\nارسل رابط كالتالي\nhttps://t.me/example"
move_is_busy   = "هناك عملية نقل حالياً\nلإلغائها ارسل /stop_all"
send_t_url          = "✅ تم حفظ مجموعة الإضافة كالتالي\n++URL++\nقم بإرسال الرابط الخاص أو العام للمجموعة التي سيتم نقل الأعضاء إليها\nارسل رابط كالتالي\nhttps://t.me/example"
try_send_url       = "خطأ\nهذا ليس رابطا لجروب تيليجرام\nارسل رابط كالتالي\nhttps://t.me/example"
send_count        = "✅ تم حفظ مجموعة المضافين كالتالي\n++URL++\nقم بإرسال عدد الأعضاء الذي سيتم نقلهم من ++FROM++ إلى ++TO++\n\nارسل أعدادا فقط ، كالتالي\n20"
try_send_int       = "خطأ\nهذا ليس عددا صحيحا\nارسل عدد كالتالي\n22"
send_timer         = "✅ تم حفظ عدد المضافين كالتالي\n++COUNT++\nسيتم نقل ++COUNT++ من ++FROM++ إلى ++TO++\nارسل الوقت الفاصل بين كل عملية إضافة ( بالثانية ما بين 1 و 59 ) كالتالي\n5"
data_is_saved   = "✅ تم حفظ البيانات كالتالي\nسيتم نقل ++COUNT++ عضو من المجموعة ++FROM++ إلى المجموعة ++TO++ في غضون ++TIME++ ثانية\nجار الإنضمام إلى مجموعة الإضافة....."
cancled               = "تم الإلغاء"
no_cancled        = " لا يوجد عملية لإلغائها"
checking             = " جار فحص ++COUNT++ حسابا\n يرجى التحلي بالصبر ... يمكنك رؤية العمليات مباشرة عبر الرسالة التالية"
send_sup_url     = " قم بإرسال رابط القناة أو المجموعة التي سيتم ضخ الأعضاء إليها......"
send_sup_count = " قم بإرسال عدد الأعضاء الذين سيتم ضخهم إلى ++URL++"


config = configparser.ConfigParser()
config.read("jello.ini")

THE_SESSIONS = os.listdir('sessions')
cSessions           = len(THE_SESSIONS)

api_id       = config['owner']['id']
api_hash = config['owner']['hash']
client        = telethon.TelegramClient('center', api_id, api_hash)

token = config['API_KEYs']['mover']
botID  =  int(token.split(':')[0])
admin = config['owner']['admin']


bt_start     = [
		[
				Button.inline(buttonsAdder['MoveM'],'MoveM')
		],
		[
				Button.inline(buttonsAdder['JoinM'],'JoinM'),
				Button.inline(buttonsAdder['AddViews'],'AddViews')
		],
		[
				Button.inline(buttonsAdder['CheckAccounts'],'CheckAccounts'),
				Button.inline(extraButtons['Leave'],'Leave')
		],
]

bt_cancle    = [
		[
				Button.inline(extraButtons['Cancle'],'Cancle')
		],
]

bt_select      = [
		[
				Button.inline(extraButtons['MoveNormal'],'MoveNormal'),
				Button.inline(extraButtons['MovePro'],'MovePro')
		],
		[
				Button.inline(extraButtons['Back'],'Back')
		]
]

bt_back = [
		[
				Button.inline(extraButtons['Back'],'Back')
		]
]


client.start(bot_token=token)
client.connect()

@client.on(events.CallbackQuery())
async def callback(event):
	try:
		chat     = event.original_update.peer.user_id
		fData    = event.data
		data      = fData.decode("utf-8")
		f_data   = data.split('_')
	except:
		data       = False
	from_id          = str(event.sender_id)
	chat_id           = event.chat_id

	status       = get(from_id,'status','database/mover.json')

	if data == 'MoveM':
		await event.edit(AdderTexts['selectMoveMode'],parse_mode='md',buttons=bt_select)
		return

	if data == 'Back':
		await event.edit(textsStart,buttons=bt_start,parse_mode='md')
		return

	if data == 'MoveNormal' or data == 'MovePro':
		if status is not False:
			await event.edit(move_is_busy,parse_mode='md',buttons=bt_start)
		else:
			await event.edit(AdderTexts['sendURLfrom'],buttons=bt_cancle,parse_mode='md')
			set(from_id,'status','move','database/mover.json')
			set(from_id,'ModeMove',data,'database/mover.json')
		return

	if data == 'Cancle':
		await event.edit(textsStart,buttons=bt_start,parse_mode='md')
		delete(from_id,None,'database/mover.json')
		return

	if data == 'CheckAccounts':
		subprocess.Popen(["python3", "control.py", "check",from_id])
		await event.edit(checking.replace('++COUNT++',str(cSessions)),parse_mode='md',buttons=bt_back)
		return

	if data == 'JoinM':
		if status is not False:
			await event.edit(ExtraTexts['serverIsBusy'],parse_mode='md',buttons=bt_cancle)
		else:
			await event.edit(ExtraTexts['supportCHGP'],parse_mode='md',buttons=bt_cancle)
			set(from_id,'status','support','database/mover.json')
		return

	if f_data[0] == 'StartMove':
		OPid        = f_data[1]
		subprocess.Popen(["python3", "control.py", "start", OPid])
		await event.edit(ExtraTexts['StartedMove'],buttons=bt_back,parse_mode='md')
		return

	if f_data[0] == 'StopMove':
		OPid        = f_data[1]
		delete(OPid,None,'database/users.json')
		return

	if data == 'Leave':
		await event.edit(ExtraTexts['Leave'],buttons=bt_cancle,parse_mode='md')
		set(from_id,'status','leave','database/mover.json')
		return

	if data == 'AddViews':
		await event.edit(ExtraTexts['ViewURL'],buttons=bt_cancle,parse_mode='md')
		set(from_id,'status','viewUrl','database/mover.json')
		return

@client.on(events.NewMessage())
async def main(event):
	chattt = await event.get_chat()
	if chattt.__class__.__name__ != 'User':
		return
	try:
		b = event.message.peer_id.channel_id
		b = f"-100{b}"
	except:
		pass

	text                 = event.raw_text
	message_id  = event.message.id
	from_id          = str(event.sender_id)
	chat_id           = event.chat_id

	if from_id == botID:
		return

	if from_id not in admin:
		return

	status       = get(from_id,'status','database/mover.json')
	FROM       = get(from_id,'from','database/mover.json')
	TO             = get(from_id,'to','database/mover.json')
	COUNT    = get(from_id,'count','database/mover.json')
	TIMER      = get(from_id,'timer','database/mover.json')
	MMove     = get(from_id,'ModeMove','database/mover.json')

	if text == '/start':
		await event.reply(textsStart,buttons=bt_start,parse_mode='md')
		return
	if text == '/cancle':
		if status is not False:
			delete(from_id,None,'database/mover.json')
			await event.reply(cancled)
		else:
			await event.reply(no_cancled)
		return
	if text == '/support':
		if status is not False:
			await event.reply(move_is_busy)
		else:
			await event.reply(send_sup_url+to_cancle)
			set(from_id,'status','support','database/mover.json')
		return

	if text == '/check':
		subprocess.Popen(["python3", "control.py", "check",from_id])
		await event.reply(checking.replace('++COUNT++',str(cSessions)))
	if text == '/copy' or text == '/MovePro':
		if status is not False:
			await event.reply(move_is_busy)
		else:
			await event.reply(send_f_url+to_cancle)
			set(from_id,'status','move','database/mover.json')
			set(from_id,'ModeMove',text,'database/mover.json')
		return
	if text and status == 'move':
		test_url    = URLc(text)
		if test_url is not False:
			rp_text     = AdderTexts['sendURLto']
			await event.reply(rp_text,parse_mode='md',buttons=bt_cancle)
			set(from_id,'status','adding_group','database/mover.json')
			set(from_id,'from',text,'database/mover.json')
			return
		else:
			await event.reply(try_send_url,parse_mode='md',buttons=bt_cancle)
	if text and status == 'adding_group':
		test_url    = URLc(text)
		if test_url is not False:
			rp_text   = AdderTexts['sendCount'].replace('++TO++',text).replace('++FROM++',FROM)
			await event.reply(rp_text,parse_mode='md',buttons=bt_cancle)
			set(from_id,'status','select_members','database/mover.json')
			set(from_id,'to',text,'database/mover.json')
		else:
			await event.reply(try_send_url,parse_mode='md',buttons=bt_cancle)
		return
	if text and status == 'select_members':
		regExNu   = re.findall("^[0-9]+",text)
		if len(regExNu) > 0:
			rp_text   = AdderTexts['sendTime']
			await event.reply(rp_text,parse_mode='md',buttons=bt_cancle)
			set(from_id,'status','set_timer','database/mover.json')
			set(from_id,'count',text,'database/mover.json')
		else:
			await event.reply(try_send_int,parse_mode='md',buttons=bt_cancle)
		return
	if text and status == 'set_timer':
		regExNu   = re.findall("^[0-9]+",text)
		if len(regExNu) > 0:
			rp_text   = AdderTexts['Joining'].replace('++TO++',TO).replace('++FROM++',FROM).replace('++COUNT++',str(COUNT)).replace('++TIME++',str(text))
			await event.reply(rp_text,parse_mode='md',buttons=bt_cancle)
			delete(from_id,'status','database/mover.json')
			set(from_id,'timer',text,'database/mover.json')
			opID       = makeKey()

			if MMove == 'MovePro':
				run_script(f"python3 control.py joinPro {opID} {from_id} {FROM} {TO} {COUNT} {text}")
			else:
				run_script(f"python3 control.py join {opID} {from_id} {FROM} {TO} {COUNT} {text}")

			delete(from_id,None,'database/mover.json')
		else:
			await event.reply(try_send_int+to_cancle)
		return

	if text and status == 'viewUrl':
		regExNu   = re.findall("^https?:\/\/t\.me\/([a-zA-Z0-9_]+)\/([0-9]+)",text)
		if len(regExNu) > 0:
			UNC    = '@'+str(regExNu[0][0])
			IDC      = regExNu[0][1]
			set(from_id,'username_view',UNC,'database/mover.json')
			set(from_id,'ID_view',IDC,'database/mover.json')
			set(from_id,'status','viewCount','database/mover.json')
			await event.reply(ExtraTexts['ViewCount'],buttons=bt_cancle,parse_mode='md')
			return

	if text and status == 'viewCount':
		regExNu   = re.findall("^[0-9]+$",text)
		if len(regExNu) > 0:
			ugn    = get(from_id,'username_view','database/mover.json')
			idn      = get(from_id,'ID_view','database/mover.json')
			await event.reply(ExtraTexts['Viewing'],buttons=bt_back,parse_mode='md')
			subprocess.Popen(["python3", "control.py", "View", ugn, idn, text, from_id])
			delete(from_id,None,'database/mover.json')
			return

	if text and status == 'leave':
		regExNu   = re.findall("^\-[0-9]+",text)
		if len(regExNu) > 0:
			await event.reply(ExtraTexts['Leaved'],buttons=bt_back)
			subprocess.Popen(["python3", "control.py", "leaveChat", text])
			delete(from_id,None,'database/mover.json')

	if text and status == 'support':
		test_url    = URLc(text)
		if test_url is not False:
			await event.reply(send_sup_count.replace('++URL++',test_url[1]),parse_mode='md',buttons=bt_cancle)
			set(from_id,'status','select_sup_members','database/mover.json')
			set(from_id,'username_sup',test_url[1],'database/mover.json')
		else:
			await event.reply(try_send_url+to_cancle)
		return
	if text and status == 'select_sup_members':
		regExNu   = re.findall("^[0-9]+",text)
		if len(regExNu) > 0:
			opID       = makeKey()
			set(opID,'owner',from_id,'database/support.json')
			set(opID,'requested_count',text,'database/support.json')
			set(opID,'supported_username',get(from_id,'username_sup','database/mover.json'),'database/support.json')
			run_script(f"python3 control.py joining {opID}")
			delete(from_id,None,'database/mover.json')
		else:
			await event.reply(try_send_int,parse_mode='md',buttons=bt_cancle)
		return


client.run_until_disconnected()
