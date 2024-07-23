import 'package:flutter/material.dart';
import 'dart:html' as html;
import 'dart:math';
import 'package:csv/csv.dart';

void main() {
  runApp(MiApp());
}

class MiApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Programa Que Realiza Calculos Estadisticos'),
        ),
        body: EstadisticasCSV(),
      ),
    );
  }
}

class EstadisticasCSV extends StatefulWidget {
  @override
  _EstadoEstadisticasCSV createState() => _EstadoEstadisticasCSV();
}

class _EstadoEstadisticasCSV extends State<EstadisticasCSV> {
  List<List<dynamic>>? datosCSV;
  List<double> datosNumericos = [];

  void cargarCSV() {
    final uploadInput = html.FileUploadInputElement();
    uploadInput.accept = '.csv';
    uploadInput.click();

    uploadInput.onChange.listen((event) {
      final file = uploadInput.files!.first;
      final reader = html.FileReader();

      reader.onLoadEnd.listen((event) {
        final content = reader.result as String;
        List<List<dynamic>> filasComoLista = const CsvToListConverter(eol: '\n', fieldDelimiter: ';').convert(content);
        
        setState(() {
          datosCSV = filasComoLista;
          datosNumericos = filasComoLista
              .expand((fila) => fila.map((dato) => double.tryParse(dato.toString()) ?? 0.0))
              .toList();
        });
      });

      reader.readAsText(file);
    });
  }

  double calcularMedia(List<double> datos) {
    if (datos.isEmpty) return 0.0;
    return calcularMediaEstadistica(datos);
  }

  num calcularMediana(List<double> datos) {
    if (datos.isEmpty) return 0.0;
    return calcularMedianaEstadistica(datos);
  }

  double calcularDesviacionEstandar(List<double> datos) {
    if (datos.isEmpty) return 0.0;
    return calcularDesviacionEstandarEstadistica(datos);
  }

  double calcularModa(List<double> datos) {
    if (datos.isEmpty) return 0.0;
    return calcularModaEstadistica(datos);
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            ElevatedButton(
              onPressed: cargarCSV,
              child: Text('Cargar Archivo CSV'),
            ),
            if (datosCSV != null) ...[
              Text('Datos Cargados'),
              SizedBox(height: 20),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: DataTable(
                  columns: List.generate(
                    datosCSV![0].length,
                    (index) => DataColumn(label: Text('')), // Dejar el label vacío para no mostrar encabezados
                  ),
                  rows: List.generate(
                    datosCSV!.length,
                    (index) => DataRow(
                      cells: List.generate(
                        datosCSV![index].length,
                        (cellIndex) => DataCell(Text(datosCSV![index][cellIndex].toString())),
                      ),
                    ),
                  ),
                ),
              ),
              Text('Calculos Estadisticos'),
              SizedBox(height: 20),
              Text('Media: ${calcularMedia(datosNumericos).toStringAsFixed(2)}'),
              Text('Mediana: ${calcularMediana(datosNumericos).toStringAsFixed(2)}'),
              Text('Desviación Estándar: ${calcularDesviacionEstandar(datosNumericos).toStringAsFixed(2)}'),
              Text('Moda: ${calcularModa(datosNumericos).toStringAsFixed(2)}'),
            ],
          ],
        ),
      ),
    );
  }
}

// Funciones estadísticas adaptadas
double calcularMediaEstadistica(List<double> datos) {
  if (datos.isEmpty) return 0.0;
  return datos.reduce((a, b) => a + b) / datos.length;
}

num calcularMedianaEstadistica(List<double> datos) {
  if (datos.isEmpty) return 0.0;
  datos.sort();
  final medio = datos.length ~/ 2;
  return datos.length % 2 == 0 ? (datos[medio - 1] + datos[medio]) / 2 : datos[medio];
}

double calcularDesviacionEstandarEstadistica(List<double> datos) {
  if (datos.isEmpty) return 0.0;
  final media = calcularMediaEstadistica(datos);
  final sumaCuadrados = datos.map((dato) => (dato - media) * (dato - media)).reduce((a, b) => a + b);
  return sqrt(sumaCuadrados / datos.length);
}

double calcularModaEstadistica(List<double> datos) {
  if (datos.isEmpty) return 0.0;
  final frecuencias = <double, int>{};
  for (var dato in datos) {
    frecuencias[dato] = (frecuencias[dato] ?? 0) + 1;
  }
  final moda = frecuencias.entries.reduce((a, b) => a.value > b.value ? a : b).key;
  return moda;
}
