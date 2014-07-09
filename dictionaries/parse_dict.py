#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def parse_dict(fn):
	with open('parsed_dict.txt', 'w') as fout:
		#i = 0
		with open(fn) as f:
			for line in f:
				#i+=1
				#if i > 1000:
				#	return
				parsed = parse_line(line.rstrip('\n'))
				if parsed:
					for d in parsed['defs']:
						if is_one_word(d):
							fout.write(parsed['chinese'] + '\t' + parsed['pinyin'] + '\t' + d + '\n')
	return

def parse_line(line):
	temp = line.split('[')
	if len(temp) > 1:
		chinese = temp[0].rstrip()
		#print temp
		temp2 = temp[1].split(']')
		pinyin = temp2[0]
		defs = [d for d in temp2[1].rstrip().lstrip().split('/') if d != ""]

		parsed = {}
		parsed['chinese'] = chinese
		parsed['pinyin'] = pinyin
		parsed['defs'] = defs
		return parsed
	else:
		return None
def is_one_word(phrase):
	return True if len(phrase.split(' ')) == 1 else False

if __name__ == "__main__":
	parse_dict('diccionario.u8')
	#test = "下旋 下旋 [xia4 xuan2] /(sport) backspin/"
	#parse_line("下水 下水 [xia4 shui3] /downstream/to go into the water/to put into water/to launch (a ship)/fig. to fall into bad ways/to lead astray/to go to pot/")
