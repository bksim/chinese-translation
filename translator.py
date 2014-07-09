#!/usr/bin/python
# -*- coding: utf-8 -*-
import nltk
import sys
import os.path
reload(sys)
sys.setdefaultencoding('utf8')

def load_dictionary(fn):
	dictionary = {}
	with open(fn) as f:
		for line in f:
			line = line.replace('\r', '')
			chinese, pinyin, defn = line.rstrip('\n').split('\t')
			trad = chinese.split(' ')[0]
			simp = chinese.split(' ')[1]
			if defn in dictionary:
				dictionary[defn] = dictionary[defn] + [(trad, simp, pinyin)]
			else:
				dictionary[defn] = [(trad, simp, pinyin)]
	print "dictionary loaded"
	return dictionary

def match_rule(pos):
	e2c_rules = {}


	# negative sentences
	# how can we put I can't eat or I cannot eat.
	#Please have the code output punctuation marks

	#Things to Fix
	e2c_rules['IN', 'EX'] = ['Come', 'LocationParticleHere']
	e2c_rules['IN-GO', 'EX'] = ['Go', 'LocationParticleThere']
	#^These two are the same format on the left hand side. So the latter one is always gonna
	#overwrite the first one. Is there any way to hard code this?
	#The easiest way to fix this is just to hard code it. There's no other variation or case 
	#in which u will use these two than the current one. 

	e2c_rules['PRP', 'MD', 'VBP', 'NN','IN','NN'] = ['PRP', 'FutureParticle','PresentPerfectParticle','NN','VBP', 'NN']
	# i will eat rice at home. The word for rice and home is interchanged- since it's the same tag, 
	#the program doesn't know how to differentiate

	#e2c_rules['PRP','MD','VBP','PRP','RB'] = ['PRP','RB','FutureParticle','VBP']
	#i will do it later: wo yi hou hui zhuo - not sure why this doesn't work


	#e2c_rules['PRP', 'VBP', 'TO', 'VBP', 'CC', 'VB'] = ['PRP', 'VBP', 'VBP','Also', 'VBP' , 'VB'] #I want to eat and sleep															 #I want to eat and sleep
	#i want to eat and sleep - too many VPB- messing the program up

	

	#if u try to enter a word that isn't in the dictionary, it returns
	# an internal sevice error. It should display we currently cannot provide
	#a translation. also, we need to reference a dictionary for random words
	
	#we need to add the romanization to the chinese translation -how?
	#should we make the translation bigger and centered? -#design question


	#e2c['do'] = ''
	# there are two solutions to get rid of the do problem
	# the first is to have the chinese translation output the second VBP
	#the second is to set e2c['do'] = whatever the other verb in the sentence is.
	
	#if tagged[i][0] == 'do':
			#tagged[i] = ('do', 'VBP')

	#e2c_rules[ 'VBP', 'PRP', 'VB','TO', 'VBP'] = ['PRP', 'DoDesire','VBP', 'QuestionParticle']
	#^ this is what i thought the mapping for: "do you want to eat: ni yao chi ma" should be. It doesn't work




	#SingleWord
	e2c_rules['NN'] = ['NN']
	e2c_rules['VBP'] = ['VBP']
	e2c_rules['PRP'] = ['PRP']
	e2c_rules['VBD'] = ['VBD']
	e2c_rules['JJ'] = ['JJ']
	e2c_rules['RB'] = ['RB']
	e2c_rules['CD'] = ['CD']
	

	#SVO
	e2c_rules['PRP','VBP','NN'] = ['PRP','VBP','NN'] #i eat rice: wo chi fan
	e2c_rules['PRP','VBZ','NN'] = ['PRP','VBZ','NN'] #he eats rice: ta chi fan
	e2c_rules['PRP','VBD','NN'] = ['PRP','NN','VBD','PastParticle'] #i ate rice: wo ba fan chi le
	e2c_rules['PRP','MD','VB','NN'] = ['PRP','FutureParticle','VB', 'NN'] #i will eat rice: wo hui chi fan
	e2c_rules['PRP','VBZ','VBG','NN'] = ['PRP','PresentPerfectParticle', 'VBG', 'NN'] #i am eating rice: wo zai chi fan
	#I am eating rice doesn't work properly
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
	e2c_rules['PRP','UH','NOT-MD','VBN'] = ['PRP','not', 'VBN'] # i am not tired : wo bu lei
	e2c_rules['PRP','UH','VBN'] = ['PRP','VBN'] # i am tired : wo lei
	e2c_rules['PRP','UH','NOT-MD','JJ'] = ['PRP','not', 'JJ'] # i am not pretty : wo bu lei
	e2c_rules['PRP','UH','RB','VBN'] = ['PRP','very','VBN'] # i am very tired : wo hen lei
	e2c_rules['PRP','UH','NOT-MD','RB','VBN'] = ['PRP','not','is' ,'very','VBN'] #i am not very tired
	e2c_rules['PRP','UH','RB','JJ'] = ['PRP','very','JJ'] # i am very tired : wo hen lei
	e2c_rules['PRP','UH','NOT-MD','RB','JJ'] = ['PRP','not','is' ,'very','JJ'] #i am not very pretty
	e2c_rules['PRP','UH','RB','VBN', 'CC', 'RB', 'JJ'] = ['PRP','very','VBN','Also','very','JJ'] # i am very tired and very hungry : wo hen lei
	#the above has output error not utf8
	e2c_rules['PRP','VBZ','VBN'] = ['PRP','VBN'] #she is tired
	e2c_rules['PRP','VBZ','NOT-MD','VBN'] = ['PRP','NOT-MD', 'VBN'] #she is not tired
	e2c_rules['PRP','VBZ','JJ'] = ['PRP','JJ'] #she is pretty
	
	e2c_rules['PRP','VBZ','NOT-MD', 'JJ'] = ['PRP','NOT-MD','JJ'] #she is not pretty
	
	#this responds as ta hen lei
	e2c_rules['PRP','VBZ','RB','VBN'] = ['PRP','very','VBN'] #she is very tired
	e2c_rules['PRP','VBZ','NOT-MD','RB', 'VBN'] = ['PRP','NOT-MD','is','very','VBN'] #she is not very tired
	e2c_rules['PRP','VBZ','RB','JJ'] = ['PRP','very','JJ'] #she is very tired
	e2c_rules['PRP','VBZ','NOT-MD','RB', 'JJ'] = ['PRP','NOT-MD','is','very','JJ'] #she is not very pretty
	#this is improper grammar


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
	e2c_rules['PRP','VBD','TO','VBP', 'NN'] = ['PRP', 'NN','want','VBP', 'PastParticle']
	#e2c_rules['PRP','VBD','NN'] = ['PRP', 'want','VBP', 'PastParticle'] # i wanted to eat

	# some research needs to be done on this: it seems like chinese past desire is equivalent to the
	#"already tense in english present tense"

	#Commands
	e2c_rules['IN-GO', 'IN'] = ['Out','Go']
	e2c_rules['IN-GO','NN'] = ['Go','NN'] 
	e2c_rules['VBP','NN'] = ['VBP','NN'] #Eat rice: chi fan
	e2c_rules['VBP','PRP'] = ['VBP','PRP'] #hit him doesnt work
	#eat it doesnt work
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
	

	#LocationDescriptors
	e2c_rules['PRP','VBD','IN','NN'] = ['PRP','PresentPerfectParticle','NN','VBD','PastParticle'] # i ate at home: wo chai jia li chi le
	e2c_rules['PRP','VBD','NN','IN','NN'] = ['PRP','PresentPerfectParticle','NN','VBD','PastParticle', 'NN'] # i ate rice at home: wo chai jia li chi le fan
	e2c_rules['PRP','MD','VBP','IN','NN'] = ['PRP', 'FutureParticle','PresentPerfectParticle','NN','VBP'] # I will eat at home: wo hui zhai jia chi



	#Questions
	e2c_rules['WP','VBP','PRP'] = ['PRP','VBP','WP'] #who are you: ni shi shei?
	e2c_rules['WP','UH','PRP'] = ['PRP','UH','WP'] #who am i: wo shi shei?
	e2c_rules['WP','VBZ','PRP' ] = ['PRP','VBZ','WP'] #who is he: ta shi shei?
	e2c_rules['WP','VBZ','NN'] = ['NN','VBZ','WP'] #what is rice: fan shi she me?
	e2c_rules['WRB','CAN-MD','VB', 'VBP', 'NN' ] = ['VB','how', 'CAN-MD','VBP','NN'] #how can i eat rice: wo ze me nen chi fan
	e2c_rules['WRB','CAN-MD','VB', 'VBP' ] = ['VB','how', 'CAN-MD','VBP'] #how can i eat
	e2c_rules['CAN-MD','PRP', 'VBP', 'NN' ] = ['PRP','CAN-MD','VBP','NN','QuestionParticle'] #can i eat rice
	e2c_rules['CAN-MD','PRP', 'VBP' ] = ['PRP','CAN-MD','VBP','QuestionParticle'] #can i eat rice
	e2c_rules['VBP','PRP', 'VBD' ] = ['PRP','VBD','QuestionParticle']

	#e2c_rules['MD','PRP','VBP' ] = ['PRP','VBP','WP']


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
	e2c_rules['NN','CC','NN','MD','VBP'] = ['NN', 'AndParticle' ,'NN', 'FutureParticle', 'VBP'] #David and brandon will eat
	e2c_rules['NN', 'CC', 'NN', 'VBP'] = ['NN', 'AndParticle' ,'NN', 'VBP'] #david and brandon eat
	e2c_rules['NN', 'CC', 'NN', 'VBP', 'NN'] = ['NN', 'AndParticle' ,'NN', 'VBP', 'NN'] #david and brandon eat rice
	e2c_rules['NN', 'CC', 'NN', 'MD', 'VBP', 'NN'] = ['NN', 'AndParticle' ,'NN', 'MD', 'VBP', 'NN'] #david and brandon will eat rice
	#in the above it gives jiang as will but without rice, the same sentence gives the correct future particle
	#either delete the word will from source dictionary or when code grabs source dictionary replace input jiang with hui
	e2c_rules['NN', 'CC', 'NN', 'VBD', 'NN'] = ['NN', 'AndParticle' ,'NN', 'NN','VBD','PastParticle'] #david and brandon ate rice
	e2c_rules['NN', 'CC', 'NN', 'VBD'] = ['NN', 'AndParticle' ,'NN', 'VBD','PastParticle'] #David and Brandon ate

	e2c_rules['NN', 'CC', 'NN', 'VBP', 'JJ','NN'] = ['NN', 'AndParticle' ,'NN', 'VBP', 'JJ', 'NN'] #david and brandon eat sweet rice
	e2c_rules['NN', 'CC', 'NN', 'VBD', 'JJ', 'NN'] = ['NN', 'AndParticle' ,'NN', 'JJ','NN','VBD','PastParticle'] #david and brandon ate sweet rice
	e2c_rules['NN', 'CC', 'NN', 'MD', 'VBP', 'JJ','NN'] = ['NN', 'AndParticle' ,'NN', 'MD', 'VBP', 'JJ', 'NN'] #david and brandon will eat sweet rice
	#Negative Sentences
	e2c_rules['PRP', 'CAN-MD', 'RB', 'VBP'] = ['PRP','not','can', 'VBP'] 
	#i can not eat
	e2c_rules['PRP', 'CAN-MD', 'RB', 'VBP', 'NN'] = ['PRP','not','can', 'VBP', 'NN']
	#i can not eat rice
	#e2c_rules['PRP', 'VBP', 'RB', 'VBP'] = ['PRP','not','VBP'] # i do not eat
	#Because there are two VBP, the translation takes the first VBP
	
	#Uncategorized 

	e2c_rules['DT', 'NN', 'VBZ'] = ['NN', 'VBZ'] #the girl eats: nu hai chi
	e2c_rules['PRP', 'VBP','DT', 'JJ', 'NN'] = ['PRP', 'VBP','JJ', 'NN'] #i love the pretty girl
	e2c_rules['PRP', 'VBZ','DT', 'JJ', 'NN'] = ['PRP', 'VBZ','JJ', 'NN'] #he loves the pretty girl
	e2c_rules['PRP', 'MD', 'VBP','DT', 'JJ', 'NN'] = ['PRP', 'FutureParticle', 'VBP','JJ', 'NN'] #he will love the pretty girl


	#e2c_rules['PRP', 'VBD','DT', 'JJ', 'NN'] = ['PRP', 'VBD','JJ', 'NN'] #i loved the pretty girl
	#need to check on the grammar about this 
	e2c_rules['PRP', 'MD', 'VB','DT', 'JJ', 'NN'] = ['PRP', 'FutureParticle', 'VB','JJ', 'NN'] #i will love the pretty girl

	e2c_rules['DT', 'NN', 'VBZ', 'NN'] = ['NN', 'VBZ', 'NN'] #the girl eats rice: nu hai chi fan
	#e2c_rules['DT', 'NN', 'VBZ', 'JJ'] = ['NN', 'am', 'JJ', 'PossesiveParticle']
	#the shirt is blue conflcits with the boy is happy - the grammar for the chinese is different
	e2c_rules['DT', 'NN', 'VBZ', 'NNS'] = ['NN', 'VBZ', 'NNS'] #the girl eats noodles: nu hai chi mien
	e2c_rules['PRP', 'VBP', 'PRP'] = ['PRP','VBP','PRP'] #i love you: wo ai ni
	e2c_rules['PRP', 'VBD', 'PRP'] = ['PRP','VBD','PastParticle', 'PRP']
	e2c_rules['PRP', 'VBZ', 'PRP$'] = ['PRP','VBZ','PRP$'] # he loves her: ta ai ta
	e2c_rules['PRP', 'VBZ', 'PRP'] = ['PRP','VBZ','PRP'] #he loves them: ta ai ta men
	e2c_rules['PRP', 'VBP', 'TO', 'VBP'] = ['PRP', 'VBP', 'VBP'] # I want to eat: wo xiang yao chi
	

	e2c_rules['PRP', 'VBP', 'TO', 'VBP', 'NN'] = ['PRP', 'VBP', 'VBP', 'NN'] # I want to eat rice: wo xiang yao chi fan
	e2c_rules['PRP', 'RB', 'VBP', 'TO', 'VBP', 'NN'] = ['PRP','Also' ,'VBP', 'VBP', 'NN'] #I also want to eat rice
	e2c_rules['PRP', 'RB', 'VBP', 'TO', 'VBP'] = ['PRP','Also' ,'VBP', 'VBP'] #I also want to eat 
	e2c_rules['WP', 'VBP', 'PRP', 'VBG'] = ['PRP', 'VBG','what'] #What are you doing: ni zai zuo se ma
	e2c_rules['WP', 'VBD', 'PRP', 'VBP'] = ['PRP','VBD','PastParticle', 'what'] #what did you do
	e2c_rules['WP', 'MD', 'PRP', 'VB'] = ['PRP','FutureParticle','VB', 'what'] # ni hui zuo se me
	#the boy loves the girl- code this later - will be a less commonly used expression
	
	#2NounVerb
	e2c_rules['VBD', 'CC', 'NN', 'VBP'] = ['VBD','AndParticle','NN', 'VBP' ] #david and brandon eat
	e2c_rules['VBD', 'CC', 'NN','MD','VBP'] = ['VBD','AndParticle','NN','FutureParticle','VBP' ] #david and brandon will eat
	e2c_rules['VBD', 'CC', 'NN','VBD'] = ['VBD','AndParticle','NN','VBD', 'PastParticle' ] #david and brandon ate
	e2c_rules['VBD', 'CC', 'NN', 'VBP', 'NN'] = ['VBD','AndParticle','NN', 'VBP', 'NN' ] #david and brandon eat rice
	e2c_rules['VBD', 'CC', 'NN', 'VBP','JJ' ,'NN'] = ['VBD','AndParticle','NN', 'VBP','JJ' ,'NN' ] #david and brandon eat sweet rice
	e2c_rules['VBD', 'CC', 'NN','MD','VBP','NN'] = ['VBD','AndParticle','NN','FutureParticle','VBP', 'NN' ] #david and brandon will eat rice
	e2c_rules['VBD', 'CC', 'NN','MD','VBP','JJ', 'NN'] = ['VBD','AndParticle','NN','FutureParticle','VBP', 'JJ', 'NN' ] #david and brandon will eat rice

	#may need to change VBD to NN - this is incorrect tagging 
	e2c_rules['VBD', 'CC', 'NN','VBZ', 'NN'] = ['VBD','AndParticle','NN','NN', 'VBZ', 'PastParticle' ] #david and brandon ate rice
	#doesn't work

	#Compound Sentence
	e2c_rules['PRP', 'VBP','NN' ,'CC', 'NN','NN'] = ['PRP', 'VBP','NN', 'AndParticle','NN', 'NN'] #i eat rice and drink water
	e2c_rules['PRP', 'MD', 'VBP','NN' ,'CC', 'NN','NN'] = ['PRP', 'FutureParticle', 'VBP','NN', 'AndParticle','NN', 'NN'] #i eat rice and drink water
	#e2c_rules['PRP', 'VBD','NN' ,'CC', 'NN','NN'] = ['PRP', 'NN','VBD','PastParticle', 'AndParticle','NN', 'NN', 'PastParticle']
	#^ same issue as with past tense

	e2c_rules['PRP', 'VBZ','NN' ,'CC', 'NNS','NN'] = ['PRP', 'VBZ','NN', 'AndParticle','NNS', 'NN'] #i eat rice and drink water
	e2c_rules['PRP', 'MD', 'VBZ','NN' ,'CC', 'NNS','NN'] = ['PRP', 'FutureParticle', 'VBZ','NN', 'AndParticle','NNS', 'NN'] #i eat rice and drink water
	e2c_rules['PRP', 'VBD','NN' ,'CC', 'NNS','NN'] = ['PRP', 'NN','VBD','PastParticle', 'AndParticle','NN', 'NNS', 'PastParticle']
	#^she ate rice and drank water - drank and water are interchanged regardles of changing the rul
	

	e2c_rules['DT', 'JJ','NN' ,'VBZ'] = ['JJ', 'NN', 'VBZ'] #piao liang nu hai chi
	e2c_rules['DT', 'JJ','NN' ,'VBZ', 'JJ', 'NN'] = ['JJ', 'NN', 'VBZ', 'JJ', 'NN'] #the pretty girl eats sweet rice
	e2c_rules['DT', 'NN' ,'VBZ', 'JJ', 'NN'] = ['NN', 'VBZ', 'JJ', 'NN'] #the girl eats sweet rice
	e2c_rules['PRP','VBP', 'JJ', 'NN'] = ['PRP', 'VBP', 'JJ', 'NN'] #they eat sweet rice


	#e2c_rules['PRP','UH', 'DT', 'NN'] = ['PRP', 'UH', 'DT', 'NN'] #I am a boy
	#'DT' doesn't reflect  "a"

	e2c_rules['WRB','VBP', 'PRP'] = ['PRP', 'good', 'QuestionParticle'] #How are you?
	e2c_rules['WRB','VBZ', 'PRP'] = ['PRP', 'good', 'QuestionParticle'] #How is she
	e2c_rules['WRB','JJ', 'VBZ', 'PRP'] = ['PRP', 'AmountParticle', 'JJ'] #How pretty is she?
	e2c_rules['WRB','JJ', 'VBP', 'PRP'] = ['PRP', 'AmountParticle', 'JJ'] #How pretty are they?



	#e2c_rules['WRB','MD', 'VB', 'VBP'] = ['VB', 'CanQuestion', 'VBP'] #How can I eat
	e2c_rules['WRB', 'MD', 'PRP', 'VBP'] = ['PRP', 'should','CanQuestion','VBP'] #How should I eat?
	#^Currently it retruns wo zen me chi: A better return would be: wo ing gai zen me chi-although this does work
	#the code should have it return ing gai- but it doesnt- im guessing its a characteristic of the language tag
	e2c_rules[ 'MD', 'PRP', 'VBP'] = ['PRP', 'should','VBP', 'QuestionParticle'] #Should I eat?
	e2c_rules[ 'WP', 'MD', 'VB', 'VBP'] = ['VB', 'should','VBP', 'WP'] #What should I eat?
	#How should I eat worked properly before when Should I eat didn't work. The current reverse case is true too.

	
	e2c_rules[ 'VB', 'JJ'] = ['PRP', 'should','VBP', 'QuestionParticle']
	#e2c_rules['VBD', 'CC', 'NN','VBD', 'JJ', 'NN'] = ['VBD','AndParticle','NN','JJ', 'NN', 'VBZ', 'PastParticle' ] #david and brandon ate sweet rice
	#this doesn't work. An exception needs to be coded

	e2c_rules[ 'PRP', 'UH', 'JJ', 'CC', 'JJ'] = ['PRP', 'JJ','AndAdjective', 'JJ'] #i am pretty and smart
	#but and #and are both CC so i am pretty and smart and i am pretty but smart output the same thing- problematic

	e2c_rules[ 'PRP', 'UH', 'VBG', 'NN'] = ['PRP', 'PresentPerfectParticle','DoParticle', 'NN'] #I am making rice
	e2c_rules[ 'VBP', 'PRP', 'VBG', 'NN'] = ['PRP', 'PresentPerfectParticle','DoParticle', 'NN', 'QuestionParticle']
	
	#TestingWithDictionary
	e2c_rules[ 'PRP', 'VBP', 'NNS'] = ['PRP','VBP','DoParticle', 'NNS'] #I read books
	#this is wrong
	e2c_rules[ 'PRP', 'VBP', 'TO', 'VB'] = ['PRP','LikeParticle', 'VB'] # I like to sleep -check again once UTF-8 works
	
	e2c_rules[ 'PRP', 'VBPLIKE', 'TO', 'VBP'] = ['PRP','LikeParticle', 'VBP']

	#New Rules
	#e2c_rules[ 'PRP', 'VBP', 'RB'] = ['PRP','VBP', 'RB']
	#wo kuai chi or wo chi kuai?

	e2c_rules[ 'DT', 'NN', 'VBZ', 'JJ'] = ['NN','JJ'] #the food is spicy
	e2c_rules[ 'HAVE', 'PRP', 'VBP'] = ['PRP','VBP', 'PastParticle', 'QuestionParticle'] #Have you drank?
	e2c_rules[ 'HAVE', 'PRP', 'VBN'] = ['PRP','VBP', 'PastParticle', 'QuestionParticle']
	#Have you eaten?

	e2c_rules[ 'PRP', 'VBP','TO', 'VB', 'DT', 'NN'] = ['PRP','want', 'VB', 'NN'] #i want to see a movie
	#e2c_rules[ 'PRP', 'VBP','TO', 'IN-GO', 'TO', 'NN'] = ['PRP','want', 'Go', 'NN'] 
	#i want to go to school - it reads input "go" as "can"
	#work can be noun and verb

	e2c_rules[ 'PRP', 'UH', 'RB', 'JJ'] = ['PRP','very', 'JJ']

	
	e2c_rules[ 'PRP', 'VBPLIKE', 'TO', 'VBP'] = ['PRP','LikeParticle', 'VBP']
	e2c_rules[ 'PRP', 'VBPLIKE', 'NN'] = ['PRP','LikeParticle', 'NN'] # i like rice
	e2c_rules[ 'PRP', 'VBPHOPE', 'PRP', 'VBP', 'JJ'] = ['PRP','HopeParticle', 'PRP', 'JJ'] #i hope you are happy
	e2c_rules[ 'PRP', 'VBPLIKE', 'PRP'] = ['PRP','LikeParticle', 'PRP']
	e2c_rules[ 'DT', 'NN', 'CC', 'NN', 'VBP', 'JJ'] = ['NN','AndParticle','NN', 'PRP', 'JJ']
	e2c_rules[ 'DT', 'NN', 'CC', 'NN', 'VBP', 'RB' ,'JJ'] = ['NN','AndParticle','NN', 'PRP', 'very','JJ']
	e2c_rules[  'WRB', 'VBP', 'PRP', 'VBG'] = ['PRP','when','VBG']
	e2c_rules[  'WRB', 'VBZ', 'PRP', 'VBG'] = ['PRP','when','VBG']      
	e2c_rules[  'PRP', 'VBP', 'PRP', 'VBP', 'JJ'] = ['PRP','think','PRP', 'JJ'] 
	e2c_rules[  'PRP', 'VBP', 'PRP', 'VBZ', 'JJ'] = ['PRP','think','PRP', 'JJ'] 
	e2c_rules[  'PRP', 'VBP', 'PRP', 'VBZ','RB' ,'JJ'] = ['PRP','think','PRP','RB','JJ'] 
	e2c_rules[  'PRP', 'VBP', 'PRP', 'VBP','RB' ,'JJ'] = ['PRP','think','PRP','RB','JJ'] 
	e2c_rules[  'PRP', 'CAN-MD', 'VBP'] = ['PRP','can','VBP'] # I can eat
	e2c_rules[  'PRP', 'CAN-MD','NOT-MD', 'VBP'] = ['PRP','not', 'can','VBP'] #I can not eat
	e2c_rules[  'PRP', 'CAN-MD','NOT-MD', 'VBP', 'NN'] = ['PRP','not', 'can','VBP', 'NN'] #I can not eat rice
	e2c_rules[  'PRP', 'CANNOT-MD', 'VBP'] = ['PRP','not', 'can','VBP'] #I cannot eat
	e2c_rules[  'PRP', 'CANNOT-MD', 'VBP', 'NN'] = ['PRP','not', 'can','VBP', 'NN'] #I cannot eat rice
	e2c_rules[  'PRP', 'CAN-MD', 'VBP', 'NN'] = ['PRP','can','VBP','NN'] #I can eat rice
	e2c_rules[  'PRP', 'UH', 'DT', 'NN'] = ['PRP','is','NN'] #I am a cat
	e2c_rules[  'PRP', 'UH', 'RB', 'DT', 'NN'] = ['PRP','not','is','NN'] #I am not a cat
	e2c_rules[  'PRP', 'UH', 'RB', 'DT','JJ' ,'NN'] = ['PRP','not','is','JJ', 'NN'] #I am not a pretty cat
	e2c_rules[  'PRP', 'UH', 'DT','JJ','NN'] = ['PRP','is','JJ', 'NN'] #I am a pretty cat
	e2c_rules[  'PRP', 'UH', 'NOT-MD', 'DT','JJ','NN'] = ['PRP','NOT-MD','is','JJ', 'NN'] #I am not a pretty cat
	e2c_rules[  'PRP', 'UH', 'NOT-MD', 'DT','NN'] = ['PRP','NOT-MD', 'is', 'NN'] #I am not a cat
	e2c_rules[  'PRP', 'VBZ', 'NOT-MD', 'DT','NN'] = ['PRP','NOT-MD','is', 'NN'] #He is not a cat
	e2c_rules[  'PRP', 'VBZ', 'NOT-MD', 'DT','JJ', 'NN'] = ['PRP','NOT-MD','is','JJ', 'NN'] #He is not pretty a cat
	e2c_rules[  'PRP', 'VBZ', 'DT','JJ','NN'] = ['PRP','is','JJ', 'NN'] #He is a pretty cat
	e2c_rules[  'PRP', 'VBZ', 'DT', 'NN'] = ['PRP','is','NN'] #He is a cat
	e2c_rules[  'WRB', 'VBP', 'PRP', 'VBG', 'TO', 'VB'] = ['PRP','when','want', 'VB']
	e2c_rules[  'WP', 'NN', 'VBP', 'PRP', 'VBG','TO', 'VB'] = ['PRP','WhatTime','want', 'VB']
	#What time do you want to sleep? - just hardcode this - too much work to go back and make special tag for every sntence tha has want
	e2c_rules[  'WP', 'NN', 'VBP', 'PRP', 'VBG', 'TO', 'VB'] = ['PRP','WhatTime','FutureParticle', 'VB']
	e2c_rules[  'VBP', 'PRP', 'RB', 'VBN'] = ['PRP','really','very', 'VBN', 'QuestionParticle']
	e2c_rules[  'PRP', 'VBZ', 'VBG'] = ['PresentPerfectParticle','VBG']
	e2c_rules[  'UH', 'PRP', 'JJ'] = ['PRP', 'JJ', 'QuestionParticle']
	e2c_rules[  'VBP', 'PRP', 'JJ'] = ['PRP', 'JJ', 'QuestionParticle']
	
	e2c_rules[  'UH', 'PRP', 'RB', 'JJ'] = ['PRP', 'RB', 'JJ', 'QuestionParticle']
	e2c_rules[  'VBP', 'PRP', 'RB', 'JJ'] = ['PRP', 'RB', 'JJ', 'QuestionParticle']
	#e2c_rules[  'WP', 'VBP', 'PRP', 'VBG'] = ['PRP', 'VBG', 'what']
	#e2c_rules[  'WP', 'VBP', 'PRP', 'VBG'] = ['PRP','PresentPerfectParticle' ,'VBG', 'what']
	e2c_rules['WP', 'VBP', 'PRP', 'VBG', 'RB'] = ['PRP', 'PresentPerfectParticle', 'VBG','what'] #What are you doing 
	#How to say I thought you are pretty - does this grammar even exist?
	e2c_rules['NN', 'POS', 'JJ'] = ['NN', 'JJ'] #Jenny's pretty
	e2c_rules['PRP', 'VBPLIKE', 'TO', 'VB', 'NN'] = ['PRP', 'LikeParticle', 'hit', 'NN' ] #Jenny's pretty
	e2c_rules['PRP', 'VBPLIKE', 'NNS', 'CC', 'PRP', 'VBP', 'DT', 'RB', 'JJ'] = ['PRP', 'LikeParticle', 'NNS', 'But','TheyObjects' , 'is', 'have', 'a little', 'JJ' ] # I like strawberries but they are a little sweet
	#Check to see if this or dan shi tan men you yi dian tian is more natural- then write an assertion accordingly
	#they particle cahnges depending on male female or unanimated
	e2c_rules['PRP', 'VBZ', 'JJ', 'CC', 'PRP', 'VBZ', 'RB', 'JJ'] = ['PRP', 'JJ', 'But','is', 'PRP' , 'also', 'JJ' ] #She is pretty but she is also stupid
	e2c_rules['PRP', 'VBZ', 'JJ', 'CC', 'JJ'] = ['PRP', 'JJ', 'But', 'JJ' ] #she is pretty but stupid
	
	#e2c_rules['PRP', 'VBZ', 'JJ', 'CC', 'PRP', 'VBZ', 'RB', 'JJ'] = ['PRP', 'JJ', 'Also', 'PRP' , 'also', 'JJ' ] #She is pretty but she is also stupid
	e2c_rules['PRP', 'VBZ', 'JJ', 'CC', 'JJ'] = ['PRP', 'JJ', 'Also', 'JJ' ] #she is pretty but stupid
	#if the above two are uncommented the previous two return assertion error
	# the two sentences are: she is pretty and stupid
	#she is pretty and she is stupid
	#if you try to put she is pretty and stupid with the two current e2c rules it returns as she is pretty but stupid and likewise for the second case
	#if you comment otu the assertions, u get output error not utf8 and a 4 shows up

	e2c_rules['PRP', 'RB', 'VBPLIKE', 'NN'] = ['PRP', 'only', 'LikeParticle', 'NN' ] # i only like rice
	e2c_rules['PRP', 'RB', 'VBPLIKE', 'PRP'] = ['PRP', 'only', 'LikeParticle', 'PRP' ] # i only like him
	e2c_rules['PRP', 'RB', 'VBPLIKES', 'PRP'] = ['PRP', 'only', 'LikeParticle', 'PRP' ] # he only likes him
	e2c_rules['PRP', 'RB', 'VBPLIKES', 'NN'] = ['PRP', 'only', 'LikeParticle', 'NN' ] # he only likes rice
	e2c_rules['PRP', 'VBPLIKES', 'NN'] = ['PRP', 'LikeParticle', 'NN' ] # he likes rice
	e2c_rules['PRP', 'VBPLIKES', 'PRP'] = ['PRP', 'LikeParticle', 'PRP' ] # he likes you
	e2c_rules['PRP', 'RB', 'VBZ', 'NN'] = ['PRP', 'only', 'VBZ', 'NN' ] # he only eats rice
	e2c_rules['PRP', 'RB', 'VBZ'] = ['PRP', 'only', 'VBZ'] # he only eats 
	e2c_rules['PRP', 'RB', 'VBP', 'NN'] = ['PRP', 'only', 'VBP', 'NN' ] # i only eat rice
	e2c_rules['PRP', 'RB', 'VBP'] = ['PRP', 'only', 'VBP' ] # i only eat 
	e2c_rules['VBP', 'JJR'] = ['VBP', 'AmountParticle', 'a little' ] # eat more
	e2c_rules['VBP', 'JJR', 'NN'] = ['VBP', 'AmountParticle', 'a little', 'NN' ] # eat more rice
	#e2c_rules['VBP', 'JJR'] = ['VBP', 'LessAmountParticle', 'a little' ] # eat more
	#e2c_rules['VBP', 'JJR', 'NN'] = ['VBP', 'LessAmountParticle', 'a little', 'NN' ] # eat less rice
	# when i try to add less, inputing more reults in translating to less
	#this needs to be asseted when fixed
	e2c_rules['PRP', 'JJR', 'NN'] = ['VBP', 'AmountParticle', 'a little', 'NN' ] #eat a little more rice
	e2c_rules['NN', 'VBZ', 'JJ'] = ['NN', 'JJ' ] #jenny is pretty
	e2c_rules['NN', 'POS', 'IN-GO'] = ['we', 'Go' ] #let's go
	e2c_rules['NN', 'PRP', 'IN-GO'] = ['we', 'Go'] #let us go
	#I'd like to add the aux verb here for the two above but it breaks the code for some reason
	#make an assertion rule when this is fixed
	#might be best just to ahrdcode this - not variation when it comes to these two phrases

	e2c_rules['IN', 'PRP', 'VBP', 'VBN','VBP'] = ['IfParticle', 'PRP', 'VBN', 'VBP' ]
	#If you are tired, eat - needs to be fixed
	if pos in e2c_rules:
		return e2c_rules[pos]
	else:
		return None




