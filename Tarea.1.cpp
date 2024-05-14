#include <iostream>
using namespace std;

int main() {
    int nElementos, lonMaxima, totalCombinaciones = 0;
    const int MaxElementos = 10;
    char alfabeto[MaxElementos];

    cout << "Ingrese el numero de elementos del alfabeto: ";
    cin >> nElementos;

    cout << "Ingrese la longitud maxima del lenguaje: ";
    cin >> lonMaxima;

    cout << "Ingrese los elementos del alfabeto: ";
    for (int i = 0; i < nElementos; ++i) {
        cin >> alfabeto[i];
    }

    cout << "\nCOMBINACIONES DEL LENGUAJE " << endl;
    for(int i = 0; i < nElementos; i++) {
        cout << i + 1 << ": " << alfabeto[i] << endl;
        totalCombinaciones++;
    }

    for(int i = 0; i < nElementos; i++) {
        cout<<totalCombinaciones + 1 <<": "<<alfabeto[i]<<alfabeto[i]<<endl;
        totalCombinaciones++;
    }

    for(int i = 0; i < nElementos; i++) {
        for (int j = 0; j < nElementos; j++) {
            if (i != j) {
                cout<<totalCombinaciones + 1 << ": "<<alfabeto[i];
				cout<<alfabeto[j]<<endl;
                totalCombinaciones++;
            }
        }
    }

    cout << "\nEL NUMERO TOTAL DE COMBINACIONES ES : "<<totalCombinaciones<<endl;
    return 0;
}


