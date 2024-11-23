package br.udesc.MicroServiceUserData;

import br.udesc.MicroServiceUserData.jpa.PasswordEncoder;
import br.udesc.MicroServiceUserData.model.BcryptPasswordEncoder;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@SpringBootApplication
@Configuration
@EnableJpaRepositories(basePackages = "br.udesc.MicroServiceUserData.jpa")
public class MicroServiceUserDataApplication {

    public static void main(String[] args) {
        SpringApplication.run(MicroServiceUserDataApplication.class, args);
    }

    @Bean
    public WebMvcConfigurer configCORS() {
        return new WebMvcConfigurer() {
            public void addCorsMappings(CorsRegistry registry) {
                registry.addMapping("/**")
                        .allowedMethods("*")
                        .allowedOrigins("http://localhost:3000");
            }
        };
    }
    
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BcryptPasswordEncoder();
    }
    
    @Bean
    @ConditionalOnProperty(name = "swagger.enabled", havingValue = "true", matchIfMissing = false)
    public OpenAPI customApi(){
        return new OpenAPI().info(new Info().title("Test Swagger Maven APi").version("1.0.0").license(new License().name("Licença do Sistema").url("www.daniel.com")));
    }

}
