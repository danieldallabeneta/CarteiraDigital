package br.udesc.MicroServiceUserData.model;

public class ModelUsuarioAuxiliar extends ModelUsuarioBase {

    public ModelUsuarioAuxiliar(String nome, String email, String password) {
        super(nome, email, password);
    }

    @Override
    public String toString() {
        return "ModelUsuarioAuxiliar{" + "nome=" + getNome() + ", email=" + getEmail() + ", password=" + getPassword() + '}';
    }
}
