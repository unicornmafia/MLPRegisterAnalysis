class TextStats:
    def __init__(self, file_name):
        self.file_name = file_name
        # keep track of frequencies of tokens and tags
        self.tokens = dict()
        self.tags = dict()
        self.num_words = 0
        self.words = list()
        self.sentences = list()
        self.speakers = list()

    def add_word(self, word):
        self.num_words += 1
        try:
            self.tokens[word] += 1
        except KeyError:
            self.tokens[word] = 1
        self.words.append(word)

    def add_tag(self, tag):
        if tag == ",":
            tag = "comma"
        try:
            self.tags[tag] += 1
        except KeyError:
            self.tags[tag] = 1

    def get_num_tokens(self):
        keys = set(self.tokens.keys())
        return len(keys)

    def get_num_sentences(self):
        return len(self.sentences)

    def get_num_speakers(self):
        return len(self.speakers)

    def get_average_sentence_length(self):
        num_sentences = self.get_num_sentences()
        total_length = 0
        for sentence in self.sentences:
            total_length += len(sentence)
        return total_length/float(num_sentences)

    def get_average_word_length(self):
        num_words = self.num_words
        total_length = 0
        for word in self.words:
            total_length += len(word)
        return total_length/float(num_words)

    def add_tuple(self, tuple):
        self.add_word(tuple[0])
        self.add_tag(tuple[1])

    def add_sentence(self, sentence):
        self.sentences.append(sentence)

    def add_speaker(self, speaker):
        self.speakers.append(speaker)

    def get_output_stat_set(self, full_ordered_tag_set):
        output_stats = list()
        output_stats.append(("num_words", self.num_words))
        output_stats.append(("num_tokens", self.get_num_tokens()))
        output_stats.append(("num_sentences", self.get_num_sentences()))
        output_stats.append(("num_speakers", self.get_num_speakers()))
        output_stats.append(("ave_sentence_len", self.get_average_sentence_length()))
        output_stats.append(("ave_word_len", self.get_average_word_length()))
        for tag in full_ordered_tag_set:
            try:
                output_stats.append((tag, self.tags[tag]))
            except KeyError:
                output_stats.append((tag, 0))

    def get_normalized_output_stat_set(self, full_ordered_tag_set, normalization_length):
        normalization_factor = normalization_length/float(self.num_words)
        output_stats = list()
        output_stats.append(("num_words", normalization_factor*self.num_words))
        output_stats.append(("num_tokens", normalization_factor*self.get_num_tokens()))
        output_stats.append(("num_sentences", normalization_factor*self.get_num_sentences()))
        output_stats.append(("num_speakers", self.get_num_speakers()))
        output_stats.append(("ave_sentence_len", self.get_average_sentence_length()))
        output_stats.append(("ave_word_len", self.get_average_word_length()))
        for tag in full_ordered_tag_set:
            try:
                output_stats.append((tag, normalization_factor*self.tags[tag]))
            except KeyError:
                output_stats.append((tag, 0))
        return output_stats

    def get_output_line(self, full_ordered_tag_set):
        output_line = self.file_name
        output_line += ", " + str(self.num_words)
        output_line += ", " + str(self.get_num_tokens())
        output_line += ", " + str(self.get_num_sentences())
        output_line += ", " + str(self.get_num_speakers())
        output_line += ", " + str(round(self.get_average_sentence_length(), 2))
        output_line += ", " + str(round(self.get_average_word_length(), 2))
        for tag in full_ordered_tag_set:
            try:
                output_line += ", " + str(self.tags[tag])
            except KeyError:
                output_line += ", 0"
        return output_line

    def get_normalized_output_line(self, full_ordered_tag_set, normalization_length):
        normalization_factor = normalization_length/float(self.num_words)
        output_line = self.file_name
        output_line += ", " + str(round(normalization_factor*self.num_words, 2))
        output_line += ", " + str(round(normalization_factor*self.get_num_tokens(), 2))
        output_line += ", " + str(round(normalization_factor*self.get_num_sentences(), 2))
        output_line += ", " + str(self.get_num_speakers())
        output_line += ", " + str(round(self.get_average_sentence_length(), 2))
        output_line += ", " + str(round(self.get_average_word_length(), 2))
        for tag in full_ordered_tag_set:
            try:
                output_line += ", " + str(round(normalization_factor*self.tags[tag], 2))
            except KeyError:
                output_line += ", 0"

        return output_line
