import org.apache.lucene.analysis.TokenFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.core.StopFilter;
import org.apache.lucene.analysis.shingle.ShingleFilter;
import org.apache.lucene.analysis.standard.StandardFilter;
import org.apache.lucene.analysis.standard.StandardTokenizer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.analysis.util.CharArraySet;
import org.apache.lucene.util.Version;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;


public class QueryExpansion {


  static {

  }

  private Map<String, Double> getTermFrequencies(String sentence, int ngramCount) {
    StringReader reader = new StringReader(sentence);

    final List<String> stopWords = Arrays.asList(
            "a", "an", "and", "are", "as", "at", "be", "but", "by",
            "for", "if", "in", "into", "is", "it",
            "no", "not", "of", "on", "or", "such",
            "that", "the", "their", "then", "there", "these",
            "they", "this", "to", "was", "will", "with", "would", "should",
            "after", "less",
            "has", "see", "also", "have", "been");

    final CharArraySet stopSet = new CharArraySet(Version.LUCENE_47,
            stopWords.size(), false);
    stopSet.addAll(stopWords);
    CharArraySet ENGLISH_STOP_WORDS_SET;
    ENGLISH_STOP_WORDS_SET = CharArraySet.unmodifiableSet(stopSet);

    Map<String, Integer> nGrams = new HashMap<>();
    Map<String, Double> tf = new HashMap<>();
    int docTermCount = 0;

    //Generate tokens
    StandardTokenizer source = new StandardTokenizer(Version.LUCENE_47, reader);
    TokenStream tokenStream = new StandardFilter(Version.LUCENE_47, source);
    tokenStream = new StopFilter(Version.LUCENE_47, tokenStream,
            ENGLISH_STOP_WORDS_SET = CharArraySet.unmodifiableSet(stopSet));

    TokenFilter sf = null;
    sf = new ShingleFilter(tokenStream);
    ((ShingleFilter) sf).setMaxShingleSize(ngramCount);
    ((ShingleFilter) sf).setMinShingleSize(ngramCount);
    ((ShingleFilter) sf).setOutputUnigrams(false);


    CharTermAttribute charTermAttribute = sf.addAttribute(CharTermAttribute.class);
    try {
      sf.reset();
      while (sf.incrementToken()) {
        String token = charTermAttribute.toString().toLowerCase();
        if (!token.contains("_")) {
          docTermCount++;
          if (nGrams.containsKey(token)) {
            int newCount = nGrams.get(token);
            nGrams.put(token, newCount + 1);
          } else {
            nGrams.put(token, 1);
          }
        }
      }
      sf.end();
      sf.close();
    } catch (IOException ex) {
      ex.printStackTrace();
    }

    //Compute the TF values
    for (Map.Entry<String, Integer> entry : nGrams.entrySet()) {
      tf.put(entry.getKey(), entry.getValue() / (double) docTermCount);
    }

    return tf;
  }

  private void printExpansionWords(LinkedHashMap<String, Double> result,
                                   String query) throws IOException {
    int i = 1, n = 6;
    File dir = new File("Query_Expansion_Terms");
    File fWrite =
            new File(dir, query + "_expansion_n_" + n +
                    ".txt");
    FileWriter fWriter = new FileWriter(fWrite, false);
    for (Map.Entry entry : result.entrySet()) {
      if (i > n) {
        break;
      } else {
        System.out.println(entry.getKey());
        fWriter.write(entry.getKey() + "\n");
        i++;
      }
    }
    fWriter.close();
  }

  public static void main(String[] args) throws IOException {

    String[] queryList = {"Robotic space missions", "Mars exploration",
            "unmanned spacecraft", "Planetary moons", "Satellites in Space"};


    int no_of_documents = 0;
    for (String query : queryList) {
      no_of_documents = 0;

      Map<String, Double> tf_map = new HashMap<>();
      Map<String, Integer> idf = new HashMap<>();
      Map<String, Double> idf_map = new HashMap<>();
      Map<String, Double> tfidf_map = new HashMap<>();
      QueryExpansion classObj = new QueryExpansion();
      Map<String, Map> tf = new HashMap<>();
      int k = 10;

      //Read the files from the folder which are the top K documents
      BufferedReader reader = new BufferedReader(new FileReader(query + ".txt"));
      while (no_of_documents < k) {
        no_of_documents++;
        String fileName = reader.readLine();
        //Generate the tf values
        String docText = classObj.readFile(fileName);
        //Store the tf values for each document.
        tf.put(fileName, classObj.getTermFrequencies(docText, 2));
      }

      //Get the TF values for all the terms in the corpus
      for (Map.Entry<String, Map> entry : tf.entrySet()) {
        Map<String, Double> tf_each_document = entry.getValue();
        for (Map.Entry<String, Double> item : tf_each_document.entrySet()) {
          String bigGram = item.getKey();
          Double frequency = item.getValue();
          if (tf_map.containsKey(bigGram)) {
            tf_map.put(bigGram, tf_map.get(bigGram) + frequency);
            idf.put(bigGram, idf.get(bigGram) + 1);
          } else {
            idf.put(bigGram, 1);
            tf_map.put(bigGram, frequency);
          }
        }
      }

      //computer idf properly
      for (Map.Entry<String, Integer> entry : idf.entrySet()) {
        idf_map.put(entry.getKey(), Math.log(no_of_documents / entry.getValue()));
      }

      for (Map.Entry<String, Integer> entry : idf.entrySet()) {
        tfidf_map.put(entry.getKey(), entry.getValue() * tf_map.get(entry.getKey()));
      }

      LinkedHashMap<String, Double> sorted_tfidf = new LinkedHashMap<>();

      tfidf_map.entrySet()
              .stream()
              .sorted(Map.Entry.comparingByValue(Comparator.reverseOrder()))
              .forEachOrdered(x -> sorted_tfidf.put(x.getKey(), x.getValue()));

      System.out.println("Printing expansion words for " + query);
      classObj.printExpansionWords(sorted_tfidf, query);
    }


  }


  private String readFile(String fileName) throws IOException {
    BufferedReader br = new BufferedReader(new FileReader(fileName));
    try {
      StringBuilder sb = new StringBuilder();
      String line = br.readLine();

      while (line != null) {
        sb.append(line);
        sb.append("\n");
        line = br.readLine();
      }
      return sb.toString();
    } finally {
      br.close();
    }
  }
}