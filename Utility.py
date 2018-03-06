
class Utility:
    def __init__(self):
        # Current number of different tokens seen
        self.obs_counter = 0
        # Map from token to number 
        self.obs_map = {}
        # 
        self.obs = []

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
                line = line.strip()
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

    def sample_line(self, hmm, n_words = 10):
        reverse_map = self.obs_map_reverser()

        emission, states = hmm.generate_emission(n_words)
        sentence = [reverse_map[i] for i in emission]
        return ' '.join(sentence).capitalize()


