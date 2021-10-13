# State

This code is not production ready. Consider it an alpha release. Feel free to report any issues.

# Usage

This module takes as input an OrigQuote string and occurrence on the one hand,
and a text that is presumed to have the OrigQuote on the other hand.

It computes which words in the text match the OrigQuote string.
The end result is a list of integers that are the relative tokens of 
the text when it is tokenized on spaces.

For instance:

    text = בְּרֵאשִׁ֖ית בָּרָ֣א אֱלֹהִ֑ים אֵ֥ת הַשָּׁמַ֖יִם וְאֵ֥ת הָאָֽרֶץ׃
    quote = בָּרָ֣א
    occurrence = 1

The matching token in the text is: 1. (We use Python's zero-based indexing)
This means that if the text is tokenized on white-space, token number 1 is
the token that matched the OrigQuote. (Note that token number 1 is the second
token with zero-based indexing)

To get that result run:

    results, to_exclude = retrieve_quote(quote, text)
    parsed_results = extract_quotes(results, text, to_exclude,occurrence=1)
    parsed_results[1]

The parsed result returns two values: the first is the character spans that
actually match the string, the second is an array of the relative tokens that
match the OrigQuote.

The way the exact token is retrieved is as follows:
    1. turn the quote into a regex
    2. get all the results, and get all tokens that need to be excluded
    3. the results of steps 1 and 2 are character ranges within the text,
    This step converts character ranges to relative token numbers

A future version of this tool should handle pretokenized texts.

# Tests

Run the tests by using 

    python tests.py

# License

MIT

# Authors

J. de Joode

unfoldingWord