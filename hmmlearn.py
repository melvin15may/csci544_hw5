import sys
from math import log
from json import dump


start_matrix = {}
tag_tag_matrix = {}
tag_word_matrix = {}


def divide_tag_value(sentence):

	# Returns 2 dict
	# 1 - tag-tag matrix
	# 2 - tag-word matrix

	split_sentence = [i.rsplit('/',1) for i in sentence.split(' ')]

	if split_sentence[0][1] in start_matrix:
		start_matrix[split_sentence[0][1]] += 1
	else:
		start_matrix[split_sentence[0][1]] = 1

	for i in xrange(0,len(split_sentence) - 1):

		if split_sentence[i][1] in tag_tag_matrix:
			if split_sentence[i+1][1] in tag_tag_matrix[split_sentence[i][1]]:
				tag_tag_matrix[split_sentence[i][1]][split_sentence[i+1][1]] += 1
			else:
				tag_tag_matrix[split_sentence[i][1]][split_sentence[i+1][1]] = 1

			if split_sentence[i][0] in tag_word_matrix[split_sentence[i][1]]:
				tag_word_matrix[split_sentence[i][1]][split_sentence[i][0]] += 1
			else:
				tag_word_matrix[split_sentence[i][1]][split_sentence[i][0]] = 1

		else:
			tag_tag_matrix[split_sentence[i][1]] = {}
			tag_tag_matrix[split_sentence[i][1]][split_sentence[i+1][1]] = 1

			tag_word_matrix[split_sentence[i][1]] = {}
			tag_word_matrix[split_sentence[i][1]][split_sentence[i][0]] = 1


def main():
	global start_matrix, tag_word_matrix,tag_tag_matrix
	training_file = sys.argv[1]

	with open(training_file) as l:
		lines = [i.strip('\n\r') for i in l.readlines()]
		no_lines = len(lines) * 1.0
		for ll in lines:
			divide_tag_value(ll)

	start_matrix = {k: log(v / no_lines) for k, v in start_matrix.iteritems()}
	for dic in tag_tag_matrix:
		total = sum(tag_tag_matrix[dic].itervalues(), 0.0)
		tag_tag_matrix[dic] = {k: log(v / total) for k, v in tag_tag_matrix[dic].iteritems()}
		tag_word_matrix[dic] = {k: log(v / total) for k, v in tag_word_matrix[dic].iteritems()}

	new_model = {}
	new_model["start_tag"] = start_matrix
	new_model["tag_tag"] = tag_tag_matrix
	new_model["tag_word"] = tag_word_matrix

	with open('hmmmodel.txt','w+') as f:
		dump(new_model,f)

main()