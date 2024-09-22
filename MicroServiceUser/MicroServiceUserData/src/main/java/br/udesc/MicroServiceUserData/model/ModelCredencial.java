package br.udesc.MicroServiceUserData.model;

import org.mindrot.jbcrypt.BCrypt;

public class ModelCredencial {

    private String userEmail;
    private String senha;

    public ModelCredencial() {
    }

    public ModelCredencial(String userEmail, String senha) {
        this.userEmail = userEmail;
        this.senha = senha;
    }

    public ModelCredencial(String senha) {
        super();
        this.senha = senha;
    }

    public String getUserEmail() {
        return userEmail;
    }

    public void setUserEmail(String userEmail) {
        this.userEmail = userEmail;
    }

    public String getSenha() {
        return senha;
    }

    public void setSenha(String senha) {
        this.senha = senha;
    }

    public String[] getSenhaCriptografada() {
        final String salt = BCrypt.gensalt();
        String senhaEncrypt = BCrypt.hashpw(this.getSenha(), salt);
        return new String[]{senhaEncrypt, salt};
    }

}
