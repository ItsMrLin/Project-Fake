import edu.cmu.sphinx.decoder.search.Token;
import edu.cmu.sphinx.frontend.Data;
import edu.cmu.sphinx.frontend.FloatData;
import edu.cmu.sphinx.linguist.HMMSearchState;
import edu.cmu.sphinx.linguist.SearchState;
import edu.cmu.sphinx.linguist.acoustic.Unit;
import edu.cmu.sphinx.result.Result;


public class PhonemeMain {
	 public static void showUnitTimes(Result result) {
		  Token token = result.getBestToken();

		  while (token != null) {

				// find the last token 
				while (token != null && !isLastUnit(token)) {
					 token = token.getPredecessor();
				}

				if (token == null) {
					 break;
				}

				// token is now set to the end of a unit.
				// get the unit:

				Unit unit = getUnit(token);
				float endTime = getTime(token.getData());

				token = findFirstToken(token);

				if (token == null) {
					 break;
				}

				float startTime = getTime(token.getData());

				System.out.println("Unit " + unit + " start: " +
						  startTime + " end: " + endTime);
				token = token.getPredecessor();
		  }
	 }


	 private static Unit getUnit(Token token) {
		  SearchState state = token.getSearchState();
		  if (state instanceof HMMSearchState) {
				HMMSearchState hss = (HMMSearchState) state;
				return hss.getHMMState().getHMM().getBaseUnit();
		  }
		  return null;
	 }

	 private static boolean isLastUnit(Token token) {
		  return token.isEmitting();
	 }

	 private static Token findFirstToken(Token token) {
		  while (token != null & !isFirstUnit(token)) {
				token = token.getPredecessor();
		  }
		  while (isFirstUnit(token.getPredecessor())) {
				token = token.getPredecessor();
		  }
		  return token;
	 }
	 private static boolean isFirstUnit(Token token) {
		  SearchState state = token.getSearchState();
		  if (state instanceof HMMSearchState) {
				HMMSearchState hss = (HMMSearchState) state;
				return (hss.getHMMState().getState() == 0);
		  } else {
				return false;
		  }
	 }

	 private static float getTime(Data data) {
		  if (data == null) {
				throw new Error("No data saved in token");
		  }

		  if (! (data instanceof FloatData)) {
				throw new Error("Expecting float data");
		  }

		  FloatData fd = (FloatData) data;
		  return  ((float) fd.getFirstSampleNumber()/ fd.getSampleRate());
	 }
}
