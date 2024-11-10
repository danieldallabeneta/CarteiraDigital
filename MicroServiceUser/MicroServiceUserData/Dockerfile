FROM maven:3.8.5-openjdk-17 as builder

WORKDIR /app2

COPY . .

RUN mvn dependency:go-offline

WORKDIR /app2

RUN mvn clean package -DskipTests

CMD [ "java", "-jar",  "/app2/target/MicroServiceUserData-1.0.0-SNAPSHOT.jar"]
