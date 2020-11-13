
Version 1.0 2015
Created by Luís Marujo (luis.marujo@inesc-id.pt / lmarujo@cs.cmu.edu)

If you use this dataset please cite:

Luis Marujo, Wang Ling, Isabel Trancoso, Chris Dyer, Alan W Black, Anatole Gershman, David Martins de Matos, João Neto and Jaime Carbonell. 2015. Automatic Keyword Extraction on Twitter. In
Proceedings of the 53th Annual Meeting of the Association
for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing of the Asian Federation of Natural Language Processing: short papers. Beijing, China. Association for Computational Linguistics
 

The original dataset without keyword annotations was obtained from:

Kevin Gimpel, Nathan Schneider, Brendan O’Connor,
Dipanjan Das, Daniel Mills, Jacob Eisenstein,
Michael Heilman, Dani Yogatama, Jeffrey Flanigan,
and Noah A. Smith. 2011. Part-of-speech tagging
for twitter: annotation, features, and experiments. In
Proceedings of the 49th Annual Meeting of the Association
for Computational Linguistics: Human Language
Technologies: short papers - Volume 2, HLT-11. Portland, Oregon, USA. 
Association for Computational Linguistics 


We kept their train, dev, and test splits.
This corresponds to the folders train, dev, and test.
Each folder contains 3 files for each tweet in the following format:
tweet.<set>.tok.en-<id>.txt - the original tweet
tweet.<set>.tok.en-<id>-CrowdCountskey - the ranked list of keywords annotated by the turkers with respective number of votes. Each line has a keyword,
followed by a tab (\t) and the number of votes.
tweet.<set>.tok.en-<id>.key - has keywords in the tweet-id.CrowdCounts file, without the number of votes.

where <set> is either train, dev and test, and <id> is the unique identifier of the tweet starting from 1. 
This corresponds to the ordering of tweets in the original dataset. 


