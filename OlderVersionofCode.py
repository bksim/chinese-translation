#!/usr/bin/python
# -*- coding: utf-8 -*-
import nltk
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def match_rule(pos):
	e2c_rules = {}


	# negative sentences
	# how can we put I can't eat or I cannot eat.

	#SVO
	e2c_rules['PRP','VBP','NN'] = ['PRP','VBP','NN'] #i eat rice: wo chi fan
	e2c_rules['PRP','VBZ','NN'] = ['PRP','VBZ','NN'] #he eats rice: ta chi fan
	e2c_rules['PRP','VBD','NN'] = ['PRP','NN','VBD','PastParticle'] #i ate rice: wo ba fan chi le
	e2c_rules['PRP','MD','VB','NN'] = ['PRP','FutureParticle','VB', 'NN'] #i will eat rice: wo hui chi fan
	e2c_rules['PRP','VBP','VBG','NN'] = ['PRP','PresentPerfectParticle', 'VBG', 'NN'] #i am eating rice: wo zai chi fan
	e2c_rules['PRP','VBZ','VBG','NN'] = ['PRP','PresentPerfectParticle', 'VBG', 'NN'] #he is eating rice: ta zai chi fan
	e2c_rules['PRP','VBD'] = ['PRP','VBD','PastParticle'] #i ate
	
	#Adjectives
	e2c_rules['PRP','VBZ','RB','JJ'] = ['PRP','RB','JJ'] #She is very pretty: Ta hen piao liang
	e2c_rules['PRP','VBZ','JJ'] = ['PRP','JJ'] #She is pretty: Ta piao liang


	e2c_rules['PRP','VBP','RB','JJ'] = ['PRP','RB','JJ'] #They are very pretty: Ta men hen piao liang
	e2c_rules['PRP','VBP','JJ'] = ['PRP','JJ'] #They are pretty: Ta men piao liang

	# the prior two rules work for most other adjectives. However, since pretty is a feminine descriptive verb,
	#the character for they should also be the female version.

	e2c_rules['PRP','UH','JJ'] = ['PRP','JJ'] # i am tired : wo lei
	e2c_rules['PRP','UH','RB','VBN'] = ['PRP','very','VBN'] # i am tired : wo lei
	e2c_rules['PRP','VBZ','VBN'] = ['PRP','VBN'] #she is tired
	e2c_rules['PRP','VBZ','VBN'] = ['PRP','very','VBN'] #she is very tired


	#the pretty girl ate the sweet rice
	#SubjectVerb
	e2c_rules['PRP','VBP'] = ['PRP','VBP'] #i eat: wo chi 
	e2c_rules['PRP','VBZ'] = ['PRP','VBZ'] #he eats": ta chi 
	e2c_rules['PRP','VBZ'] = ['PRP','VBZ'] #he drinks": ta he
	e2c_rules['PRP','MD','VB'] = ['PRP' 'FutureParticle','VB'] #he will drink": ta hui he
	
	
	#FutureDesire
	e2c_rules['PRP','MD','VB','TO','VBP'] = ['PRP', 'FutureParticle', 'want','VBP']# i will want to eat: wo hui yao chi 
	e2c_rules['PRP','MD','VB','TO','VBP','NN'] = ['PRP', 'FutureParticle', 'want','VBP', 'NN']
	e2c_rules['PRP','MD','VB','NN'] = ['PRP','FutureParticle', 'want','NN']
	
	#PastDesire
	e2c_rules['PRP','VBD','TO','VBP'] = ['PRP','want','VBP', 'PastParticle'] # i wanted to eat
	e2c_rules['PRP','VBD','TO','VBP', 'NN'] = ['PRP', 'want','VBP', 'PastParticle', 'NN']
	#e2c_rules['PRP','VBD','NN'] = ['PRP', 'want','VBP', 'PastParticle'] # i wanted to eat

	# some research needs to be done on this: it seems like chinese past desire is equivalent to the
	#"already tense in english present tense"

	#Commands
	e2c_rules['IN','EX'] = ['IN','LocationParticleThere'] #Go there : Chu na li.
	e2c_rules['IN','EX'] = ['IN','LocationParticleHere'] #Come here : Lai ze li.
	e2c_rules['IN','NN'] = ['IN','NN'] 
	e2c_rules['VBP','NN'] = ['VBP','NN'] #Eat rice: chi fan
	e2c_rules['VBP','PRP'] = ['VBP']

	#Negative Commands
	e2c_rules['VBP','RB','VBP','NN'] = ['not','want','VBP', 'NN']
	#same problem as before(scroll down)- program tries to account for "do" 
	#but that doesn't exist in english - it is omitted`- i think it has something do 
	#with the pop method which returns the first word- if we could change that to 
	#return the second, i think it would work
	e2c_rules['VBP','RB' 'VBP','NN'] = ['not','want','VBP', 'NN']
	
	#TimeDescriptors
	e2c_rules['PRP','RB','VBD'] = ['PRP','RB','VBD', 'PastParticle'] #I already ate: Wo yi jin chi le
	e2c_rules['PRP','VBD','RB'] = ['PRP','RB','VBD', 'PastParticle'] #I ate yesterday: Wo zuo tian chi le
	e2c_rules['PRP','MD','VBP','NN','RB'] = ['PRP','RB','FutureParticle','VBP','NN'] #I will eat rice tomorrow : wo mian tian hui chi fan
	e2c_rules['PRP','MD','VBP','NN'] = ['PRP','FutureParticle','VBP','NN'] #I will eat rice : wo hui chi fan	
	e2c_rules['PRP','MD','VBP'] = ['PRP','FutureParticle','VBP'] #I will eat: wo hui chi 	

	e2c_rules['RB','PRP','MD','VBP','NN'] = ['RB','PRP','FutureParticle','VBP','NN']#Tomorrow, I will eat rice : Ming tian, wo hui chi fan
	e2c_rules['PRP','MD','VBP','RB'] = ['PRP','RB','FutureParticle','VBP']
	
	#e2c_rules['PRP','MD','VBP','PRP','RB'] = ['PRP','RB','FutureParticle','VBP']
	#i will do it later: wo yi hou hui zhuo - not sure why this doesn't work

	#LocationDescriptors
	e2c_rules['PRP','VBD','IN','NN'] = ['PRP','PresentPerfectParticle','NN','VBD','PastParticle'] # i ate at home: wo chai jia li chi le
	e2c_rules['PRP','VBD','NN','IN','NN'] = ['PRP','PresentPerfectParticle','NN','VBD','PastParticle', 'NN'] # i ate rice at home: wo chai jia li chi le fan
	e2c_rules['PRP','MD','VBP','IN','NN'] = ['PRP', 'FutureParticle','PresentPerfectParticle','NN','VBP'] # I will eat at home: wo hui zhai jia chi
	#e2c_rules['PRP', 'MD', 'VBP', 'NNS','IN','NN'] = ['PRP', 'FutureParticle','PresentPerfectParticle','NN','VBP', 'NN']
	# i will eat rice at home. this should be made using actual sentence structure




	#Questions
	e2c_rules['WP','VBP','PRP'] = ['PRP','VBP','WP'] #who are you: ni shi shei?
	e2c_rules['WP','UH','PRP'] = ['PRP','UH','WP'] #who am i: wo shi shei?
	e2c_rules['WP','VBZ','PRP' ] = ['PRP','VBZ','WP'] #who is he: ta shi shei?
	e2c_rules['WP','VBZ','NN'] = ['NN','VBZ','WP'] #what is rice: fan shi she me?
	e2c_rules['WRB','VBZ','PRP' ] = ['PRP','WRB'] #how is she: ta ru he- formal
	#colliqual-ta hao ma? - needs to be coded - divergence from textbook grammar structure
	e2c_rules['WRB','MD','VB', 'VBP', 'NN' ] = ['VB','MD','VBP','NN'] #how can i eat rice: wo ze me nen chi fan
	#e2c_rules['VBP','PRP', 'VBD' ] = ['PRP','VBP','QuestionParticle']
	# are you tired - instead of ni lei ma - it translates to ni shi ma
	#e2c_rules['MD','PRP','VBP' ] = ['PRP','VBP','WP']
	#can i eat- this there are two translations for can- see below in the dictionary

	#NounTwoVerbs

	#SubjectTwoObjects
	e2c_rules['PRP','VBP','NN','CC','NNS'] = ['PRP','VBP','NN','AndParticle','NNS'] #i eat rice and noodles
	e2c_rules['PRP','MD','VBP','NN','CC','NNS'] = ['PRP','FutureParticle', 'VBP','NN','AndParticle','NNS'] #i will eat rice and noodles
	e2c_rules['PRP','VBD','NN','CC','NNS'] = ['PRP','NN','AndParticle','NNS','VBP', 'PastParticle',] #i ate rice and noodles
	#not sure why VBP is showing up as an error in this case

	#2NounVerb
	e2c_rules['PRP','CC','PRP','VBP','NN'] = ['PRP', 'AndParticle' ,'PRP', 'VBP', 'NN']
	e2c_rules['PRP','CC','PRP','VBP'] = ['PRP', 'AndParticle' ,'PRP', 'VBP']
	#you and i eat rice: ni he wo chi fan
	e2c_rules['NN', 'CC', 'NN', 'VBP'] = ['NN', 'AndParticle' ,'NN', 'VBP']

	#Negative Sentences
	e2c_rules['PRP', 'MD', 'RB', 'VBP'] = ['PRP','not','can', 'VBP'] 
	#i can not eat
	e2c_rules['PRP', 'MD', 'RB', 'VBP', 'NN'] = ['PRP','not','can', 'VBP', 'NN']
	#i can not eat rice
	#e2c_rules['PRP', 'VBP', 'RB', 'VBP'] = ['PRP','not','VBP'] # i do not eat
	#Because there are two VBP, the translation takes the first VBP
	#Uncategorized 

	e2c_rules['DT', 'NN', 'VBZ'] = ['NN', 'VBZ'] #the girl eats: nu hai chi
	e2c_rules['DT', 'NN', 'VBZ', 'NN'] = ['NN', 'VBZ', 'NN'] #the girl eats rice: nu hai chi fan
	e2c_rules['DT', 'NN', 'VBZ', 'NNS'] = ['NN', 'VBZ', 'NNS'] #the girl eats noodles: nu hai chi mien
	e2c_rules['PRP', 'VBP', 'PRP'] = ['PRP','VBP','PRP'] #i love you: wo ai ni
	e2c_rules['PRP', 'VBD', 'PRP'] = ['PRP','VBD','PastParticle', 'PRP']
	e2c_rules['PRP', 'VBZ', 'PRP$'] = ['PRP','VBZ','PRP$'] # he loves her: ta ai ta
	e2c_rules['PRP', 'VBZ', 'PRP'] = ['PRP','VBZ','PRP'] #he loves them: ta ai ta men
	e2c_rules['PRP', 'VBP', 'TO', 'VBP'] = ['PRP', 'VBP', 'VBP'] # I want to eat: wo xiang yao chi
	e2c_rules['PRP', 'VBP', 'TO', 'VBP', 'NN'] = ['PRP', 'VBP', 'VBP', 'NN'] # I want to eat rice: wo xiang yao chi fan
	e2c_rules['WP', 'VBP', 'PRP', 'VBG'] = ['PRP', 'PresentPerfectParticle', 'VBG','what'] #What are you doing: ni zai zuo se ma
	e2c_rules['WP', 'VBD', 'PRP', 'VBP'] = ['PRP','VBD','PastParticle', 'what'] #what did you do
	e2c_rules['WP', 'MD', 'PRP', 'VB'] = ['PRP','FutureParticle','VB', 'what'] # ni hui zuo se me
	#the boy loves the girl- code this later - will be a less commonly used expression
	
	#2NounVerb
	e2c_rules['VBD', 'CC', 'NN', 'VBP'] = ['VBD','AndParticle','NN', 'VBP' ] #david and brandon eat
	e2c_rules['VBD', 'CC', 'NN','MD','VBP'] = ['VBD','AndParticle','NN','FutureParticle','VBP' ] #david and brandon will eat
	e2c_rules['VBD', 'CC', 'NN','VBD'] = ['VBD','AndParticle','NN','VBD', 'PastParticle' ] #david and brandon ate
	e2c_rules['VBD', 'CC', 'NN', 'VBP', 'NN'] = ['VBD','AndParticle','NN', 'VBP', 'NN' ] #david and brandon eat rice
	e2c_rules['VBD', 'CC', 'NN','MD','VBP','NN'] = ['VBD','AndParticle','NN','FutureParticle','VBP', 'NN' ] #david and brandon will eat rice
	e2c_rules['VBD', 'CC', 'NN','VBD', 'NN'] = ['VBD','AndParticle','NN','NN', 'VBD', 'PastParticle' ] #david and brandon ate rice

	#hello and #hi need to be coded
	#e2c_rules['NN'] = ['NN']
	#the translator doesn't handle translations of single words
	#like rice or noodles

	#if u try to enter a word that isn't in the dictionary, it returns
	# an internal sevice error. It should display we currently cannot provide
	#a translation. also, we need to reference a dictionary for random words
	
	#we need to add the romanization to the chinese translation -how?
	#should we make the translation bigger and centered? -#design question

	#Compound Sentence
	e2c_rules['PRP', 'VBP','NN' ,'CC', 'NN','NN'] = ['PRP', 'VBP','NN', 'AndParticle','NN', 'NN'] #i eat rice and drink water
	e2c_rules['PRP', 'MD', 'VBP','NN' ,'CC', 'NN','NN'] = ['PRP', 'FutureParticle', 'VBP','NN', 'AndParticle','NN', 'NN'] #i eat rice and drink water
	#e2c_rules['PRP', 'VBD','NN' ,'CC', 'NN','NN'] = ['PRP', 'NN','VBD','PastParticle', 'AndParticle','NN', 'NN', 'PastParticle']
	#^ same issue as with past tense

	e2c_rules['PRP', 'VBZ','NN' ,'CC', 'NNS','NN'] = ['PRP', 'VBZ','NN', 'AndParticle','NNS', 'NN'] #i eat rice and drink water
	e2c_rules['PRP', 'MD', 'VBZ','NN' ,'CC', 'NNS','NN'] = ['PRP', 'FutureParticle', 'VBZ','NN', 'AndParticle','NNS', 'NN'] #i eat rice and drink water
	e2c_rules['PRP', 'VBD','NN' ,'CC', 'NNS','NN'] = ['PRP', 'NN','VBD','PastParticle', 'AndParticle','NN', 'NNS', 'PastParticle']
	#^she ate rice and drank water - rank and water are interchanged regardles of changing the rul
	
	if pos in e2c_rules:
		return e2c_rules[pos]
	else:
		return None



