# Documentación del proyecto

La API fue documentada haciendo uso de Postman. 
La documentación se encuentra aqui: https://documenter.getpostman.com/view/22590903/2s93CPpX9H

Pruebas fueron realizadas para garantizar la calidad de la api, pueden ser encontradas en el archivo API COMPRESIONES INC.postman_collection
Para usarlo simplemente se abre Postman y en la sección de Colections se importa el archivo. Aquí encontrará todos los endpoints con sus respectivos tests de tipo de response, response time y schema de las responses.

Para correr el back, en la carpeta prroyecto_cloud correr el comando docker compose up

Para correr el front se debe ingresar a la carpeta front end y correr el comando docker compose -f "docker-compose.prod.yml" up


Lo que se muestra a continuación es el ideal de la arquitectura, es decir, el estado actual del proyecto no cuenta con la arquitectura expuesta, pero sí es a donde se espera lllegar con los recursos de la clase

### Diagrama de Arquitectura

![Cloud](https://user-images.githubusercontent.com/33431725/221440716-a6afdcef-37c2-456f-8979-d4ec7651aab8.png)

Se observa el diagrama de arquitectura, el cual esta basado completamente en AWS, donde el usuario ingresa por un Edge Location al sistema y consume todo el front. Contamos con un DNS que es el encargado de enrutar las peticiones y servicios de la aplicación. Detras de esto, tenemos un load balancer que guia el trafico según disponibilidad y carga de las zonas. Justo detrás tenemos un poco de seguridad con un WAF para la aplicación y poder controlar las peticiones que llegan al servicio. El core de la arquitectura vendría siendo el servicio de conetenedores llamada ECS el cual nos permite escalar y crear clusters con servicios necesarios para el negocio, es importante observar que todas las peticiones llegan por un API Gateway. Detrás de esto encontramos las BD las cuales deben de sincronizarse entre las dos zonas para no perder información.

### Diagrama de Despliegue

![Cloud (1)](https://user-images.githubusercontent.com/33431725/221444244-88ed5e6f-60ec-43b0-9804-5705a1ebe1cd.png)

Por otro lado, tenemos el diagrama de despliegue donde se observa que todo se basa en protoclos de comunicación por medio de HTTPS y TCP. Este se divide en el lado del cliente y en el lado de la nube, donde se enceuntra todo lo relacionado a los servicios que se prestan al cliente.
