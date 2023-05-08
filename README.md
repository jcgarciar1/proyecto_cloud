
# Documentación del proyecto
# Entrega 1

Aqui se encuentra el video de pruebas del back en postman: https://youtu.be/PJwXEXLL4KY

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


# Entrega 3 (Migracion a GCP)
<img width="530" alt="DiagramaEntrega" src="https://user-images.githubusercontent.com/54164818/230737243-ccb3b063-2aae-4b2d-9cbe-cb0fba153809.png">

# Entrega 4

Video sustentación: https://youtu.be/TADWZhQhIZM

**Pruebas de carga de la aplicación**

**Escenario 1:**

**50 peticiones:**

Log in:

![](Aspose.Words.90bb327f-bc64-4026-9ece-e1f6c6606989.001.png)

List Files:

![](Aspose.Words.90bb327f-bc64-4026-9ece-e1f6c6606989.002.png)

Detail File:

![](Aspose.Words.90bb327f-bc64-4026-9ece-e1f6c6606989.003.png)

**100 peticiones:**

Log in:

![](Aspose.Words.90bb327f-bc64-4026-9ece-e1f6c6606989.004.png)

List Files:

![](Aspose.Words.90bb327f-bc64-4026-9ece-e1f6c6606989.005.png)

Detail File:

![](Aspose.Words.90bb327f-bc64-4026-9ece-e1f6c6606989.006.png)

**1000 peticiones:**

Log in:

![](Aspose.Words.90bb327f-bc64-4026-9ece-e1f6c6606989.007.png)

List Files:

![](Aspose.Words.90bb327f-bc64-4026-9ece-e1f6c6606989.008.png)

Detail File:

![](Aspose.Words.90bb327f-bc64-4026-9ece-e1f6c6606989.009.png)


**5000 peticiones:**

5000 peticiones en 60 segundos rompen con el esquema de escalado de nuestro sistema. El sistema aumenta la cantidad de instancias a 5 y ni siquiera de esta manera pueden sostener esa cantidad de peticiones por segundo.

![](Aspose.Words.90bb327f-bc64-4026-9ece-e1f6c6606989.010.png)

![](Aspose.Words.90bb327f-bc64-4026-9ece-e1f6c6606989.011.png)

**Escenario 2:**

50 peticiones:

![](Aspose.Words.90bb327f-bc64-4026-9ece-e1f6c6606989.012.png)

100 peticiones:

![](Aspose.Words.90bb327f-bc64-4026-9ece-e1f6c6606989.013.png)

1000 peticiones:

![](Aspose.Words.90bb327f-bc64-4026-9ece-e1f6c6606989.014.png)

**5000 peticiones:**

Debido a los resultados anteriores decidimos no correr las pruebas con 5000 peticiones ya que no va a ser viable para el sistema de Cloud Functions

**Conclusiones:**

- El backend esta escalando correctamente hasta 1000 peticiones cada 60 segundos con un 0% de error. 
- Al subir a mas de 1000 peticiones por 60 segundos, se llegan a crear el máximo de instancias (5 instancias) en el Scaling Group. Si se desea escalar el backend a mas peticiones por minuto, se debe aumentar la capacidad de las maquinas (0.6 GB RAM actualmente) o aumentar el número de instancias.
- El sistema de convertir archivos no esta siendo escalable como deseábamos. A pesar de configurar el Cloud Function para realizarlo, con solo 100 peticiones por minuto, falle en alrededor del 35% y ya con 1000 peticiones por minuto falla en el 90%. Habría que entender las necesidades del cliente y ajustar el código para evitar que tantas funciones fallen paralelamente.
- Revisando los logs, encontramos que los fallos se pueden deber a un pequenio delay que existe entre la comunicación de Cloud Storage con el Cloud Function. Al enviar una cantidad tan elevada de peticiones, el sistema no alcanza a escribir el archivo en Storage, cuando el código de la función le pide la ubicación para escribirla en la base de datos este no la encuentra ya que no se encuentra el archivo escrito. Es algo que se debe corregir del cuerpo de la Cloud Function para la siguiente entrega.
- El sistema se convirtió en algo mas escalable comparado con la anterior entrega, por lo cual se debe tener en consideración las mejoras mencionadas en las anteriores conclusiones con el fin de volver el sistema aun más fiable y escalable.

