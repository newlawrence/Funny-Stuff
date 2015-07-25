#Rep2D v1.2

**Rep2D** es un pequeño programita (el primer GUI "serio") que realicé allá por mayo de 2012. Por aquel entonces el estándar gráfico era **Microsoft Excel** (a **MATLAB** no se habían resinado aún mis compañeros), pero claro, nos topamos con la primera asignatura (**Cálculo Numérico II**) donde debíamos visualizar un mapa de curvas de nivel.

Habiendo aprendido mi primera biblioteca para gráficos para esa misma asignatura el año anterior y viendo las dificultades de mis compañeros, me dispuse a hacer un pequeño programita gráfico que permitiera leer el fichero que contuviera la matriz de datos y los graficase. Así nació **Rep2D**.

**Rep2D** está escrito en **Fortran95** y utiliza la biblioteca gráfica [DISLIN](https://www.mps.mpg.de/dislin/). Acepta como entrada una única matriz cuyos valores serán la coordenada **z** (los valores límites de los ejes **x** e **y** han de introducirse a mano en el programa). El programa permite tanto la visualización de líneas de nivel, como del contorno interpolado de la función, así como la exportación a PDF de las imágenes.

Como la compilación requiere de distintas bibliotecas dependiendo de la plataforma, no se incluye ningún **Makefile** para el proyecto (de momento).

En la carpeta `examples` se incluyen dos ejemplos de programas cuya salida está pensada para utilizar con **Rep2D**:

* **num2012**: resolución de la **Ecuación del Calor** sobre una placa cuadrada bajo unas determinadas condiciones de contorno.
* **stab**: cálculo del **Polinomio de Estabilidad** de un esquema Adams-Bashford de segundo orden.

Este proyecto se distribuye bajo licencia [MIT](http://opensource.org/licenses/MIT).