package com.example.gpsloc;


import android.content.Context;
import android.content.SharedPreferences;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.widget.TextView;
import android.widget.Toast;
import android.view.Menu;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;

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
	private Marker userMarker;
	public static final String MY_PREFERENCES = "myPreferences";
	private SharedPreferences preferences;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);		
		
		preferences = getSharedPreferences(MY_PREFERENCES, MainActivity.MODE_PRIVATE);
		
		lat=Double.valueOf(preferences.getString("lastLatitude", "52.259"));
		lng=Double.valueOf(preferences.getString("lastLongitude", "21.020"));
		
		userIcon = R.drawable.yellow_point;
		destinationIcon = R.drawable.green_point;
		
		map = ((SupportMapFragment)  getSupportFragmentManager().findFragmentById(R.id.map)).getMap();
		map.setMapType(GoogleMap.MAP_TYPE_HYBRID);
		mlocManager = (LocationManager)getSystemService(Context.LOCATION_SERVICE);
		
		if(userMarker!=null) userMarker.remove();
		
		userMarker = map.addMarker(new MarkerOptions()
	    .position(new LatLng(lat, lng))
	    .title("Your last position")
	    .icon(BitmapDescriptorFactory.fromResource(userIcon))
	    .snippet(""));
		
		map.animateCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(lat, lng),12.0f), 3000, null);
		
		LocationListener mlocListener = new MyLocationListener();

		mlocManager.requestLocationUpdates( LocationManager.GPS_PROVIDER, 0, 0, mlocListener);
		
	}
	
	private void updatePlaces()
	{
		Location lastLoc = mlocManager.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
		//lat = lastLoc.getLatitude();
		//lng = lastLoc.getLongitude();
		LatLng lastLatLng = new LatLng(lat,lng);
		
		if(userMarker!=null) userMarker.remove();
		
		userMarker = map.addMarker(new MarkerOptions()
	    .position(lastLatLng)
	    .title("Your last position")
	    .icon(BitmapDescriptorFactory.fromResource(userIcon))
	    .snippet(""));
		
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

}
