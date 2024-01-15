#Bot	tools
import	discord
import	os
from	keep_alive	import	keep_alive
from	discord.ext	import	commands
import	asyncio
import	mysql.connector

mydb	=	mysql.connector.connect(
		host=os.environ['########CENSORED######'],
		database	=	os.environ['########CENSORED######'],
		user=os.environ['########CENSORED######'],
		password=os.environ['########CENSORED######']
)

mycursor	=	mydb.cursor(buffered=True)

# mycursor.execute("""CREATE	TABLE	pointboard	(
# 					name text,
# 					priority text,
# 		 			class	text,
# 					subclass text,
# 		 			lifetimepoints integer,
# 					totalpoints integer,
# 		 			gainedpoints integer)""")

client	=	commands.Bot(command_prefix=',',	intents=discord.Intents.all(),	prefix="+")

@client.event
async	def	on_ready():
				#	await	timer()
				print('We	have	logged	in	as	{0.user}'.format(client))

@client.event
async	def	on_message(message):

	if	message.author	==	client.user:
			return

	msg	=	message.content

	#host commands
	if (message.channel.id == ########CENSORED######):
		
		if msg.startswith('%decay'):
				await decay(message)

		if msg.startswith('%reset leaderboard'):
				await resetleaderboard(message)

		if msg.startswith('%reset everyone gp'):
				await resetgainedeveryone(message)
		if msg.startswith('%reset everyone tp'):
				await resettotaleveryone(message)
		if msg.startswith('%reset everyone lt'):
				await resetlifeeveryone(message)
		
	#leader commands
	if (message.channel.id == ########CENSORED######):
		
		if	msg.startswith('%add player'):
				name	=	msg.split(" ")[2].lower()
				priority = msg.split(" ")[3].lower()
				classification = msg.split(" ")[4].lower()
				subclass = msg.split(" ")[5].lower()
				await newplayer(message,name, priority, classification,subclass)

		if msg.startswith('%delete player'):
				name	=	msg.split(" ")[2].lower()
				await deleteplayer(message,name)

		if msg.startswith('%update player info'):
				name	=	msg.split(" ")[3].lower()
				info = msg.split(" ")[4].lower()
				await updateplayer(message,name,info)
			

		if msg.startswith('%set tp'):
				player = msg.split(" ")[2].lower()
				dkp = int(msg.split(" ")[3])
				await settotalpoints(message,player,dkp)

		if msg.startswith('%set gp'):
				player = msg.split(" ")[2].lower()
				dkp = int(msg.split(" ")[3])
				await setgainedpoints(message,player,dkp)

		if msg.startswith('%set lt'):
				player = msg.split(" ")[2].lower()
				dkp = int(msg.split(" ")[3])
				await setlifepoints(message,player,dkp)

		
		if msg.startswith('%buy'):
				player = msg.split(" ")[1].lower()
				dkp = int(msg.split(" ")[2])
				await pay(message,player,dkp)

		if msg.startswith('%give'):
				player = msg.split(" ")[1].lower()
				dkp = int(msg.split(" ")[2])
				await give(message,player,dkp)
	
		
		if msg.startswith('%boss'):
				boss = msg.split(" ")[1]
				star = msg.split(" ")[2]
				namessaturated = msg.split(" ")[3:]
				names = [x.lower() for x in namessaturated]
				print(names)
				await addpoints(message,boss,star,names)
	
		if msg.startswith('%camp'):
				boss = msg.split(" ")[1]
				namessaturated = msg.split(" ")[2:]
				names = [x.lower() for x in namessaturated]
				await camppoints(message,boss,names)

	#clansman commands
	if (message.channel.id == ########CENSORED######) or (message.channel.id == ########CENSORED######):
		
		if msg.startswith('%leaderboard p1'):
				await leaderboardone(message)
		if msg.startswith('%leaderboard p2'):
				await leaderboardtwo(message)
		if msg.startswith('%leaderboard p3'):
				await leaderboardthree(message)

		if msg.startswith('%classboard'):
				classification = msg.split(" ")[1].lower()
				await classscoring(message,classification)

		if msg.startswith('%score'):
				name = msg.split(" ")[1].lower()
				await score(message,name)


			
@client.command()
async def newplayer(message,name, priority, classification,subclass):
	mycursor.execute("SELECT name FROM pointboard WHERE name = %s",([name]))
	try:
		duplicate = mycursor.fetchone()[0]
		if duplicate == name:
			await message.channel.send(f"Player {name} already in database.")
		

	except:
		if (classification == 'warrior' or classification == 'rogue' or classification == 'ranger' or classification == 'mage' or classification == 'druid') and (subclass == 'fire' or subclass == 'ice' or subclass == 'dps' or subclass == 'support' or subclass == 'tank') and (priority == '1' or priority == '2' or priority == '3' or priority == '4'):
	
			mycursor.execute("INSERT INTO pointboard VALUES (%s,%s,%s,%s,%s,%s,%s)",(name, priority, classification, subclass, 0, 0, 0))
			mydb.commit()
			await message.channel.send(f"Player {name} has been added.")
		else:
			await message.channel.send(f"Player {name} has not been added, check again please.")

@client.command()
async def deleteplayer(message,name):
	mycursor.execute("SELECT name FROM pointboard WHERE name = %s",([name]))
	try:
		mycursor.fetchone()[0]
		mycursor.execute("DELETE FROM pointboard WHERE name = %s",([name]))
		mydb.commit()
		await message.channel.send(f"Player {name} has been removed from database.")
	except:
		await message.channel.send(f"Player {name} not in database.")
		


@client.command()
async def updateplayer(message,name,info):
	if info == 'warrior' or info == 'rogue' or info == 'ranger' or info == 'mage' or info == 'druid':
		mycursor.execute("SELECT name FROM pointboard WHERE name = %s",([name]))
		try: 
			mycursor.fetchone()[0]
			mycursor.execute("UPDATE pointboard SET class = %s WHERE name = %s",(info, name))
			mydb.commit()
			await message.channel.send(f"Player class {name} has been updated.")
		except:
			await message.channel.send(f"Player {name} not in database.")
	elif info == 'fire' or info == 'ice' or info == 'dps' or info == 'support' or info == 'tank':
		mycursor.execute("SELECT name FROM pointboard WHERE name = %s",([name]))
		try:
			mycursor.fetchone()[0]
			mycursor.execute("UPDATE pointboard SET subclass = %s WHERE name = %s",(info, name))
			mydb.commit()
			await message.channel.send(f"Player subclass {name} has been updated.")
		except:
			await message.channel.send(f"Player {name} not in database.")
	elif info == '1' or info == '2' or info == '3' or info == '4':
		mycursor.execute("SELECT name FROM pointboard WHERE name = %s",([name]))
		try:
			mycursor.fetchone()[0]
			mycursor.execute("UPDATE pointboard SET priority = %s WHERE name = %s",(info, name))
			mydb.commit()
			await message.channel.send(f"Player priority {name} has been updated.")
		except:
			await message.channel.send(f"Player {name} not in database.")
	else:
		await message.channel.send(f"Player (sub)class/priority {name} has not been updated, check again please.")

@client.command()
async def leaderboardone(message):
	mycursor.execute("SELECT * FROM pointboard ORDER BY totalpoints DESC")
	board=mycursor.fetchall()
	people = []
	for character in board[:21]:
		newcharacter= [str(x) for x in character]
		cleancharacter=' '.join(list(newcharacter))
		people.append(cleancharacter)

	def format_list(lst):
		formatted_list = "```Name            |  Priority  |  Class  |  Subclass  |  LT        |  TP           |  GP\n"
		for item in lst:
				fields = item.split()
				name = fields[0]
				priority = fields[1]
				role = fields[2]
				subclass = fields[3]
				lifetimepoints = fields[4]
				totalpoints = fields[5]
				gainedpoints = fields[6]
				formatted_list += f"{name:<15} | {priority:<10} | {role:<7} | {subclass:<10} | {lifetimepoints:<10} | {totalpoints:<10}	| {gainedpoints:<1}\n"
		formatted_list += "```"
		return formatted_list


	formatted_list = format_list(people)
	await message.channel.send(formatted_list)

async def leaderboardtwo(message):
	mycursor.execute("SELECT * FROM pointboard ORDER BY totalpoints DESC")
	board=mycursor.fetchall()
	people = []
	for character in board[21:41]:
		newcharacter= [str(x) for x in character]
		cleancharacter=' '.join(list(newcharacter))
		people.append(cleancharacter)

	def format_list(lst):
		formatted_list = "```Name            |  Priority  |  Class  |  Subclass  |  LT        |  TP           |  GP\n"
		for item in lst:
				fields = item.split()
				name = fields[0]
				priority = fields[1]
				role = fields[2]
				subclass = fields[3]
				lifetimepoints = fields[4]
				totalpoints = fields[5]
				gainedpoints = fields[6]
				formatted_list += f"{name:<15} | {priority:<10} | {role:<7} | {subclass:<10} | {lifetimepoints:<10} | {totalpoints:<10}	| {gainedpoints:<1}\n"
		formatted_list += "```"
		return formatted_list

	formatted_list = format_list(people)
	await message.channel.send(formatted_list)

async def leaderboardthree(message):
	mycursor.execute("SELECT * FROM pointboard ORDER BY totalpoints DESC")
	board=mycursor.fetchall()
	people = []
	for character in board[41:]:
		newcharacter= [str(x) for x in character]
		cleancharacter=' '.join(list(newcharacter))
		people.append(cleancharacter)

	def format_list(lst):
		formatted_list = "```Name            |  Priority  |  Class  |  Subclass  |  LT        |  TP           |  GP\n"
		for item in lst:
				fields = item.split()
				name = fields[0]
				priority = fields[1]
				role = fields[2]
				subclass = fields[3]
				lifetimepoints = fields[4]
				totalpoints = fields[5]
				gainedpoints = fields[6]
				formatted_list += f"{name:<15} | {priority:<10} | {role:<7} | {subclass:<10} | {lifetimepoints:<10} | {totalpoints:<10}	| {gainedpoints:<1}\n"
		formatted_list += "```"
		return formatted_list

	formatted_list = format_list(people)
	await message.channel.send(formatted_list)




@client.command()
async def classscoring(message,classification):
	if classification == 'warrior' or classification == 'rogue' or classification == 'ranger' or classification == 'mage' or classification == 'druid':
		mycursor.execute("SELECT * FROM pointboard WHERE class = %s ORDER BY totalpoints DESC",([classification]))
		board=mycursor.fetchall()
		people = []
		for character in board:
			newcharacter= [str(x) for x in character]
			cleancharacter=' '.join(list(newcharacter))
			people.append(cleancharacter)
	
		def format_list(lst):
			formatted_list = "```Name            |  Priority  |  Class  |  Subclass  |  LT        |  TP           |  GP\n"
			for item in lst:
					fields = item.split()
					name = fields[0]
					priority = fields[1]
					role = fields[2]
					subclass = fields[3]
					lifetimepoints = fields[4]
					totalpoints = fields[5]
					gainedpoints = fields[6]
					formatted_list += f"{name:<15} | {priority:<10} | {role:<7} | {subclass:<10} | {lifetimepoints:<10} | {totalpoints:<10}	| {gainedpoints:<1}\n"
			formatted_list += "```"
			return formatted_list
	
		formatted_list = format_list(people)
		await message.channel.send(formatted_list)
	else:
		await message.channel.send('Command did not work, rewrite your sentence correctly please.')

@client.command()
async def score(message,name):
	try:
		mycursor.execute("SELECT * FROM pointboard WHERE name = %s",([name]))
		board=mycursor.fetchall()
		people = []
		for character in board:
			newcharacter= [str(x) for x in character]
			cleancharacter=' '.join(list(newcharacter))
			people.append(cleancharacter)
		if not people:
			pass
		else:
			def format_list(lst):
				formatted_list = "```Name            |  Priority  |  Class  |  Subclass  |  LT        |  TP           |  GP\n"
				for item in lst:
						fields = item.split()
						name = fields[0]
						priority = fields[1]
						role = fields[2]
						subclass = fields[3]
						lifetimepoints = fields[4]
						totalpoints = fields[5]
						gainedpoints = fields[6]
						formatted_list += f"{name:<15} | {priority:<10} | {role:<7} | {subclass:<10} | {lifetimepoints:<10} | {totalpoints:<10}	| {gainedpoints:<1}\n"
				formatted_list += "```"
				return formatted_list

		formatted_list = format_list(people)
		await message.channel.send(formatted_list)
	except:
		await message.channel.send(f"{name} not in database.")
	
@client.command()
async def addpoints(message,boss,star,names):

	if boss == '170' and star == '4':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+5*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+5*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+5*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if boss == '170' and star == '5':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+10*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+10*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+10*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if boss == '170' and star == '6':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+30*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+30*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+30*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if boss == '180' and star == '4':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+10*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+10*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+10*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if boss == '180' and star == '5':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+20*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+20*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+20*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if boss == '180' and star == '6':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+60*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+60*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+60*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if (boss == '215' or boss == '210') and star == '4':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+15*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+15*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+15*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if (boss == '215' or boss == '210') and star == '5':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+30*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+30*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+30*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if (boss == '215' or boss == '210') and star == '6':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+90*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+90*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+90*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if boss == 'aggy' and star == '6':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+50*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+50*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+50*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if boss == 'hrung' and star == '6':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+125*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+125*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+125*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if boss == 'mord' and star == '6':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+150*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+150*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+150*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if boss == 'necro' and star == '6':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+200*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+200*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+200*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")

	if boss == 'prot' and star == 'base':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+250*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+250*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+250*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if boss == 'prot' and star == 'prime':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+300*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+300*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+300*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if boss == 'gele' and star == '6':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+500*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+500*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+500*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if boss == 'bt' and star == '6':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+750*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+750*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+750*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if boss == 'dhio' and star == '6':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+1000*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+1000*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+1000*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")

	if boss == 'ring' and star == '5':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+25*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+25*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+25*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")

	if boss == 'ring' and star == '6':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+100*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+100*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+100*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")

	if boss == 'legacy' and star == '5':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+25*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+25*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+25*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")

	if boss == 'legacy' and star == '6':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+75*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+75*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+75*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} {star}* dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")


@client.command()
async def camppoints(message,boss,names):
	
	if boss == 'hrung':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+12*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+12*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+12*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if boss == 'mord':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+15*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+15*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+15*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if boss == 'necro':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+18*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+18*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+18*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")

	if boss == 'prot':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+10*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+10*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+10*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if boss == 'gele':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+21*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+21*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+21*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if boss == 'bt':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+24*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+24*perc, name))
				mydb.commit()
				
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+24*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
	if boss == 'dhio':
		try:
			for name in names:
				perc = 0
				mycursor.execute("SELECT priority FROM pointboard WHERE name = %s",([name]))
				priority = mycursor.fetchone()[0]
				if priority == '1':
					perc = 1
				elif priority == '2':
					perc = 0.5
				elif priority == '3' or priority == '4':
					perc = 0.25
				else:
					await message.channel.send(f"Add {name} priority first, before assigning points.")

				
				mycursor.execute("SELECT lifetimepoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				 
				mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(currentpoints+27*perc, name))
				mydb.commit()
							
				mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(currentpoints+27*perc, name))
				mydb.commit()
			
				mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([name]))
				currentpoints = mycursor.fetchone()[0]
				mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(currentpoints+27*perc, name))
				mydb.commit()
			await message.channel.send(f"Added {boss} dkp points to {' '.join(names)}.")
		except:
			await message.channel.send(f"Player {name} not registered, any player mentioned after this will receive no points either.")
			

