import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import info.debatty.java.stringsimilarity.NGram;
import info.debatty.java.stringsimilarity.NormalizedLevenshtein;

/**
 * See unit tests (ReshaStemmerTest.java) for more examples
 */

public class Examples {
	public static void main(String[] args)
			throws InterruptedException, FileNotFoundException, IOException, ParseException {

		System.out.println("Start");
		wordMap = ReduceMap(Resha.Instance.map);
		System.out.println("Map to List Finished");
		levenshtein = new NormalizedLevenshtein();
		stemmer = Resha.Instance;
		ReadJsonFile();
	}
	public static Map<String,String> wordMap;
	public static Stemmer stemmer;
	public static NormalizedLevenshtein levenshtein;

	public static void ReadJsonFile() throws FileNotFoundException, IOException, ParseException {
		JSONParser parser = new JSONParser();
		// new FileReader("C:/Users/mertg/workspace/Stemmer/src/Cookshop.json")

		Object obj = parser.parse(new InputStreamReader(
				new FileInputStream("C:/Users/mertg/workspace/Stemmer/src/LivaBistro.json"), "UTF-8"));

		JSONObject jsonObject = (JSONObject) obj;

		JSONArray tips = (JSONArray) jsonObject.get("tips");
		int i = 0;
		Iterator<JSONObject> iterator = tips.iterator();
		while (iterator.hasNext()) {
			System.out.println(i);
			i++;
			JSONObject tip = iterator.next();
			String comment = (String) tip.get("comment");
			JSONArray foodp = (JSONArray) tip.get("food+");
			JSONArray foodn = (JSONArray) tip.get("food-");

			JSONArray newfoodp = CelarLabelArray(foodp);
			JSONArray newfoodn = CelarLabelArray(foodn);

			comment = ClearString(comment);

			tip.remove("comment");
			tip.put("comment", comment);

			tip.remove("food+");
			tip.put("food+", newfoodp);

			tip.remove("food-");
			tip.put("food-", newfoodn);
			//if( i > 100) break; //TODO
		}
		WriteJsonToFile(jsonObject);
	}

	public static JSONArray CelarLabelArray(JSONArray labelArr) {
		Iterator<String> iterator2 = labelArr.iterator();
		JSONArray newArr = new JSONArray();
		while (iterator2.hasNext()) {
			String element = iterator2.next();
			element = ClearString(element);
			newArr.add(element);
		}
		return newArr;
	}

	public static String ClearString(String str) {
		str = str.toLowerCase();
		str = str.replaceAll("ý", "i");
		str = str.replaceAll("þ", "s");
		str = str.replaceAll("ð", "g");
		str = str.replaceAll("ü", "u");
		str = str.replaceAll("ç", "c");
		str = str.replaceAll("ö", "o");
		str = str.replaceAll("[^a-z0-9 ]", " ");
		str = StemSentence(str);
		return str;
	}

	public static String StemSentence(String str) {
		String[] words = str.split(" ");
		for (int i = 0; i < words.length; i++) {
			String temp = words[i];
			words[i] = stemmer.stem(words[i]);
			if (temp == words[i] && !Resha.Instance.map.containsKey(temp)) {
				words[i] = CorrectTypo(temp, 0.2);
			}
		}
		return String.join(" ", words);
	}

	public static String CorrectTypo(String str, double treshold) {
		double minDist = treshold;
		String correctWord = str;
		for (Map.Entry<String, String> entry : wordMap.entrySet()) {
			String value = entry.getKey();
			double distance = levenshtein.distance(str, value);
			if (minDist > distance) {
				correctWord = value;
				minDist = distance;
			}
		}
		return correctWord;
	}

	public static Map<String, String> ReduceMap(Map<String, String> map){
		Map<String, String> newMap = new HashMap<String, String>();
		for (Map.Entry<String, String> entry : map.entrySet()) {
			String value = entry.getValue();
			newMap.put(value, null);
		}
		return newMap;
	}
	
	public static void WriteJsonToFile(JSONObject obj) throws IOException {
		Writer out = new BufferedWriter(new OutputStreamWriter(
				new FileOutputStream("C:/Users/mertg/workspace/Stemmer/src/LivaBistro-Clean.json"), "UTF-8"));
		out.write(obj.toJSONString());
		System.out.println("Successfully Copied JSON Object to File...");
		out.close();

	}
}
