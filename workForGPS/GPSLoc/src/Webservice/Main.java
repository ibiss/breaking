package Webservice;


import com.sun.org.apache.xerces.internal.impl.dv.util.Base64;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import org.codehaus.jackson.JsonParseException;
import org.codehaus.jackson.map.JsonMappingException;
import org.codehaus.jackson.map.ObjectMapper;

public class Main {
	
	public static int login(String name, String password) throws JsonParseException, JsonMappingException, Exception {

        String webPage = "http://projectbreaking.herokuapp.com/webservices/login/" + name + "/?format=json";
        URL url = new URL(webPage);
        URLConnection urlConnection = url.openConnection();
        String val = (new StringBuffer(name).append(":").append(password)).toString();
        byte[] base = val.getBytes();
        String authorizationString = "Basic " + new String(new Base64().encode(base));
        urlConnection.setRequestProperty("Authorization", authorizationString);
        String json = "";
        try {
            InputStream is = urlConnection.getInputStream();
            InputStreamReader isr = new InputStreamReader(is);
            BufferedReader reader = new BufferedReader(isr);
            String str;
            while ((str = reader.readLine()) != null) {
                json = str;
                System.out.println(str);

            }
        } catch (Exception e) {
            System.out.println("nieporpawne dane");
            return -1;
        }

        String newjson = json.substring(1, json.length());
        Main converter = new Main();
        
        UserId userId = (UserId) converter.fromJsonU(newjson);
        
        return Integer.valueOf(userId.getId());
        
    }
	
    public static ArrayList<Mission> getMission(int id, String name, String password) throws JsonParseException, JsonMappingException, Exception 
    {
        ArrayList<Mission> missions = new ArrayList<Mission>();
        
        //String webPage = "http://projectbreaking.herokuapp.com/webservices/login/" + name + "/?format=json";
        String webPage = "http://projectbreaking.herokuapp.com/webservices/mission/"+id+"/?format=json";
        URL url = new URL(webPage);
        URLConnection urlConnection = url.openConnection();
        String val = (new StringBuffer(name).append(":").append(password)).toString();
        byte[] base = val.getBytes();
        String authorizationString = "Basic " + new String(new Base64().encode(base));
        urlConnection.setRequestProperty("Authorization", authorizationString);
        String json = "";
        try {
            InputStream is = urlConnection.getInputStream();
            InputStreamReader isr = new InputStreamReader(is);
            BufferedReader reader = new BufferedReader(isr);
            String str;
            while ((str = reader.readLine()) != null) {
                json += str;
                System.out.println(str);

            }
        } catch (Exception e) {
            System.out.println("nieporpawne dane");
        }

        String newjson = json.substring(1, json.length());
        Main converter = new Main();
        Mission miss = new Mission();
        
        while(newjson.indexOf("}")+2<=newjson.length())
        {
        	miss = (Mission) converter.fromJsonM(newjson);
        	missions.add(miss);
        	newjson = newjson.substring(newjson.indexOf("}")+2, newjson.length());
        }
        
        return missions;
    }
    
    public Object fromJsonU(String json) throws JsonParseException, JsonMappingException, IOException {
        UserId garima = new ObjectMapper().readValue(json, UserId.class);

        return garima;
    }
    
    public Object fromJsonM(String json) throws JsonParseException, JsonMappingException, IOException {
        Mission garima = new ObjectMapper().readValue(json, Mission.class);

        return garima;
    }

    
}