@client.command()
async def settotalpoints(message,name,dkp):
	mycursor.execute("SELECT name FROM pointboard WHERE name = %s",([name]))
	try: 
		mycursor.fetchone()[0]
		mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(dkp, name))
		mydb.commit()
		await message.channel.send(f"Player {name} TP dkp points has been set to {dkp}.")
	except:
		await message.channel.send(f"Player {name} not registered.")

async def setgainedpoints(message,name,dkp):
	mycursor.execute("SELECT name FROM pointboard WHERE name = %s",([name]))
	try: 
		mycursor.fetchone()[0]
		mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(dkp, name))
		mydb.commit()
		await message.channel.send(f"Player {name} GP dkp points has been set to {dkp}.")
	except:
		await message.channel.send(f"Player {name} not registered.")

async def setlifepoints(message,name,dkp):
	mycursor.execute("SELECT name FROM pointboard WHERE name = %s",([name]))
	try: 
		mycursor.fetchone()[0]
		mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(dkp, name))
		mydb.commit()
		await message.channel.send(f"Player {name} LT dkp points has been set to {dkp}.")
	except:
		await message.channel.send(f"Player {name} not registered.")

@client.command()
async def pay(message,name,dkp):
	mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
	try: 
		points=mycursor.fetchone()[0]
		mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(points-dkp, name))
		mydb.commit()
		await message.channel.send(f"Player {name} has bought an item for {dkp} dkp.")
	except:
		await message.channel.send(f"Player {name} not registered.")

