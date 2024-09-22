package br.udesc.MicroServiceUserData.jpa;

public interface PasswordEncoder {
    
    public boolean checkPassword(String rawPassword, String encryptedPassword);
    
}
