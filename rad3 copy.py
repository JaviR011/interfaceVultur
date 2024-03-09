import sys
import serial.tools.list_ports
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame, QGridLayout, QComboBox, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import csv
import serial
data_Y = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
class WorkerThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port=None):
        super().__init__()
        self.port = port

    def run(self):
        try:
            with serial.Serial(self.port, 9600, timeout=0.5) as puerto_serie:
                while True:
                    # Lee una línea desde Arduino
                    linea = puerto_serie.readline().decode('utf-8').rstrip()
                    # Emite la señal con los datos recibidos
                    self.data_received.emit(linea)
                    print(linea)
        except Exception as e:
            print("Error en la comunicación serial:", e)

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()

        # Configurar la ventana principal
        self.setWindowTitle('Vultur')
        self.setGeometry(100, 100, 1200, 600)
        self.setStyleSheet("background-color: #111111; color: white;")

        # Crear layout general
        layout_general = QGridLayout(self)

        # Crear ComboBox para seleccionar el puerto serie
        self.port_combo = QComboBox(self)
        self.port_combo.addItem("Seleccionar puerto")
        self.port_combo.addItems(self.listar_puertos_serie())
        layout_general.addWidget(self.port_combo, 0, 0)

        # Botón para actualizar la lista de puertos serie
        self.update_button = QPushButton("Actualizar", self)
        self.update_button.clicked.connect(self.actualizar_lista_puertos)
        layout_general.addWidget(self.update_button, 0, 1)

        # Botón para iniciar la comunicación serie
        self.start_button = QPushButton("Iniciar", self)
        self.start_button.clicked.connect(self.iniciar_comunicacion)
        layout_general.addWidget(self.start_button, 1, 0)

        # Gráfica usando vectores personalizados
        datos_personalizados = data_Y
        self.frame_personalizado = self.crear_qframe_con_vectores('Altitud', datos_personalizados, '#222222')
        layout_general.addWidget(self.frame_personalizado, 2, 0, 1, 2)
         # Lista para almacenar los valores del eje x   # Lista para almacenar los valores del eje y
        # Crear un temporizador para actualizar el valor del entero cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_datos)
        self.timer.start(250)  # Actualizar cada medio segundo

        self.worker_thread = None

    def actualizar_lista_puertos(self):
        """Actualizar la lista de puertos serie disponibles"""
        self.port_combo.clear()
        self.port_combo.addItem("Seleccionar puerto")
        self.port_combo.addItems(self.listar_puertos_serie())

    def listar_puertos_serie(self):
        """Lista los puertos serie disponibles"""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def iniciar_comunicacion(self):
        port_index = self.port_combo.currentIndex()
        if port_index <= 0:
            QMessageBox.warning(self, "Error", "Por favor, selecciona un puerto serie.")
            return

        port = self.port_combo.currentText()
        self.worker_thread = WorkerThread(port)
        self.worker_thread.data_received.connect(self.procesar_datos)
        self.worker_thread.start()

        self.start_button.setEnabled(False)  # Deshabilitar el botón después de iniciar la comunicación

    def procesar_datos(self, datos):
        global data_Y  # Hacer referencia a la variable global data_Y
        # Aquí puedes procesar los datos recibidos y actualizar la interfaz de usuario según sea necesario
        if datos:
            print(datos)
            nombre_archivo = 'ejemplo.csv'
            with open(nombre_archivo, 'a', newline='') as archivo_csv:
                escritor_csv = csv.writer(archivo_csv)
                escritor_csv.writerow(datos)
            v1a = float(datos)
            data_Y = np.append(data_Y, v1a)  # Modificar directamente data_Y
            print(v1a)
            self.actualizar_datos()

    def actualizar_datos(self):
        # Actualizar la gráfica 1
        self.actualizar_qframe_con_vectores(self.frame_personalizado, 'Altitud', data_Y)

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