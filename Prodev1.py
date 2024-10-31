import random

class Equipo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.eficiencia_arquero = random.randint(1, 10)
        self.rendimiento_general = random.randint(1, 10)
        self.eficiencia_gol = random.randint(1, 10)
        self.historial_resultados = []

    def calcular_ventaja_competitiva(self):
        if len(self.historial_resultados) < 5:
            return None
        return max(set(self.historial_resultados), key=self.historial_resultados.count)

    def __str__(self):
        return f"{self.nombre} (Arquero: {self.eficiencia_arquero}, Rendimiento: {self.rendimiento_general}, Gol: {self.eficiencia_gol})"


class Partido:
    def __init__(self, local, visitante):
        self.local = local
        self.visitante = visitante
        self.resultado = None

    def ejecutar_partido(self):
        local_score = (self.local.rendimiento_general + self.local.eficiencia_arquero + self.local.eficiencia_gol)
        visitante_score = (self.visitante.rendimiento_general + self.visitante.eficiencia_arquero + self.visitante.eficiencia_gol)

        if local_score > visitante_score:
            self.resultado = 'L'
            self.local.historial_resultados.append('V')
            self.visitante.historial_resultados.append('D')
        elif visitante_score > local_score:
            self.resultado = 'V'
            self.local.historial_resultados.append('D')
            self.visitante.historial_resultados.append('V')
        else:
            self.resultado = 'E'
            self.local.historial_resultados.append('E')
            self.visitante.historial_resultados.append('E')

    def __str__(self):
        return f"{self.local.nombre} vs {self.visitante.nombre} - Resultado: {self.resultado if self.resultado else 'Sin jugar'}"


class Boleta:
    def __init__(self, usuario):
        self.usuario = usuario
        self.partidos = []

    def agregar_partido(self, partido):
        self.partidos.append(partido)

    def mostrar_boleta(self, fecha_ejecutada):
        print("\n{:<3} | {:<15} | {:<15} | {:<10} | {:<10}".format(
            "#", "Local", "Visitante", "Pronóstico", "Resultado"))
        print("-" * 60)
        for i, partido in enumerate(self.partidos, start=1):
            pronostico = self.usuario.pronosticos[i - 1]
            resultado = partido.resultado if fecha_ejecutada else "Pendiente"
            print("{:<3} | {:<15} | {:<15} | {:^10} | {:^10}".format(
                i, partido.local.nombre, partido.visitante.nombre, pronostico, resultado))


class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre
        self.pronosticos = []
        self.puntos_totales = 0
        self.partidos_totales = 0

    def apostar(self, boleta):
        print("\nApostar en los partidos:")
        print("{:<3} | {:<15} | {:<15}".format("#", "Local", "Visitante"))
        print("-" * 40)
        for i, partido in enumerate(boleta.partidos, start=1):
            print("{:<3} | {:<15} | {:<15}".format(i, partido.local.nombre, partido.visitante.nombre))
            while True:
                pronostico = input("Pronóstico (L = Local, V = Visitante, E = Empate): ").upper()
                if pronostico in ['L', 'V', 'E']:
                    self.pronosticos.append(pronostico)
                    self.partidos_totales += 1
                    break
                else:
                    print("Error: Debe ingresar una opción válida (L, V o E).")

    def calcular_promedio(self):
        if self.partidos_totales == 0:
            return 0
        return self.puntos_totales / self.partidos_totales


class SistemaProde:
    def __init__(self):
        self.equipos = []
        self.boleta = None
        self.usuario = None
        self.mejores_promedios = {}
        self.estado = 1

    def cargar_equipos(self):
        nombres_equipos = [
            "River Plate", "Boca Juniors", "Independiente", "Racing Club", "San Lorenzo",
            "Huracán", "Talleres", "Lanús", "Newell's Old Boys", "Rosario Central",
            "Nueva Chicago", "Gimnasia", "Estudiantes", "Argentinos Juniors",
            "Vélez Sarsfield", "Defensa y Justicia"
        ]
        for nombre in nombres_equipos:
            self.equipos.append(Equipo(nombre))

    def crear_boleta(self):
        if self.estado == 1:
            nombre_usuario = input("Ingrese el nombre del usuario: ")
            self.usuario = Usuario(nombre_usuario)
            self.boleta = Boleta(self.usuario)
            random.shuffle(self.equipos)
            for i in range(0, len(self.equipos), 2):
                partido = Partido(self.equipos[i], self.equipos[i + 1])
                self.boleta.agregar_partido(partido)
            print("Boleta creada.")
            self.estado = 2
        else:
            print("Primero debe Crear boleta")

    def apostar(self):
        if self.estado == 2 and self.boleta:
            self.usuario.apostar(self.boleta)
            print("Apuestas realizadas.")
            self.estado = 3
        else:
            print("Primero debe crear una boleta.")

    def ejecutar_fecha(self):
        if self.estado == 3 and self.boleta:
            for partido in self.boleta.partidos:
                partido.ejecutar_partido()
            for i, partido in enumerate(self.boleta.partidos):
                pronostico = self.usuario.pronosticos[i]
                if (pronostico == 'L' and partido.resultado == 'L') or \
                   (pronostico == 'V' and partido.resultado == 'V') or \
                   (pronostico == 'E' and partido.resultado == 'E'):
                    self.usuario.puntos_totales += 3
            promedio_usuario = self.usuario.calcular_promedio()
            self.mejores_promedios[self.usuario.nombre] = promedio_usuario
            print("Fecha ejecutada y promedio del usuario guardado.")
            self.estado = 4
        else:
            print("Primero debe crear una boleta.")

    def mostrar_boleta(self):
        if self.estado == 4 and self.boleta:
            fecha_ejecutada = all(p.resultado for p in self.boleta.partidos)
            self.boleta.mostrar_boleta(fecha_ejecutada)
            self.estado = 1
        else:
            print("Primero debe ejecutar la fecha")

    def mostrar_mejores_promedios(self):
        print("\nUsuarios con mejores promedios de aciertos:")
        for usuario, promedio in self.mejores_promedios.items():
            print(f"{usuario}: {promedio:.2f}")

    def menu(self):
        self.cargar_equipos()
        while True:
            print("\n--- Sistema de Prode ---")
            print("1. Crear boleta")
            print("2. Apostar")
            print("3. Ejecutar fecha")
            print("4. Mostrar boleta")
            print("5. Mostrar Mejores Promedios")
            print("6. Salir")
            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                self.crear_boleta()
            elif opcion == "2":
                self.apostar()
            elif opcion == "3":
                self.ejecutar_fecha()
            elif opcion == "4":
                self.mostrar_boleta()
            elif opcion == "5":
                self.mostrar_mejores_promedios()
            elif opcion == "6":
                break
            else:
                print("Opción inválida.")

sistema = SistemaProde()
sistema.menu()
