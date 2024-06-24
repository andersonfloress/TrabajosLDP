import os
import cherrypy
from jinja2 import Environment, FileSystemLoader
import pandas as pd
from io import BytesIO

env = Environment(loader=FileSystemLoader('Templates'))

def contar_loc(contenido_archivo):
    lineas = contenido_archivo.split('\n')
    total_lineas = len(lineas)
    lineas_no_vacias = sum(1 for linea in lineas if linea.strip() != '')
    lineas_comentarios = sum(1 for linea in lineas if linea.strip().startswith('#'))
    lineas_codigo = lineas_no_vacias - lineas_comentarios
    lineas_blanco = total_lineas - lineas_no_vacias
    relacion_comentarios_codigo = lineas_comentarios / lineas_codigo if lineas_codigo > 0 else 0

    return {
        "Lines of Code (LOC)": total_lineas,
        "Executable Lines of Code (ELOC)": lineas_codigo,
        "Comment Lines of Code (CLOC)": lineas_comentarios,
        "Comment to Code Ratio (CCR)": round(relacion_comentarios_codigo, 2),
        "Non-Comment Lines of Code (NCLOC)": lineas_no_vacias,
        "Blank Lines of Code (BLOC)": lineas_blanco
    }

class LOCApp:
    @cherrypy.expose
    def index(self):
        return self.render_template()

    @cherrypy.expose
    def upload(self, myfile):
        contenido_archivo = myfile.file.read().decode('utf-8')
        resultados = contar_loc(contenido_archivo)
        df_resultados = pd.DataFrame(resultados.items(), columns=['Métrica', 'Cantidad'])
        df_resultados['Cantidad'] = df_resultados['Cantidad'].astype(int)
        
        return self.render_template(tablas=[df_resultados.to_html(classes='data', header="true", index=False)])

    @cherrypy.expose
    def download_excel(self, myfile):
        contenido_archivo = myfile.file.read().decode('utf-8')
        resultados = contar_loc(contenido_archivo)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            pd.DataFrame(resultados.items(), columns=['Métrica', 'Cantidad']).to_excel(writer, index=False, sheet_name='Métricas LOC')

        datos_excel = output.getvalue()
        cherrypy.response.headers['Content-Disposition'] = 'attachment; filename=resultados_loc.xlsx'
        cherrypy.response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        return datos_excel

    def render_template(self, tablas=None):
        tmpl = env.get_template('index.html')
        return tmpl.render(tablas=tablas or [])

if __name__ == '__main__':
    cherrypy.quickstart(LOCApp(), '/', {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        }
    })
