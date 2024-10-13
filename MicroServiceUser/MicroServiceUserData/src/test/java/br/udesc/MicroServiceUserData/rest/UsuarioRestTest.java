package br.udesc.MicroServiceUserData;

import br.udesc.MicroServiceUserData.jpa.PasswordEncoder;
import br.udesc.MicroServiceUserData.jpa.UsuarioRepository;
import br.udesc.MicroServiceUserData.model.HashDateSingleton;
import br.udesc.MicroServiceUserData.model.ModelUsuarioAuxiliar;
import br.udesc.MicroServiceUserData.model.ModelUsuario;
import br.udesc.MicroServiceUserData.rest.UsuarioRest;
import java.util.List;

import java.util.Optional;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.HttpStatus;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

@SpringBootTest
@ContextConfiguration(classes = MicroServiceUserDataApplication.class)
@Transactional
public class UsuarioRestTest {
    
    @Autowired
    private UsuarioRepository usuarioRepository;
    
    @Autowired
    private PasswordEncoder passwordEncoder;
    
    @Autowired
    private UsuarioRest usuarioRest;
    
    private ModelUsuarioAuxiliar testUserAuxiliar;    
    
    @BeforeEach
    void setUp() {        
        testUserAuxiliar = new ModelUsuarioAuxiliar("Usuario Teste", "usuario@teste.com", "senha123");
    }
    
    @Test
    public void createUser_newUser() throws Exception {
        Integer createUserId = usuarioRest.createUser(testUserAuxiliar);
        
        Optional<ModelUsuario> savedUser = usuarioRepository.findById(createUserId);
        assertTrue(savedUser.isPresent());
        assertEquals(testUserAuxiliar.getNome(), savedUser.get().getNome());
        assertEquals(testUserAuxiliar.getEmail(), savedUser.get().getEmail());
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
    }
    
    @Test
    public void getUserId_ShouldThrowNotFound_WhenUserNotExists() throws Exception {         
        ResponseStatusException exception = assertThrows(ResponseStatusException.class, () -> {
            usuarioRest.getUser(0);
        });
        
        assertEquals(HttpStatus.NOT_FOUND, exception.getStatusCode());
        assertEquals("Usuário não encontrado.", exception.getReason());       
    }
    
}
