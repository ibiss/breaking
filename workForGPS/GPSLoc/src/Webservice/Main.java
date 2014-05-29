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
				while(true){
					
				
				String webPage = "http://projectbreaking.herokuapp.com/webservices/login/"+ name + "/?format=json";
				URL url = null;
				try {
					url = new URL(webPage);
				} catch (MalformedURLException e2) {
					e2.printStackTrace();
					break;
				}
				URLConnection urlConnection = null;
				try {
					urlConnection = url.openConnection();
				} catch (IOException e1) {
					e1.printStackTrace();
					break;
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
					break;
					
				}
					
				//String json =  "{\"count\": 1, \"next\": null, \"previous\": null, \"results\": [{\"id\": 1}]}";
				String newjson = json.substring(1, json.length());
				Main converter = new Main();
				newjson = newjson.substring(newjson.indexOf("{"), newjson.length());

				UserId userId = null;
				try {
					userId = (UserId) converter.fromJsonU(newjson);
				} catch (JsonParseException e) {
					e.printStackTrace();
					break;
				} catch (JsonMappingException e) {
					e.printStackTrace();
					break;
				} catch (IOException e) {
					e.printStackTrace();
					break;
				}

				returnInt = Integer.valueOf(userId.getId());
				break;
				}

			}
		}).start();

		while (returnInt == 0) {
		}

		return returnInt;
	}
	
	public List<GameInstance> getGames(final int id, final String name,
			final String password) throws JsonParseException,
			JsonMappingException, Exception {
		final List<GameInstance> gamesInstance = new ArrayList<GameInstance>();
		returnInt = 0;

		new Thread(new Runnable() {
			public void run() {
				while(true)
				{
				System.out.println(id + name + password);
				
				// String webPage =
				// "http://projectbreaking.herokuapp.com/webservices/login/" +
				// name + "/?format=json";
				String webPage = "http://projectbreaking.herokuapp.com/webservices/gameinstance/"
						+ id + "/?format=json";
				URL url = null;
				try {
					url = new URL(webPage);
				} catch (MalformedURLException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
					break;
				}
				URLConnection urlConnection = null;
				try {
					urlConnection = url.openConnection();
				} catch (IOException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
					break;
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
					break;
				}
				
				System.out.println(json.length());
				System.out.println(json);
				//String json = "{\"count\": 2, \"next\": null, \"previous\": null, \"results\": [{\"id\": 1, \"player1\": \"kuba\", \"player2\": \"suchar\",  \"available\": true}, {\"id\": 2, \"player1\": \"kuba\", \"player2\": \"suchar\", \"available\": false}]}";
				
				String newjson = json.substring(1, json.length());
				Main converter = new Main();
				GameInstance game = new GameInstance();
				
				try
				{
					newjson = newjson.substring(newjson.indexOf("{"), newjson.length());
					
					while (newjson.indexOf("}") + 2 <= newjson.length()) {
						try {
							game = (GameInstance) converter.fromJsonG(newjson);
						} catch (JsonParseException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
							break;
						} catch (JsonMappingException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
							break;
						} catch (IOException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
							break;
						}
						gamesInstance.add(game);
						newjson = newjson.substring(newjson.indexOf("}") + 2,
								newjson.length());
					}

					returnInt = 1;
					break;
					
				}
				catch (StringIndexOutOfBoundsException e)
				{
					returnInt = 1;
					break;
				}

				
				}
			}
		}).start();

		while (returnInt == 0) {
		}

		return gamesInstance;

	}
	
	public ArrayList<CheckPoint> getCheckPoints(final int id, final String name,
			final String password) throws JsonParseException,
			JsonMappingException, Exception {
		final ArrayList<CheckPoint> chekcPoints = new ArrayList<CheckPoint>();
		returnInt = 0;

		new Thread(new Runnable() {
			public void run() {
				while(true)
				{
				System.out.println(id + name + password);
				
				// String webPage =
				// "http://projectbreaking.herokuapp.com/webservices/login/" +
				// name + "/?format=json";
				String webPage = "http://projectbreaking.herokuapp.com/webservices/checkpoints/"
						+ id + "/?format=json";
				URL url = null;
				try {
					url = new URL(webPage);
				} catch (MalformedURLException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
					break;
				}
				URLConnection urlConnection = null;
				try {
					urlConnection = url.openConnection();
				} catch (IOException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
					break;
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
					break;
				}
				
				//System.out.println(json.length());
				//System.out.println(json);
				//String json = "{\"count\": 3, \"next\": null, \"previous\": null, \"results\": [{\"id\": 3, \"latitudeP1\": \"51.055558773389026\", \"longitudeP1\": \"19.91201162338257\", \"latitudeP2\": \"50.531838773389026\", \"longitudeP2\": \"20.91201162338257\"}, {\"id\": 2, \"latitudeP1\": \"52.031838773389026\", \"longitudeP1\": \"18.912016666666\", \"latitudeP2\": \"49.531838773389026\", \"longitudeP2\": \"20.9120133333357\"}]}";
				
				String newjson = json.substring(1, json.length());
				Main converter = new Main();
				CheckPoint check = new CheckPoint();
				
				try
				{
					newjson = newjson.substring(newjson.indexOf("{"), newjson.length());
					
					while (newjson.indexOf("}") + 2 <= newjson.length()) {
						try {
							check = (CheckPoint) converter.fromJsonC(newjson);
						} catch (JsonParseException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
							break;
						} catch (JsonMappingException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
							break;
						} catch (IOException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
							break;
						}
						chekcPoints.add(check);
						newjson = newjson.substring(newjson.indexOf("}") + 2,
								newjson.length());
					}

					returnInt = 1;
					break;
					
				}
				catch (StringIndexOutOfBoundsException e)
				{
					returnInt = 1;
					break;
				}
				
				}
			}
		}).start();

		while (returnInt == 0) {
		}

		return chekcPoints;

	}
	
	public void callWinner(final int uid, final int gid, final long date, final String name,
			final String password) throws Exception {
		
		new Thread(new Runnable() {
			public void run() {
				
				while(true)
				{
				
				// String webPage =
				// "http://projectbreaking.herokuapp.com/webservices/login/" +
				// name + "/?format=json";
				String webPage = "http://projectbreaking.herokuapp.com/webservices/acceptgame/"+ uid +"/"+ gid + "/"+ date +"/?format=json";
				URL url = null;
				try {
					url = new URL(webPage);
				} catch (MalformedURLException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
					break;
				}
				URLConnection urlConnection = null;
				try {
					urlConnection = url.openConnection();
				} catch (IOException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
					break;
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
					
					System.out.println("nieporpawne dane");
					break;
				}
				
				break;
				}
			}
		}).start();


	}

	public Object fromJsonU(String json) throws JsonParseException,
			JsonMappingException, IOException {
		UserId garima = new ObjectMapper().readValue(json, UserId.class);

		return garima;
	}

	/*public Object fromJsonM(String json) throws JsonParseException,
			JsonMappingException, IOException {
		Mission garima = new ObjectMapper().readValue(json, Mission.class);

		return garima;
	}*/
	
	public Object fromJsonG(String json) throws JsonParseException,
			JsonMappingException, IOException {
		GameInstance garima = new ObjectMapper().readValue(json, GameInstance.class);

		return garima;
	}
	
	public Object fromJsonC(String json) throws JsonParseException,
	JsonMappingException, IOException {
		CheckPoint garima = new ObjectMapper().readValue(json, CheckPoint.class);

		return garima;
	}
	
}
