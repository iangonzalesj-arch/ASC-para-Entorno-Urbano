import sys
import matplotlib
matplotlib.use('QtAgg')

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):
    """Lienzo de Matplotlib adaptado como widget de PyQt6."""
    def __init__(self, parent=None, width=6, height=5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        
        # Subplot 1: Sensor de Suelo (Top)
        self.axes_ground = fig.add_subplot(211) 
        # Subplot 2: Sensor Aéreo (Bottom)
        self.axes_aerial = fig.add_subplot(212) 
        
        fig.tight_layout(pad=3.0)
        super().__init__(fig)

class CaneSimulatorWindow(QMainWindow):
    """
    Interfaz gráfica principal para visualizar la telemetría 
    de los sensores del bastón en tiempo real.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de Entorno - Bastón Inteligente ASC")
        self.resize(850, 750)

        # Widget central y layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        
        # Panel de alertas de estado
        self.status_label = QLabel("SISTEMA EN ESPERA: Conecte los sensores")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; padding: 15px; "
            "background-color: #e0e0e0; color: #333333; border-radius: 5px;"
        )
        self.layout.addWidget(self.status_label)

        # Instanciar y acoplar los gráficos
        self.setup_plots()

    def setup_plots(self):
        """Prepara el área de gráficos con los umbrales críticos."""
        self.canvas = MplCanvas(self, width=6, height=5, dpi=100)
        
        # Configuración visual del perfil del suelo (Ultrasonido inferior)
        self.canvas.axes_ground.set_title("Perfil del Suelo (Detección de Fosas / Buzones)")
        self.canvas.axes_ground.set_ylabel("Distancia (cm)")
        self.canvas.axes_ground.set_ylim(0, 200)
        self.canvas.axes_ground.axhline(y=120, color='red', linestyle='--', label="Umbral Crítico Caída (>120cm)")
        self.canvas.axes_ground.legend(loc="upper left")
        self.canvas.axes_ground.grid(True, linestyle=':', alpha=0.6)
        
        # Configuración visual de obstáculos aéreos (ToF superior)
        self.canvas.axes_aerial.set_title("Escaneo Aéreo (Detección de Toldos / Cables)")
        self.canvas.axes_aerial.set_xlabel("Muestras de tiempo (Ciclos de lectura)")
        self.canvas.axes_aerial.set_ylabel("Distancia (cm)")
        self.canvas.axes_aerial.set_ylim(0, 150)
        self.canvas.axes_aerial.axhline(y=80, color='orange', linestyle='--', label="Umbral Alerta Frontal (<80cm)")
        self.canvas.axes_aerial.legend(loc="upper left")
        self.canvas.axes_aerial.grid(True, linestyle=':', alpha=0.6)
        
        self.layout.addWidget(self.canvas)

    def update_alert_display(self, alert_text: str, color_hex: str, text_color: str = "#000000"):
        """Actualiza la interfaz visual cuando el patrón Observer notifica un riesgo."""
        self.status_label.setText(alert_text)
        self.status_label.setStyleSheet(
            f"font-size: 18px; font-weight: bold; padding: 15px; "
            f"background-color: {color_hex}; color: {text_color}; border-radius: 5px;"
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CaneSimulatorWindow()
    window.show()
    sys.exit(app.exec())