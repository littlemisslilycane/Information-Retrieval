Project Goal -->
Design  and  build  your  own  information  retrieval  systems  and  evaluate  and  compare  their performance levels in terms of retrieval effectiveness.

Requirement to run the project
1. Python Version 2.7
2. PyLucene  
    To setup PyLucene-->

       -Install  Anaconda2 (Python 2.7.x)
       -Install Apache Ant and set environment variables
       -Install cygwin 64 and set environment variables
       -Download source code of PyLucene and extract, we obtain a directory named ‘PyLucene-6.5’
       -Execute command under directory JCC
         1. python setup.py build
         2. python setup.py install
        restart your computer
        -configure the required paths PyLucene
        -Execute command ‘make’ under directory ‘PyLucene-6.5.0’ to build the whole project.
        -Execute command ‘make install’ under directory ‘PyLucene-6.5.0’
		
To run the tasks 		
		

Phase 1- Task1 --> Build your own retrieval systems:

  To run the tasks run CACMSearchEngine.py

--> Place all the required files into the folder called data.
--> config.py fetches the required files from data folder
--> the results generated will be placed in results folder having folders mapped for each task.


Retrieval Model : TF_IDF

-->python TFIDFRetrievalModel.py is to be run for TF_IDF related results. 
-->The config andd utility files help in configuring various paths required for the run.(If needed change the paths in the config file)


Retrieval Model : BM25

-->python BM25RetrievalModel.py is to be run for BM25 related results. 
-->The config andd utility files help in configuring various paths required for the run.(If needed change the paths in the config file)

Retrieval Model : Query likelihood model(JM)

-->python QueryLMJMSRetrievalModel.py is to be run for Query likelihood model(JM) related results. 
-->The config andd utility files help in configuring various paths required for the run.(If needed change the paths in the config file)

Retrieval Model : Lucene

-->python LuceneRetrievalModel.py is to be run for Lucene related results. 
-->The config andd utility files help in configuring various paths required for the run.(If needed change the paths in the config file)


Phase 1- Task2 --> query enhancement 

a) query time stemming -- > stemming.py is to be run.
b) pseudo relevance feedback --PesudoRelevanceFeedback.py is to be run.

After query enhancement, the queries are run with BM25 as baseline by running BM25RetrievalModel.py, by setting the right configuration in config file.

Phase 1- Task3 --> Four runs: using two baseline search engines and two variations (with stopping, with the stemmed corpus and stemmed query subset).

--> StemmedBM25RetrievalModel.py and StemmedLuceneRetrievalModel.py is to generate the stemmed corpuses.
--> Utility.py is having necessary part of code for stopping, by running CACMSearchEngine.py Phase1-task3 will be achieved.
The results are used on baseline BM25 and Lucene

Phase2 --> snippet generation

--> snippetgeneration.py is run to acheive snippet generation and query term highlighting with BM25 as baseline.
--> Results are generated as .html files.

Phase3 -->  Evaluation 

--> Run TF_IDF adapting stopping
--> Evaluation.py is run to generate recall, precision, P@K, MAP and MRR values.

Extra Credits(b) --> Design and implement a query interface that is tolerant of spelling errors in the query terms

--> run QueryInterface.py to achieve the desired results.
--> the results will be placed in results\extra credit folder.

Note: -->For any changes required in the path, do the changes in the config.py file 
      -->for the common functions refer utility.py file.
      -->the results generated will be placed in results folder having folders mapped for each task


 
		
		
