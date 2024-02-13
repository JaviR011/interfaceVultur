import sys
import serial
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame, QGridLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PyQt5.QtWidgets import QLabel

v1 = []
v2 = []
v3 = []
v4 = []
v5 = []
v6 = []
batery = 0


class WorkerThread(QThread):
    data_received = pyqtSignal(str)

    def run(self):
        puerto_serie = serial.Serial('COM9', 9600, timeout=2)
        try:
            while True:
                # Lee una línea desde Arduino
                linea = puerto_serie.readline().decode('utf-8').rstrip()

                # Emite la señal con los datos recibidos
                self.data_received.emit(linea)
        except KeyboardInterrupt:
            # Cierra el puerto serie al presionar Ctrl+C
            puerto_serie.close()
            print("Puerto serie cerrado.")


class MiVentana(QWidget):
    def __init__(self):
        super().__init__()

        # Configurar la ventana principal
        self.setWindowTitle('Mi Aplicación Qt')
        self.setGeometry(100, 100, 1200, 600)
        self.setStyleSheet("background-color: #111111; color: white;")

        # Crear layout general
        layout_general = QGridLayout(self)

        # Crear QFrames con gráficas
        color_fondo = '#222222'  # Puedes ajustar este color según tus preferencias

        # Gráfica usando vectores personalizados
        datos_personalizados = np.array([1, 4, 7, 2, 5, 8, 3, 6, 9])
        self.frame_personalizado = self.crear_qframe_con_vectores('Altitud', datos_personalizados, color_fondo)
        layout_general.addWidget(self.frame_personalizado, 0, 2)

        # Nueva gráfica usando otros vectores personalizados
        datos_otro_personalizado = np.array([2, 5, 8, 1, 4, 7, 3, 6, 9])
        self.frame_otro_personalizado = self.crear_qframe_con_vectores('Temperatura', datos_otro_personalizado,
                                                                        color_fondo)
        layout_general.addWidget(self.frame_otro_personalizado, 0, 3)

        # Gráfica usando vectores personalizados
        datos_personalizados1 = np.array([1, 4, 7, 2, 5, 8, 3, 6, 9])
        self.frame_personalizado1 = self.crear_qframe_con_vectores('Humedad', datos_personalizados1, color_fondo)
        layout_general.addWidget(self.frame_personalizado1, 0, 4)

        # Nueva gráfica usando otros vectores personalizados
        datos_otro_personalizado = np.array([2, 5, 8, 1, 4, 7, 3, 6, 9])
        self.frame_otro_personalizado = self.crear_qframe_con_vectores('posición', datos_otro_personalizado,
                                                                        color_fondo)
        layout_general.addWidget(self.frame_otro_personalizado, 1, 2)
        # Nueva gráfica usando otros vectores personalizados

        datos_otro_personalizado3 = np.array([2, 5, 8, 1, 4, 7, 3, 6, 9])
        self.frame_otro_personalizado3 = self.crear_qframe_con_vectores('vibracion', datos_otro_personalizado3,
                                                                         color_fondo)
        layout_general.addWidget(self.frame_otro_personalizado3, 1, 3)
        # Nueva gráfica usando otros vectores personalizados

        datos_otro_personalizado3 = np.array([2, 5, 8, 1, 4, 7, 3, 6, 9])
        self.frame_otro_personalizado3 = self.crear_qframe_con_vectores('temperatura interna',
                                                                         datos_otro_personalizado3, color_fondo)
        layout_general.addWidget(self.frame_otro_personalizado3, 1, 4)

        # Crear QFrame para imprimir un entero
        self.frame_entero = QFrame(self)
        self.frame_entero.setStyleSheet(f"background-color: {color_fondo};")

        # Crear un QLabel para mostrar el entero
        self.label_entero = QLabel('Bateria: [###########]-100%', self.frame_entero)
        self.label_entero.setStyleSheet("color: lightblue; font-size: 18px;")
        layout_entero = QVBoxLayout(self.frame_entero)
        layout_entero.addWidget(self.label_entero)
        layout_general.addWidget(self.frame_entero, 0, 5, 1, 5)

        # Crear un temporizador para actualizar el valor del entero cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_datos)
        self.timer.start(1000)  # Actualizar cada segundo

        datos_personalizados = np.array([0.1, 0.2, -0.3])
        self.frame_vector_3d = self.crear_qframe_3d('Vector 3D', datos_personalizados, color_fondo)
        layout_general.addWidget(self.frame_vector_3d, 1, 2)

        # Crear e iniciar el hilo para la lectura continua de datos
        self.worker_thread = WorkerThread()
        self.worker_thread.data_received.connect(self.procesar_datos)
        self.worker_thread.start()

    def procesar_datos(self, datos):
        # Aquí puedes procesar los datos recibidos y actualizar la interfaz de usuario según sea necesario
        print("Datos procesados:", datos)

    def actualizar_datos(self):
        # Aquí puedes actualizar cualquier parte de la interfaz de usuario que necesite actualización periódica
        pass

    def crear_qframe_3d(self, titulo, componentes, color_fondo):
        # Crear un QFrame con gráfica 3D
        frame = QFrame(self)
        frame.setStyleSheet(f"background-color: {color_fondo};")

        # Crear una gráfica 3D con matplotlib
        figure = Figure(facecolor=color_fondo)
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111, projection='3d')
        ax.set_facecolor(color_fondo)  # Configurar el color de fondo de la gráfica

        # Descomponer las componentes del vector
        x, y, z = componentes
