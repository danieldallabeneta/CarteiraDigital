package br.udesc.MicroServiceUserData.rest;

import br.udesc.MicroServiceUserData.jpa.PasswordEncoder;
import br.udesc.MicroServiceUserData.jpa.UsuarioRepository;
import br.udesc.MicroServiceUserData.model.ModelCredencial;
import br.udesc.MicroServiceUserData.model.ModelUsuario;
import br.udesc.MicroServiceUserData.model.ModelUsuarioAuxiliar;
import jakarta.validation.Valid;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;


@RestController
public class UsuarioRest {

    private final UsuarioRepository usuarioRepository;
    private final PasswordEncoder passwordEncoder;

    @Autowired
    public UsuarioRest(UsuarioRepository usuarioRepository, PasswordEncoder passwordEncoder) {
        this.usuarioRepository = usuarioRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @PostMapping("/users")
    public Integer createUser(@Valid @RequestBody ModelUsuarioAuxiliar user) {
        Optional<ModelUsuario> aux = usuarioRepository.findByEmail(user.getEmail());

        if (aux.isEmpty()) {
            ModelUsuario usuario = new ModelUsuario();
            usuario.setNome(user.getNome());
            usuario.setEmail(user.getEmail());
            usuario.setPassword(user.getPassword());
            
            ModelCredencial cred = new ModelCredencial(usuario.getPassword());
            String[] encript = cred.getSenhaCriptografada();
            usuario.setPassword(encript[0]);
            usuario.setSalt(encript[1]);
            ModelUsuario savedUser = usuarioRepository.save(usuario);

            return savedUser.getId();
        }

        return aux.get().getId();
    }

    @GetMapping("/users")
    public List<ModelUsuario> allUsers() {
        return usuarioRepository.findAll();
    }

    @GetMapping("/users/{id}")
    public ModelUsuario getUser(@PathVariable int id) throws Exception {
        Optional<ModelUsuario> user = usuarioRepository.findById(id);
        if (user.isEmpty()) {
            throw new Exception("Erro: Id do usuário não encontrado");
        }
        return user.get();
    }

    @GetMapping("/usuario/{email}")
    public ModelUsuario getUserByEmail(@PathVariable String email) throws Exception {
        Optional<ModelUsuario> user = usuarioRepository.findByEmail(email);
        if (user.isEmpty()) {
            throw new Exception("Erro: Id do usuário não encontrado");
        }
        return user.get();
    }

    @DeleteMapping("/users/{id}")
    public void deleteUser(@PathVariable int id) {
        usuarioRepository.deleteById(id);
    }

    @PostMapping("/autenticar")
    public Boolean autenticar(@RequestBody ModelCredencial credencial) {
        Optional<ModelUsuario> user = usuarioRepository.findByEmail(credencial.getUserEmail());
        if (user.isEmpty()) {
            return false;
        }
        boolean valido = passwordEncoder.checkPassword(credencial.getSenha(), user.get().getPassword());
        return valido;
    }

    @PutMapping("/user")
    public ModelUsuario updateUser(@Valid @RequestBody ModelUsuario user) throws Exception {
        List<ModelUsuario> users = usuarioRepository.findAll();
        if(users.isEmpty()){
            throw new Exception("Não existe usuário cadastrado.");
        }
        Optional<ModelUsuario> aux = usuarioRepository.findById(user.getId());

        if (aux.isEmpty()) {
            return new ModelUsuario();
        } 
        ModelUsuario usuario = aux.get();
        if(user.getNome() != null){
            usuario.setNome(user.getNome());
        }
        if(user.getPassword()!= null){
            ModelCredencial cred = new ModelCredencial(usuario.getPassword());
            String[] encript = cred.getSenhaCriptografada();
            usuario.setPassword(encript[0]);
            usuario.setSalt(encript[1]);
        }
        if(user.getEmail()!= null){
            usuario.setEmail(user.getEmail());
        }
        return usuarioRepository.save(usuario);
        
    }

}