def tag(phrase):
	tokens = nltk.word_tokenize(phrase.lower())	
	#firstletter= phrase[0]
	tagged = nltk.pos_tag(tokens)

	# exceptions
	for i in range(len(tagged)):
		# ate is a past tense verb

		

		if tagged[i][0] == 'ate':
			tagged[i] = ('ate', 'VBD')
		if tagged[i][0] == 'home':
			tagged[i] = ('home', 'NN')

		if tagged[i][0] == 'come':
			tagged[i] = ('come', 'IN')

		if tagged[i][0] == 'here':
			tagged[i] = ('here', 'EX')

		if tagged[i][0] == 'eat':
			tagged[i] = ('eat', 'VBP')

		if tagged[i][0] == 'eats':
			tagged[i] = ('eats', 'VBZ')

		if tagged[i][0] == 'close':
			tagged[i] = ('close', 'VBP')

		if tagged[i][0] == 'tomorrow':
			tagged[i] = ('tomorrow', 'RB')

		if tagged[i][0] == 'today':
			tagged[i] = ('today', 'RB')

		if tagged[i][0] == 'yesterday':
			tagged[i] = ('yesterday', 'RB')

		if tagged[i][0] == 'later':
			tagged[i] = ('later', 'RB')

		if tagged[i][0] == 'am':
			tagged[i] = ('am', 'UH')

		if tagged[i][0] == 'me':
			tagged[i] = ('me', 'NN')

	#pretty is an adjective
		if tagged[i][0] == 'pretty':
			tagged[i] = ('pretty', 'JJ')

	return tagged