def tag(phrase):
	tokens = nltk.word_tokenize(phrase.lower())	
	tagged = nltk.pos_tag(tokens)

	# exceptions
	for i in range(len(tagged)):
		# ate is a past tense verb

		
		if tagged[i][0] == 'can':
			tagged[i] = ('can', 'CAN-MD') #special class for can
		if tagged[i][0] == 'not':
			tagged[i] = ('not', 'NOT-MD') #special class for can
		if tagged[i][0] == 'cannot':
			tagged[i] = ('cannot', 'CANNOT-MD') #special class for can
		if tagged[i][0] == 'tired':
			tagged[i] = ('tired', 'VBN') #special class for can
		

		if tagged[i][0] == 'go':
			tagged[i] = ('can', 'IN-GO') #special class for can


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

		if tagged[i][0] == 'beef':
			tagged[i] = ('beef', 'NN')

		if tagged[i][0] == 'like':
			tagged[i] = ('like', 'VBPLIKE')
		if tagged[i][0] == 'is it':
			tagged[i] = ('is it', 'ISIT')
		if tagged[i][0] == 'david':
			tagged[i] = ('david', 'NN')
		if tagged[i][0] == 'chicken':
			tagged[i] = ('chicken', 'NN')
		if tagged[i][0] == 'cat':
			tagged[i] = ('cat', 'NN')
		if tagged[i][0] == 'happy':
			tagged[i] = ('happy', 'JJ')	
		if tagged[i][0] == 'basketball':
			tagged[i] = ('basketball', 'NN')			
		if tagged[i][0] == 'stawberries':
			tagged[i] = ('strawberries', 'NNS')		
		if tagged[i][0] == 'likes':
			tagged[i] = ('likes', 'VBPLIKES')		

	#pretty is an adjective
		if tagged[i][0] == 'pretty':
			tagged[i] = ('pretty', 'JJ')
		if tagged[i][0] == 'spicy':
			tagged[i] = ('spicy', 'JJ')	
		if tagged[i][0] == 'salty':
			tagged[i] = ('salty', 'JJ')	
		if tagged[i][0] == 'sweet':
			tagged[i] = ('sweet', 'JJ')	
		if tagged[i][0] == 'have':
			tagged[i] = ('have', 'HAVE')
		if tagged[i][0] == 'hope':
			tagged[i] = ('hope', 'VBPHOPE')	
		if tagged[i][0] == 'blue':
			tagged[i] = ('blue', 'JJ')		
		if tagged[i][0] == 'eight':
			tagged[i] = ('eight', 'CD')
		if tagged[i][0] == 'twenty-one':
			tagged[i] = ('twenty-one', 'CD')			
		if tagged[i][0] == 'eleven':
			tagged[i] = ('eleven', 'CD')
		if tagged[i][0] == 'twelve':
			tagged[i] = ('twelve', 'CD')	
		if tagged[i][0] == 'thirteen':
			tagged[i] = ('thirteen', 'CD')
		if tagged[i][0] == 'ugly':
			tagged[i] = ('ugly', 'JJ')	
		if tagged[i][0] == 'hit':
			tagged[i] = ('hit', 'VBP')	
		if tagged[i][0] == 'meeting':
			tagged[i] = ('meeting', 'VBG')
		#if tagged[i][0] == 'sleep':
		#	tagged[i] = ('sleep', 'VBP')
		#want to sleep is VB sleep is VBP
		#if tagged[i][0] == 'less':
			#tagged[i] = ('less', 'JJR')
			#could also be a noun - will have to remove this once we account for multiple parts of speech

	return tagged

