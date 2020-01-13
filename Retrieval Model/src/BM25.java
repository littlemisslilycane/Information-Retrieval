import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public class BM25 {

  private final double k1 = 1.2;
  private final double b = 0.75;
  private final double k2 = 100;
  private final double r = 0;
  private final double R = 0;

  private Map<String, Integer> dl;

  public BM25() {

    dl = new HashMap<>();
  }


  private Map<String, Map> getInvertedIndex() {

    try {
      File toRead = new File("invertedIndex.txt");
      ObjectInputStream in =
              new ObjectInputStream(new BufferedInputStream(new FileInputStream(toRead)));

      Map<String, Map> retrievedIndex = (HashMap<String, Map>) in.readObject();

      in.close();
      return retrievedIndex;
    } catch (Exception ex) {
      ex.getStackTrace();
    }
    return null;

  }

  private Map<String, Integer> getDocumentTermLength() {

    try {
      File toRead = new File("documentLength.txt");
      FileInputStream fis = new FileInputStream(toRead);
      ObjectInputStream ois = new ObjectInputStream(fis);

      Map<String, Integer> retrievedIndex =
              (HashMap<String, Integer>) ois.readObject();

      ois.close();
      fis.close();
      return retrievedIndex;
    } catch (Exception ex) {
      ex.getStackTrace();
    }
    return null;

  }


  public static void main(String[] args) throws IOException, ClassNotFoundException {

    BM25 classObj = new BM25();


    //Get the inverted index and document length from the index files.
    classObj.dl = classObj.getDocumentTermLength(); //Document lengths
    Map<String, Map> inverted_index = classObj.getInvertedIndex(); //Index


    //Read the Queries from file and add them to the query list
    BufferedReader reader = new BufferedReader(new FileReader("Queries.txt"));
    List<String> query = new ArrayList();
    String fileName = reader.readLine();
    while (fileName != null) {


      query.add(fileName);
      fileName = reader.readLine();
    }

    //Find the top 100 documents for each query
    for (String queryID : query) {
      Map<String, Double> bm25 = new TreeMap<>();
      System.out.println("Query processing: " + queryID);

      //Given the query get the create a map of the query term frequency
      Map<String, Integer> qf = new TreeMap<>(String.CASE_INSENSITIVE_ORDER);
      for (String term : queryID.split(" ")) {
        term = term.trim();
        if (!term.isEmpty()) {
          if (qf.containsKey(term)) {
            qf.put(term, qf.get(term) + 1);
          } else {
            qf.put(term, 1);
          }
        }
      }


      double logNumerator = (classObj.r + 0.5) / (classObj.R - classObj.r + 0.5);
      double avdl =
              classObj.dl.values().stream().mapToDouble(Integer::doubleValue).average().orElse(0);

      //Compute the BM25 rank for each document
      for (String document : classObj.dl.keySet()) {
        int dl = classObj.dl.get(document);
        double K =
                classObj.k1 * ((1 - classObj.b) + (classObj.b * (dl / avdl)));
        double score = 0;
        for (String q : qf.keySet()) {
          int qfValue = qf.get(q);
          int n = inverted_index.get(q).size();
          int f = 0;
          Object o = inverted_index.get(q).get(document);
          if (o != null) {
            f = (int) o;
          }
          double logDenominator =
                  (n - classObj.r + 0.5) / (996 - n - classObj.R + classObj.r + 0.5);
          double logValue = Math.log(logNumerator / logDenominator);
          double secondValue = ((classObj.k1 + 1) * f) / (K + f);
          double thirdValue =
                  ((classObj.k2 + 1) * qfValue) / (classObj.k2 + qfValue);

          score = score + (logValue * secondValue * thirdValue);

        }
        bm25.put(document, score);
      }


      //Sort the documents as per the bm25 scores.
      bm25 = classObj.sort(bm25);


      //Write the results to file
      File fWrite =
              new File("BM25_" + queryID + ".txt");
      FileWriter fWriter = new FileWriter(fWrite, false);
      int rank = 0;
      for (Map.Entry<String, Double> entry : bm25.entrySet()) {
        if (rank > 100) break;
        rank++;
        String docID = entry.getKey().split(".txt")[0];
        String result =
                queryID + " Q0 " + docID + " " + rank + " " + entry.getValue() +
                        " BM25 \n";
        fWriter.write(result);
      }
      fWriter.close();

    }


  }

  /**
   * Sort the documents as per the descending order of their bm25 score.
   */
  private Map<String, Double> sort(Map<String, Double> bm25) {
    Map<String, Double> sorted = new TreeMap<String, Double>(
            new BM25Comparator(bm25));
    sorted.putAll(bm25);
    return sorted;

  }

  public class BM25Comparator implements Comparator<String> {

    private Map<String, Double> map = new TreeMap<>();

    public BM25Comparator(Map<String, Double> map) {

      this.map.putAll(map);
    }

    public int compare(String a, String b) {
      int compare = map.get(a).compareTo(map.get(b));
      if (compare == -1) {
        return 1;
      } else if (compare == 1) {
        return -1;
      } else {
        return 0;
      }
    }
  }
}
