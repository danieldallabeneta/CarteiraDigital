package br.udesc.MicroServiceUserData.model;

import br.udesc.MicroServiceUserData.jpa.PasswordEncoder;
import org.mindrot.jbcrypt.BCrypt;
import org.springframework.stereotype.Component;

@Component
public class BcryptPasswordEncoder implements PasswordEncoder{
    
    @Override
    public boolean checkPassword(String rawPassword, String encryptedPassword) {
        return BCrypt.checkpw(rawPassword, encryptedPassword);
    }
}
