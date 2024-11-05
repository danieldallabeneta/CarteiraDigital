FROM maven:3.8.5-openjdk-17 as builder

WORKDIR /app2

COPY . .

RUN mvn dependency:go-offline

WORKDIR /app2

RUN mvn clean package -DskipTests

FROM openjdk:17-slim
WORKDIR /app2
COPY --from=build /app2/target/MicroServiceUserData-0.0.1-SNAPSHOT.jar microserviceuserdata.jar

CMD [ "java", "-jar",  "microserviceuserdata.jar"]