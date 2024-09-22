package br.udesc.MicroServiceUserData.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;

@Entity(name = "tbusuario")
public class ModelUsuario extends ModelUsuarioBase {

    @Id
    @GeneratedValue
    private Integer id;

    private String salt;

    public ModelUsuario(Integer id, String nome, String email, String password, String salt) {
        super(nome, email, password);
        this.id = id;
        this.salt = salt;
    }

    public ModelUsuario() {
        super("", "", "");
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getSalt() {
        return salt;
    }

    public void setSalt(String salt) {
        this.salt = salt;
    }

    @Override
    public String toString() {
        return "ModelUsuario{" + "id=" + id + ", nome=" + getNome() + ", email=" + getEmail() + ", password=" + getPassword() + ", salt=" + salt + '}';
    }
}