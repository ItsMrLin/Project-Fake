import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import edu.cmu.sphinx.alignment.LongTextAligner;
import edu.cmu.sphinx.api.SpeechAligner;
import edu.cmu.sphinx.result.WordResult;

public class WordMain {
    
	private final static String NUMBERS_OUTPUT = "numbers-timeframes.txt";
	private final static String NUMBERS_AUDIO = "media/numbers.wav";
	private final static String NUMBERS_TRANSCRIPT = "media/numbers-transcript.txt";
	
	private final static String OBAMA_OUTPUT = "media/obama-timeframes.txt";
	private final static String OBAMA_AUDIO = "media/obama-speech.wav";
	private final static String OBAMA_TRANSCRIPT = "media/obama-speech-transcript.txt";
	
    public static void main(String[] args) throws Exception {
    	PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(OBAMA_OUTPUT)));
    	getWordTimeframes(OBAMA_AUDIO, OBAMA_TRANSCRIPT, out);
    }
    
    public static void getWordTimeframes(String audioFile, String transcriptFile, PrintWriter out) throws Exception {
        URL audioUrl;
        String transcript;
        audioUrl = new File(audioFile).toURI().toURL();
        Scanner scanner = new Scanner(new File(transcriptFile));  
        scanner.useDelimiter("\\Z");  
        transcript = scanner.next();
        scanner.close();
        
        String acousticModelPath = "res/en_us_generic";
        String dictionaryPath = "res/en_us_nostress/cmudict-5prealpha.dict";
        String g2pPath = "res/en_us_nostress/model.fst.ser";
        SpeechAligner aligner = new SpeechAligner(acousticModelPath, dictionaryPath, g2pPath);

        List<WordResult> results = aligner.align(audioUrl, transcript);
        List<String> stringResults = new ArrayList<String>();
        for (WordResult wr : results) {
            stringResults.add(wr.getWord().getSpelling());
        }
        
        LongTextAligner textAligner = new LongTextAligner(stringResults, 2);
        List<String> sentences = aligner.getTokenizer().expand(transcript);
        List<String> words = aligner.sentenceToWords(sentences);
        
        int[] aid = textAligner.align(words);
        
        int lastId = -1;
        for (int i = 0; i < aid.length; ++i) {
            if (aid[i] == -1) {
                //System.out.format("- %s\n", words.get(i));
            } else {
                if (aid[i] - lastId > 1) {
                    for (WordResult result : results.subList(lastId + 1,
                            aid[i])) {
                        //System.out.format("+ %-25s [%s]\n", result.getWord().getSpelling(), result.getTimeFrame());
                    }
                }
                //System.out.format("  %-25s [%s]hi\n", results.get(aid[i]).getWord().getSpelling(),
                //		results.get(aid[i]).getTimeFrame());
                /*WordResult theResult = results.get(aid[i]);
                String word = theResult.getWord().getSpelling();
                String phonemesString = GetPhonemeUtil.getPhonemeString(word);
                phonemesString = phonemesString.replace(".", "").trim();
                String[] phonemes = phonemesString.split(" ");
                long wordStart = theResult.getTimeFrame().getStart();
                long wordEnd = theResult.getTimeFrame().getEnd();
                long phonemeStart = wordStart;
                long phonemeLength= (wordEnd-wordStart)/phonemes.length;
                long phonemeEnd= phonemeStart+phonemeLength;
                for(String phoneme: phonemes) {
                	out.println(phonemeStart + "\t" + phonemeEnd
                    		+ "\t" + phoneme);
                	phonemeStart = phonemeEnd;
                	phonemeEnd += phonemeLength;
                }
                */
                WordResult theResult = results.get(aid[i]);
                String word = theResult.getWord().getSpelling();
                long wordStart = theResult.getTimeFrame().getStart();
                long wordEnd = theResult.getTimeFrame().getEnd();
                out.println(wordStart + "\t" + wordEnd
                            + "\t" + word);
                lastId = aid[i];
            }
        }

        if (lastId >= 0 && results.size() - lastId > 1) {
            for (WordResult result : results.subList(lastId + 1,
                    results.size())) {
                //System.out.format("+ %-25s [%s]\n", result.getWord().getSpelling(), result.getTimeFrame());
            }
        }
        
        out.flush();
        out.close();
    }
}
