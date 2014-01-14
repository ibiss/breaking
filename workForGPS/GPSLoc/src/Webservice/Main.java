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

    public static void main(String[] args) throws JsonParseException, JsonMappingException, Exception {
        String name = "kuba";
        String password = "1234";
        //String webPage = "http://projectbreaking.herokuapp.com/webservices/login/" + name + "/?format=json";
        String webPage = "http://projectbreaking.herokuapp.com/webservices/mission/2/?format=json";
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
        
        while(newjson.indexOf("}")+2<=newjson.length())
        {
        Mission userId = (Mission) converter.fromJson(newjson);
        System.out.println(userId.getLatitude());
        newjson = newjson.substring(newjson.indexOf("}")+2, newjson.length());
        }/*userId = (Mission) converter.fromJson(newjson);
        System.out.println(userId.getLatitude());
        newjson = newjson.substring(newjson.indexOf("}")+2, newjson.length());
        userId = (Mission) converter.fromJson(newjson);
        System.out.println(userId.getLatitude());
        newjson = newjson.substring(newjson.indexOf("}")+2, newjson.length());
        userId = (Mission) converter.fromJson(newjson);
        System.out.println(userId.getLatitude());*/

//String webPage = "http://projectbreaking.herokuapp.com/webservices/mission/2/?format=json";
//String webPage = "http://projectbreaking.herokuapp.com/webservices/login/" + name + "/?format=json";
    }

    public Object fromJson(String json) throws JsonParseException, JsonMappingException, IOException {
        Mission garima = new ObjectMapper().readValue(json, Mission.class);


        return garima;
    }

    public static class UserId {

        private String id;

        public String getId() {
            return id;
        }

        public void setName(String name) {
            this.id = name;
        }

        @Override
        public String toString() {
            return "User [name=" + id + "]";
        }
    }
    
    public static class Mission {
        private String latitude;
        private String longitude;
        private String timestamp;
        private String mission;
        
        public String getLatitude() {
            return latitude;
        }
        
        public String getLongitude() {
            return longitude;
        }
        
        public String getTimestamp() {
            return timestamp;
        }
        
        public String getMission() {
            return mission;
        }
    }
}