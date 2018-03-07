import re
import random

class Utility:
    def __init__(self):
        # Current number of different tokens seen
        self.obs_counter = 0
        # Map from token to number 
        self.obs_map = {}
        # List of observation sequences (list of lists)
        self.obs = []
        # Dictionary from word to syllable count
        self.s_count_raw = {}
        # Dictionary from word to syllable count for last word in a line
        self.end_count_raw = {}
        # Dictionary from observation number to syllable count
        self.s_count = {}
        # Dictionary from observation number to syllable count for last word in a line
        self.end_count = {}
        # List of rhymes
        self.rhymes = []
        self.load_syllable_dict()


    def parse_observations(self, sonnet):
        '''
        Loads a piece of text into our observations, represented by a list of lists
        '''
        # Tokenizing naively, just by spaces
        # Each line in a sonnet is a sequence
        for line in sonnet:
            obs_seq = []
            for word in line:
                if word not in self.obs_map:
                    self.obs_map[word] = self.obs_counter
                    self.obs_counter += 1

                obs_seq.append(self.obs_map[word])
            self.obs.append(obs_seq)
    
    def parse_observations_reverse(self, sonnet):
        '''
        Loads a piece of text into our observations IN REVERSE
        represented by a list of lists. This allows us to seed the last word
        and incorporate rhyme
        '''
        # Tokenizing naively, just by spaces
        # Each line in a sonnet is a sequence
        for line in sonnet:
            obs_seq = []
            for word in line:
                if word not in self.obs_map:
                    self.obs_map[word] = self.obs_counter
                    self.obs_counter += 1
                    # update s_count and end_count dictionaries
                    clean_word = re.sub(r'[^\w]', '', word).lower()
                    self.s_count[self.obs_map[word]] = self.s_count_raw[clean_word]
                    if clean_word in self.end_count_raw:
                        self.end_count[self.obs_map[word]] = self.end_count_raw[clean_word]

                obs_seq.append(self.obs_map[word])
            self.obs.append(list(reversed(obs_seq)))

    def obs_map_reverser(self):
        '''
        Returns map from number to word
        '''
        reverse_map = {}
        for key in self.obs_map:
            reverse_map[self.obs_map[key]] = key
        return reverse_map

    def get_shakespeare(self):
        '''
        Returns a dictionary of sonnets.
        Each element of the dict is one of the sonnets, keyed by sonnet number
        Each sonnet is a list of lists of lines
        '''
        filename = 'data/shakespeare.txt'
        num = 0
        sonnets = {}
        sonnet_lines = []
        with open(filename) as f:
            for line in f:
                line = re.sub('[:;.()?!]', '', line.strip()).lower()
                try:
                    num = int(line)
                    sonnets[num] = []
                    sonnet_lines = []
                    continue
                except ValueError:
                    pass
                next_line = line.split()
                if len(next_line) > 0:
                    sonnets[num].append(next_line)
        return sonnets

    def sample_line_naive(self, hmm, n_words = 10):
        '''
        Given a trained hmm, outputs a sonnet line
        '''
        reverse_map = self.obs_map_reverser()

        emission, states = hmm.generate_emission(n_words)
        sentence = [reverse_map[i] for i in emission]
        return ' '.join(sentence).capitalize()

    def sample_line(self, hmm):
        '''
        Given a trained hmm, outputs two rhyming lines with the correct syllable count
        '''
        reverse_map = self.obs_map_reverser()
        # Get random pair of rhyming words
        words = self.rhymes[random.randint(0, len(self.rhymes) - 1)]

        # Generate rhyming sentences
        emission1, states1 = hmm.generate_emission_shakespeare(self.obs_map[words[0]],\
                self.s_count, self.end_count) 
        emission2, states2 = hmm.generate_emission_shakespeare(self.obs_map[words[1]],\
                self.s_count, self.end_count)

        line1 = [reverse_map[i] for i in emission1]
        # Reverse sentence to return
        line1 = list(reversed(line1))
        line1 = ' '.join(line1).capitalize()

        line2 = [reverse_map[i] for i in emission2]
        # Reverse sentence to return
        line2 = list(reversed(line2))
        line2 = ' '.join(line2).capitalize()

        return line1, line2

    def load_syllable_dict(self):
        with open('data/Syllable_dictionary.txt') as f:
            for line in f:
                arr = line.split()
                word = arr[0]
                word = re.sub(r'[^\w]', '', word).lower()
                # List of valid syllable counts
                # self.s_count[word] = []
                for i in range(1, len(arr)):
                    token = arr[i]
                    if token[0] == 'E':
                        self.end_count_raw[word] = int(token[1:])
                    else:
                        #self.s_count[word].append(int(token))
                        self.s_count_raw[word] = int(token)

    def load_rhyme_list(self, sonnet):
        self.rhymes.append( (sonnet[0][-1], sonnet[2][-1]) )
        self.rhymes.append( (sonnet[1][-1], sonnet[3][-1]) )
        self.rhymes.append( (sonnet[4][-1], sonnet[6][-1]) )
        self.rhymes.append( (sonnet[5][-1], sonnet[7][-1]) )
        self.rhymes.append( (sonnet[8][-1], sonnet[10][-1]) )
        self.rhymes.append( (sonnet[9][-1], sonnet[11][-1]) )
        self.rhymes.append( (sonnet[12][-1], sonnet[13][-1]) )
        

