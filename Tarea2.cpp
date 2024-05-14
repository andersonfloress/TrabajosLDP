#include<iostream>
#include<vector>
#include<fstream>
#include<string>
#include<iomanip>
#include<numeric>

using namespace std;
int main() {
	
	string nomArchivoEntrada = "C:\\Users\\Usuario\\Documents\\datos.txt";
	string nomArchivoSalida = "resultado.txt";
	
	ifstream archivo_entrada(nomArchivoEntrada.c_str());
	if (!archivo_entrada.is_open()) {
		cerr<<"No se pudo abrir el archivo: "<<nomArchivoEntrada<<endl;
		return 1;
	}
	
	vector<double> datos;
	double dat;
	while (archivo_entrada >> dat) {
		datos.push_back(dat);
	}
	archivo_entrada.close();
	
	double promedio = 0.0;
	if (!datos.empty()) {
		promedio = accumulate(datos.begin(), datos.end(), 0.0) / datos.size();
	}
	
	ofstream archivo_salida(nomArchivoSalida.c_str());
	if (!archivo_salida.is_open()) {
		cerr<<"No se pudo abrir el archivo de salida: "<<nomArchivoSalida<<endl;
		return 1;
	}
	
	archivo_salida<<"El promedio de los datos es: "<<fixed<<setprecision(2)<<promedio<<endl;
	archivo_salida.close();
	
	cout<<"Se a calculado el promedio y se ha guardado en el archivo resultado.txt"<<endl;
	
	return 0;
}
