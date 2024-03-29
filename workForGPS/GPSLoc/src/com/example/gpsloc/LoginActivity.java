package com.example.gpsloc;

import Webservice.Main;
import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class LoginActivity extends Activity {

	private Button zaloguj;
	private EditText login, pass;
	private int UID;
	private Main main;
	public static final String MY_PREFERENCES = "myPreferences";
	private SharedPreferences preferences;

	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.login);

		zaloguj = (Button) findViewById(R.id.logIn);
		login = (EditText) findViewById(R.id.userNameEditText);
		pass = (EditText) findViewById(R.id.passwordEditText);
		
		preferences = getSharedPreferences(MY_PREFERENCES, MainActivity.MODE_PRIVATE);
		main=new Main();
		zaloguj.setOnClickListener(new View.OnClickListener() {
			public void onClick(View v) {
				String log = login.getText().toString();
				String pswd = pass.getText().toString();

				if (log == "" || pswd == "") 
				{
					Toast.makeText(getApplicationContext(),	"Wpisz login i haslo", Toast.LENGTH_SHORT).show();
				} 
				else 
				{
					try 
					{
						UID = main.login(log, pswd);
						if (UID != -1) 
						{
							System.out.println(UID);
							SharedPreferences.Editor preferencesEditor = preferences.edit();
							preferencesEditor.putInt("userID", UID);
							preferencesEditor.putString("userLogin", log);
							preferencesEditor.putString("userPassword", pswd);
							preferencesEditor.commit();
							System.out.println(preferences.getInt("userID", -1));
							System.out.println(preferences.getString("userLogin", ""));
							System.out.println(preferences.getString("userPassword", ""));
							finish();
						} 
						else 
						{
							Toast.makeText(getApplicationContext(),"Niepoprawny login lub haslo",Toast.LENGTH_SHORT).show();
						}
					} 
					catch (Exception e) 
					{
						Toast.makeText(getApplicationContext(),"Nie udalo sie zalogowac, sprawdz polaczenie z interentem",Toast.LENGTH_SHORT).show();
						e.printStackTrace();
					}
				}
			}
		});

	}
	
	@Override
	public boolean onKeyDown(int keyCode, KeyEvent event)  {
	    if (  Integer.valueOf(android.os.Build.VERSION.SDK) < 7 
	            && keyCode == KeyEvent.KEYCODE_BACK
	            && event.getRepeatCount() == 0) {
	        onBackPressed();
	    }

	    return super.onKeyDown(keyCode, event);
	}

	@Override
	public void onBackPressed() {
	    return;
	}
	

}
