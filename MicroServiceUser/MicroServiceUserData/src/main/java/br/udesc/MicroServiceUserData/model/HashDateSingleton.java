package br.udesc.MicroServiceUserData.model;

import java.util.Map;
import java.time.LocalDateTime;
import java.util.HashMap;

public class HashDateSingleton {
    
    private static HashDateSingleton instance;

    private Map<String, LocalDateTime> hashDateMap;
    private long validade = 5;
    
    private HashDateSingleton(){
        hashDateMap = new HashMap<>();
    }

    public static synchronized HashDateSingleton getInstance() {
        if (instance == null) {
            instance = new HashDateSingleton();
        }
        return instance;
    }

    public void addHashDate(String hash, LocalDateTime date) {
        hashDateMap.put(hash, date);
    }

    public LocalDateTime getDateByHash(String hash) {
        return hashDateMap.get(hash);
    }

    public boolean containsHash(String hash) {
        return hashDateMap.containsKey(hash);
    }

    public void removeHash(String hash) {
        hashDateMap.remove(hash);
    }

    public int getSize() {
        return hashDateMap.size();
    }

    public boolean validaHash(String hash){
        if(containsHash(hash)){
            LocalDateTime data = hashDateMap.get(hash);
            return data.plusMinutes(validade).isAfter(LocalDateTime.now());
        }
        return false;
    }

}