@client.command()
async def give(message,name,dkp):
	mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([name]))
	try: 
		points=mycursor.fetchone()[0]
		mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(points+dkp, name))
		mydb.commit()
		await message.channel.send(f"Player {name} has been given {dkp} dkp.")
	except:
		await message.channel.send(f"Player {name} not registered.")

@client.command()
async def resetgainedeveryone(message):
	await message.channel.send(f"GP is going to reset, might take a while, no other commands available meanwhile processing.")
	mycursor.execute("SELECT name FROM pointboard")
	board=mycursor.fetchall()
	people = []
	for character in board:
		newcharacter= [str(x) for x in character]
		cleancharacter=' '.join(list(newcharacter))
		people.append(cleancharacter)
	for character in people:
		mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([character]))
		try: 
			totalpoints=mycursor.fetchone()[0]
			mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(0, character))
			mydb.commit()
		except:
			await message.channel.send(f"GP couldn't be resetted, please try again.")
	await message.channel.send(f"GP has been resetted.")

async def resettotaleveryone(message):
	await message.channel.send(f"TP is going to reset, might take a while, no other commands available meanwhile processing.")
	mycursor.execute("SELECT name FROM pointboard")
	board=mycursor.fetchall()
	people = []
	for character in board:
		newcharacter= [str(x) for x in character]
		cleancharacter=' '.join(list(newcharacter))
		people.append(cleancharacter)
	for character in people:
		mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([character]))
		try: 
			totalpoints=mycursor.fetchone()[0]
			mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(0, character))
			mydb.commit()
		except:
			await message.channel.send(f"TP couldn't be resetted, please try again.")
	await message.channel.send(f"TP has been resetted.")

