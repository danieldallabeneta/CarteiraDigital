package br.udesc.MicroServiceUserData.jpa;

import br.udesc.MicroServiceUserData.model.ModelUsuario;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UsuarioRepository extends JpaRepository<ModelUsuario, Integer> {

    Optional<ModelUsuario> findByEmail(String email);

}
