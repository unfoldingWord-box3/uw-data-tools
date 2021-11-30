# State

This repo contains code that is not production ready. Consider it an alpha release. Feel free to report any issues.

# Usage

The notebook folder contains jupyter notebooks that have been used to identify
whether changes to the data are necessary and whether changes that were made 
are effective. 

The orig_quote folder contains a module that takes as input an OrigQuote string and occurrence on the one hand,
and a text that is presumed to have the OrigQuote on the other hand.

It computes which words in the text match the OrigQuote string.
The end result is a list of integers that are the relative tokens of 
the text when it is tokenized on spaces. For more details, see the README in the orig_quote module.

# License

MIT

# Authors

J. de Joode

unfoldingWord