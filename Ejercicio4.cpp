#include<iostream>
#include<fstream>
#include<sstream>
#include<string>
#include<iomanip>

using namespace std;

int main() {
	
	ifstream inputFile("C:\\LDP\\Temperaturas.txt");
	ofstream outputFile("registro de temperaturas.txt");
	
	if(!inputFile.is_open()) {
		cerr<<"No se pudo abrir el archivo de entrada "<<endl;
		return 1;
	}
	if(!outputFile.is_open()) {
		cerr<<"No se pudo abrir el archivo de salida "<<endl;
		return 1;
	}
	
	string line;
	string min, max;
	double maxTem = -250.0;
	double minTem = 200.0;
	
	while(getline(inputFile, line)) {
		istringstream iss(line);
		string fecha;
		double temperatura;
		
		getline(iss, fecha, ',');
		iss>>temperatura;
		
		
		if(temperatura > maxTem) {
			maxTem = temperatura;
			max = fecha;
		}
		if(temperatura < minTem) {
			minTem = temperatura;
			min = fecha;
		}
	}
	outputFile<<"Dia de temperatura maxima: "<<max<<", "<<maxTem<<endl;
	outputFile<<"Dia de temperatura minima: "<<min<<", "<<minTem<<endl;
	
	inputFile.close();
	outputFile.close();
	
	cout<<"El registro de temperaturas se guardo en 'registro de temperaturas'"<<endl;
	
    return 0; 
}
    

