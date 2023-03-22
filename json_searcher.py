import argparse
import json
import csv

class JSONSearcher:
    """
    Esta clase implementa un buscador y editor de datos en formato JSON.
    """

    def __init__(self, data):
        """
        Constructor de la clase.

        Parameters
        ----------
        data : list
            Lista de objetos en formato JSON.
        """
        self.data = data

    def search(self, **kwargs):
        """
        Busca objetos en la lista de datos que coincidan con los argumentos de búsqueda.

        Parameters
        ----------
        **kwargs : dict
            Argumentos de búsqueda en formato clave-valor.

        Returns
        -------
        list
            Lista de objetos que coinciden con los argumentos de búsqueda.
        """
        results = []
        for item in self.data:
            if all(item.get(key) == value for key, value in kwargs.items()):
                results.append(item)
        return results

    def insert(self, **kwargs):
        """
        Inserta un nuevo objeto en la lista de datos.

        Parameters
        ----------
        **kwargs : dict
            Nuevo objeto en formato clave-valor.
        """
        self.data.append(kwargs)

    def edit(self, index, **kwargs):
        """
        Edita un objeto existente en la lista de datos.

        Parameters
        ----------
        index : int
            Índice del objeto a editar.
        **kwargs : dict
            Nuevos valores en formato clave-valor para el objeto.
        """
        self.data[index].update(kwargs)

    def delete(self, index):
        """
        Elimina un objeto existente en la lista de datos.

        Parameters
        ----------
        index : int
            Índice del objeto a eliminar.
        """
        del self.data[index]

    def export(self, file_path, export_format="csv", results=None, results_only=False):
        """
        Exporta la lista de datos a un archivo en formato CSV o JSON.

        Parameters
        ----------
        file_path : str
            Ruta del archivo de salida.
        export_format : str, optional
            Formato de exportación (csv o json), por defecto "csv".
        results : list, optional
            Lista de objetos a exportar, por defecto None.
        results_only : bool, optional
            Si se exportan solo los resultados de una búsqueda, por defecto False.
        """
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


def main():
    parser = argparse.ArgumentParser(description="Search a JSON file for objects with specific attributes")
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

# Este bloque de código maneja las opciones de búsqueda, inserción, edición o eliminación
# que se ingresan como argumentos de línea de comando y llama a los métodos correspondientes
# del objeto `searcher`. Luego, se almacenan los resultados de la operación en la variable `results`.

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

    # Si se encontraron resultados, mostrarlos por pantalla y exportarlos a un archivo de salida
    if results:
        print(f"{len(results)} results found:")
        for item in results:
            print(item)
        searcher.export(args.output_file,
                        export_format=args.export_format,
                        results=results,
                        results_only=True)
    else: # Si no se encontraron resultados, mostrar un mensaje indicando esto
        print("No results found.")



if __name__ == "__main__":
    main()
