import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.PrintWriter;


public class GetPhonemeUtil {
	/**
	 * 
	 * @param args needs to be of size 3:
	 *		<audio_file>.wav
	 *		<transcript_file>.txt
	 *	 	<output_file>.txt
	 */
	public static void main(String[] args) throws Exception {
		if(args.length != 3) {
			System.out.println("Failed: requires three arguments :(");
			System.exit(-1);
		}
		PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(args[2])));
		WordMain.getWordTimeframes(args[0], args[1], out);
	}
}
