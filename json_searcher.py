import argparse
import json
import csv

class JSONSearcher: #Esta clase implementa un buscador y editor de datos en formato JSON.

    def __init__(self, data):
        """ Constructor de la clase.
        Recibe como parámetro una lista de objetos JSON que se almacenan en data."""
        self.data = data

#Métods de la clase JSONSearcher
    def search(self, **kwargs):
        """ Busca objetos en la lista de datos que coincidan con los argumentos de búsqueda (name= Alice).
        Devuelve una lista de objetos que coinciden con los argumentos de búsqueda."""
        results = []
        for item in self.data:
            if all(item.get(key) == value for key, value in kwargs.items()):
                results.append(item)
        return results

    def insert(self, **kwargs): #Inserta un nuevo objeto en la lista (name= Hiram).
        self.data.append(kwargs)

    def edit(self, index, **kwargs): #Edita un objeto en la lista de datos.
        """ index : Índice del objeto a editar.
        **kwargs : Nuevos valores en formato clave-valor."""
        self.data[index].update(kwargs)

    def delete(self, index): #Elimina un objeto existente en la lista de datos.
        del self.data[index]

    def export(self, file_path, export_format="csv", results=None, results_only=False): #Exporta la lista de datos a un archivo CSV o JSON.
        """ file_path : Ruta del archivo de salida.
        export_format : Formato de exportación, csv o json.
        results : Lista de objetos a exportar.
        results_only : Exportar solo los resultados de una búsqueda."""
        if not results:
            results = self.data

        if results_only:
            data_to_export = results
        else:
            data_to_export = self.data

        if export_format == "csv":
            with open(file_path, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=data_to_export[0].keys())
                writer.writeheader()
                writer.writerows(data_to_export)
        elif export_format == "json":
            with open(file_path, "w") as file:
                json.dump(data_to_export, file, indent=4)

""" La función main() maneja los métodos de search, insert, edit y delete que se ingresan como argumentos
en la CLI. Luego, se almacenan los resultados de la operación en `results`. """

def main():
    #El módulo argparse para usa para definir los argumentos de la línea de comandos.
    parser = argparse.ArgumentParser(prog="JSON Searcher", description="Search a JSON file for objects with specific attributes")
    parser.add_argument("--input_file", type=str, required=True, help="Path to input JSON file")
    parser.add_argument("--output_file", type=str, required=True, help="Path to output file")
    parser.add_argument("--search", type=str, nargs="*", help="Search query in the format 'key=value'")
    parser.add_argument("--insert", type=str, nargs="*", help="Object to insert in the format 'key=value'")
    parser.add_argument("--edit", type=int, help="Index of object to edit")
    parser.add_argument("--delete", type=int, help="Index of object to delete")
    parser.add_argument("--export_format", type=str, choices=["csv", "json"], default="csv", help="Export format (csv or json)")
    args = parser.parse_args()

    with open(args.input_file, "r") as file:
        data = json.load(file)

    searcher = JSONSearcher(data)


    if args.search: # Si se ha especificado una búsqueda
        search_query = {}
        for item in args.search:
            key, value = item.split("=")
            search_query[key] = value
        results = searcher.search(**search_query) # Realizar la búsqueda utilizando los parámetros especificados

    elif args.insert: # Si se ha especificado una inserción
        insert_query = {}
        for item in args.insert:
            key, value = item.split("=")
            insert_query[key] = value
        searcher.insert(**insert_query) # Insertar el elemento en el objeto JSON
        results = [insert_query] # Almacenar el elemento insertado en la variable `results`

    elif args.edit is not None: # Si se ha especificado una edición
        edit_query = {}
        for item in args.insert:
            key, value = item.split("=")
            edit_query[key] = value
        searcher.edit(args.edit, **edit_query) # Editar el elemento en el objeto JSON
        results = [searcher.data[args.edit]] # Almacenar el elemento editado en la variable `results`

    elif args.delete is not None: # Si se ha especificado una eliminación
        searcher.delete(args.delete) # Eliminar el elemento del objeto JSON
        results = [] # Establecer la variable `results` en una lista vacía

    else: # Si no se ha especificado ninguna operación, mostrar todo el contenido del objeto JSON
        results = searcher.data

    # Exportar los resultados a un archivo de salida
    searcher.export(args.output_file, export_format=args.export_format)

    # Si se encontraron resultados, mostrarlos por pantalla y exportarlos a un archivo csv
    if results:
        print(f"{len(results)} results found:")
        for item in results:
            print(item)
        searcher.export(args.output_file,
                        export_format=args.export_format,
                        results=results,
                        results_only=True)
    else: # Si no se encuentrann resultados
        print("No results found.")



if __name__ == "__main__":
    main()
