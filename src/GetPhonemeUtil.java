import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.InputStreamReader;
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
	
	public static String getPhonemeString(String word) {
		try
		{
			ProcessBuilder pb = new ProcessBuilder("python", "getPhonemesHelper.py", "hi");
			Process p = pb.start();
			BufferedReader bfr = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String line = bfr.readLine();
			return line;
		}
		catch (Exception e)
		{
			return "";
		}
	}
}
