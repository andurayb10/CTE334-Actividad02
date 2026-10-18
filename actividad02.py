import math
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def validar_coordenadas(lat1, lon1, lat2, lon2):
    """Comprueba que las latitudes y longitudes se encuentren en los rangos permitidos."""
    if (-90 <= lat1 <= 90) and (-90 <= lat2 <= 90) and (-180 <= lon1 <= 180) and (-180 <= lon2 <= 180):
        return True
    return False

def calcular_distancia(lat1, lon1, lat2, lon2):
    """Aplica la ecuación de Haversine utilizando R = 6371.0088 km."""
    R = 6371.0088
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_phi / 2) ** 2) + math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))
    
    distancia = R * c
    return distancia

def determinar_direccion(lat1, lon1, lat2, lon2):
    """Compara las posiciones para establecer la ubicación general de B respecto a A."""
    if lat1 == lat2 and lon1 == lon2:
        return "Misma ubicación"
    elif lat1 < lat2 and lon1 == lon2:
        return "Norte"
    elif lat1 > lat2 and lon1 == lon2:
        return "Sur"
    elif lat1 == lat2 and lon1 < lon2:
        return "Este"
    elif lat1 == lat2 and lon1 > lon2:
        return "Oeste"
    elif lat1 < lat2 and lon1 < lon2:
        return "Noreste"
    elif lat1 < lat2 and lon1 > lon2:
        return "Noroeste"
    elif lat1 > lat2 and lon1 < lon2:
        return "Sureste"
    elif lat1 > lat2 and lon1 > lon2:
        return "Suroeste"
    return "Misma ubicación"

def clasificar_distancia(distancia):
    """Aplica los intervalos de distancia establecidos."""
    if distancia < 1.0:
        return "Muy cercano"
    elif 1.0 <= distancia < 10.0:
        return "Cercano"
    elif 10.0 <= distancia < 50.0:
        return "Distancia media"
    else:
        return "Distante"


class AppAnalisisEspacial:
    def __init__(self, root):
        self.root = root
        self.root.title("CTE-334 Análisis entre dos puntos geográficos")
        self.root.geometry("520x560")
        self.root.minsize(480, 520)
        
        # Estilo visual limpio y moderno
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Contenedor principal con márgenes
        main_frame = ttk.Frame(root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Títulos e instrucciones
        title_label = ttk.Label(main_frame, text="CTE-334 Análisis entre dos puntos geográficos", font=("Arial", 11, "bold"))
        title_label.pack(anchor="w", pady=(0, 5))
        
        instruction_label = ttk.Label(main_frame, text="Ingrese las coordenadas en grados decimales", font=("Arial", 9, "italic"))
        instruction_label.pack(anchor="w", pady=(0, 15))
        
        # Marcos para coordenadas (Punto A y Punto B)
        frames_coord = ttk.Frame(main_frame)
        frames_coord.pack(fill=tk.X, pady=(0, 15))
        
        # Punto A
        frame_a = ttk.LabelFrame(frames_coord, text="Punto A", padding="12")
        frame_a.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))
        
        ttk.Label(frame_a, text="Latitud:").grid(row=0, column=0, sticky="w", pady=6)
        self.entry_lat_a = ttk.Entry(frame_a, width=14)
        self.entry_lat_a.grid(row=0, column=1, pady=6, padx=5)
        
        ttk.Label(frame_a, text="Longitud:").grid(row=1, column=0, sticky="w", pady=6)
        self.entry_lon_a = ttk.Entry(frame_a, width=14)
        self.entry_lon_a.grid(row=1, column=1, pady=6, padx=5)
        
        # Punto B
        frame_b = ttk.LabelFrame(frames_coord, text="Punto B", padding="12")
        frame_b.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 0))
        
        ttk.Label(frame_b, text="Latitud:").grid(row=0, column=0, sticky="w", pady=6)
        self.entry_lat_b = ttk.Entry(frame_b, width=14)
        self.entry_lat_b.grid(row=0, column=1, pady=6, padx=5)
        
        ttk.Label(frame_b, text="Longitud:").grid(row=1, column=0, sticky="w", pady=6)
        self.entry_lon_b = ttk.Entry(frame_b, width=14)
        self.entry_lon_b.grid(row=1, column=1, pady=6, padx=5)
        
        # Botones de acción
        frame_buttons = ttk.Frame(main_frame)
        frame_buttons.pack(fill=tk.X, pady=10)
        
        self.btn_calcular = ttk.Button(frame_buttons, text="Calcular", command=self.ejecutar_calculo)
        self.btn_calcular.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        
        self.btn_limpiar = ttk.Button(frame_buttons, text="Limpiar", command=self.limpiar_campos)
        self.btn_limpiar.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(5, 0))
        
        # Área de resultados (Widget Text con barra de desplazamiento)
        frame_result = ttk.LabelFrame(main_frame, text="Resultado", padding="12")
        frame_result.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.text_resultado = tk.Text(frame_result, height=7, width=42, font=("Courier New", 10), state=tk.DISABLED, bg="#fafafa", relief="solid", bd=1)
        self.text_resultado.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(frame_result, orient="vertical", command=self.text_resultado.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_resultado.configure(yscrollcommand=scrollbar.set)

    def ejecutar_calculo(self):
        """Recupera, valida y procesa los datos desde el botón de la interfaz."""
        # 1 y 2. Intentar conversión numérica mediante try-except
        try:
            lat_a = float(self.entry_lat_a.get())
            lon_a = float(self.entry_lon_a.get())
            lat_b = float(self.entry_lat_b.get())
            lon_b = float(self.entry_lon_b.get())
        except ValueError:
            messagebox.showinfo("Entrada no numérica", "Todos los campos deben contener valores numéricos.")
            return

        # 3. Comprobar intervalos válidos de latitud y longitud
        if not validar_coordenadas(lat_a, lon_a, lat_b, lon_b):
            messagebox.showinfo("Coordenada fuera de rango", "La latitud debe estar entre -90 y 90 grados y la longitud entre -180 y 180 grados.")
            return

        # 4. Ejecutar funciones de distancia, dirección y clasificación
        distancia = calcular_distancia(lat_a, lon_a, lat_b, lon_b)
        direccion = determinar_direccion(lat_a, lon_a, lat_b, lon_b)
        clasificacion = clasificar_distancia(distancia)

        # Formato de presentación requerido
        informe = (
            "RESULTADO DEL ANÁLISIS\n\n"
            f"Distancia: {distancia:.3f} km\n"
            f"Dirección: {direccion}\n"
            f"Clasificación: {clasificacion}"
        )

        # 5. Limpiar área anterior y escribir el nuevo informe actualizado
        self.text_resultado.configure(state=tk.NORMAL)
        self.text_resultado.delete('1.0', tk.END)
        self.text_resultado.insert(tk.END, informe)
        self.text_resultado.configure(state=tk.DISABLED)

    def limpiar_campos(self):
        """Restablece los campos de entrada y el panel de resultados."""
        self.entry_lat_a.delete(0, tk.END)
        self.entry_lon_a.delete(0, tk.END)
        self.entry_lat_b.delete(0, tk.END)
        self.entry_lon_b.delete(0, tk.END)
        
        self.text_resultado.configure(state=tk.NORMAL)
        self.text_resultado.delete('1.0', tk.END)
        self.text_resultado.configure(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = AppAnalisisEspacial(root)
    root.mainloop()

if __name__ == "__main__":
    main()
