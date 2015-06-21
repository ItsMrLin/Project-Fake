import java.net.URL;
import java.util.List;

import edu.cmu.sphinx.api.Configuration;
import edu.cmu.sphinx.api.SpeechAligner;
import edu.cmu.sphinx.result.WordResult;
import edu.cmu.sphinx.util.TimeFrame;


public class WordMain {
	public static void main(String[] args) throws Exception
	{
		Configuration configuration = new Configuration();
		 
		// Set path to acoustic model.
		configuration.setAcousticModelPath("resource:");
		// Set path to dictionary.
		configuration.setDictionaryPath("resource:");
		// Set language model.
		configuration.setLanguageModelPath("resource:");
		SpeechAligner aligner = new SpeechAligner("/edu/cmu/sphinx/models/en-us/en-us",
				"/edu/cmu/sphinx/models/en-us/cmudict-en-us.dict",
				"/edu/cmu/sphinx/models/en-us/en-us.lm.dmp");
		List<WordResult> result = aligner.align(new URL("101-42.wav"), "one oh one four two");
		for(WordResult wordResult: result)
		{
			TimeFrame times = wordResult.getTimeFrame();
			wordResult.getPronunciation();
			
		}
	}
}
