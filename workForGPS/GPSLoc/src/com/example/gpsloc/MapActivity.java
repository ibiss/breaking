package com.example.gpsloc;


import java.util.ArrayList;
import java.util.Calendar;

import Webservice.CheckPoint;
import Webservice.GameInstance;
import Webservice.Main;
import android.content.Context;
import android.content.SharedPreferences;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.gson.Gson;

public class MapActivity extends FragmentActivity {
	
	private GoogleMap map;
	private int userIcon, destinationIcon;
	private LocationManager mlocManager;
	private LocationListener mlocListener;
	private double lat,lng;
	private Marker userMarker;
	private ArrayList<Marker> destinationMarkers;
	public static final String MY_PREFERENCES = "myPreferences";
	private SharedPreferences preferences;
	private GameInstance game;
	private ArrayList<Boolean> completed;
	private Main main;
	private ArrayList<CheckPoint> checkPoints;
	
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.map);
		
		Gson gS = new Gson();
		String src = getIntent().getStringExtra("game");
		game = gS.fromJson(src, GameInstance.class);
		
		preferences = getSharedPreferences(MY_PREFERENCES, MainActivity.MODE_PRIVATE);
		
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
		
		mlocListener = new MyLocationListener();

		mlocManager.requestLocationUpdates( LocationManager.GPS_PROVIDER, 1000, 0, mlocListener);
		
		destinationMarkers=new ArrayList<Marker>();
		completed=new ArrayList<Boolean>();
		
		checkPoints = game.getList();
		
		for(int i=0; i<checkPoints.size(); i++)
		{
			/*if(destinationMarkers.get(i)!=null) {
				destinationMarkers.get(i).remove();
			}*/
			
			if(preferences.getString("userLogin", "").equals(game.getPlayer1()))
			{
				destinationMarkers.add( 
						map.addMarker(new MarkerOptions()
						.position(new LatLng( Double.valueOf(checkPoints.get(i).getLatitudeP1()), Double.valueOf(checkPoints.get(i).getLongitudeP1()) ))
						.title("Checkpoint "+(i+1))
						.icon(BitmapDescriptorFactory.fromResource(destinationIcon))
						.snippet(""))
			    );
			}
			else
			{
				destinationMarkers.add( 
						map.addMarker(new MarkerOptions()
						.position(new LatLng( Double.valueOf(checkPoints.get(i).getLatitudeP2()), Double.valueOf(checkPoints.get(i).getLongitudeP2()) ))
						.title("Checkpoint "+(i+1))
						.icon(BitmapDescriptorFactory.fromResource(destinationIcon))
						.snippet(""))
			    );
			}
			
			completed.add(false);
			
		}
		
	}
	
	@Override
	public void onResume(){
		System.out.println("onResume MapActivity");
		mlocListener = new MyLocationListener();
		mlocManager.requestLocationUpdates( LocationManager.GPS_PROVIDER, 1000, 0, mlocListener);
	    super.onResume();
	}
	
	@Override
	public void onPause(){
		System.out.println("onPause MapActivity");
		if(mlocListener!=null)
		{
			mlocManager.removeUpdates(mlocListener);
			mlocListener=null;
		}
	    
	    super.onPause();
	} 
	
	@Override
	protected void onDestroy() {
		System.out.println("onDestroy MapActivity");
		super.onDestroy();
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
		
		boolean all=true;
		
		for(int i=0; i<destinationMarkers.size(); i++)
		{
			
			if( destinationMarkers.get(i)!=null && (Math.abs(userMarker.getPosition().latitude-destinationMarkers.get(i).getPosition().latitude))<0.005 && (Math.abs(userMarker.getPosition().longitude-destinationMarkers.get(i).getPosition().longitude))<0.005 )
			{
				
				Toast.makeText( getApplicationContext(),"Zdobyles ten checkpoint",	Toast.LENGTH_SHORT ).show();
				
				completed.set(i, true);
				
				main = new Main();
				
				try {
					
					Calendar rightNow = Calendar.getInstance();
					
					if(isNetworkAvailable())
					{
						main.callWinner(preferences.getInt("userID", -1), game.getId(), rightNow.getTimeInMillis(),preferences.getString("userLogin", ""), preferences.getString("userPassword", ""));
					}
					else
					{
						Toast.makeText( getApplicationContext(),"Brak po³¹czenia z internetem, zsynchronizuj dane potem",	Toast.LENGTH_SHORT ).show();
						
						preferences.getInt("GameID", game.getId());
						preferences.getInt("NumOfChek", checkPoints.size());
						preferences.getLong("Hour", rightNow.getTimeInMillis());
						
					}
					
				} catch (Exception e) {
					
					e.printStackTrace();
				}
				
			}
			
			if(completed.get(i)==false)
			{
				all=false;
			}
			
		}
		
		
		if(all==true)
		{
			Toast.makeText( getApplicationContext(),"Zaliczyles gre! Gratulacje!",	Toast.LENGTH_SHORT ).show();
			
			try {
								
				mlocManager.removeUpdates(mlocListener);
				mlocListener=null;
				finish();
				
			} catch (Exception e) {
				
				e.printStackTrace();
			}
			
			finish();
		}
		
		map.animateCamera(CameraUpdateFactory.newLatLng(lastLatLng), 1000, null);
		
	}
	
	private boolean isNetworkAvailable() {
	    ConnectivityManager connectivityManager = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
	    NetworkInfo activeNetworkInfo = connectivityManager.getActiveNetworkInfo();
	    return activeNetworkInfo != null && activeNetworkInfo.isConnected();
	}
	
	public class MyLocationListener implements LocationListener
	{

		@Override
		public void onLocationChanged(Location loc)
		{
			SharedPreferences.Editor preferencesEditor = preferences.edit();
			
			lat = loc.getLatitude();
			lng = loc.getLongitude();
			
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
	
	@Override
	public void onBackPressed() {
	    finish();
	}
	
}