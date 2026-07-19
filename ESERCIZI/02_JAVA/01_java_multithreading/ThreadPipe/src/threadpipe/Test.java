package threadpipe;

import java.io.PipedOutputStream;

public class Test {
	
	public static void main(String[] args)  {
		// TODO Auto-generated method stub
		
		/* A piped output stream can be connected to a piped input stream to create a communications pipe. 
		   The piped output stream is the sending end of the pipe. Typically, data is written to a 
		   PipedOutputStream object by one thread and data is read from the connected PipedInputStream by some other thread. */
		PipedOutputStream pipeOut = new PipedOutputStream();
		
		WriterThread w = new WriterThread (pipeOut);
		ReaderThread r = new ReaderThread (pipeOut);
		
		w.start();
		r.start();
		
		
	}

}
