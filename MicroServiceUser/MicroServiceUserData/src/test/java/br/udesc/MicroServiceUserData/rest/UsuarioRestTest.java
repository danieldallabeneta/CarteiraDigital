package br.udesc.MicroServiceUserData.rest;

import br.udesc.MicroServiceUserData.jpa.PasswordEncoder;
import br.udesc.MicroServiceUserData.jpa.UsuarioRepository;
import br.udesc.MicroServiceUserData.model.BcryptPasswordEncoder;
import br.udesc.MicroServiceUserData.model.HashDateSingleton;
import br.udesc.MicroServiceUserData.model.ModelCredencial;
import br.udesc.MicroServiceUserData.model.ModelUsuarioAuxiliar;
import br.udesc.MicroServiceUserData.model.ModelUsuario;

import java.util.Optional;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.HttpStatus;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

@SpringBootTest
@Transactional
public class UsuarioRestTest {
    
    @Autowired(required=true)
    private UsuarioRepository usuarioRepository;
    
    @Autowired
    private PasswordEncoder passwordEncoder;
    
    @Autowired
    private UsuarioRest usuarioRest;
    
    private ModelUsuarioAuxiliar testUserAuxiliar;    

    private ModelCredencial testCredencial;

    private ModelUsuario testUser;
    
    @BeforeEach
    void setUp() {        
        testUserAuxiliar = new ModelUsuarioAuxiliar("Usuario Teste", "usuario@teste.com", "senha123");
        testCredencial = new ModelCredencial("usuario@teste.com", "senha123");
        usuarioRest = new UsuarioRest(usuarioRepository, new BcryptPasswordEncoder());
    }
    
    @Test
    public void createUser_newUser() throws Exception {        
        Integer createUserId = usuarioRest.createUser(testUserAuxiliar);
        
        Optional<ModelUsuario> savedUser = usuarioRepository.findById(createUserId);
        assertTrue(savedUser.isPresent());
        assertEquals(testUserAuxiliar.getNome(), savedUser.get().getNome());
        assertEquals(testUserAuxiliar.getEmail(), savedUser.get().getEmail());
        testUser = savedUser.get();
    }
    
    @Test
    public void createUser_ShouldThrowConflict_WhenEmailIsAlreadyTaken() {        
        ModelUsuario existingUser = new ModelUsuario();
        existingUser.setNome("Usuario Existente");
        existingUser.setEmail("usuario@teste.com");
        existingUser.setPassword("senha123");
        usuarioRepository.save(existingUser);
        
        ResponseStatusException exception = assertThrows(ResponseStatusException.class, () -> {
            usuarioRest.createUser(testUserAuxiliar);
        });

        assertEquals(HttpStatus.CONFLICT, exception.getStatusCode());
        assertEquals("Usuário já existente", exception.getReason());
    }
        
    @Test
    public void getUserId_ShouldReturnUser_WhenUserExists() throws Exception { 
        Integer savedUser = usuarioRest.createUser(testUserAuxiliar);
        
        ModelUsuario result = usuarioRest.getUser(savedUser);

        assertEquals(savedUser, result.getId());
        assertEquals(testUserAuxiliar.getNome(), result.getNome());        
    }
    
    @Test
    public void getUserId_ShouldThrowUnauthorized_WhenUserExists() throws Exception { 
        Integer savedUser = usuarioRest.createUser(testUserAuxiliar);
        HashDateSingleton.getInstance().setValidade(0);
        
        ResponseStatusException exception = assertThrows(ResponseStatusException.class, () -> {
            usuarioRest.getUser(savedUser);
        });
        
        assertEquals(HttpStatus.UNAUTHORIZED, exception.getStatusCode());
        assertEquals("Usuário não autorizado", exception.getReason()); 
        
        HashDateSingleton.getInstance().setValidade(5);
    }
    
    @Test
    public void getUserId_ShouldThrowNotFound_WhenUserNotExists() throws Exception {         
        ResponseStatusException exception = assertThrows(ResponseStatusException.class, () -> {
            usuarioRest.getUser(0);
        });
        
        assertEquals(HttpStatus.NOT_FOUND, exception.getStatusCode());
        assertEquals("Usuário não encontrado.", exception.getReason());       
    }

    @Test
    public void autenticar_UsuarioExists() throws Exception {
        boolean valido = usuarioRest.autenticar(testCredencial);

        assertTrue(valido);
    }

    @Test
    public void autenticar_UsuarioNaoExists() throws Exception {
        testCredencial.setSenha("1234");
        boolean valido = usuarioRest.autenticar(testCredencial);

        assertFalse(valido);
    }

    @Test
    public void updateUser_ShouldThrowNotFound_WhenUserNotExists() throws Exception {   
        ModelUsuario user = testUser.clone();
        user.setId(0);
        user.setEmail("teste@teste.com.br");

        ResponseStatusException exception = assertThrows(ResponseStatusException.class, () -> {
            usuarioRest.updateUser(user);
        });

        assertEquals(HttpStatus.NOT_FOUND, exception.getStatusCode());
        assertEquals("Usuário não encontrado.", exception.getReason()); 
    }

    @Test
    public void updateUser_ShouldThrowUnauthorized_WhenUserExists() throws Exception {   
        ModelUsuario user = testUser.clone();
        user.setEmail("teste@teste.com.br");
        HashDateSingleton.getInstance().setValidade(0);

        ResponseStatusException exception = assertThrows(ResponseStatusException.class, () -> {
            usuarioRest.updateUser(user);
        });

        assertEquals(HttpStatus.UNAUTHORIZED, exception.getStatusCode());
        assertEquals("Usuário não autorizado", exception.getReason());  
    }
    
}
