package br.udesc.MicroServiceUserData.rest;

import br.udesc.MicroServiceUserData.jpa.PasswordEncoder;
import br.udesc.MicroServiceUserData.jpa.UsuarioRepository;
import br.udesc.MicroServiceUserData.model.HashDateSingleton;
import br.udesc.MicroServiceUserData.model.ModelCredencial;
import br.udesc.MicroServiceUserData.model.ModelUsuario;
import br.udesc.MicroServiceUserData.model.ModelUsuarioAuxiliar;
import jakarta.validation.Valid;
import java.util.List;
import java.time.LocalDateTime;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.server.ResponseStatusException;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;

@RestController
@RequestMapping()
public class UsuarioRest {

    private final UsuarioRepository usuarioRepository;
    private final PasswordEncoder passwordEncoder;

    @Autowired
    public UsuarioRest(UsuarioRepository usuarioRepository, PasswordEncoder passwordEncoder) {
        this.usuarioRepository = usuarioRepository;
        this.passwordEncoder = passwordEncoder;
    }
    
    @Operation(summary = "Cadastra um novo usuário", description = "Cadastra um usuário caso as informações enviadas ainda não existam.")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Usuário cadastrado com sucesso.", 
                     content = @Content(mediaType = "application/json", schema = @Schema(implementation = Integer.class))),
        @ApiResponse(responseCode = "409", description = "Usuário já existe.", 
                     content = @Content(mediaType = "application/json"))
    })
    @PostMapping("/users")
    @ResponseStatus(HttpStatus.CREATED)
    public Integer createUser(@io.swagger.v3.oas.annotations.parameters.RequestBody(description = "User data", 
                              required = true, 
                              content = @Content(schema = @Schema(implementation = ModelUsuarioAuxiliar.class)))
                              @RequestBody @Valid ModelUsuarioAuxiliar user) throws Exception {
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

            HashDateSingleton.getInstance().addHashDate(savedUser.getSalt(), LocalDateTime.now());

            return savedUser.getId();
        }
        throw new ResponseStatusException(HttpStatus.CONFLICT, "Usuário já existente");
    }
    
    @Operation(summary = "Retorna todos os usuários", description = "Retorna uma lista com todos os usuários cadastrados.")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Lista de usuários retornado com sucesso.", 
                     content = @Content(mediaType = "application/json", schema = @Schema(implementation = ModelUsuario.class)))
    })
    @GetMapping("/users")
    public List<ModelUsuario> allUsers() {
        return usuarioRepository.findAll();
    }

    @Operation(summary = "Retorna o Modelo de usuário do ID", description = "Retorna o modelo do usuário conforme o ID informado, se o usuário estiver autenticado.")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Usuário retornado com sucesso.",
                     content = @Content(mediaType = "application/json", schema = @Schema(implementation = ModelUsuario.class))),
        @ApiResponse(responseCode = "404", description = "Usuário não encontrado.",
                     content = @Content(mediaType = "application/json")),
        @ApiResponse(responseCode = "401", description = "Usuário não autorizado.",
                     content = @Content(mediaType = "application/json"))
    })
    @GetMapping("/users/{id}")
    public ModelUsuario getUser(@Parameter(description = "ID do usuário a ser retornado.", required = true)
                                @PathVariable int id) throws Exception {
        Optional<ModelUsuario> user = usuarioRepository.findById(id);

        if (user.isEmpty()) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Usuário não encontrado.");
        }
        HashDateSingleton hashValidation = HashDateSingleton.getInstance();
        boolean logado = hashValidation.validaHash(user.get().getSalt());
        if(logado){
            return user.get();
        }
        throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Usuário não autorizado");
        
    }
    
    @Operation(summary = "Retorna o usuário do email", description = "Retorna o modelo do usuário do email enviado, se autenticado.")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Usuário retornado com sucesso.",
                     content = @Content(mediaType = "application/json", schema = @Schema(implementation = ModelUsuario.class))),
        @ApiResponse(responseCode = "404", description = "Usuário não encontrado.",
                     content = @Content(mediaType = "application/json")),
        @ApiResponse(responseCode = "401", description = "Usuário não autorizado.",
                     content = @Content(mediaType = "application/json"))
    })
    @GetMapping("/usuario/{email}")
    public ModelUsuario getUserByEmail(@Parameter(description = "Email do usuário a ser retornado.", required = true)
                                       @PathVariable String email) throws Exception {
        Optional<ModelUsuario> user = usuarioRepository.findByEmail(email);
        if (user.isEmpty()) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Usuário não encontrado.");
        }
        HashDateSingleton hashValidation = HashDateSingleton.getInstance();
        boolean logado = hashValidation.validaHash(user.get().getSalt());
        if(logado){
            return user.get();
        }
        throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Usuário não autorizado");
    }
    
    @Operation(summary = "Deleta o usuário do ID", description = "Deleta o modelo do usuário conforme ID, se o usuário existir e se autenticado.")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "204", description = "Usuário deletado com sucesso."),
        @ApiResponse(responseCode = "404", description = "Usuário não encontrado.",
                     content = @Content(mediaType = "application/json")),
        @ApiResponse(responseCode = "401", description = "Usuário não autorizado.",
                     content = @Content(mediaType = "application/json"))
    })
    @DeleteMapping("/users/{id}")
    public void deleteUser(@PathVariable int id) throws Exception {
        Optional<ModelUsuario> user = usuarioRepository.findById(id);

        if (user.isEmpty()) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Usuário não encontrado");
        }

        HashDateSingleton hashValidation = HashDateSingleton.getInstance();
        boolean logado = hashValidation.validaHash(user.get().getSalt());
        if(logado){
            usuarioRepository.deleteById(id);
        } else {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Usuário não autorizado");
        }
    }

    @Operation(summary = "Autentica o usuário", description = "Autentica o usuário conforme informações de email e senha.")
    @ApiResponses(value = {@ApiResponse(responseCode = "200", description = "Autenticado com sucesso.",
                           content = @Content(mediaType = "application/json", schema = @Schema(implementation = Boolean.class)))})
    @PostMapping("/autenticar")
    public Boolean autenticar(@io.swagger.v3.oas.annotations.parameters.RequestBody(description = "User credentials for authentication", 
                              required = true,
                              content = @Content(schema = @Schema(implementation = ModelCredencial.class)))
                              @RequestBody @Valid ModelCredencial credencial) {
        Optional<ModelUsuario> user = usuarioRepository.findByEmail(credencial.getUserEmail());
        if (user.isEmpty()) {
            return false;
        }
        boolean valido = passwordEncoder.checkPassword(credencial.getSenha(), user.get().getPassword());
        if(valido){
            HashDateSingleton hashValidation = HashDateSingleton.getInstance();
            if(hashValidation.containsHash(user.get().getSalt())){
                hashValidation.removeHash(user.get().getSalt());                
            };
            hashValidation.addHashDate(user.get().getSalt(), LocalDateTime.now());
        }
        return valido;
    }
    
    @Operation(summary = "Atualiza informações do usuário.", description = "Atualiza as informações do usuário, se o usuário existir e se o usuário estiver autenticado.")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Usuário autenticado com sucesso.",
                     content = @Content(mediaType = "application/json", schema = @Schema(implementation = ModelUsuario.class))),
        @ApiResponse(responseCode = "404", description = "Usuário não encontrado",
                     content = @Content(mediaType = "application/json")),
        @ApiResponse(responseCode = "401", description = "Usuário não autorizado",
                     content = @Content(mediaType = "application/json"))
    })
    @PutMapping("/user")
    public ModelUsuario updateUser(@io.swagger.v3.oas.annotations.parameters.RequestBody(description = "Usuário a ser atualizado.", 
                                   required = true,
                                   content = @Content(schema = @Schema(implementation = ModelUsuario.class)))
                                   @RequestBody @Valid ModelUsuario user) throws Exception {
        List<ModelUsuario> users = usuarioRepository.findAll();
        if(users.isEmpty()){
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Usuário não encontrado");
        }
        Optional<ModelUsuario> aux = usuarioRepository.findById(user.getId());

        if (aux.isEmpty()) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Usuário não encontrado");
        } 

        ModelUsuario usuario = aux.get();
        HashDateSingleton hashValidation = HashDateSingleton.getInstance();
        boolean logado = hashValidation.validaHash(usuario.getSalt());

        if(!logado){
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Usuário não autorizado");
        }

        if(user.getNome() != null){
            usuario.setNome(user.getNome());
        }
        if(user.getPassword() != null){
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
    
    @Operation(summary = "Verifica a autorização do usuário", description = "Verifica se o usuário informado está autorizado no sistema.")
    @ApiResponses(value = {
        @ApiResponse(responseCode = "200", description = "Usuário autorizado.",
                     content = @Content(mediaType = "application/json", schema = @Schema(implementation = Boolean.class))),
        @ApiResponse(responseCode = "404", description = "Usuário não encontrado",
                     content = @Content(mediaType = "application/json")),
        @ApiResponse(responseCode = "401", description = "Usuário não autorizado",
                     content = @Content(mediaType = "application/json"))
    })
    @GetMapping("/aut/{id}")
    public Boolean authorization(@PathVariable Integer id) throws Exception {
        Optional<ModelUsuario> aux = usuarioRepository.findById(id);
        if (aux.isEmpty()) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Usuário não encontrado");
        }
        HashDateSingleton hashValidation = HashDateSingleton.getInstance();
        boolean logado = hashValidation.validaHash(aux.get().getSalt());
        if(!logado){
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Usuário não autorizado");
        }
        return logado;
    }

}
