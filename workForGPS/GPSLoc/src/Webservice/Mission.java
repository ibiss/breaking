package Webservice;

import org.codehaus.jackson.map.ser.std.ToStringSerializer;

public class Mission {
    private String latitude;
    private String longitude;
    private String timestamp;
    private String mission;
    
    public String getLatitude() {
        return latitude;
    }
    
    public String getLongitude() {
        return longitude;
    }
    
    public String getTimestamp() {
        return timestamp;
    }
    
    public String getMission() {
        return mission;
    }
    
    @Override
    public String toString()
    {
    	return "mission: "+mission;
    }
}
