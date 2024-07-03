import matplotlib.pyplot as plt

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        self.raiz = self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo, valor):
        if nodo is None:
            return Nodo(valor)
        if valor < nodo.valor:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, valor)
        else:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, valor)
        return nodo

    def dibujar(self):
        fig, ax = plt.subplots(figsize=(10, 8))
        self._dibujar_recursivo(ax, self.raiz, 1000, 1000, 500)
        ax.axis('off')
        plt.show()

    def _dibujar_recursivo(self, ax, nodo, x, y, espacio):
        if nodo:
            ax.text(x, y, str(nodo.valor), style='italic', ha='center', va='center',
                    bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))
            for i, hijo in enumerate([nodo.izquierda, nodo.derecha]):
                if hijo:
                    signo = -1 if i == 0 else 1
                    x_hijo = x + signo * espacio
                    y_hijo = y - 100
                    ax.plot([x, x_hijo], [y, y_hijo], linewidth=1, color='blue')
                    self._dibujar_recursivo(ax, hijo, x_hijo, y_hijo, espacio / 2)

arbol = ArbolBinario()
valores = [50, 30, 20, 40, 70, 60, 80, 10, 25, 35, 45, 65, 75, 90]

for valor in valores:
    arbol.insertar(valor)

arbol.dibujar()