# translates a phrase from english to chinese
def english_to_chinese(phrase):
	tagged = tag(phrase)
	print tagged

	words, pos = zip(*tagged)
	pos = list(pos)
	print pos
	punctuation = None
	# remove punctuation
	if pos[-1] == '.' or pos[-1] == '?' or pos[-1] == '!':
		punctuation = words[-1]
		pos.pop()

	if len(pos) == 1:
		rule = match_rule(pos[0])
	else:
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
	e2c['PossesiveParticle'] = ('的', 'de')
	e2c['PastParticle'] = ('了', 'le')
	e2c['FutureParticle'] = ('会', 'hui4')
	e2c['PresentPerfectParticle']= ('在', 'zai')
	e2c['LocationParticleThere']=('那里', 'na4 li3')
	e2c['LocationParticleHere']=('这里', 'ze4 li3')
	e2c['AuxVerb']=('把, ba3')
	e2c['TheyFemale']=('她们', 'ta1 meng2')
	e2c['AndParticle']= ('和', 'he2')
	e2c['not']=('不', 'bu4')
	e2c['QuestionParticle']=('吗', 'ma')
	e2c['know'] =('会', 'hui4')
	e2c['can'] =('能', 'neng2')
	e2c['AmountParticle']=('多', 'duo')
	e2c['Also'] =('也, ye3')
	e2c['AndAdjective'] =('跟', 'gen')
	e2c['LikeParticle'] =('喜欢', 'xi3huan1')
	 #this is different in the traditional
	#When i try to use this likeparticle, it says it is not UTF-8
	e2c['ISIT'] =('什么', 'sen3 me')
	e2c['is'] =('是', 'shi4')



	
	#another word for can is 可以 - which is more
	#appropriate in the case of can i eat
	e2c['should'] =('应该', 'ying1 gai1')
	e2c['CanQuestion'] =('怎么', 'zeng3me')
	e2c['Go'] =('去', 'chu4')
	e2c['Come'] = ('来', 'lai2')
	e2c['Out'] =('出', 'chu1')
	e2c['HopeParticle'] =('希望', 'xi1wang4')
	
	#Hardcode
	#e2c['Go out'] ='出去'
	e2c['But'] =('但', 'dan4')
	


	#Vocabulary
	e2c['i'] = ('我', 'wo3')
	e2c['he'] = ('他', 'ta1')
	e2c['she'] = ('她', 'ta1')
	e2c['him'] = ('他','ta1')
	e2c['her'] = ('她', 'ta1')
	e2c['us'] = ('我们', 'wo3 men2')
	e2c['we'] = ('我们', 'wo3 men2')
	e2c['they'] = ('他们', 'ta1 men2')
	e2c['them'] = ('他们', 'ta1 men2')	
	e2c['it'] =  ('它', 'ta1')
	e2c['eat'] = ('吃', 'chi1')
	e2c['eats'] = ('吃', 'chi1')
	e2c['ate'] = ('吃', 'chi1')
	e2c['eating'] = ('吃', 'chi1')
	e2c['rice'] = ('饭', 'fan4')
	e2c['home'] =('家', 'jia1')
	e2c['very'] = ('很', 'hen3')
	e2c['pretty'] = ('漂亮', 'piao4 liang4')
	e2c['drinks'] = ('喝', 'he1')
	e2c['drank'] = ('喝', 'he1')
	e2c['drink'] = ('喝', 'he1')
	e2c['drinking'] = ('喝', 'he1')
	e2c['tired'] = ('累', 'lei4')
	e2c['want'] = ('要' , 'yao4')
	e2c['wanted'] = ('要' , 'yao4')
	e2c['food'] = ('食物' , 'shi2wu4')
	e2c['beer'] = ('酒', 'jiu3')
	e2c['close'] = ('关', 'guan1')
	e2c['already'] = ('已经', 'yi3jing1')
	e2c['yesterday'] = ('昨天', 'zuo2tian1')
	e2c['today'] = ('今天', 'jing1tian1')
	e2c['tomorrow'] = ('明天', 'ming2tian1')
	e2c['later'] = ('以后', 'yi3hou4')
	e2c['DoParticle'] = ('做', 'zuo4')
	e2c['DoDesire'] = ('要', 'yao4')
	e2c['made'] = ('做', 'zuo4')
	#i am making rice
	e2c['david'] =('大卫' , 'da4 wei2')
	e2c['brandon'] = ('布兰登', 'bu4lan2deng1')
	e2c['right now'] =('现在', 'xian4zai4')
	e2c['school'] =('学校', 'xue2xiao4')
	e2c['noodles'] =('面', 'mian4')
	e2c['tired'] =('累', 'lei4')
	e2c['love'] =('爱', 'ai4')
	e2c['loves'] =('爱', 'ai4')
	e2c['loved'] =('爱', 'ai4')
	e2c['you'] =('你', 'ni3')
	e2c['hi'] =('你好', 'ni3 hao3')
	e2c['hello'] =('你好', 'ni3 hao3')
	e2c['me'] =('我', 'wo3')
	e2c['who'] =('谁', 'shei2')
	e2c['what'] =('什么', 'she3me')
	e2c['how'] =('怎么', 'zen3 me')
	e2c['why'] =('为什么', 'wei4 se3 me')
	e2c['when'] =('什么时候', 'she3meshi2hou4')
	e2c['are'] =('是', 'shi4')
	e2c['am'] =('是', 'shi4')
	e2c['is'] =('是', 'shi4')
	e2c['girl'] =('女孩', 'nǚ3 hái2')
	e2c['boy'] =('男孩', 'nan2 hai2')
	e2c['good'] =('好', 'hao3')
	e2c['well'] =('好', 'hao3')
	e2c['water'] =('水', 'sui3')
	e2c['sleep'] =('睡觉', 'sui4 jiao4')
	e2c['sleeping'] =('睡觉', 'sui4 jiao4')
	e2c['cat'] =('猫', 'mao1')
	
	#homeoverwrite
	e2c['stupid'] =('笨', 'ben4')
	e2c['hungry'] =('饿', 'e4')
	e2c['run'] =('跑', 'pao3')
	e2c['running'] =('跑', 'pao3')
	e2c['fast'] =('快', 'kuai4')
	e2c['quickly'] =('快', 'kuai4')
	e2c['quick'] =('快', 'kuai4')
	#quickly is adverb quick is adjective
	e2c['slowly'] =('慢', 'man4')
	e2c['slow'] =('慢', 'man4')
	e2c['happy'] =('快乐', 'kuai4le4')
	e2c['cute'] =('可爱', 'ke3ai4')
	e2c['sad'] =('伤心', 'shang1xin1')
	e2c['dog'] =('狗', 'gou3')
	e2c['tall'] =('高 ', 'gao1')
	e2c['short'] =('矮', 'ai3')
	e2c['lazy'] =('懒', 'lan3')
	e2c['sings'] =('唱', 'chang4')
	e2c['time'] =('时间', 'shi2jian1')
	e2c['generation'] =('代', 'dai4')
	e2c['forever'] =('永远', 'yong2yuan3')
	e2c['mother'] =('妈', 'ma3ma2')
	e2c['mom'] =('妈妈', 'ma3ma2')
	e2c['dad'] =('爸', 'ba4')
	e2c['father'] =('爸爸', 'ba2ba3')
	#fuqin muqin more formal for mother father
	#e2c['sister'] =('妹妹 ', 'mei4mei') - younger sister
	e2c['brother'] =('哥哥', 'ge1ge1')
	e2c['sister'] =('姐姐', 'jie3jie2')
	#e2c['brother'] =('弟弟', 'di4di4') - younger brother 
	# we should provide feature where it has dropdown menu to choose from
	#brother(younger) or brother(older)
	#there should be a star by the translation to notify that it may be different
	#depending on what they mean
	
 

	#tastes
	e2c['sweet'] =('甜 ', 'tian2')
	e2c['spicy'] =('辣', 'la4')
	e2c['salty'] =('咸 ', 'xian2')
	e2c['bitter'] =('苦', 'ku3')

	#colors
	e2c['blue'] =('蓝色', 'lan2se4')
	e2c['red'] =('红色', 'hong2se4')
	e2c['yellow'] =('黄色', 'huang2se4')
	e2c['green'] =('绿色 ', 'lu4se4') #need to figure out how to make that special u
	e2c['black'] =('黑色', 'heise4')
	e2c['white'] =('白色 ', 'bai2se4')
	e2c['pink'] =('粉红色 ', 'fen3hong2se4')
	e2c['brown'] =('棕色', 'zong1se4')
	e2c['purple'] =('紫色', 'zi1se4')

	#Fruits
	e2c['apple'] =('苹果', 'ping2guo3')
	e2c['apples'] =('苹果', 'ping2guo3')
	e2c['banana'] =('香蕉', 'xiang1jiao1')
	e2c['bananas'] =('香蕉', 'xiang1jiao1')
	e2c['strawberry'] =('草莓', 'cao3mei2')
	e2c['strawberries'] =('草莓', 'cao3mei2')
	e2c['peach'] =('桃子', 'tao2zi')
	e2c['peaches'] =('桃子', 'tao2zi')
	e2c['watermelons'] =('西瓜', 'xi1gua1')
	e2c['doing'] =('做', 'zuo4')
	#Animals
	e2c['fish'] =('魚', 'yu2')
	e2c['fishes'] =('魚', 'yu2')
	e2c['bird'] =('鸟', 'niao3')
	e2c['birds'] =('鸟', 'niao3')
	e2c['work'] =('工作', 'gong1zuo4')
	e2c['school'] =('学校', 'xue2xiao4')
	e2c['think'] =('认为', 'ren4wei2')
	e2c['thinks'] =('认为', 'ren4wei2')
	e2c['thought'] =('认为', 'ren4wei2')
	e2c['okay'] =('行', 'xing2')
	e2c['ok'] =('行', 'xing2')
	e2c['cow'] =('牛', 'niu2')
	e2c['milk'] =('牛奶', 'niu2nai3')
	e2c['brian'] =('布莱恩 ', 'bu4lai2en')
	e2c['joshua'] =('约书亚', 'yue1 shu1 ya4')
	e2c['andrew'] =('安德鲁', 'an1de2lu3')
	e2c['jenny'] =('珍妮', 'zhen1ni1')
	e2c['jennifer'] =('珍妮弗', 'zhen1ni1fu2')
	e2c['annie'] =('安妮', 'an1ni1')
	e2c['sean'] =('李福善', 'li3fu2shan4')
	e2c['house'] =('房子', 'fang2zi')
	e2c['chocolate'] =('巧克力', 'qiao3keli4')
	e2c['donut'] =('甜甜圈', 'tian2tian2quan1')
	e2c['mister'] =('先生', 'xian1sheng5')
	e2c['mr.'] =('先生', 'xian1sheng5')
	e2c['teacher'] =('老师', 'lao3shi1')
	e2c['professor'] =('教授', 'jiao4shou4')
	e2c['ms.'] =('小姐', 'xiao3jie3')
	e2c['WhatTime'] =('几点', 'ji3dian3')
	e2c['raining'] =('下雨', 'xia4yu3')
	e2c['also'] =('也', 'yie3')
	e2c['only'] =('只', 'zhi3')
	e2c['likes'] =('喜欢', 'xi3huan1')
	e2c[''] =('', '')
	e2c[''] =('', '')
	e2c[''] =('', '')
	e2c[''] =('', '')
	e2c[''] =('', '')
	e2c[''] =('', '')
	#food
	e2c['chicken'] =('鸡肉', 'ji1ruo4')

	#DaysOfTheWeek
	e2c['Monday'] =( '星期一', 'xing1qi2yi1')
	e2c['Tuesday'] =( '星期二', 'xing1qi2er4')
	e2c['Wednesday'] =( '星期三', 'xing1qi2san1')
	e2c['Thursday'] =( '星期四', 'xing1qi2si4')
	e2c['Friday'] =( '星期五', 'xing1qi2wu3')
	e2c['Saturday'] =( '星期六', 'xing1qi2liu4')
	e2c['Sunday'] =( '星期天', 'xing1qi2tian1')
	e2c['a little'] =( '一点', 'yi4dian3')
	e2c['TheyObjects'] =( '它们', 'ta1men2')


 

	#Nature
	e2c['Sky'] =( '天', 'tian1')
	e2c['Ground'] =('地', 'di4')
	e2c['Tree'] =('树', 'shu4')
	e2c['Trees'] =('树', 'shu4')
	e2c['Wood'] =('木头', 'mu4tou2')
	e2c['Rock'] =('乭', 'si2tou2')
	e2c['Rocks'] =('乭', 'si2tou2')
	
	#Household Items
	e2c['phone'] =('电话', 'dian4hua4')
	e2c['phones'] =('电话', 'dian4hua4')
	e2c['closet'] =('衣柜', 'yi1gui4')
	e2c['closets'] =('衣柜', 'yi1gui4')


	#Transportation
	e2c['boat'] =('船', 'chuan2')
	e2c['boats'] =('船', 'chuan2')
	e2c['airplanes'] =('飞机', 'fei1ji1')
	e2c['airplane'] =('飞机', 'fei1ji1')
	
	#Numbers
	e2c['one'] =('一 ', 'yi1')
	e2c['two'] =('二', 'er4')
	e2c['three'] =('三 ', 'san1')
	e2c['four'] =('四 ', 'si4')
	e2c['five'] =('五', 'wu3')
	e2c['six'] =('六 ', 'liu4')
	e2c['seven'] =('七 ', 'qi1')
	e2c['eight'] =('八 ', 'ba1')
	e2c['nine'] =('九', 'jiu3')
	e2c['ten'] =('十', 'shi2')
	e2c['twenty-one'] =('二十一', 'er4shi2yi1')

	#we can make a code to have it create new chinese numbers
	
	#Time

	e2c['winter'] =('冬天 ', 'dong1tian1')
	e2c['summer'] =('夏天', 'xia4tian1')
	e2c['autumn'] =('秋天 ', 'qiu1tian1')
	e2c['fall'] =('秋天 ', 'qiu1tian1')
	e2c['spring'] =('春天', 'chun1tian1')


	e2c['america'] =('美国', 'mei3guo2')
	e2c['china'] =('中国', 'zhong1guo2')
	e2c['chinese'] =('中文', 'zhong1wen2')
 	e2c['britain'] =(' 英国', 'ying1guo2')
 	e2c['UK'] =(' 英国', 'ying1guo2')
 	e2c['England'] =(' 英国', 'ying1guo2')
 	e2c['English'] =(' 英文', 'ying1wen2')
	e2c['france'] =('法国', 'fa4guo2')
	e2c['french'] =('法文', 'fa4wen2')
	e2c['germany'] =('德文', 'de2wen2')
	e2c['german'] =('德国', 'de2guo2')
	e2c['korea'] =('韩国 ', 'han2guo2')
	e2c['korean'] =('韩文 ', 'han2wen2')
	e2c['spain'] =('西班牙 ', 'xi1ban1ya2')
	e2c['spanish'] =('西班牙文 ', 'xi1ban1ya2wen2')
	e2c['austrailia'] =('澳洲', 'ao4zhou1')
	e2c['Europe'] =('欧洲', 'ou1zhou1')
	e2c['Asia'] =('亚洲', 'ya3zhou1')
	e2c['Africa'] =('非洲', 'fei1zhou1')

	#Sports
	e2c['basketball'] =('篮球 ', 'lan2qui2')
	e2c['soccer'] =('足球 ', 'zu2qiu2')
	e2c['tennis'] =('网球', 'wang3qiu2')
	e2c['swim'] =('游泳 ', 'you2yong3')
	e2c['walk'] =('走 ','zou3')
	e2c['jump'] =('跳','tiao4')
	e2c['movie'] =('电影', 'dian4ying3')
	e2c['see'] =('看', 'kan4')
	e2c['shirt'] =('衬衫', 'chen4shan1')
	e2c['ugly'] =('难看', 'nan2kan4')

	e2c['eaten'] =('吃', 'chi1') #eaten comes back as bao you its not being overwritten
	e2c['hit'] =('打', 'da3')
	e2c['meeting'] =('见面', 'jian4mian4')
	e2c['baby'] =('婴儿', 'ying1er2')
	e2c['feel'] =('感觉', 'gan3jue2')
	e2c['feels'] =('感觉', 'gan3jue2')
	e2c['felt'] =('感觉', 'gan3jue2')
	e2c['answer'] =('答案', 'da2an4')
	e2c['money'] =('钱', 'qian2')
	e2c['study'] =('读书', 'du2shu1')	
	e2c['bottle'] =('瓶子', 'ping2zi')
	e2c['cup'] =('杯子', 'bei1zi')
	e2c['friend'] =('朋友', 'peng2you3')
	e2c['lover'] =('情人', 'qing2ren2')	
	e2c['people'] =('人', 'ren2')
	e2c['flower'] =('花', 'hua1')
	e2c['grass'] =('草', 'cao3')	
	e2c['translate'] =('翻譯 ', 'fan1yi4')
	e2c['porridge'] =('稀饭', 'xi1fan4')
	e2c['favorite'] =('最喜欢', 'zui4xi3huan1')	
	e2c['clock'] =('时钟', 'zhi2zhong1')
	e2c['smart'] =('聪明', 'cong1ming2')
	e2c['stupid'] =('笨', 'ben4')
	e2c['animals'] =('动物', 'dong4wu4')
	e2c['pet'] =('宠物', 'chong3wu4')
	e2c['pets'] =('宠物', 'chong3wu4')
	e2c['fruit'] =('水果', 'shui3guo3')
	e2c['fruits'] =('水果', 'shui3guo3')
	e2c['vegetable'] =('蔬菜', 'shu1cai4')
	e2c['vegetables'] =('蔬菜', 'shu1cai4')
	e2c['god'] =('神', 'shen2')
	e2c['morning'] =('早上', 'zao3shang4')
	e2c['afternoon'] =('下午 ', 'xiao4wu3')
	e2c['night'] =('晚上', 'wan3shang4')
	e2c['evening'] =('晚上', 'wan3shang4')
	e2c['forget'] =('忘记', 'wang4ji4')
	e2c['forgets'] =('忘记', 'wang4ji4')
	e2c['forgot'] =('忘记', 'wang4ji4')
	e2c['juice'] =('果汁', 'guo3zhi1')
	e2c['jump'] =('跳', 'tiao4')
	e2c['rose'] =('玫瑰花 ', 'mei2gui4hua1')
	e2c['computer'] =('电脑', 'dian4nao3')
	e2c['really'] =('真的', 'zhen1de')
	e2c['have'] =('有', 'you3')
	e2c['LessAmountParticle'] =('少', 'shao3')
	e2c['IfParticle'] =('如果', 'ru2guo3')
	e2c[''] =('', '')
	e2c[''] =('', '')
	e2c[''] =('', '')
	e2c[''] =('', '')
	#old should have ji shui or lao as translation depending on context
	#play can be da for sports and wan just as the regular verb
	#watch can be both noun and verb
	#light can be deng(bulb) or guang (sun)
	#love can be both noun and verb
 	#kiss can be verb and noun




	


	#MultipleUsage
	#fast can be adjective or adverb- you are fast, you run fast
	#short can be ai3 or duan3

	
	
	
	#牠 - him or it for dieties
	#祂 - him or it for animals


	translated = ''
	pinyin = []

	folder = os.path.dirname(os.path.realpath(__file__))
	file_path = os.path.join(folder, 'static/OriginalParsedDictionary.txt')
	e2c_external = load_dictionary(file_path)

	for r in rule:
		if r in to_translate:
			temp = to_translate[r]
			popped = temp.pop(0)
			to_translate[r] = temp
			if popped in e2c:
				pinyin.append(e2c[popped][1])
				translated += e2c[popped][0]
			elif popped in e2c_external:
				pinyin.append(e2c_external[popped][0][2])
				translated += e2c_external[popped][0][0] #gets the first chinese that matches. we can change this later .currently using traditional characters.
		else:
			if r in e2c:
				pinyin.append(e2c[r][1])
				translated += e2c[r][0]
			elif r in e2c_external:
				pinyin.append(e2c_external[r][0][2])
				translated += e2c_external[r][0][0]

	chinese_translation = translated + punctuation if punctuation else translated

	return chinese_translation + "\n" + " ".join(pinyin)


	#things to ask: wo zhai jia chi le fan or wo zhai jia fan chi le

