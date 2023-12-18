from flask import Flask, render_template, request, jsonify, send_file
from DatabaseController import DatabaseController
from Link_loader import Link_loader
from Adapter import Adapter
import os

UPLOAD_FOLDER = r'C:\NO_SQL_proj\relate-data\dbmss\dbms-fe9cad2d-7010-4966-a5ac-8d744843ce3c\import'


app = Flask(__name__)

db = DatabaseController(database_url="bolt://localhost:7687", username="neo4j", password="12345678")


@app.route('/', methods=["GET"])
def load_main_page():
    return render_template("main.html")

@app.route('/export', methods=["GET"])
def export_graph():
    end_path = db.export()
    file_path = os.path.join(UPLOAD_FOLDER, end_path)
    return send_file(file_path, as_attachment=True)

@app.route('/import', methods=["POST"])
def import_graph():

    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    uploaded_file.save(file_path)

    db.import_(filename)
    return jsonify({"message": "Link created successfully"})


@app.route('/', methods=['POST'])
def enter_link():
    link = request.data.decode(encoding="utf-8")
    nodes_counter = 0
    limit = 500

    Link_loader.reset_active_nodes(db)

    while (nodes_counter < limit):
        if link:
            temp, nodes_counter = Link_loader.links_search(db, link, limit, nodes_counter)
        for i in temp:
            if nodes_counter >= limit:
                break
            if i:
                nodes_counter = Link_loader.links_search(db, i, limit, nodes_counter)[1]

        if temp:
            link = temp[0]
        else:
            break

    return jsonify({"message": "Link created successfully"})


@app.route('/graph_data', methods=["GET"])
def update_graph_data():
    return Adapter.get_graph(db)

@app.route('/all_graph', methods=["GET"])
def show_all_graph():
    return Adapter.get_all_graph(db)


app.run(host="127.0.0.1", port=3000)
