from pyrogram import Client
from pyrogram.raw import functions
import sys, time
import asyncio
import json
import configparser
from pyrogram.errors import FloodWait, UserPrivacyRestricted, UserRestricted, PeerFlood, UserNotMutualContact, UserChannelsTooMuch
from database import *

opreat      = sys.argv[1];
opreats    = ['join','left','check','send','getusers','adduser','getUsers','joining','CX','MovePro'];


if opreat not in opreats:
	exit();

ses    = sys.argv[2].split('.')[0];



config = configparser.ConfigParser()
config.read("jello.ini")

api_id       = config['owner']['id'];
api_hash = config['owner']['hash'];

async def Controll():
	try:
		app	  = Client(f"sessions/{ses}",api_id=api_id, api_hash=api_hash);		connect  = await app.connect();

		if opreat == 'check':
			try:
				await app.get_me();
				print('true');
			except:
				print('false');

		await app.get_me();
	except Exception as Errors:
		RESPONSE      = str(Errors).replace('Telegram says: ', '').split(' - ')[0];

		if RESPONSE in ['[401 AUTH_KEY_UNREGISTERED]', '[401 USER_DEACTIVATED]', '[401 USER_DEACTIVATED_BAN]', '[401 SESSION_REVOKED]']:
			try:
				print('deleted');
				os.remove(f"sessions/{ses}.session");
			except:
				pass
		if opreat == 'check':
			print(RESPONSE);
		print('false',Errors);
		connect   = False;
		#print(ses);
		return
	if not connect:
		print('NO_CONNECTED');
		return

	try:
		await app.invoke(functions.account.UpdateStatus(
			offline=False
		));
	except:
		pass

	if opreat == 'CX':
		
		UNChat     = "phpmm"
		IDsUsers    = [];
		ListUsers   = [];
		
		async for message in app.get_chat_history(UNChat):
			if message.from_user.username is not None:
				print(message.from_user.username);


	if opreat == 'join':
		urlF	 = sys.argv[3];
		urlL	 = sys.argv[4];
		
		URL_f     = URLc(urlF)[1];
		if urlF == urlL:
			URL_l  = URL_f;
		else:
			URL_l  = URLc(urlL)[1];
		print(URL_f,URL_l);

		try:
			joinF    = await app.join_chat(URL_f);
			if urlF == urlL:
				joinF = joinL;
			else:
				joinL  = await app.join_chat(URL_l);
			print('true');
			print(joinF.id);
			print(joinL.id);
		except Exception as Error:
			RESPONSE      = str(Error).replace('Telegram says: ', '').split(' - ')[0];
			if RESPONSE is not False:
				print('true');
				print(9000);
				print(9000);
			else :
				print('false',Error);
			pass
	if opreat == 'left':
		leaveID   = int(sys.argv[3]);
		leaveID2 = int(sys.argv[4]);

		try:
			await app.leave_chat(leaveID);
			if leaveID != leaveID2:
				await app.leave_chat(leaveID2);
			print('true');
		except Exception as Error:
			print('false',Error);
			pass
		pass

	if opreat == 'getusers':
		groupID   = int(sys.argv[3]);
		groupID2 = int(sys.argv[4]);
		OpreatID   = str(sys.argv[5]);
		
		foundUsers       = [];
		notFountUsers = [];
		jart      = get('continue',None,'database/continue.json');
		try :
			countinue_users = jart.split(',');
		except :
			countinue_users = [];
		
		try:
			getFoundUsers     = app.get_chat_members(groupID2);
			async for foundY in getFoundUsers:

				if foundY.user.username is not None:
					foundUsers.append(foundY.user.username);
				else:
					if foundY.user.phone_number is not None:
						foundUsers.append(foundY.user.phone_number);
				pass

			getNotFoundUsers = app.get_chat_members(groupID);
			async for foundN in getNotFoundUsers:

				if foundN.user.username is not None:
					if foundN.user.username not in foundUsers and foundN.user.username not in countinue_users:
						notFountUsers.append(f"@{foundN.user.username}");
						continue;
				
				if foundN.user.phone_number is not None:
					if foundN.user.phone_number not in foundUsers and foundN.user.phone_number not in countinue_users:
						notFountUsers.append(f"+{foundN.user.phone_number}");
			
			readyStore    = "\n".join(notFountUsers);
			#storedMembers(OpreatID,readyStore);
			print('true');
			print(','.join(notFountUsers));
		except:
			print('false');
			pass
	
	if opreat == 'MovePro':
		
		ToChat      = int(sys.argv[4]); #"TestMovePro"; #toGroupID
		UNChat      = int(sys.argv[3]); #"phpmm"; #fromGroupID
		
		FoundedUsers   = [];
		try:
			GetUsers      = app.get_chat_members(ToChat);
			async for foundedQ in GetUsers:
				if foundedQ.user.id is not None:
					FoundedUsers.append(foundedQ.user.id);
		except Exception as Aroz:
			print('false');
			print('inGetGroupOldMembers!');
			print(Aroz);
		
		if len(sys.argv) > 5:
			AddedReq = int(sys.argv[5]) + 200;
		else:
			AddedReq = 1000 + 200;
			
		IDsUsers    = [];
		ListUsers   = [];
		SuccessUsers = '';
		AddedCount   = 0;
		try:
			async for message in app.get_chat_history(UNChat):
				if AddedCount >= AddedReq:
					print(f"Added {AddedReq} !!");
					break;
				
				if message.from_user is None:
					continue;
				if message.from_user.id is None:
					continue;
				if message.from_user.id in FoundedUsers:
					continue;
				if message.from_user.id in IDsUsers:
					continue;
				
				if message.from_user.id not in IDsUsers:
					IDsUsers.append(message.from_user.id);
					if message.from_user.username is not None:
						ListUsers.append(f"@{message.from_user.username}")
						#SuccessUsers     += str(message.from_user.username)+',';
						AddedCount     += 1;
					elif message.from_user.phone_number is not None:
						ListUsers.append(f"+{message.from_user.phone_number}")
						#SuccessUsers     += str(message.from_user.phone_number)+',';
						AddedCount     += 1;
			print('true');
			print(','.join(ListUsers));
		except Exception as Arooz:
			print('false');
			print(Arooz);
			print('inNewGroupFetchMembers!');
	
	if opreat == 'getUsers':
		groupID	= int(sys.argv[3]);
		groupUsers  = [];
		xxz = 0;
		try:
			#getUser     = app.get_chat_members(groupID);
			#async with app:
			async for user in app.iter_chat_members(groupID):
				xxz += 1;
				if xxz >= 1000:
					xxz = 0;
						#time.sleep(5);
					print("Soor "+str(len(groupUsers)));
				if user.user.id is not None:
					groupUsers.append(f"@{user.user.id}");
				else:
					if user.user.phone_number is not None:
						groupUsers.append(f"+{user.user.phone_number}");
				#pass
			#print('true');
			#print(','.join(groupUsers));
			#set("now","mem",','.join(groupUsers));
		except Exception as hhg:
			print('false');
			print(hhg);
			pass
		print(len(groupUsers));

	if opreat == 'adduser':
		groupID	= int(sys.argv[3]);
		userID	   = sys.argv[4];
		jart      = get('continue',None,'database/continue.json');
		try :
			countinue_users = jart.split(',');
		except :
			countinue_users = [];
		try:
			await app.add_chat_members(groupID,str(userID));
			print('true');
		except FloodWait as Error:
			print('flood');
			print(ses);
		except PeerFlood as Error:
			print('floodANDcontinue');
			print(ses);
		except UserPrivacyRestricted as Error:
			countinue_users.append(str(userID));
			set('continue',str(','.join(countinue_users)),None,'database/continue.json');
			print('continue');
			print(countinue_users);
		except UserNotMutualContact as Error:
			countinue_users.append(str(userID));
			set('continue',str(','.join(countinue_users)),None,'database/continue.json');
			print('continue');
			print(countinue_users);
		except UserChannelsTooMuch as Error:
			countinue_users.append(str(userID));
			set('continue',str(','.join(countinue_users)),None,'database/continue.json');
			print('continue');
			print(countinue_users);
		except Exception as Errors:
			print('continues',groupID,userID,Errors);
		pass

	if opreat == 'send':
		senderID	= sys.argv[3];
		messageID   = sys.argv[4];
		recivedID       = sys.argv[5];
		try:
			await app.copy_message(recivedID,senderID,messageID);
			print('true');
		except FloodWait as Error:
			print('flood');
		except UserRestricted as Error:
			print('continue');
		except PeerFlood as Error:
			print('flood');
		except Exception as Errors:
			print(Errors,'all');
		pass
	
	if opreat == 'joining':
		username     = sys.argv[3];
		try:
			join_to_username    = await app.join_chat(username);
			joining_id                    = join_to_username.id;
			print(['true',joining_id]);
		except Exception as prim:
			print(['false',prim]);
		pass
			
	if opreat == 'CX':
		
		UNChat     = "phpmm"
		IDsUsers    = [];
		ListUsers   = [];
		
		async for message in app.get_chat_history(UNChat):
			if message.from_user.id not in IDsUsers:
				IDsUsers.append(message.from_user.id);
				if message.from_user.username is not None:
					ListUsers.append(message.from_user.username)
				elif message.from_user.phone_number is not None:
					ListUsers.append(message.from_user.phone_number)
		print("Useranames\n\n");
		print(ListUsers);

asyncio.get_event_loop().run_until_complete(Controll());



