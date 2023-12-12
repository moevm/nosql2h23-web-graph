from flask import Flask, render_template, request, jsonify

from DatabaseController import DatabaseController
from Link_loader import Link_loader
from Adapter import Adapter

app = Flask(__name__)

db = DatabaseController(database_url="bolt://localhost:7687", username="Anton_Korsunov", password="123456789")


@app.route('/', methods=["GET"])
def load_main_page():
    return render_template("main.html")


@app.route('/', methods=['POST'])
def enter_link():
    link = request.data.decode(encoding="utf-8")
    nodes_counter = 0
    limit = 500

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


app.run(host="127.0.0.1", port=3000)
