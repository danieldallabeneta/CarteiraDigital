package br.udesc.MicroServiceUserData;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.License;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@ConditionalOnProperty(name = "swagger.enabled", havingValue = "true", matchIfMissing = false)
public class SwaggerConfiguration {
    
    @Bean
    public OpenAPI customApi(){
        return new OpenAPI().info(new Info().title("Test Swagger Maven APi").version("1.0.0").license(new License().name("Licença do Sistema").url("www.daniel.com")));
    }
}
