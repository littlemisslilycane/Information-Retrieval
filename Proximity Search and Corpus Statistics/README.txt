README - Assignment 4


Version: Python 3.7.2 

*************************
Steps to run the program:
*************************
1)Unzip the contents of the package Vasavi_venkatesh_HW3 and place it in your local system.
2)Install the below packages through python terminal:
pip install nltk
3)Run the program Indexing.py as below in windows powershell or command prompt:
'python Indexing.py'
(The corpus is present in the folder BFS_PARSED. The documents were generated from last assignment. The files are deleted now for submission)
4)The inverted indexes, document & term frequency, number of terms per document and conjuctive processing results are generated as text files in the same folder. 
5)However, for the purpose of submission, the results generated are put in the folder "Results"
6)The result text files and their description are listed below:


Inverted_Index_1_gram.txt		Inverted Index for Unigrams					Task 1a
Inverted_Index_2_gram.txt		Inverted Index for Bigrams					Task 1a
Inverted_Index_3_gram.txt		Inverted Index for Trigrams					Task 1a
Number_of_terms_in_document.txt		Number of terms in each document				Task 1b
Positional_Index.txt                    Positional Index of Unigrams					Task 1d
space_mission_12.txt                    Conjunctive Proximity Results for "Space" & "Mission" k=12	Task 2b
space_mission_6.txt			Conjunctive Proximity Results for "Space" & "Mission" k=6	Task 2b
earth_orbit_10.txt			Conjunctive Proximity Results for "Earth" & "Orbit" k=10	Task 2b
earth_orbit_5.txt			Conjunctive Proximity Results for "Earth" & "Orbit" k=5		Task 2b
Term_Frequency_1.txt			Term Frequency of Unigrams					Task 3a
Term_Frequency_2.txt			Term Frequency of Bigrams					Task 3a
Term_Frequency_3.txt			Term Frequency of Trigrams					Task 3a
Document_Frequency_1.txt		Document Frequency of Uigrams					Task 3b
Document_Frequency_2.txt		Document Frequency of Bigrams					Task 3b
Document_Frequency_3.txt		Document Frequency of Trigrams					Task 3b
StopList_Unigram.txt			Stop List for Unigram						Task 3c
StopList_Bigram.txt			Stop Lists for Bigrams						Task 3c
StopList_Trigram.txt			Stop Lists for Trigram						Task 3c
idf_1.txt				IDF value list for unigram terms
idf_2.txt				IDF value list for Bigram terms				
idf_3.txt				IDF value list for Trigram terms



7)The explanation for the stop list is present in the text file \Results\Task 3\Explanation.txt

*************************
Design Choices
*************************
1)All the three tasks are implemented in a single program "Indexing.py". Since all the three tasks share the inverted indexes created by one of the tasks. 
2)The Inverted index are stored in python dictionary with the term as the key.


