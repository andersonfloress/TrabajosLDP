#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <map>

using namespace std;

int main() {
    
    ifstream inputFile("C:\\LDP\\Registro de errores.txt");
    ofstream outputFile("Errores.txt");

    if (!inputFile.is_open()) {
        cerr << "No se pudo abrir el archivo de entrada" << endl;
        return 1;
    }
    if (!outputFile.is_open()) {
        cerr << "No se pudo abrir el archivo de salida" << endl;
        return 1;
    }

    map<string, int> Errores;

    string line;
    while (getline(inputFile, line)) {
        string t_error = line.substr(0, line.find(":"));

        Errores[t_error]++;
    }
    for (map<string, int>::iterator it = Errores.begin(); it != Errores.end(); ++it) {
        outputFile<<it->first<<": "<<it->second<<endl;
    }
    
    inputFile.close();
    outputFile.close();

    cout << "El registro se ha guardado en 'Errores.txt'" << endl;

    return 0;
}