# translates a phrase from english to chinese
def english_to_chinese(phrase):
	tagged = tag(phrase)
	print tagged

	pos = list(zip(*tagged)[1])
	# remove punctuation - can we make it so that the punctuation the user enters is also outputed? 
	if pos[-1] == '.' or pos[-1] == '?' or pos[-1] == '!':
		pos.pop()

	rule = match_rule(tuple(pos))
	if rule is None:
		return "We cannot currently provide a translation."

	# dictionary of things to translate
	to_translate = {}
	for t, u in tagged:
		if u not in to_translate:
			to_translate[u] = [t]
		else:
			to_translate[u] = to_translate[u] + [t]
	print to_translate

	e2c = {}


	#Chinese Particles
	e2c['PastParticle'] = '了'
	e2c['FutureParticle'] = '会'
	e2c['PresentPerfectParticle']='在'
	e2c['LocationParticleThere']='那里'
	e2c['LocationParticleHere']='这里'
	e2c['AuxVerb']='把'
	e2c['TheyFemale']='她们'
	e2c['AndParticle']='和'
	e2c['not']='不'
	e2c['QuestionParticle']='吗'
	e2c['know'] ='会'
	e2c['can'] ='能'
	#another word for can is 可以 - which is more
	#appropriate in the case of can i eat
	e2c['should'] ='应该'

	#Vocabulary
	e2c['i'] = '我'
	e2c['he'] = '他'
	e2c['she'] = '她'
	e2c['him'] = '他'
	e2c['her'] = '她'
	e2c['us'] = '我们'
	e2c['we'] = '我们'
	e2c['they'] = '他们'
	e2c['them'] = '他们'		
	e2c['it'] = '它'
	e2c['eat'] = '吃'
	e2c['eats'] = '吃'
	e2c['ate'] = '吃'
	e2c['eating'] = '吃'
	e2c['rice'] = '饭'
	e2c['home'] ='家'
	e2c['very'] = '很'
	e2c['pretty'] = '漂亮'
	e2c['drinks'] = '喝'
	e2c['drank'] = '喝'
	e2c['drink'] = '喝'
	e2c['drinking'] = '喝'
	e2c['tired'] = '累'
	e2c['want'] = '要'
	e2c['wanted'] = '要'
	e2c['go'] = '去'
	e2c['food'] = '食物'
	e2c['beer'] = '酒'
	e2c['come'] = '来'
	e2c['close'] = '关闭'
	e2c['already'] = '已经'
	e2c['yesterday'] = '昨天'
	e2c['today'] = '今天'
	e2c['tomorrow'] = '明天'
	e2c['later'] = '以后'
	e2c['make'] = '做'
	e2c['makes'] = '做'
	e2c['made'] = '做'
	#i am making rice
	e2c['david'] ='大卫' 
	e2c['brandon'] ='布兰登'
	e2c['right now'] ='现在'
	e2c['school'] ='学校'
	e2c['noodles'] ='面'
	e2c['tired'] ='累'
	e2c['love'] ='爱'
	e2c['loves'] ='爱'
	e2c['loved'] ='爱'
	e2c['you'] ='你'
	e2c['hi'] ='你好'
	e2c['hello'] ='你好'
	e2c['me'] ='我'
	e2c['who'] ='谁'
	e2c['what'] ='什么'
	e2c['how'] ='如何'
	e2c['why'] ='为什么'
	e2c['when'] ='何时'
	e2c['are'] ='是'
	e2c['am'] ='是'
	e2c['is'] ='是'
	e2c['girl'] ='女孩'
	e2c['boy'] ='男孩'
	e2c['good'] ='好'
	e2c['water'] ='水'

	#there are two ands in chinese he and gen. 
	#Not sure if interchangeable -doesn't seem like it
	#if not interchangeable, the program would have to read the surrounding
	#text and make a decision about which one to use
	
	#e2c['do'] = ''
	# there are two solutions to get rid of the do problem
	# the first is to have the chinese translation output the second VBP
	#the second is to set e2c['do'] = whatever the other verb in the sentence is.
	
	#if tagged[i][0] == 'do':
			#tagged[i] = ('do', 'VBP')


	#should is equated with tag MD, which happens to be the same one for "can"
	#this code needs to be fixed

	#牠 - him or it for dieties
	#祂 - him or it for animals


	translated = ''

	for r in rule:
		if r in to_translate:
			temp = to_translate[r]
			popped = temp.pop(0)
			to_translate[r] = temp
			translated += e2c[popped]
		else:
			translated += e2c[r]

	return translated


	#things to ask: wo zhai jia chi le fan or wo zhai jia fan chi le

