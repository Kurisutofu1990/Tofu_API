from flask import Flask
from flask_restful import Resource, Api


to_do_list = Flask(__name__)
api = Api(to_do_list)
Data = []

"""Basic Class"""

class Entries(Resource):
    """Basic Class"""
    def get(self, name):
        """Method for reading existing entries"""
        for x in Data:
            if x["Data"] == name:
                return x
        return {"Data": None}

    def post(self, name):
        """Method for posting new entries"""
        tem = {"Data": name}
        Data.append(tem)
        return tem

    def update(self, name):
        """Method for updating existing entries"""
        for ind, x in enumerate(Data):
            if x["Data"] == name:
                name = input("New Entrie")
        return name

    def delete(self, name):
        """Method for deleting existing entries"""
        for ind, x in enumerate(Data):
            if x["Data"] == name:
                Data.pop(ind)
                return {"Note": "Deleted"}
            else:
                print("No Entry")


api.add_resource(Entries, "/Name/<string:name>")


if __name__ == "__main__":
    to_do_list.run(debug=True)