#unittest
def unit_test_all():

	
	assert english_to_chinese("rice").split("\n")[0] == '饭'
	assert english_to_chinese("I").split("\n")[0] == '我'
	assert english_to_chinese("eat").split("\n")[0] == '吃'
	#assert english_to_chinese("ate").split("\n")[0] == '吃了'
	assert english_to_chinese("pretty").split("\n")[0] == '漂亮'
	assert english_to_chinese("quickly").split("\n")[0] == '快'
	assert english_to_chinese("He eats rice").split("\n")[0] == '他吃饭'
	assert english_to_chinese("i ate").split("\n")[0] == '我吃了'
	assert english_to_chinese("He is eating rice").split("\n")[0] == '他在吃饭'
	assert english_to_chinese("She is pretty").split("\n")[0] == '她漂亮'
	assert english_to_chinese("She is very pretty").split("\n")[0] == '她很漂亮'
	assert english_to_chinese("They are very pretty").split("\n")[0] == '他们很漂亮'
	assert english_to_chinese("They are pretty").split("\n")[0] == '他们漂亮'
	assert english_to_chinese("i eat rice").split("\n")[0] == '我吃饭'
	assert english_to_chinese("i ate rice").split("\n")[0] == '我饭吃了'
	assert english_to_chinese("i will eat rice").split("\n")[0] =='我会吃饭'
	assert english_to_chinese("i will eat").split("\n")[0] =='我会吃'
	assert english_to_chinese("Eat rice").split("\n")[0] =='吃饭'
	assert english_to_chinese("i love you").split("\n")[0] =='我爱你'
	assert english_to_chinese("i am tired").split("\n")[0] =='我累'
	assert english_to_chinese("i am not tired").split("\n")[0] =='我不累'
	assert english_to_chinese("who am i").split("\n")[0] =='我是谁'
	assert english_to_chinese("what am i").split("\n")[0] =='我是什么'
	assert english_to_chinese("the girl eats").split("\n")[0] =='女孩吃'
	assert english_to_chinese("the girl eats rice").split("\n")[0] =='女孩吃饭'
	assert english_to_chinese("I am very tired").split("\n")[0] == '我很累'
	assert english_to_chinese("I want to eat rice").split("\n")[0] == '我要吃饭'
	assert english_to_chinese("The food is spicy").split("\n")[0] == '食物辣'
	assert english_to_chinese("I am making rice").split("\n")[0] == '我在做饭'
	assert english_to_chinese("What should I eat?").split("\n")[0] == '我应该吃什么?'
	assert english_to_chinese("Should I eat?").split("\n")[0] == '我应该吃吗?'
	assert english_to_chinese("How can I eat?").split("\n")[0] == '我怎么能吃?'
	assert english_to_chinese("Can I eat?").split("\n")[0] == '我能吃吗?'
	assert english_to_chinese("How pretty are they?").split("\n")[0] == '他们多漂亮?'
	assert english_to_chinese("How pretty is she?").split("\n")[0] == '她多漂亮?'
	assert english_to_chinese("How is she?").split("\n")[0] == '她好吗?'
	assert english_to_chinese("How are you?").split("\n")[0] == '你好吗?'
	assert english_to_chinese("they eat sweet rice").split("\n")[0] == '他们吃甜 饭'
	assert english_to_chinese("the girl eats sweet rice").split("\n")[0] == '女孩吃甜 饭'
	#The two above is correct but theres a space before rice 
	assert english_to_chinese("the pretty girl eats").split("\n")[0] == '漂亮女孩吃'
	assert english_to_chinese("I will eat rice and drink water").split("\n")[0] == '我会吃饭和喝水'
	assert english_to_chinese("I eat rice and drink water").split("\n")[0] == '我吃饭和喝水'
	assert english_to_chinese("i eat").split("\n")[0] == '我吃'
	assert english_to_chinese("he eats").split("\n")[0] == '他吃'
	assert english_to_chinese("he will eat").split("\n")[0] == '他会吃'
	assert english_to_chinese("have you drank?").split("\n")[0] == '你喝了吗?'
	assert english_to_chinese("i want to see a movie").split("\n")[0] == '我要看电影'
	assert english_to_chinese("i am very hungry").split("\n")[0] == '我很饿'
	assert english_to_chinese("i like rice").split("\n")[0] == '我喜欢饭'
	assert english_to_chinese("i like you").split("\n")[0] == '我喜欢你'
	assert english_to_chinese("i hope you are happy").split("\n")[0] == '我希望你快乐'
	assert english_to_chinese("i will want to eat").split("\n")[0] == '我会要吃'
	assert english_to_chinese("i will want to eat rice").split("\n")[0] == '我会要吃饭'
	assert english_to_chinese("i will want rice").split("\n")[0] == '我会要饭'
	assert english_to_chinese("david and brandon eat").split("\n")[0] == '大卫和布兰登吃'
	assert english_to_chinese("david and brandon will eat").split("\n")[0] == '大卫和布兰登会吃'
	assert english_to_chinese("david and brandon eat rice").split("\n")[0] == '大卫和布兰登吃饭'
	assert english_to_chinese("david and brandon ate rice").split("\n")[0] == '大卫和布兰登饭吃了'
	assert english_to_chinese("david and brandon ate").split("\n")[0] == '大卫和布兰登吃了'
	assert english_to_chinese("david and brandon ate sweet rice").split("\n")[0] == '大卫和布兰登甜 饭吃了'
	assert english_to_chinese("david and brandon eat sweet rice").split("\n")[0] == '大卫和布兰登吃甜 饭'
	assert english_to_chinese("i wanted to eat").split("\n")[0] == '我要吃了'
	assert english_to_chinese("i wanted to eat rice").split("\n")[0] == '我饭要吃了'
	assert english_to_chinese("i wanted rice").split("\n")[0] == '我饭要了'
	assert english_to_chinese("eat rice").split("\n")[0] == '吃饭'
	assert english_to_chinese("go out").split("\n")[0] == '出去'
	assert english_to_chinese("go home").split("\n")[0] == '去家'
	assert english_to_chinese("the dog and cat are ugly").split("\n")[0] == '狗和猫难看'
	assert english_to_chinese("the dog and cat are very ugly").split("\n")[0] == '狗和猫很难看'
	assert english_to_chinese("hit him").split("\n")[0] == '打他'
	assert english_to_chinese("when are we meeting?").split("\n")[0] == '我们什么时候见面?'
	assert english_to_chinese("when is she running?").split("\n")[0] == '她什么时候跑?'
	assert english_to_chinese("i think you are pretty").split("\n")[0] == '我认为你漂亮'
	assert english_to_chinese("i think she is pretty").split("\n")[0] == '我认为她漂亮'
	assert english_to_chinese("i think you are very pretty").split("\n")[0] == '我认为你很漂亮'
	assert english_to_chinese("i think she is very pretty").split("\n")[0] == '我认为她很漂亮'
	assert english_to_chinese("i can eat").split("\n")[0] == '我能吃'
	assert english_to_chinese("i can eat rice").split("\n")[0] == '我能吃饭'
	assert english_to_chinese("i cannot eat").split("\n")[0] == '我不能吃'
	assert english_to_chinese("i cannot eat rice").split("\n")[0] == '我不能吃饭'
	assert english_to_chinese("i can not eat").split("\n")[0] == '我不能吃'
	assert english_to_chinese("i can not eat rice").split("\n")[0] == '我不能吃饭'
	assert english_to_chinese("i am a cat").split("\n")[0] == '我是猫'
	assert english_to_chinese("he is a cat").split("\n")[0] == '他是猫'
	assert english_to_chinese("he is a pretty cat").split("\n")[0] == '他是漂亮猫'
	assert english_to_chinese("i am not a pretty cat").split("\n")[0] == '我不是漂亮猫'
	assert english_to_chinese("i am not a cat").split("\n")[0] == '我不是猫'
	assert english_to_chinese("he is not a pretty cat").split("\n")[0] == '他不是漂亮猫'
	assert english_to_chinese("he is not a cat").split("\n")[0] == '他不是猫'
	
	
	assert english_to_chinese("i am pretty").split("\n")[0] == '我漂亮'
	assert english_to_chinese("i am not pretty").split("\n")[0] == '我不漂亮'
	assert english_to_chinese("i am very pretty").split("\n")[0] == '我很漂亮'
	assert english_to_chinese("i am very tired").split("\n")[0] == '我很累'
	assert english_to_chinese("i am not very tired").split("\n")[0] == '我不是很累'
	assert english_to_chinese("i am not very pretty").split("\n")[0] == '我不是很漂亮'
	assert english_to_chinese("she is very tired").split("\n")[0] == '她很累'
	assert english_to_chinese("she is very pretty").split("\n")[0] == '她很漂亮'
	assert english_to_chinese("she is not very tired").split("\n")[0] == '她不是很累'
	assert english_to_chinese("she is not very pretty").split("\n")[0] == '她不是很漂亮'
	assert english_to_chinese("When are you going to sleep?").split("\n")[0] == '你什么时候要睡觉?'
	#assert english_to_chinese("what time do you want to sleep?").split("\n")[0] == '你几点会睡觉??'
	assert english_to_chinese("It is raining").split("\n")[0] == '在下雨'
	assert english_to_chinese("Am i happy?").split("\n")[0] == '我快乐吗?'
	assert english_to_chinese("Am you happy?").split("\n")[0] == '你快乐吗?'
	assert english_to_chinese("Am i really happy?").split("\n")[0] == '我真的快乐吗?'
	assert english_to_chinese("Am you really happy?").split("\n")[0] == '你真的快乐吗?'
	assert english_to_chinese("what are you doing now?").split("\n")[0] == '你在做什么?'
	assert english_to_chinese("what are you doing?").split("\n")[0] == '你做什么?'
	#assert english_to_chinese("she is pretty but she is also stupid").split("\n")[0] == '她漂亮但是她也笨'
	#assert english_to_chinese("she is pretty but stupid").split("\n")[0] == '她漂亮但笨'
	assert english_to_chinese("i only like rice").split("\n")[0] == '我只喜欢饭'
	assert english_to_chinese("he only likes rice").split("\n")[0] == '他只喜欢饭'
	assert english_to_chinese("i only like him").split("\n")[0] == '我只喜欢他'
	assert english_to_chinese("he only likes him").split("\n")[0] == '他只喜欢他'
	assert english_to_chinese("he likes rice").split("\n")[0] == '他喜欢饭'
	assert english_to_chinese("he likes you").split("\n")[0] == '他喜欢你'
	assert english_to_chinese("he only eats rice").split("\n")[0] == '他只吃饭'
	assert english_to_chinese("i only eat rice").split("\n")[0] == '我只吃饭'
	assert english_to_chinese("he only eats").split("\n")[0] == '他只吃'
	assert english_to_chinese("i only eat").split("\n")[0] == '我只吃'
	assert english_to_chinese("eat more").split("\n")[0] == '吃多一点'
	assert english_to_chinese("eat more rice").split("\n")[0] == '吃多一点饭'
	assert english_to_chinese("jenny is pretty").split("\n")[0] == '珍妮漂亮'
	#assert english_to_chinese("let's go").split("\n")[0] == '珍妮漂亮'

	print 'all unit tests complete. success.'

