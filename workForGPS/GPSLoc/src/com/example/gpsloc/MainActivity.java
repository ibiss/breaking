package com.example.gpsloc;


import java.util.ArrayList;
import java.util.List;

import Webservice.GameInstance;
import Webservice.Main;
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
import android.widget.Toast;

import com.google.gson.Gson;

public class MainActivity extends FragmentActivity {
	
	
	public static final String MY_PREFERENCES = "myPreferences";
	private SharedPreferences preferences;
	private Main main;
	private int userId;
	private String userLogin, userPassword;
	private List<GameInstance> missions;
	private ArrayAdapter<GameInstance> missionAdapter;
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
		
		/*if(userId==-1)
		{
			i = new Intent(this, LoginActivity.class);
			startActivity(i);
		}*/
		
		main=new Main();
		missions=new ArrayList<GameInstance>();
		missionList = (ListView) findViewById(R.id.missions);
		missionAdapter = new ArrayAdapter<GameInstance>(this, R.layout.text, missions);
		
		Button button = (Button) findViewById(R.id.getMission);
		
		button.setOnClickListener(new View.OnClickListener() {
		    public void onClick(View v) {
		    	missions=new ArrayList<GameInstance>();
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
						missions=main.getGames(userId, userLogin, userPassword);
						System.out.println(missions);
						missionAdapter.addAll(missions);
						missionList.setAdapter(missionAdapter);
					}
					
				} catch (Exception e) {
					e.printStackTrace();
				}
		        
		    }
		});
		
		//missionAdapter = new ArrayAdapter<Mission>(this, R.layout.text, missions);
		//missionList.setAdapter(missionAdapter);
		
		missionList.setOnItemClickListener(new OnItemClickListener() {
			@Override
			public void onItemClick(AdapterView<?> parent, View view, int position, long id)
			{
				GameInstance clicked=(GameInstance) missionList.getItemAtPosition(position);
				
				int gameId=clicked.getId();
	    		userLogin=preferences.getString("userLogin", "");
	    		userPassword=preferences.getString("userPassword", "");
				
	    		
	    		if(clicked.isAvailable()) {
	    			
	    			try {
						clicked.setList(main.getCheckPoints(gameId, userLogin, userPassword));
						
						Intent j = new Intent(MainActivity.this, MapActivity.class);
						
						Gson gS = new Gson();
						String target = gS.toJson(clicked);					
						
						j.putExtra("game", target);
						startActivity(j);
						
						missionAdapter.clear();
						missionList.setAdapter(missionAdapter);
						
					} catch (Exception e) {
						
						e.printStackTrace();
					}
	    			
	    		}
	    		else
	    		{
	    			Toast.makeText( getApplicationContext(),"Ta gra nie jest jescze dostêpna",	Toast.LENGTH_SHORT ).show();
	    		}
	    		
				//SharedPreferences.Editor preferencesEditor = preferences.edit();
				//preferencesEditor.putString("currentGame", clicked);
				//preferencesEditor.commit();
				
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