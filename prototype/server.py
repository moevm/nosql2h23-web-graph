from flask import Flask, render_template, request, jsonify
import neo4jTools
from get_link import get_link

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
    temp = get_link(link)
    for i in temp:
        print(i)
    print(len(temp))

    #conn.query("CREATE (n:Test {link: " + link + "})", db="test")
    return jsonify({"message": "Link created successfully"})


if __name__ == '__main__':
    app.run()
