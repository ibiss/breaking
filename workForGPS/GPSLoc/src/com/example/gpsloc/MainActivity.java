package com.example.gpsloc;


import android.content.Context;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.widget.TextView;
import android.widget.Toast;
import android.view.Menu;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentActivity;

import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.SupportMapFragment;

public class MainActivity extends FragmentActivity {
	
	private GoogleMap map;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		
		map = ((SupportMapFragment)  getSupportFragmentManager().findFragmentById(R.id.map)).getMap();
		
		LocationManager mlocManager = (LocationManager)getSystemService(Context.LOCATION_SERVICE);

		LocationListener mlocListener = new MyLocationListener();

		mlocManager.requestLocationUpdates( LocationManager.GPS_PROVIDER, 0, 0, mlocListener);
		
	}

	public class MyLocationListener implements LocationListener
	{

		@Override
		public void onLocationChanged(Location loc)
		{
			loc.getLatitude();
			loc.getLongitude();
			
			String Text = "My current location is: " +"Latitud = " + loc.getLatitude() + "Longitud = " + loc.getLongitude();
			
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