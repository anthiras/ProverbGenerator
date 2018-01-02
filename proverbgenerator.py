from collections import defaultdict
import string
import random
import sys

def load_phrases(filename):
	"""Load phrases from file and strip punctuation characters."""
	f = open(filename, 'r')
	punctuation_table = str.maketrans({key: None for key in string.punctuation})
	phrases = [line.lower().rstrip("\r\n").translate(punctuation_table) for line in f]
	f.close()
	return phrases

def build_word_graph(phrases):
	"""Build a graph of word relations.""" 
	word_graph = defaultdict(list)
	for phrase in phrases:
		words = phrase.split()
		for i, word in enumerate(words):
			if (i == 0):
				# Start word
				word_graph['_start'].append(word)
			if (i == len(words)-1):
				# End word
				word_graph[word].append('_end')
			if (i < len(words)-1):
				# Middle word
				word_graph[word].append(words[i+1])
	return word_graph

def random_phrase(word_graph, exclude=[]):
	"""Build a random phrase from the given word graph."""
	def random_path():
		chosen_words = []
		word = '_start'
		while word != '_end':
			possible_words = word_graph[word]
			word = random.choice(possible_words)
			if word != '_end':
				chosen_words.append(word)
		return " ".join(chosen_words)

	while True:
		phrase = random_path()
		if phrase not in exclude:
			return phrase

def main():
	if len(sys.argv) < 2:
		print("Usage: python proverbgenerator.py [phrase file]")
		exit()

	phrases = load_phrases(sys.argv[1])
	word_graph = build_word_graph(phrases)
	phrase = random_phrase(word_graph, exclude=phrases)
	print(phrase)

if __name__ == "__main__":
    main()
