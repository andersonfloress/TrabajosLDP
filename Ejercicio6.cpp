#include<iostream>
#include<fstream>
#include<sstream>
#include<string>
#include<map>

using namespace std;

int main() {
	
	ifstream inputFile("C:\\LDP\\Informe de horas T.txt");
	ofstream outputFile("Horas trabajadas.txt");
	
	if(!inputFile.is_open()) {
		cerr<<"No se pudo abrir el archivo de entrada "<<endl;
		return 1;
	}
	if(!outputFile.is_open()){
		cerr<<"No se pudo abrir el archivo de salida "<<endl;
		return 1;
	}
	
	map<string, int> Htrabajadas;
	
	string line;
	while(getline(inputFile, line)) {
		stringstream iss(line);
		string nombre;
		int horas;
		getline(iss, nombre, ',');
		iss>>horas;
		
		if(!nombre.empty() && nombre[0] == ' '){
			nombre.erase(0, 1);
		}
		
		if(Htrabajadas.find(nombre) == Htrabajadas.end()) {
			Htrabajadas[nombre] = 0;
		}
		Htrabajadas[nombre] += horas;
	}
	
    for(map<string, int>::iterator it = Htrabajadas.begin(); it != Htrabajadas.end(); ++it) {
        outputFile<< it->first<<", Horas Totales: "<<it->second<<endl;
    }
	
	inputFile.close();
	outputFile.close();
	
	cout<<"El informe de horas trabajadas se ha guardado en 'Horas trabajadas'"<<endl;
	
	return 0;
}
