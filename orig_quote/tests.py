import unittest

from orig_quote_parser import retrieve_quote, retokenize, extract_quotes


class TestQuoteExtractionHebrew(unittest.TestCase):
    
    def setUp(self):
        self.sample = "בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ׃"
    
    def test_single_word(self):
        quote = 'בָּרָ֣א'
        results, to_exclude = retrieve_quote(quote, self.sample)
        parsed_results = extract_quotes(results, self.sample, to_exclude)
        self.assertEqual(parsed_results[1], [1])
    
    def test_two_words(self):
        quote = 'בָּרָ֣א אֱלֹהִ֑ים'
        results, to_exclude = retrieve_quote(quote, self.sample)
        parsed_results = extract_quotes(results, self.sample, to_exclude)
        self.assertEqual(parsed_results[1], [1,2])    

    def test_longer_phrase(self):
        quote = 'בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת'
        results, to_exclude = retrieve_quote(quote, self.sample)
        parsed_results = extract_quotes(results, self.sample, to_exclude)
        self.assertEqual(parsed_results[1], [0,1,2,3])  
  
    def test_longer_phrase_with_trailing_space(self):
        quote = 'בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת '
        results, to_exclude = retrieve_quote(quote, self.sample)
        parsed_results = extract_quotes(results, self.sample, to_exclude)
        self.assertEqual(parsed_results[1], [0,1,2,3])  
    
    def test_phrase_with_punctuation(self):
        quote = 'אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ׃'
        results, to_exclude = retrieve_quote(quote, self.sample)
        parsed_results = extract_quotes(results, self.sample, to_exclude)
        self.assertEqual(parsed_results[1], [3,4,5,6])       
        
    def test_discontinuous_tokens(self):
        '''
        Should *not* include token number 6.
        '''
        quote = 'אֵ֥ת הַשָּׁמַ֖יִם & הָאָֽרֶץ'
        results, to_exclude = retrieve_quote(quote, self.sample)
        parsed_results = extract_quotes(results, self.sample, to_exclude)
        self.assertEqual(parsed_results[1], [3,4,6])    
   
    def test_multiple_discontinuous_tokens(self):
        quote = 'אֱלֹהִ֑ים & הַשָּׁמַ֖יִם & הָאָֽרֶץ׃'
        results, to_exclude = retrieve_quote(quote, self.sample)
        parsed_results = extract_quotes(results, self.sample, to_exclude)
        self.assertEqual(parsed_results[1], [2,4,6])    

    def test_discontinuous_tokens_with_punctuation(self):
        quote = 'אֵ֥ת & הָאָֽרֶץ׃'
        results, to_exclude = retrieve_quote(quote, self.sample)
        parsed_results = extract_quotes(results, self.sample, to_exclude)
        self.assertEqual(parsed_results[1], [3,6])    


class TestQuoteExtractionWithOccurrence(unittest.TestCase):
    
    def setUp(self):
        self.sample = 'ἐπερωτηθεὶς δὲ ὑπὸ τῶν Φαρισαίων πότε ἔρχεται ἡ Βασιλεία τοῦ Θεοῦ ἀπεκρίθη αὐτοῖς καὶ εἶπεν οὐκ ἔρχεται ἡ Βασιλεία τοῦ Θεοῦ μετὰ παρατηρήσεως'
    
    def test_single_word_first_occurrence(self):
        quote = 'Βασιλεία'
        results, to_exclude = retrieve_quote(quote, self.sample)
        parsed_results = extract_quotes(results, self.sample, to_exclude)
        self.assertEqual(parsed_results[1], [8])

    def test_single_word_second_occurrence(self):
        quote = 'Βασιλεία'
        results, to_exclude = retrieve_quote(quote, self.sample)
        parsed_results = extract_quotes(results, self.sample, to_exclude, 2)
        self.assertEqual(parsed_results[1], [18])       
        
    def test_single_phrase(self):
        quote = 'Βασιλεία τοῦ Θεοῦ'
        results, to_exclude = retrieve_quote(quote, self.sample)
        parsed_results = extract_quotes(results, self.sample, to_exclude)
        self.assertEqual(parsed_results[1], [8,9,10])

    def test_discontinuous_tokens(self):
        quote = 'Βασιλεία & Θεοῦ'
        results, to_exclude = retrieve_quote(quote, self.sample)
        parsed_results = extract_quotes(results, self.sample, to_exclude)
        self.assertEqual(parsed_results[1], [8,10])
        
    def test_discontinuous_tokens_second_occurrence(self):
        quote = 'Βασιλεία & Θεοῦ'
        results, to_exclude = retrieve_quote(quote, self.sample)
        parsed_results = extract_quotes(results, self.sample, to_exclude, 2)
        self.assertEqual(parsed_results[1], [18,20])

    def test_multiple_discontinuous_tokens_ampersand(self):
        quote = 'Φαρισαίων & Βασιλεία'
        results, to_exclude = retrieve_quote(quote, self.sample)
        parsed_results = extract_quotes(results, self.sample, to_exclude, 1)
        self.assertEqual(parsed_results[1], [4,8])    
        
    def test_multiple_discontinuous_tokens_duplicated_ampersand(self):
        quote = 'Φαρισαίων & & Βασιλεία'
        results, to_exclude = retrieve_quote(quote, self.sample)
        parsed_results = extract_quotes(results, self.sample, to_exclude, 1)
        self.assertEqual(parsed_results[1], [4,8]) 
        
unittest.main(argv=[''], verbosity=2, exit=False)