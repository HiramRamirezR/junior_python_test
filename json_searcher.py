import argparse
import json
import csv


class JSONSearcher:
    def __init__(self, data):
        self.data = data

    def search(self, **kwargs):
        results = []
        for item in self.data:
            if all(item.get(key) == value for key, value in kwargs.items()):
                results.append(item)
        return results

    def insert(self, **kwargs):
        self.data.append(kwargs)

    def edit(self, index, **kwargs):
        self.data[index].update(kwargs)

    def delete(self, index):
        del self.data[index]

    def export(self, file_path, export_format="csv", results=None, results_only=False):
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

    if args.search:
        search_query = {}
        for item in args.search:
            key, value = item.split("=")
            search_query[key] = value
        results = searcher.search(**search_query)
    elif args.insert:
        insert_query = {}
        for item in args.insert:
            key, value = item.split("=")
            insert_query[key] = value
        searcher.insert(**insert_query)
        results = [insert_query]
    elif args.edit is not None:
        edit_query = {}
        for item in args.insert:
            key, value = item.split("=")
            edit_query[key] = value
        searcher.edit(args.edit, **edit_query)
        results = [searcher.data[args.edit]]
    elif args.delete is not None:
        searcher.delete(args.delete)
        results = []
    else:
        results = searcher.data

    searcher.export(args.output_file, export_format=args.export_format)

    if results:
        print(f"{len(results)} results found:")
        for item in results:
            print(item)
        searcher.export(args.output_file,
                    export_format=args.export_format,
                    results=results,
                    results_only=True)
    else:
        print("No results found.")


if __name__ == "__main__":
    main()
