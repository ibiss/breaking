package Webservice;

public class UserId {

    private String id;

    public String getId() {
        return id;
    }

    public void setName(String name) {
        this.id = name;
    }

    @Override
    public String toString() {
        return "User [name=" + id + "]";
    }
}
