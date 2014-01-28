package com.example.gpsloc;


import java.util.ArrayList;
import java.util.List;

import Webservice.Main;
import Webservice.Mission;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;

public class MainActivity extends FragmentActivity {
	
	
	public static final String MY_PREFERENCES = "myPreferences";
	private SharedPreferences preferences;
	private Main main;
	private int userId;
	private String userLogin, userPassword;
	private List<Mission> missions;
	private ArrayAdapter<Mission> missionAdapter;
	private ListView missionList;
	private TextView whoLogin;
	
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
		
		main=new Main();
		missions=new ArrayList<Mission>();
		missionList = (ListView) findViewById(R.id.missions);
		missionAdapter = new ArrayAdapter<Mission>(this, R.layout.text, missions);
		
		Button button = (Button) findViewById(R.id.getMission);
		
		button.setOnClickListener(new View.OnClickListener() {
		    public void onClick(View v) {
		    	missions=new ArrayList<Mission>();
		        try {
		        	missionAdapter.clear();
					missionList.setAdapter(missionAdapter);
					//userId=main.login("kuba", "1234");
		        	userId=preferences.getInt("userID", -1);
		    		userLogin=preferences.getString("userLogin", "");
		    		userPassword=preferences.getString("userPassword", "");
		        	System.out.println(preferences.getInt("userID", -1));
					System.out.println(preferences.getString("userLogin", ""));
					System.out.println(preferences.getString("userPassword", ""));
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
				
				preferences.getString("destLat", "0.0");
				preferences.getString("destLong", "0.0");
				
				SharedPreferences.Editor preferencesEditor = preferences.edit();
				preferencesEditor.putString("destLat", String.valueOf(clicked.getLatitude()));
				preferencesEditor.putString("destLong", String.valueOf(clicked.getLongitude()));
				preferencesEditor.putString("destName", clicked.getMission());
				preferencesEditor.commit();
				
				Intent j = new Intent(MainActivity.this, MapActivity.class);
				startActivity(j);
				
				missionAdapter.clear();
				missionList.setAdapter(missionAdapter);
			}
			
		});
		//////////////////////////////////////////////////////////////////////////////////
		
		Button loguj = (Button) findViewById(R.id.loggin);
		
		loguj.setOnClickListener(new View.OnClickListener() {
		    public void onClick(View v) {
		    	
		    	Intent i = new Intent(MainActivity.this, LoginActivity.class);
				startActivity(i);
				
				userId=preferences.getInt("userID", -1);
				userLogin=preferences.getString("userLogin", "");
				userPassword=preferences.getString("userPassword", "");
				
				//whoLogin = (TextView) findViewById(R.id.whoIn);
				///whoLogin.setText("Zalogowany jako: "+preferences.getString("userLogin", ""));
		        
		    }
		});
		
		//whoLogin = (TextView) findViewById(R.id.whoIn);
		//whoLogin.setText("Zalogowany jako: "+preferences.getString("userLogin", ""));
		
	}
	
	@Override
	protected void onResume(){
		super.onResume();
		
		whoLogin = (TextView) findViewById(R.id.whoIn);
		whoLogin.setText("Zalogowany jako: "+preferences.getString("userLogin", ""));
		
	}
	
	@Override
	protected void onStop() {
	    super.onStop();
	}

	@Override
	protected void onDestroy() {
	    super.onDestroy();
	}
	
}