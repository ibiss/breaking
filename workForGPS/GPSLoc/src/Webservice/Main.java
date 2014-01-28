package Webservice;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.List;

import org.codehaus.jackson.JsonParseException;
import org.codehaus.jackson.map.JsonMappingException;
import org.codehaus.jackson.map.ObjectMapper;

import com.sun.org.apache.xerces.internal.impl.dv.util.Base64;

public class Main {

	private static int returnInt;

	public int login(final String name, final String password)
			throws JsonParseException, JsonMappingException, Exception {

		returnInt = 0;
		
			System.out.println("Jestem w funkcji login");
		
		new Thread(new Runnable() {
			public void run() {

				String webPage = "http://projectbreaking.herokuapp.com/webservices/login/"+ name + "/?format=json";
				URL url = null;
				try {
					url = new URL(webPage);
				} catch (MalformedURLException e2) {
					// TODO Auto-generated catch block
					e2.printStackTrace();
				}
				URLConnection urlConnection = null;
				try {
					urlConnection = url.openConnection();
				} catch (IOException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
				String val = (new StringBuffer(name).append(":")
						.append(password)).toString();
				byte[] base = val.getBytes();
				String authorizationString = "Basic "
						+ new String(new Base64().encode(base));
				urlConnection.setRequestProperty("Authorization",
						authorizationString);
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
					System.out.println("niepoprawne dane");
					System.out.println(e.toString());
					returnInt = -1;
				}

				String newjson = json.substring(1, json.length());
				Main converter = new Main();

				UserId userId = null;
				try {
					userId = (UserId) converter.fromJsonU(newjson);
				} catch (JsonParseException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				} catch (JsonMappingException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}

				returnInt = Integer.valueOf(userId.getId());

			}
		}).start();

		while (returnInt == 0) {
		}

		return returnInt;
	}

	public List<Mission> getMission(final int id, final String name,
			final String password) throws JsonParseException,
			JsonMappingException, Exception {
		final List<Mission> missions = new ArrayList<Mission>();
		returnInt = 0;

		new Thread(new Runnable() {
			public void run() {

				// String webPage =
				// "http://projectbreaking.herokuapp.com/webservices/login/" +
				// name + "/?format=json";
				String webPage = "http://projectbreaking.herokuapp.com/webservices/mission/"
						+ id + "/?format=json";
				URL url = null;
				try {
					url = new URL(webPage);
				} catch (MalformedURLException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
				URLConnection urlConnection = null;
				try {
					urlConnection = url.openConnection();
				} catch (IOException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
				String val = (new StringBuffer(name).append(":")
						.append(password)).toString();
				byte[] base = val.getBytes();
				String authorizationString = "Basic "
						+ new String(new Base64().encode(base));
				urlConnection.setRequestProperty("Authorization",
						authorizationString);
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
					returnInt = 1;
					System.out.println("nieporpawne dane");
				}

				String newjson = json.substring(1, json.length());
				Main converter = new Main();
				Mission miss = new Mission();

				while (newjson.indexOf("}") + 2 <= newjson.length()) {
					try {
						miss = (Mission) converter.fromJsonM(newjson);
					} catch (JsonParseException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					} catch (JsonMappingException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					} catch (IOException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					missions.add(miss);
					newjson = newjson.substring(newjson.indexOf("}") + 2,
							newjson.length());
				}

				returnInt = 1;

			}
		}).start();

		while (returnInt == 0) {
		}

		return missions;

	}

	public Object fromJsonU(String json) throws JsonParseException,
			JsonMappingException, IOException {
		UserId garima = new ObjectMapper().readValue(json, UserId.class);

		return garima;
	}

	public Object fromJsonM(String json) throws JsonParseException,
			JsonMappingException, IOException {
		Mission garima = new ObjectMapper().readValue(json, Mission.class);

		return garima;
	}
}
