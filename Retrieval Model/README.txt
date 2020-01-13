README
**********************************
Java Version: 8
Lucene: 4.7.2

Referenced Libraries:
1) lucene-core-VERSION.jar 
2) lucene-queryparser-VERSION.jar 
3) lucene-analyzers-common-VERSION.jar.  

1)Unzip the contents of the folder "VASAVI_VENKATESH_HW5" in your local system.

2)To get the inndexes, place the corpus in the folder \BFS_PARSED and run the file Index.py through command line :
javac Index.java

3)Place the queries in each line of the file Queries.txt in the root folder.

4)Once the indexes are generated, run the program Lucene.py from command line. This will generate the Lucene ranking of documents for the above set of queries. The resultant files are generated prefixed with "Lucene_".

javac Lucene.java

5)Once the indexes are generated, run the program BM25.py from command line. This will generate the BM25 ranking of documents for the above set of queries. The resultant files are generated prefixed with "BM25_".

javac BM25.java


5)The result files are placed in the folder \results.







