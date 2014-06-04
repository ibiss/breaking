package Webservice;

import java.util.ArrayList;

public class GameInstance{
	
	private int id;
	private String player1;
	private String player2;
	private boolean available;
	private int mode;
	private ArrayList<CheckPoint> list;
	
	public int getMode() {
		return mode;
	}
	
	public void setMode(int mode) {
		this.mode = mode;
	}
	
	public boolean isAvailable() {
		return available;
	}
	public void setAvailable(boolean available) {
		this.available = available;
	}
	
	public String getPlayer2() {
		return player2;
	}
	public void setPlayer2(String player2) {
		this.player2 = player2;
	}
	public String getPlayer1() {
		return player1;
	}
	public void setPlayer1(String player1) {
		this.player1 = player1;
	}
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	
	@Override
    public String toString()
    {
		String returnStr="Typ gry ";
		
		if(mode==1)
		{
			returnStr+="Król wzgórza.";
		}
		else if(mode==2)
		{
			returnStr+="Wiêcej znaczy lepiej.";
		}
		else if(mode==3)
		{
			returnStr+="Walka gangów.";
		}
		
		returnStr+="\nDostêpna: "+this.available;
		returnStr+="; "+ player1 +" vs "+player2;
		
    	return returnStr;
    }
	
	public ArrayList<CheckPoint> getList() {
		return list;
	}
	public void setList(ArrayList<CheckPoint> list) {
		this.list = list;
	}	
	
}