async def resetlifeeveryone(message):
	await message.channel.send(f"LT is going to reset, might take a while, no other commands available meanwhile processing.")
	mycursor.execute("SELECT name FROM pointboard")
	board=mycursor.fetchall()
	people = []
	for character in board:
		newcharacter= [str(x) for x in character]
		cleancharacter=' '.join(list(newcharacter))
		people.append(cleancharacter)
	for character in people:
		mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([character]))
		try:
			totalpoints=mycursor.fetchone()[0]
			mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(0, character))
			mydb.commit()
		except:
			await message.channel.send(f"LT couldn't be resetted, please try again.")
	await message.channel.send(f"LT has been resetted.")
	
@client.command()
async def decay(message):
	await message.channel.send(f"Activating decay, might take a while, no other commands available meanwhile processing.")
	mycursor.execute("SELECT name FROM pointboard")
	board=mycursor.fetchall()
	people = []
	for character in board:
		newcharacter= [str(x) for x in character]
		cleancharacter=' '.join(list(newcharacter))
		people.append(cleancharacter)
	for character in people:
		mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([character]))
		try: 
			totalpoints=mycursor.fetchone()[0]
			mycursor.execute("SELECT gainedpoints FROM pointboard WHERE name = %s",([character]))
			gainedpoints=mycursor.fetchone()[0]
			mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(totalpoints-(abs(totalpoints-gainedpoints)*0.1), character))
			mydb.commit()
			mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(0,character))
			mydb.commit()
		except:
			await message.channel.send(f"Decay not working, please try again.")
	await message.channel.send(f"Decay applied, bot ready to go again.")
		
	
@client.command()
async def resetleaderboard(message):
	await message.channel.send(f"Leaderoard is going to reset, might take a while, no other commands available meanwhile processing.")
	mycursor.execute("SELECT name FROM pointboard")
	board=mycursor.fetchall()
	people = []
	for character in board:
		newcharacter= [str(x) for x in character]
		cleancharacter=' '.join(list(newcharacter))
		people.append(cleancharacter)
	for character in people:
		mycursor.execute("SELECT totalpoints FROM pointboard WHERE name = %s",([character]))
		try: 
			totalpoints=mycursor.fetchone()[0]
			mycursor.execute("UPDATE pointboard SET lifetimepoints = %s WHERE name = %s",(0, character))
			mydb.commit()
			mycursor.execute("UPDATE pointboard SET totalpoints = %s WHERE name = %s",(0, character))
			mydb.commit()
			mycursor.execute("UPDATE pointboard SET gainedpoints = %s WHERE name = %s",(0,character))
			mydb.commit()
		except:
			await message.channel.send(f"Leaderboard couldn't be resetted, please try again.")
	await message.channel.send(f"Leaderoard has been resetted.")

client.run(os.environ['Token'])
