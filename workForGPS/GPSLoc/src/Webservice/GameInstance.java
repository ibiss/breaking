package Webservice;

import java.util.ArrayList;

public class GameInstance{
	
	private int id;
	private String player1;
	private String player2;
	//private String dateTime1;
	//private String dateTime2;
	private boolean available;
	private ArrayList<CheckPoint> list;
	//private Object mode;
	//private int winner;
	
	
	/*public int getWinner() {
		return winner;
	}
	public void setWinner(int winner) {
		this.winner = winner;
	}*/
	//public Object getMode() {
	//	return mode;
	//}
	//public void setMode(Object mode) {
	//	this.mode = mode;
	//}
	public boolean isAvailable() {
		return available;
	}
	public void setAvailable(boolean available) {
		this.available = available;
	}
	/*public String getDateTime2() {
		return dateTime2;
	}
	public void setDateTime2(String dateTime2) {
		this.dateTime2 = dateTime2;
	}
	public String getDateTime1() {
		return dateTime1;
	}
	public void setDateTime1(String dateTime1) {
		this.dateTime1 = dateTime1;
	}*/
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
    	return player1 +" vs "+player2;
    }
	
	public ArrayList<CheckPoint> getList() {
		return list;
	}
	public void setList(ArrayList<CheckPoint> list) {
		this.list = list;
	}	
	
}