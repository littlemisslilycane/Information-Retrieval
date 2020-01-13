import org.apache.lucene.analysis.TokenFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.shingle.ShingleFilter;
import org.apache.lucene.analysis.standard.StandardFilter;
import org.apache.lucene.analysis.standard.StandardTokenizer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.util.Version;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.StringReader;
import java.util.HashMap;
import java.util.Map;

public class Index {


  private Map<String, Map> inverted_index;
  private Map<String, Integer> document_length;

  public Index() {
    inverted_index = new HashMap<>();
    document_length = new HashMap<>();
  }

  private String readFile(String fileName) {
    StringBuilder sb = new StringBuilder();
    try {
      BufferedReader br = new BufferedReader(new FileReader(fileName));
      try {
        String line = br.readLine();

        while (line != null) {
          sb.append(line);
          sb.append("\n");
          line = br.readLine();
        }

      } catch (IOException ex) {
        ex.getStackTrace();
      } finally {
        br.close();
      }
    } catch (Exception ex) {
      ex.getStackTrace();
    }
    return sb.toString();

  }

  private void getTermFrequencies(String sentence, int ngramCount,
                                  String documentID) {

    StringReader reader = new StringReader(sentence);
    Map<String, Integer> nGrams = new HashMap<>();
    Map<String, Double> tf = new HashMap<>();

    int docTermCount = 0;

    //Generate tokens
    StandardTokenizer source = new StandardTokenizer(Version.LUCENE_47, reader);
    TokenStream tokenStream = new StandardFilter(Version.LUCENE_47, source);

    TokenFilter sf = null;
    sf = new ShingleFilter(tokenStream);
    ((ShingleFilter) sf).setOutputUnigrams(true);
    ((ShingleFilter) sf).setOutputUnigramsIfNoShingles(true);

    CharTermAttribute charTermAttribute = sf.addAttribute(CharTermAttribute.class);
    try {
      tokenStream.reset();
      while (tokenStream.incrementToken()) {
        String token = charTermAttribute.toString().toLowerCase();
        if (!(token.contains(" "))) {
          docTermCount++;
          if (nGrams.containsKey(token)) {
            int newCount = nGrams.get(token);
            nGrams.put(token, newCount + 1);
          } else {
            nGrams.put(token, 1);
          }
        }
      }
      tokenStream.end();
      tokenStream.close();
      document_length.put(documentID, docTermCount);
      for (Map.Entry<String, Integer> entry : nGrams.entrySet()) {
        if (inverted_index.containsKey(entry.getKey())) {
          Map<String, Integer> docTermFrequency =
                  inverted_index.get(entry.getKey());
          docTermFrequency.put(documentID, entry.getValue());
          inverted_index.put(entry.getKey(), docTermFrequency);

        } else {
          Map<String, Integer> docTermFrequency = new HashMap<>();
          docTermFrequency.put(documentID, entry.getValue());
          inverted_index.put(entry.getKey(), docTermFrequency);
        }
      }


    } catch (IOException ex) {
      ex.printStackTrace();
    }

  }


  private void saveIndex() {
    try {
      File fileOne = new File("invertedIndex.txt");
      File fileTwo = new File("documentLength.txt");
      FileOutputStream fos = new FileOutputStream(fileOne);
      ObjectOutputStream oos = new ObjectOutputStream(fos);

      oos.writeObject(inverted_index);
      fos = new FileOutputStream(fileTwo);
      oos = new ObjectOutputStream(fos);
      oos.writeObject(document_length);

      oos.flush();
      oos.close();
      fos.close();
    } catch (Exception ex) {
      ex.getStackTrace();
    }

  }

  private void generateIndex() {
    File folder = new File("BFS_PARSED");
    File[] listOfFiles = folder.listFiles();
    for (int i = 0; i < listOfFiles.length; i++) {
      System.out.println("Scanning document " + i);
      File file = listOfFiles[i];
      if (file.isFile() && file.getName().endsWith(".txt")) {
        String fileName = file.getName();
        String content = readFile(file.getPath());
        getTermFrequencies(content, 1, fileName);
      }
    }
    saveIndex();
  }

  public Map<String, Map> getInvertedIndex() {

    try {
      File toRead = new File("invertedIndex.txt");
      FileInputStream fis = new FileInputStream(toRead);
      ObjectInputStream ois = new ObjectInputStream(fis);

      Map<String, Map> retrievedIndex = (HashMap<String, Map>) ois.readObject();

      ois.close();
      fis.close();
      return retrievedIndex;
    } catch (Exception ex) {
      ex.getStackTrace();
    }
    return null;

  }

  public static void main(String[] args) {

    Index indexer = new Index();
    indexer.generateIndex();
    Map<String, Map> invertedIndex = indexer.getInvertedIndex();
    System.out.println("Completed");

  }
}
