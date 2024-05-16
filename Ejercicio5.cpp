#include<iostream>
#include<fstream>
#include<sstream>
#include<string>
#include<iomanip>

using namespace std;

int main() {
	
	ifstream inputFile("C:\\LDP\\Registro de ventas.txt");
	ofstream outputFile("Ventas.txt");
	
	if(!inputFile.is_open()) {
		cerr<<"No se pudo abrir el archivo de entrada "<<endl;
		return 1;
	}
	if(!outputFile.is_open()) {
		cerr<<"No se pudo abrir el archivo de salida "<<endl;
		return 1;
	}
	
	string line;
	string max, min;
	double maxVenta = -10000.0;
	double minVenta = 99999999.0;
	double total = 0.0;
	int n_dias = 0;
	
	while(getline(inputFile, line)) {
		istringstream iss(line);
		string dias;
		float venta;
		
		getline(iss, dias, ',');
		iss>>venta;
		
		if(venta > maxVenta) {
			maxVenta = venta;
			max = dias;
		}
		if(venta < minVenta) {
			minVenta = venta;
			min = dias;
		}
		total += venta;
		n_dias++;
	}
	float promedio = total / n_dias;
	
	outputFile<<"Venta Total: "<<total<<endl;
	outputFile<<"Promedio de ventas: "<<fixed<<setprecision(2)<<promedio<<endl;
	outputFile<<"Dia de mayor venta: "<<max<<", "<<maxVenta<<endl;
	outputFile<<"Dia de menor venta: "<<min<<", "<<minVenta<<endl;
	
	inputFile.close();
	outputFile.close();
	
	cout<<"El promedio de ventas se ha guardado en 'Ventas.txt'"<<endl;
	
	return 0;
}