if __name__ == "__main__":
	unit_test_all()
	#phrase = "she is eating rice."
	#phrase = "I should eat"
	#inputbox
	phrase = "If you are tired, run"
	print english_to_chinese(phrase)


	#let us go perhaps wo men zo is better than wo men chu right now go===chu
	# in the case of eat it really should be chi fan
	#assert english_to_chinese("when is she running").split("\n")[0] == '我们什么时候见面?'
	# it should be more like pao bu - chinese does this a lot
	#pao bu chi fan xie zi - all of these are commonly considering, running, eating, and writing 
	#but they are literally( and techincally correct) running(with shoe?), eating rice and writing characters
	#if the user enters i want to write- we should return wo yao xie zi 
	#but if the user puts i want to write a paper - we should retun wo yao xie wen zhang


	#Things to assert


	# #Negative Commands
	# e2c_rules['VBP','RB','VBP','NN'] = ['not','want','VBP', 'NN']
	# #same problem as before(scroll down)- program tries to account for "do" 
	# #but that doesn't exist in english - it is omitted`- i think it has something do 
	# #with the pop method which returns the first word- if we could change that to 
	# #return the second, i think it would work
	# e2c_rules['VBP','RB' 'VBP','NN'] = ['not','want','VBP', 'NN']
	
	# #TimeDescriptors
	# e2c_rules['PRP','RB','VBD'] = ['PRP','RB','VBD', 'PastParticle'] #I already ate: Wo yi jin chi le
	# e2c_rules['PRP','VBD','RB'] = ['PRP','RB','VBD', 'PastParticle'] #I ate yesterday: Wo zuo tian chi le
	# e2c_rules['PRP','MD','VBP','NN','RB'] = ['PRP','RB','FutureParticle','VBP','NN'] #I will eat rice tomorrow : wo mian tian hui chi fan
	# e2c_rules['PRP','MD','VBP','NN'] = ['PRP','FutureParticle','VBP','NN'] #I will eat rice : wo hui chi fan	
	# e2c_rules['PRP','MD','VBP'] = ['PRP','FutureParticle','VBP'] #I will eat: wo hui chi 	

	# e2c_rules['RB','PRP','MD','VBP','NN'] = ['RB','PRP','FutureParticle','VBP','NN']#Tomorrow, I will eat rice : Ming tian, wo hui chi fan
	# e2c_rules['PRP','MD','VBP','RB'] = ['PRP','RB','FutureParticle','VBP']
	

	# #LocationDescriptors
	# e2c_rules['PRP','VBD','IN','NN'] = ['PRP','PresentPerfectParticle','NN','VBD','PastParticle'] # i ate at home: wo chai jia li chi le
	# e2c_rules['PRP','VBD','NN','IN','NN'] = ['PRP','PresentPerfectParticle','NN','VBD','PastParticle', 'NN'] # i ate rice at home: wo chai jia li chi le fan
	# e2c_rules['PRP','MD','VBP','IN','NN'] = ['PRP', 'FutureParticle','PresentPerfectParticle','NN','VBP'] # I will eat at home: wo hui zhai jia chi



	# #Questions
	# e2c_rules['WP','VBP','PRP'] = ['PRP','VBP','WP'] #who are you: ni shi shei?
	
	# e2c_rules['WP','VBZ','PRP' ] = ['PRP','VBZ','WP'] #who is he: ta shi shei?
	# e2c_rules['WP','VBZ','NN'] = ['NN','VBZ','WP'] #what is rice: fan shi she me?
	# e2c_rules['WRB','CAN-MD','VB', 'VBP', 'NN' ] = ['VB','how', 'CAN-MD','VBP','NN'] #how can i eat rice: wo ze me nen chi fan
	# e2c_rules['WRB','CAN-MD','VB', 'VBP' ] = ['VB','how', 'CAN-MD','VBP'] #how can i eat
	# e2c_rules['CAN-MD','PRP', 'VBP', 'NN' ] = ['PRP','CAN-MD','VBP','NN','QuestionParticle'] #can i eat rice
	# e2c_rules['CAN-MD','PRP', 'VBP' ] = ['PRP','CAN-MD','VBP','QuestionParticle'] #can i eat rice
	# e2c_rules['VBP','PRP', 'VBD' ] = ['PRP','VBD','QuestionParticle']

	# #e2c_rules['MD','PRP','VBP' ] = ['PRP','VBP','WP']


	# #SubjectTwoObjects
	# e2c_rules['PRP','VBP','NN','CC','NNS'] = ['PRP','VBP','NN','AndParticle','NNS'] #i eat rice and noodles
	# e2c_rules['PRP','MD','VBP','NN','CC','NNS'] = ['PRP','FutureParticle', 'VBP','NN','AndParticle','NNS'] #i will eat rice and noodles
	

	# #2NounVerb
	# e2c_rules['PRP','CC','PRP','VBP','NN'] = ['PRP', 'AndParticle' ,'PRP', 'VBP', 'NN']
	# e2c_rules['PRP','CC','PRP','VBP'] = ['PRP', 'AndParticle' ,'PRP', 'VBP']
	# #you and i eat rice: ni he wo chi fan
	# e2c_rules['NN', 'CC', 'NN', 'VBP'] = ['NN', 'AndParticle' ,'NN', 'VBP']

	# #Negative Sentences
	# e2c_rules['PRP', 'CAN-MD', 'RB', 'VBP'] = ['PRP','not','can', 'VBP'] 
	# #i can not eat
	# e2c_rules['PRP', 'CAN-MD', 'RB', 'VBP', 'NN'] = ['PRP','not','can', 'VBP', 'NN']
	# #i can not eat rice
	
	
	# #Uncategorized 

	
	# e2c_rules['PRP', 'VBP','DT', 'JJ', 'NN'] = ['PRP', 'VBP','JJ', 'NN'] #i love the pretty girl
	# e2c_rules['PRP', 'VBZ','DT', 'JJ', 'NN'] = ['PRP', 'VBZ','JJ', 'NN'] #he loves the pretty girl
	# e2c_rules['PRP', 'MD', 'VBP','DT', 'JJ', 'NN'] = ['PRP', 'FutureParticle', 'VBP','JJ', 'NN'] #he will love the pretty girl


	
	# e2c_rules['PRP', 'MD', 'VB','DT', 'JJ', 'NN'] = ['PRP', 'FutureParticle', 'VB','JJ', 'NN'] #i will love the pretty girl

	
	# e2c_rules['DT', 'NN', 'VBZ', 'NNS'] = ['NN', 'VBZ', 'NNS'] #the girl eats noodles: nu hai chi mien
	
	# e2c_rules['PRP', 'VBD', 'PRP'] = ['PRP','VBD','PastParticle', 'PRP']
	# e2c_rules['PRP', 'VBZ', 'PRP$'] = ['PRP','VBZ','PRP$'] # he loves her: ta ai ta
	# e2c_rules['PRP', 'VBZ', 'PRP'] = ['PRP','VBZ','PRP'] #he loves them: ta ai ta men
	# e2c_rules['PRP', 'VBP', 'TO', 'VBP'] = ['PRP', 'VBP', 'VBP'] # I want to eat: wo xiang yao chi
	

	
	# e2c_rules['PRP', 'RB', 'VBP', 'TO', 'VBP', 'NN'] = ['PRP','Also' ,'VBP', 'VBP', 'NN'] #I also want to eat rice
	# e2c_rules['PRP', 'RB', 'VBP', 'TO', 'VBP'] = ['PRP','Also' ,'VBP', 'VBP'] #I also want to eat 
	# e2c_rules['WP', 'VBP', 'PRP', 'VBG'] = ['PRP', 'PresentPerfectParticle', 'VBG','what'] #What are you doing: ni zai zuo se ma
	# e2c_rules['WP', 'VBD', 'PRP', 'VBP'] = ['PRP','VBD','PastParticle', 'what'] #what did you do
	# e2c_rules['WP', 'MD', 'PRP', 'VB'] = ['PRP','FutureParticle','VB', 'what'] # ni hui zuo se me

	

	
	# e2c_rules[ 'VB', 'JJ'] = ['PRP', 'should','VBP', 'QuestionParticle']
	# e2c_rules[ 'VBP', 'PRP', 'VBG', 'NN'] = ['PRP', 'PresentPerfectParticle','DoParticle', 'NN', 'QuestionParticle']
	


	#david and brandon will eat rice - needs to be asserted
	#david and brandon will eat sweet rice - needs to be asserted
	#hit him -needs to be asserted
	#eat it - needs to be asserted


	#ChineseGrammar
	#i am pretty and smart - the "and" should be guessing
	# i eat rice and drink water - use "he"
	#wo chi le fan he he le sui 
	#wo fan chi le
	#wo yi jian xiang chu UCLA
	#wo zuo tian xiang yao chi fan - i wanted to eat yesterday
	#ask if wo zuo tian xiang yao chi le fan also works?
	# wo ming tian hui xiang yao chi fan
	# wo ming tian hui yao chu chi fan
	# no commas after time or location phrases. 
	#commas are used to connect complete sentences
	#that are related to one another

	#be smart = dang chong ming or just chong ming?

	#Quality Assurance

	#We should write a code that stores inputs that we cannot give a translation for
	#We should write a code that records how many hits the site gets
	
	
	#I am very hungry

	#Amazing


	#e2c_rules['DT', 'NN', 'VBZ', 'JJ'] = ['NN', 'am', 'JJ', 'PossesiveParticle']
	#the shirt is blue conflcits with the boy is happy - the grammar for the chinese is different
	#Clothes

	#Grammars to add 

	#when do you want to eat?
	
	#where do you live
	#Do you like chinese food?
	#Why don't you pay?
	#I don't have any money
	#this way, please
	#What should we eat?
	





