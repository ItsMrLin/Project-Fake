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
		out.println(args[0]);
		out.println("lol");
		out.println(args[1]);
		out.println("bye");
		out.println(args[2]);
		out.flush();
		out.close();
	}
}
