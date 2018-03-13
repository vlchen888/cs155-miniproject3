import re
import random
import roman

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
        self.rhyme_classes = {}
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
    
    def get_spenser(self):
        '''
        Returns a dictionary of sonnets.
        Each element of the dict is one of the sonnets, keyed by sonnet number
        Each sonnet is a list of lists of lines
        '''
        filename = 'data/spenser.txt'
        num = 0
        sonnets = {}
        sonnet_lines = []
        with open(filename) as f:
            for line in f:
                line = re.sub('[:;.()?!]', '', line.strip()).lower()
                try:
                    num = int(roman.fromRoman(line.upper()))
                    sonnets[num] = []
                    sonnet_lines = []                 
                    continue
                except ValueError:
                    pass
                except roman.InvalidRomanNumeralError:
                    pass
                next_line = line.split()
                if len(next_line) > 0:
                    sonnets[num].append(next_line)
        return sonnets
    
    def get_other(self,filename_other):
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
        
        num = 0
        sonnet_lines = []
        with open(filename_other) as f:
            for line in f:
                line = re.sub('[:;.()?!]', '', line.strip()).lower()
                try:
                    num = 154 + int(line)
                    sonnets[num] = []
                    sonnet_lines = []                 
                    continue
                except ValueError:
                    pass
                except roman.InvalidRomanNumeralError:
                    pass
                next_line = line.split()
                if len(next_line) > 0:
                    sonnets[num].append(next_line)
        return sonnets
    
    def get_collab(self):
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
        
        filename = 'data/spenser.txt'
        num = 0
        sonnet_lines = []
        with open(filename) as f:
            for line in f:
                line = re.sub('[:;.()?!]', '', line.strip()).lower()
                try:
                    num = 154 + int(roman.fromRoman(line.upper()))
                    sonnets[num] = []
                    sonnet_lines = []                 
                    continue
                except ValueError:
                    pass
                except roman.InvalidRomanNumeralError:
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
        emission1, states1 = hmm.generate_emission_shakespeare(self.obs_map[words[0]],self.s_count, self.end_count) 
        emission2, states2 = hmm.generate_emission_shakespeare(self.obs_map[words[1]],self.s_count, self.end_count)

        line1 = [reverse_map[i] for i in emission1]
        # Reverse sentence to return
        line1 = list(reversed(line1))
        line1 = ' '.join(line1).capitalize()
        line1 = line1.replace(' i ', ' I ');

        line2 = [reverse_map[i] for i in emission2]
        # Reverse sentence to return
        line2 = list(reversed(line2))
        line2 = ' '.join(line2).capitalize()
        line2 = line2.replace(' i ', ' I ');
        
        return line1, line2
    
    def sample_line_mult(self, hmm, k, n_syllables=10, buffer=0):
        '''
        Given a trained hmm, outputs k rhyming lines with ts syllables
        '''
        reverse_map = self.obs_map_reverser()
        
        # Get a rhyming class of size at least k
        r_class = random.randint(0, len(self.rhyme_classes)-1)
        while len(self.rhyme_classes[r_class]) < k:
            r_class = random.randint(0, len(self.rhyme_classes)-1)

        words = []
        poss_words = list(self.rhyme_classes[r_class])
        while len(words) < k:
            ind = random.randint(0, len(poss_words)-1)
            words.append(poss_words[ind])
            del(poss_words[ind])
        
        # Generate rhyming sentences
        lines = []*k
        for j in range(k):
            syllable_shift = random.randint(-buffer, buffer)
            emission, states = hmm.generate_emission_shakespeare(self.obs_map[words[j]],self.s_count, self.end_count, \
                                                                 target_syllables=n_syllables+syllable_shift) 
            
            lines.append([reverse_map[i] for i in emission])
            # Reverse sentence to return
            lines[j] = list(reversed(lines[j]))
            lines[j] = ' '.join(lines[j]).capitalize()
            lines[j] = lines[j].replace(' i ', ' I ')
        
        return lines

    
    def sample_random(self, hmm, n_syllables=10):
        '''
        Given a trained hmm, outputs k rhyming lines with ts syllables
        '''
        reverse_map = self.obs_map_reverser()

        word = 'twat'

        
        # Generate rhyming sentences
        emission, states = hmm.generate_emission_shakespeare(self.obs_map[word],self.s_count, self.end_count, \
                                                                 target_syllables=n_syllables) 
            
        line = [reverse_map[i] for i in emission]
        # Reverse sentence to return
        line = list(reversed(line))
        line = ' '.join(line).capitalize()
        line = line.replace(' i ', ' I ')
        
        return line
    
    def load_syllable_dict(self):
        with open('data/syllable_dict_all.txt') as f:
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

    def load_rhyme_list(self, sonnet,pattern = 1):
        if pattern == 1:
            self.rhymes.append( (sonnet[0][-1], sonnet[2][-1]) )
            self.rhymes.append( (sonnet[1][-1], sonnet[3][-1]) )
            self.rhymes.append( (sonnet[4][-1], sonnet[6][-1]) )
            self.rhymes.append( (sonnet[5][-1], sonnet[7][-1]) )
            self.rhymes.append( (sonnet[8][-1], sonnet[10][-1]) )
            self.rhymes.append( (sonnet[9][-1], sonnet[11][-1]) )
            self.rhymes.append( (sonnet[12][-1], sonnet[13][-1]) )
        elif pattern == 2:
            try:
                self.rhymes.append( (sonnet[0][-1], sonnet[1][-1]) )
                self.rhymes.append( (sonnet[1][-1], sonnet[4][-1]) )
                self.rhymes.append( (sonnet[2][-1], sonnet[3][-1]) )
            except IndexError:
                print(sonnet)
                
    def make_rhyme_classes(self):
        pairs_tup = self.rhymes
        pairs = []
        for j in range(len(pairs_tup)):
            pairs.append(list(pairs_tup[j]))

        classes = {}
        classes_clean = {}

        # See report for clean statement of algorithm
        i = 0
        while len(pairs) > 0:
            classes[i] = list(pairs[0])
            classes_clean[i] = [re.sub(r'[^\w]', '', pairs[0][0]).lower(),re.sub(r'[^\w]', '', pairs[0][1]).lower()]
            del(pairs[0])
            '''
            j = 1
            while j < len(pairs):
                w1 = re.sub(r'[^\w]', '', pairs[j][0]).lower()
                w2 = re.sub(r'[^\w]', '', pairs[j][1]).lower()
                if (w1 in classes_clean[i]) or (w2 in classes_clean[i]):
                    if pairs[j][0] not in classes[i]:
                        classes[i].append(pairs[j][0])
                    if pairs[j][1] not in classes[i]:
                        classes[i].append(pairs[j][1])
                    if w1 not in classes_clean[i]:
                        classes_clean[i].append(w1)
                    if w2 not in classes_clean[i]:
                        classes_clean[i].append(w2)
                    del(pairs[j])
                j += 1
            i += 1
            '''
            j = 1
            while j < len(pairs):
                w1 = re.sub(r'[^\w]', '', pairs[j][0]).lower()
                w2 = re.sub(r'[^\w]', '', pairs[j][1]).lower()
                if (w1 in classes_clean[i]) or (w2 in classes_clean[i]):
                    if w1 not in classes_clean[i]:
                        classes[i].append(pairs[j][0])
                        classes_clean[i].append(w1)
                    if w2 not in classes_clean[i]:
                        classes[i].append(pairs[j][1])
                        classes_clean[i].append(w2)
                    del(pairs[j])
                else:
                    j += 1
            i += 1

        self.rhyme_classes = classes

