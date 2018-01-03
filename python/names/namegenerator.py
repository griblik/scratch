import random

forenames = {}
forenames['male'] = ["oliver","harry","george","jack","jacob","noah","charlie","muhammad","thomas","oscar","william","james","leo","alfie","henry","joshua","freddie","archie","ethan","isaac","alexander","joseph","edward","samuel","max","logan","lucas","daniel","theo","arthur","mohammed","harrison","benjamin","mason","finley","sebastian","adam","dylan","zachary","riley","teddy","theodore","david","elijah","jake","toby","louie","reuben","arlo","hugo","jaxon","luca","matthew","harvey","harley","reggie","tommy","jenson","luke","michael","jayden","jude","frankie","albert","stanley","elliot","gabriel","mohammad","ollie","ronnie","louis","charles","blake","elliott","lewis","frederick","nathan","tyler","jackson","rory","ryan","carter","dexter","alex","austin","caleb","kai","albie","ellis","bobby","ezra","leon","roman","jesse","aaron","ibrahim","liam","jasper","felix","finn",]
forenames['female'] = ["olivia","amelia","emily","isla","ava","isabella","lily","jessica","ella","mia","sophia","charlotte","poppy","sophie","grace","evie","alice","scarlett","freya","florence","isabelle","daisy","chloe","phoebe","matilda","ruby","evelyn","sienna","sofia","eva","elsie","willow","ivy","millie","esme","rosie","imogen","elizabeth","maya","layla","emilia","lola","lucy","harper","eliza","erin","eleanor","ellie","harriet","thea","maisie","holly","emma","georgia","amber","molly","hannah","abigail","jasmine","lilly","annabelle","rose","penelope","amelie","violet","bella","aria","zara","maria","nancy","darcie","lottie","anna","summer","martha","heidi","gracie","luna","maryam","beatrice","mila","darcey","megan","iris","lexi","robyn","aisha","clara","francesca","sara","victoria","zoe","julia","arabella","maddison","sarah","felicity","darcy","leah","lydia",]

surnames = ["Smith","Jones","Taylor","Williams","Brown","Davies","Evans","Wilson","Thomas","Roberts","Johnson","Lewis","Walker","Robinson","Wood","Thompson","White","Watson","Jackson","Wright","Green","Harris","Cooper","King","Lee","Martin","Clarke","James","Morgan","Hughes","Edwards","Hill","Moore","Clark","Harrison","Scott","Young","Morris","Hall","Ward","Turner","Carter","Phillips","Mitchell","Patel","Adams","Campbell","Anderson","Allen","Cook","Bailey","Parker","Miller","Davis","Murphy","Price","Bell","Baker","Griffiths","Kelly","Simpson","Marshall","Collins","Bennett","Cox","Richardson","Fox","Gray","Rose","Chapman","Hunt","Robertson","Shaw","Reynolds","Lloyd","Ellis","Richards","Russell","Wilkinson","Khan","Graham","Stewart","Reid","Murray","Powell","Palmer","Holmes","Rogers","Stevens","Walsh","Hunter","Thomson","Matthews","Ross","Owen","Mason","Knight","Kennedy","Butler","Saunders","Cole","Pearce","Dean","Foster","Harvey","Hudson","Gibson","Mills","Berry","Barnes","Pearson","Kaur","Booth","Dixon","Grant","Gordon","Lane","Harper","Ali","Hart","Mcdonald","Brooks","Ryan","Carr","Macdonald","Hamilton","Johnston","West","Gill","Dawson","Armstrong","Gardner","Stone","Andrews","Williamson","Barker","George","Fisher","Cunningham","Watts","Webb","Lawrence","Bradley","Jenkins","Wells","Chambers","Spencer","Poole","Atkinson","Lawson",]

def get_forename(gender):
	'''
	Return a random name from the list in male_surnames	or female_surnames
	as specified, or random gender if not
	'''

	return random.choice(forenames[get_gender(gender)])

def get_surname():
	''' Return a random surname from the surnames list '''

	return random.choice(surnames)

def get_full_name(gender):
	'''
	Return the concatenation of a forename and surname
	Gender is random unless passed as a param
	'''

	return get_forename(get_gender(gender)) + " " + get_surname()

def get_gender(gender):
	''' Return a random gender from genders if none is supplied '''

	genders = list(forenames.keys())

	if gender not in genders:
		gender = random.choice(genders)

	return gender

if __name__ == '__main__':
	print(get_full_name(None))