#include<iostream>
#include<fstream>
#include<sstream>
#include<string>
#include<iomanip>
using namespace std;

int main() {
	
	ifstream inputFile("C:\\LDP\\Productos.txt");
	ofstream outputFile("precios en soles");
	
	if(!inputFile.is_open()) {
		cerr<<"No se pudo abrir el archivo de entrada "<<endl;
		return 1;
	}
	if(!outputFile.is_open()) {
		cerr<<"No se pudo abrir el archivo de salida "<<endl;
		return 1;
	}
	
	const double conversion = 3.85;
	
	string line;
	while(getline(inputFile, line)) {
		istringstream iss(line);
		string producto;
		double precioDolar;
		
		getline(iss, producto, ',');
		iss>>precioDolar;
		
		double precioSoles = precioDolar * conversion;
		
		outputFile<<producto<<", "<<fixed<<setprecision(2)<<precioSoles<<endl;
		
	}
	inputFile.close();
	outputFile.close();
	
	cout<<"La conversion se completo y se guardo en 'precios en soles'"<<endl;

	return 0;
}