def unit_test_all():
	assert english_to_chinese("I want to eat rice") == '我要吃饭'
	assert english_to_chinese("i eat rice") == '我吃饭'
	assert english_to_chinese("i ate rice") == '我饭吃了'
	assert english_to_chinese("i will eat rice") =='我会吃饭'
	assert english_to_chinese("i love you") =='我爱你'
	assert english_to_chinese("i am tired") =='我累'
	assert english_to_chinese("i will eat") =='我会吃'
	assert english_to_chinese("who am i") =='我是谁'
	assert english_to_chinese("what am i") =='我是什么'
	assert english_to_chinese("the girl eats") =='女孩吃'
	assert english_to_chinese("the girl eats rice") =='女孩吃饭'
	#assert english_to_chinese("") ==''
	#assert english_to_chinese("") ==''
	#assert english_to_chinese("") ==''
	#assert english_to_chinese("") ==''

	print 'all unit tests complete. success.'

if __name__ == "__main__":
	unit_test_all()
	#phrase = "she is eating rice."
	phrase = "i eat rice"
	print english_to_chinese(phrase)

	#ChineseGrammar
	#i am pretty and smart - the "and" should be gen
	# i eat rice and drink water - use "he"
	#wo chi le fan he he le sui 
	#wo fan chi le
	#wo yi jian xiang chu UCLA
	#wo zuo tian xiang yao chi fan - i wanted to eat yesterday
	# wo ming tian hui xiang yao chi fan
	# wo ming tian hui yao chu chi fan
	# no commas after time or location phrases. 
	#commas are used to connect complete sentences
	#that are related to one another
