package com.example.gpsloc;


import java.util.ArrayList;
import java.util.List;

import Webservice.Main;
import Webservice.Mission;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;

public class MainActivity extends FragmentActivity {
	
	private GoogleMap map;
	private int userIcon, destinationIcon;
	private LocationManager mlocManager;
	private double lat,lng;
	private Marker userMarker,destinationMarker;
	public static final String MY_PREFERENCES = "myPreferences";
	private SharedPreferences preferences;
	private Main main;
	private int userId;
	private String userLogin, userPassword;
	private List<Mission> missions;
	private ArrayAdapter<Mission> missionAdapter;
	private ListView missionList;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		preferences = getSharedPreferences(MY_PREFERENCES, MainActivity.MODE_PRIVATE);
		
		userId=preferences.getInt("userID", -1);
		userLogin=preferences.getString("userLogin", "");
		userPassword=preferences.getString("userPassword", "");
		
		Intent i;
		
		if(userId==-1)
		{
			i = new Intent(this, LoginActivity.class);
			startActivity(i);
		}
		
		
		
		lat=Double.valueOf(preferences.getString("lastLatitude", "52.259"));
		lng=Double.valueOf(preferences.getString("lastLongitude", "21.020"));
		
		userIcon = R.drawable.yellow_point;
		destinationIcon = R.drawable.green_point;
		
		map = ((SupportMapFragment)  getSupportFragmentManager().findFragmentById(R.id.map)).getMap();
		map.setMapType(GoogleMap.MAP_TYPE_HYBRID);
		mlocManager = (LocationManager)getSystemService(Context.LOCATION_SERVICE);
		
		if(userMarker!=null) {
			userMarker.remove();
		}
		
		userMarker = map.addMarker(new MarkerOptions()
	    .position(new LatLng(lat, lng))
	    .title("Your last position")
	    .icon(BitmapDescriptorFactory.fromResource(userIcon))
	    .snippet(""));
		
