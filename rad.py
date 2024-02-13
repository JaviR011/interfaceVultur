import sys
import serial
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame, QGridLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PyQt5.QtWidgets import QLabel
import csv
v1=np.array([0.0,0.0,0.0,0.0,0.0])
class WorkerThread(QThread):
    data_received = pyqtSignal(str)

    def run(self):
        puerto_serie = serial.Serial('COM9', 9600,timeout=0.5)
        try:
            while True:
                # Lee una línea desde Arduino
                linea = puerto_serie.readline().decode('utf-8').rstrip()
                # Emite la señal con los datos recibidos
                self.data_received.emit(linea)
                print(linea)
        except KeyboardInterrupt:
            # Cierra el puerto serie al presionar Ctrl+C
            puerto_serie.close()
            print("Puerto serie cerrado.")
class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
       # while(True) : 
# Configurar la ventana principal
        self.setWindowTitle('Mi Aplicación Qt')
        self.setGeometry(100, 100, 1200, 600)
        self.setStyleSheet("background-color: #111111; color: white;")

            # Crear layout general
        layout_general = QGridLayout(self)

            # Crear QFrames con gráficas
        color_fondo = '#222222'  # Puedes ajustar este color según tus preferencias


            # Gráfica usando vectores personalizados
        datos_personalizados = v1
        self.frame_personalizado = self.crear_qframe_con_vectores('Altitud', datos_personalizados, color_fondo)
        layout_general.addWidget(self.frame_personalizado, 0, 2)


        # Crear un temporizador para actualizar el valor del entero cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_datos)
        self.timer.start(500)  # Actualizar cada segundo


        # Crear e iniciar el hilo para la lectura continua de datos
        self.worker_thread = WorkerThread()
        self.worker_thread.data_received.connect(self.procesar_datos)
        self.worker_thread.start()

    def procesar_datos(self, datos):
        # Aquí puedes procesar los datos recibidos y actualizar la interfaz de usuario según sea necesario
        if(datos):
            print(datos)

# Especificar el nombre del archivo CSV
            nombre_archivo = 'ejemplo.csv'

# Escribir la lista de valores en el archivo CSV
            with open(nombre_archivo, 'a', newline='') as archivo_csv:
                escritor_csv = csv.writer(archivo_csv)
                escritor_csv.writerow(datos)

            global v1
            v1a= datos[:-1]
            v1a=float(v1a)  
            v1 = np.roll(v1, 1)
            print(v1a)  
            v1[0]=v1a
            
            self.actualizar_datos()
    def actualizar_datos(self):
        # Actualizar la gráfica 1
        self.actualizar_qframe_con_vectores(self.frame_personalizado, 'Altitud', v1)

    def actualizar_qframe_con_vectores(self, frame, titulo, datos):
    # Actualizar una gráfica con vectores personalizados
        canvas = frame.findChild(FigureCanvas)
        if canvas:
            ax = canvas.figure.axes[0]
            ax.clear()  # Limpiar la gráfica anterior
            ax.set_facecolor('#222222')  # Configurar el color de fondo de la gráfica

            x = np.arange(len(datos))  # Utilizar un vector de índices como eje x
            ax.plot(x, datos, color='lightblue')  # Graficar los nuevos datos
            ax.set_title(titulo, color='lightblue')  # Cambiar el color del título a azul claro
            ax.tick_params(axis='both', colors='lightblue')  # Cambiar el color de los números de los ejes a azul claro

            ax.xaxis.label.set_color('blue')
            ax.yaxis.label.set_color('blue')
            ax.set_xlabel('Eje X', color='lightblue')
            ax.set_ylabel('Eje Y', color='lightblue')

            canvas.draw()  # Redibujar la gráfica
 
    def crear_qframe_con_vectores(self, titulo, datos, color_fondo):
        # Crear un QFrame con gráfica utilizando vectores personalizados
        frame = QFrame(self)
        frame.setStyleSheet(f"background-color: {color_fondo};")

        # Crear una gráfica con matplotlib
        figure = Figure(facecolor=color_fondo)
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        ax.set_facecolor(color_fondo)  # Configurar el color de fondo de la gráfica
        x = np.arange(len(datos))  # Utilizar un vector de índices como eje x
        ax.plot(x, datos)
        ax.set_title(titulo, color='lightblue')  # Cambiar el color del título a azul claro
        ax.tick_params(axis='both', colors='lightblue')  # Cambiar el color de los números de los ejes a azul claro
        # Configurar el color del texto de las etiquetas de los ejes
        ax.xaxis.label.set_color('blue')
        ax.yaxis.label.set_color('blue')
        ax.set_xlabel('Eje X', color='lightblue')  # Cambiar el color de la etiqueta del eje X a azul
        ax.set_ylabel('Eje Y', color='lightblue')  # Cambiar el color de la etiqueta del eje Y a verde
        # Configurar diseño vertical
        layout = QVBoxLayout(frame)
        layout.addWidget(canvas)

        return frame

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec_())
