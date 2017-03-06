import sys
import json

start_matrix = {}
tag_tag_matrix = {}
tag_word_matrix = {}

def tagger(sentence):

	split_sentence = sentence.split(' ')
	
	states = [{}]

	max_state = ""
	great = -float("inf")

	new_sent = ""

	# start state
	for i in start_matrix:
		states[0][i] = start_matrix[i] + tag_word_matrix[i].get(split_sentence[0],0)
		if states[0][i] > great:
			great = states[0][i]
			max_state = i

	sentence_tag = [max_state]
	new_sent += split_sentence[0]+"/"+str(max_state)+" "
	for i in list(xrange(1,len(split_sentence))):
		states.append({})
		great = -float("inf")
		max_state = ""
		#print states[i-1]
		for j in states[i-1]:	
			for k in tag_tag_matrix[j]:
				temp = states[i-1][j] + tag_tag_matrix[j][k] + tag_word_matrix[k].get(split_sentence[i],0)
				if temp > states[i].get(k,-float("inf")):
					states[i][k] = temp

					if states[i][k] > great:
						great = states[i][k]
						max_state = k

		sentence_tag.append(max_state)
		new_sent += split_sentence[i]+"/"+str(max_state)+" "

	return new_sent + "\n\r"



def main():
	global start_matrix,tag_word_matrix,tag_tag_matrix
	test_file = sys.argv[1]
	with open('hmmmodel.txt') as m:
		data = json.load(m)
	start_matrix = data["start_tag"]	
	tag_tag_matrix = data["tag_tag"]	
	tag_word_matrix = data["tag_word"]	
	tagged_line = []
	with open(test_file) as l:
		lines = [i.strip('\n\r') for i in l.readlines()]
		for lline in lines:
			tagged_line.append(tagger(lline))
	

	with open('hmmoutput.txt','w+') as o:
		for ll in tagged_line:
			o.write(ll)
main()	