		map.animateCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(lat, lng),12.0f), 3000, null);
		
		LocationListener mlocListener = new MyLocationListener();

		mlocManager.requestLocationUpdates( LocationManager.GPS_PROVIDER, 0, 0, mlocListener);
		
		main=new Main();
		missions=new ArrayList<Mission>();
		missionList = (ListView) findViewById(R.id.missions);
		missionAdapter = new ArrayAdapter<Mission>(this, R.layout.text, missions);
		
		Button button = (Button) findViewById(R.id.getMission);
		
		button.setOnClickListener(new View.OnClickListener() {
		    public void onClick(View v) {
		    	missions=new ArrayList<Mission>();
		        try {
		        	
					//userId=main.login("kuba", "1234");
		        	userId=preferences.getInt("userID", -1);
		    		userLogin=preferences.getString("userLogin", "");
		    		userPassword=preferences.getString("userPassword", "");
		        	//System.out.println(preferences.getInt("userID", -1));
					//System.out.println(preferences.getString("userLogin", ""));
					//System.out.println(preferences.getString("userPassword", ""));
					if(userId!=-1){
						System.out.println("jestem");
						missions=main.getMission(userId, userLogin, userPassword);
						System.out.println(missions);
						missionAdapter.addAll(missions);
						missionList.setAdapter(missionAdapter);
					}
					
				} catch (Exception e) {
					e.printStackTrace();
				}
		        
		    }
		});
		
		//System.out.println("gdzie sa misje??");
		//System.out.println(missions);
		
		//missionAdapter = new ArrayAdapter<Mission>(this, R.layout.text, missions);
		//missionList.setAdapter(missionAdapter);
		
		missionList.setOnItemClickListener(new OnItemClickListener() {
			@Override
			public void onItemClick(AdapterView<?> parent, View view, int position, long id)
			{
				Mission clicked=(Mission) missionList.getItemAtPosition(position);
				
				if(destinationMarker!=null) {
					destinationMarker.remove();
				}
				
				destinationMarker = map.addMarker(new MarkerOptions()
			    .position(new LatLng(Double.valueOf(clicked.getLatitude()), Double.valueOf(clicked.getLongitude())))
			    .title(clicked.toString())
			    .icon(BitmapDescriptorFactory.fromResource(destinationIcon))
			    .snippet(""));
				//System.out.println(userMarker.getPosition()+" "+destinationMarker.getPosition());
				
				
				
				missionAdapter.clear();
				missionList.setAdapter(missionAdapter);
			}
			
		});
		//////////////////////////////////////////////////////////////////////////////////
		
	}
	
	private void updatePlaces()
	{
		Location lastLoc = mlocManager.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
		//lat = lastLoc.getLatitude();
		//lng = lastLoc.getLongitude();
		LatLng lastLatLng = new LatLng(lat,lng);
		
		if(userMarker!=null){
			userMarker.remove();
		}
		
		userMarker = map.addMarker(new MarkerOptions()
	    .position(lastLatLng)
	    .title("Your last position")
	    .icon(BitmapDescriptorFactory.fromResource(userIcon))
	    .snippet(""));
		
		if( destinationMarker!=null && (Math.abs(userMarker.getPosition().latitude-destinationMarker.getPosition().latitude))<0.005 && (Math.abs(userMarker.getPosition().longitude-destinationMarker.getPosition().longitude))<0.005 )
		{
			Toast.makeText( getApplicationContext(),"Zdobyles!!!",	Toast.LENGTH_SHORT ).show();
		}
		
		map.animateCamera(CameraUpdateFactory.newLatLng(lastLatLng), 1000, null);
	}
	
	public class MyLocationListener implements LocationListener
	{

		@Override
		public void onLocationChanged(Location loc)
		{
			SharedPreferences.Editor preferencesEditor = preferences.edit();
			
			lat = loc.getLatitude();
			lng = loc.getLongitude();
			//Globals.lastLatitude=lat;
			//Globals.lastLongitude=lng;
			
			preferencesEditor.putString("lastLatitude", Double.toString(lat));
			preferencesEditor.putString("lastLongitude", Double.toString(lng));
			preferencesEditor.commit();
			
			String Text = "My current location is: " +"Latitud = " + loc.getLatitude() + "Longitud = " + loc.getLongitude();
			updatePlaces();
			TextView gpsData = (TextView) findViewById(R.id.wspolrzedne);
			gpsData.setText(Text);
			
		}
		
		@Override
		public void onProviderDisabled(String provider)
		{
			Toast.makeText( getApplicationContext(),"Gps Disabled",	Toast.LENGTH_SHORT ).show();
		}
		
		@Override
		public void onProviderEnabled(String provider)
		{
			Toast.makeText( getApplicationContext(),"Gps Enabled",Toast.LENGTH_SHORT).show();
		}

		@Override
		public void onStatusChanged(String provider, int status, Bundle extras)
		{
			
		}

	}/* End of Class MyLocationListener */
	
	/*
	 * public AlertDialog loginDialog(Context c, String message) {
	 * System.out.println("jestem"); final SharedPreferences.Editor
	 * preferencesEditor = preferences.edit();
	 * 
	 * LayoutInflater factory = LayoutInflater.from(c); final View textEntryView
	 * = factory.inflate(R.layout.login, null); final AlertDialog.Builder
	 * failAlert = new AlertDialog.Builder(c);
	 * failAlert.setTitle("Login/ Register Failed");
	 * 
	 * failAlert.setNegativeButton("OK", new DialogInterface.OnClickListener() {
	 * public void onClick(DialogInterface dialog, int whichButton) { //
	 * Cancelled } });
	 * 
	 * AlertDialog.Builder alert = new AlertDialog.Builder(c);
	 * alert.setTitle("Login/ Register"); alert.setMessage(message);
	 * alert.setView(textEntryView);
	 * 
	 * alert.setPositiveButton("Login", new DialogInterface.OnClickListener() {
	 * public void onClick(DialogInterface dialog, int whichButton) { try {
	 * final EditText usernameInput = (EditText)
	 * textEntryView.findViewById(R.id.userNameEditText); final EditText
	 * passwordInput = (EditText)
	 * textEntryView.findViewById(R.id.passwordEditText);
	 * preferencesEditor.putString("UserName",
	 * usernameInput.getText().toString());
	 * preferencesEditor.putString("Password",
	 * passwordInput.getText().toString()); } catch (Exception e) {
	 * e.printStackTrace(); } } });
	 * 
	 * alert.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
	 * public void onClick(DialogInterface dialog, int whichButton) { //
	 * Canceled. } });
	 * 
	 * return alert.create(); }
	 */
	
}