package com.example.alpr;

public class User {
    private String Platenumber;
    private Integer Balance;

    public User() {
    }

    public String getPlatenumber() {
        return Platenumber;
    }

    public void setPlatenumber(String platenumber) {
        Platenumber = platenumber;
    }

    public Integer getBalance() {
        return Balance;
    }

    public void setBalance(Integer balance) {
        Balance = balance;
    }
}