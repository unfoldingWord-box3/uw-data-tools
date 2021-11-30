import re


def retrieve_quote(quote, text):
    '''
    This method actually does the searching. It uses a very simply
    regular expression. That regular expression captures the `&` in groups. These
    ampersands highlight gaps that should not be part of the OrigQuote (they
    are skipped). These groups are separately returned as character ranges
    that need to be excluded.
    '''

    # all the `&` are replaced with regex groups, so that we can find and 
    # extract the words that need to be ignored
    quote = quote.strip().replace('&', '(.*?)') 
    results = re.finditer(quote, text)
    
    # we need to export which words that were matched by `&` need
    # to be excluded from the results at a later point in time
    # because we have the regex here in place, we compute the ones to 
    # be excluded and return these with this function
    to_exclude = []
    for result in results:
        groups = result.groups()
        # the main result is group 0 and should not be excluded
        for grp in range(1,len(result.groups())+1):
            # we might be excluding words from other matches as well, but that's not a problem
            # being greedy here is not an issue
            to_exclude.append(result.span(grp))
    # rerun the results because the iterator has been used
    results = re.finditer(quote, text)           
    return results, to_exclude


def retokenize(text):
    '''
    Util function to tokenize and detokenize a string to 
    check the consistency of space-based tokenization
    '''
    tokens = text.strip().split()
    detokenized = ' '.join(tokens)
    assert text == detokenized
    return text, tokens


def extract_quotes(results, text, to_exclude=[], occurrence=1):
    '''
    The inputs are the search results from the regex of `retrieve_quote`
    as well as the character ranges that need to be excluded.
    
    Searching is done using regexes, but the end result has to 
    be a list of tokens. This function jumps through a few hoops
    to map the character-based results on token-based results.
    
    Essentially, we map the indeces of the search result on an array that has the 
    start and end character indeces of each token. We then exclude the character 
    ranges of the items that need to be excluded.
    
    The function then returns both an array of the character ranges
    and an array of the relative token indeces (again 0-based indexing). 
    '''
    text, tokens = retokenize(text) 
    # generate relative token ids (relative as in 'get the fourth token')
    tokenIds = enumerate(tokens)
    
    # compute the starts and ends for each token, 
    # these will be zipped below
    ends = [itm.start() for itm in re.finditer(r' ', text)] + [len(text)]
    starts = [0] + [itm.end() for itm in re.finditer(r' ', text)]
    # convert these into a dictionary that maps character ranges to tokens
    # char_to_token = {(0, 11): (0, 'בְּרֵאשִׁ֖ית'), (12, 19): (1, 'בָּרָ֣א'),
    # (20, 29): (2, 'אֱלֹהִ֑ים'), (30, 34): (3, 'אֵ֥ת'), (35, 46): (4, 'הַשָּׁמַ֖יִם'), (47, 53): (5, 'וְאֵ֥ת'), (54, 63): (6, 'הָאָֽרֶץ׃')}
    char_to_token = dict(
        zip(
            zip(starts, ends), # [(0, 11), (12, 19), (20, 29), (30, 34), (35, 46), (47, 53), (54, 63)]
            tokenIds
        )
    )
    
    results = [range(itm.start(), itm.end()+1) for itm in results]
    
    # handle the different occurrences
    # this is done by selecting a specific result
    if not occurrence:
        # set occurrence=None to get all occurrences
        pass
    else:
        # here we select a specific occurrence, and one occurrence only
        results = [results[occurrence-1]]    
    
    # this triple for-loop goes through each of the results
    # and stitches the character-based and relative-token based results together
    # this works at a character-level again, it steps through each character and 
    # evaluates whether it is part of a specific token
    output = []
    for result in results:
        for token in zip(starts, ends):
            token_range = range(token[0], token[1]+1)
            for r in result:
                if r in token_range:
                    output.append(token)
                    continue
    output = sorted(list(set(output)))
    
    # excluded the tokens that need to be excluded
    # if multiple words are being 'escaped'
    # the exclusion will be a match for either the start-end
    # of the entire subtoken string 
    # hence any token start or end should also be excluded
    new_output = []
    excluded_starts_and_ends = []
    for itm in to_exclude:
        excluded_starts_and_ends.extend(list(range(itm[0], itm[1])))
        # excluded_starts_and_ends.append(itm[1])
    for itm in output:
        # if a single word was matched
        if itm in to_exclude:
            continue
        # if multiple words were matched by the ampersand
        if itm[0] in excluded_starts_and_ends:
            continue
        if itm[1] in excluded_starts_and_ends:
            continue
        new_output.append(itm)
    quoted_tokens = [char_to_token[itm] for itm in new_output] 
    # return the filtered output
    return new_output, [itm[0] for itm in quoted_tokens]