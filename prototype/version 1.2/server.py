from flask import Flask, render_template, request, jsonify

from DatabaseController import DatabaseController
from Link_loader import Link_loader
from Adapter import Adapter
from Algorithms import Algorithms

app = Flask(__name__)

db = DatabaseController(database_url="bolt://localhost:7687", username="neo4j", password="67tyghbn")
alg_controller = Algorithms(db)


@app.route('/', methods=["GET"])
def load_main_page():
    return render_template("home.html")


@app.route('/', methods=['POST'])
def enter_link():
    link = request.data.decode(encoding="utf-8")
    nodes_counter = 0
    limit = 400

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


@app.route("/algorithms/strongly_connected_components", methods=["GET"])
def strongly_connected_data():
    alg_controller.update_graph()
    return jsonify(alg_controller.get_strongly_connected_components())


@app.route("/algorithms/page_rank", methods=["GET"])
def get_page_rank():
    alg_controller.update_graph()
    return jsonify(alg_controller.get_page_rank())


@app.route("/algorithms/centrality", methods=["GET"])
def get_centrality():
    alg_controller.update_graph()
    centrality_type = request.args.get("type")
    config = {"type": centrality_type}
    return jsonify(alg_controller.get_centrality(config))


@app.route("/algorithms/find_path", methods=["GET"])
def find_path():
    alg_controller.update_graph()
    start_id = int(request.args.get("start_id"))
    finish_id = int(request.args.get("finish_id"))
    return jsonify(alg_controller.find_path(start_id, finish_id))


app.run(host="127.0.0.1", port=3000)
