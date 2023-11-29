from flask import Flask, render_template, request, jsonify
import neo4jTools
from links_search import links_search

app = Flask(__name__)

# подключение к СУБД (по умолчанию она разворачивается на 7687 порту, пользователя надо создать в СУБД)
# user - логин существующего пользователя в СУБД, password - его пароль
conn = neo4jTools.Neo4jConnection(uri="bolt://localhost:7687", user="Anton_Korsunov", password="123456789")


@app.route('/', methods=["GET"])
def get_search_form():
    return render_template("home.html")


@app.route('/', methods=["POST"])
def enter_link():
    link = request.form.get("link")

    nodes_counter = 0
    limit = 1500
    
    while(nodes_counter < limit):
        if link:
            temp, nodes_counter = links_search(conn, link, limit, nodes_counter)
        for i in temp:
            if nodes_counter >= limit:
                break
            if i:
                nodes_counter = links_search(conn, i, limit, nodes_counter)[1]
        
        if temp:
            link = temp[0]
        else:
            break

    return jsonify({"message": "Link created successfully"})


if __name__ == '__main__':
    app.run()
