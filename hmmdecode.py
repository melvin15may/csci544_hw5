#!/usr/local/bin/python
# coding: utf-8
import sys
import json
import codecs

start_matrix = {}
tag_tag_matrix = {}
tag_word_matrix = {}


def evaluate(tagged_line):
	with open("data/catalan_corpus_dev_tagged.txt") as l:
		lines = [i.strip('\n\r') for i in l.readlines()]

	right = 0
	wrong = 0

	for i in xrange(0,len(lines)):
		tagged_line[i] = tagged_line[i].strip('\n\r')

		split_line = [j.rsplit('/',1) for j in lines[i].split(' ')]
		split_tag_l = [j.rsplit('/',1) for j in tagged_line[i].split(' ')]

		for j in range(len(split_line)):
			if split_line[j][1] == split_tag_l[j][1]:
				right += 1
			else:
				wrong += 1

	print right,wrong

def viterbi(obs, states, start_p, trans_p, emit_p):

	V = [{}]
	check_unknown = 0
	num_states = len(states)

	for st in states:
		if not obs[0] in emit_p[st]:
			check_unknown += 1
		V[0][st] = {"prob": start_p.get(st,-float('inf')) + emit_p[st].get(obs[0],-float('inf')), "prev": None}
 
	if check_unknown == num_states:
		for st in states:
			V[0][st] = {"prob": start_p.get(st,-float('inf')), "prev": None}
	
	# Run Viterbi
	for t in range(1, len(obs)):
		V.append({})
		check_unknown = 0
		unknown = False
		for st in states:
			if not obs[t] in emit_p[st]:
				check_unknown += 1
		#print obs[t],check_unknown,num_states
		if check_unknown == num_states:
			unknown = True
		previous_state = [k for k, v in V[t-1].items() if v["prob"] > -float('inf')]	
		for st in states:
			max_prob = -float('inf')
			for prev_st in previous_state:
				if unknown:
					val = V[t-1][prev_st]["prob"] + trans_p[prev_st][st]
				else:
					val = V[t-1][prev_st]["prob"] + trans_p[prev_st][st] + emit_p[st].get(obs[t],-float('inf'))
				
				if val >= max_prob:
					max_prob = val
					V[t][st] = {"prob": val, "prev": prev_st}	
	fin = []
	max_prob = max(value["prob"] for value in V[-1].values())
	previous = None
	# Get most probable state
	for st, data in V[-1].items():
		if data["prob"] == max_prob:
			fin.append(st)
			previous = st
			break
	# Backtrack
	for t in range(len(V) - 2, -1, -1):
		fin.insert(0, V[t + 1][previous]["prev"])
		previous = V[t + 1][previous]["prev"]
	return fin

def main():
	global start_matrix,tag_word_matrix,tag_tag_matrix
	#t = time.time()
	test_file = sys.argv[1]
	m = open('hmmmodel.txt')
	data = json.loads(m.read())
	start_matrix = data["start_tag"]	
	tag_tag_matrix = data["tag_tag"]	
	tag_word_matrix = data["tag_word"]	
	states = data["states"]	
	tagged_line = []

	with open(test_file) as l:
		lines = [i.strip('\n\r') for i in l.readlines()]
		for lline in lines:
			split_sentence = [i.decode('utf-8') for i in lline.split(' ')]
			st = viterbi(split_sentence, states, start_matrix, tag_tag_matrix, tag_word_matrix)
			ss = ""
			for i in range(len(st)):
				ss += split_sentence[i] + "/" + st[i] + " "
			tagged_line.append(ss)

	file = codecs.open("hmmoutput.txt", "w", "utf-8")
	for ll in tagged_line:
		file.write(ll+"\n")
	file.close()

	#evaluate(tagged_line)

main()	