README
**********************************
Java Version: 8
Lucene: 4.7.2

Referenced Libraries:
1) lucene-core-VERSION.jar 
2) lucene-queryparser-VERSION.jar 
3) lucene-analyzers-common-VERSION.jar.  

1)Unzip the contents of the folder "VASAVI_VENKATESH_HW4" in your local system. Place the corpus in the folder \BFS_PARSED.

2)From the command line, run the file Task1.java for running Task 1:
javac Task1.java

3)This will generate the top 100 documents for each of the query terms mentioned in the assignment.

4)Run the File QueryExpansion.java to get the query expansion terms for the above query.

javac QueryExpansion.java

5)The result files are placed in the folder \results.

6)The top 100 results of the initial query search are present in the folder:
\Results\Tasks 1

7)The results for Task 2 are present in the folder \Results\Task2\Query_Expansion_Terms

-----
Design:
1)I have used Lucene 4.7.2 Standard Analyzer to index and get the top 100 documents for each query results.

2)Then, from the top 10(k) documents of each query result, I calculated the tf-idf value for each term and picked the top n terms with the higest tf-idf value for the Query expansion words.

3)I have used a HashMap in Java to store the index. 

4)I have made used of Lucene Shingle Filter,StopFilter to tokenize the words in the corpus and get the bigrams. 





