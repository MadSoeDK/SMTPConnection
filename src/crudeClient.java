    import java.io.*;
    import java.net.*;
    import java.util.*;
     
    public class crudeClient {
     
       public static void main(String argv[])
          {
	   		Scanner in = new Scanner(System.in);
	        
    	   try{
    		    Socket socketClient= new Socket("127.0.0.1",5558);
    		    System.out.println("Client: "+"Connection Established");
     
    		    BufferedReader reader = new BufferedReader(new InputStreamReader(socketClient.getInputStream()));
    		    BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(socketClient.getOutputStream()));

    		    String s,serverMsg;

				int i = 0;
				while((serverMsg = reader.readLine()) != null){
    				System.out.println("Client: " + serverMsg);

					if (i > 0 && i < 3) {
						s = in.nextLine();
						writer.write(s+"\r\n");
						writer.flush();
						i++;
					} else {
						i++;
					}
    			}
     
    	   }catch(Exception e){e.printStackTrace();}
          }
    }
