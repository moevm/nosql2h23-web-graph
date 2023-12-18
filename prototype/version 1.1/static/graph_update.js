

class Graph{

    static graph = ForceGraph()

    static{
        Graph.graph(document.getElementById('container1')).graphData({"nodes":[],"links":[]})
      .nodeId('id')
      .nodeLabel('domain')
      .linkSource('source')
      .linkTarget('target')
      .nodeAutoColorBy('group')
      .onNodeClick(node=>{
        window.open(node.url,'_blank')
      })

      Graph.graph.width(document.getElementById('container1').offsetWidth);
      Graph.graph.height(document.getElementById('container1').offsetHeight);
    }

    static update_data(path){
        fetch(path).then(res => res.json()).then(input =>{
            Graph.graph.graphData(input);
            createTable();
        })
    }

}

function load_links(){
    input_val = document.getElementById('inp-page_address').value
    // input_val = document.getElementById('input').value
    fetch("/",{
        method:'POST',
        body: input_val
    }).then(res=>{
    Graph.update_data("/graph_data");
    })
}

function getLastGraph(){
    Graph.update_data("/graph_data");
}

function getAllGraph(){
    Graph.update_data("/all_graph");
}

function export_graph(){
    window.location.href = "/export";
}

function getPageRank(){
    window.location.href = "/page_rank";
}

function getCentrality(){
    let el = document.getElementById('sel-centr');
    let option = el.options[el.selectedIndex].value;
    window.location.href = "/centrality/"+option;
}

function getPath(){
    input_val1 = document.getElementById('inp-page_address1').value
    input_val2 = document.getElementById('inp-page_address2').value
    fetch("/",{
        method:'POST',
        body: JSON.stringify([input_val,input_val2])
    }).then(res=>{
        Graph.update_data();
    })
}

function import_graph(){
    let input = document.createElement('input');
    input.type = 'file';

    input.addEventListener('change', function () {
        if (input.files.length > 0) {
            var file = input.files[0];
            upload_file(file);

            input.value = '';
        }
    });
    input.click();
}

function upload_file(file) {
    let formData = new FormData();
    formData.append('file', file);

    fetch('/import', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
}

function getOriginalGraph(){
    window.location.href = "/original-graph";
}

function getStrong(){
    window.location.href = "/strong-component";
}



function createTable() {
    var Arr = [
        ["Сайт 1", "http://site1.com"],
        ["Сайт 2", "http://site2.com"],
        ["Сайт 3", "http://site3.com"],
        ["Сайт 3", "http://site3.com"],
        ["Сайт 3", "http://site3.com"],
        ["Сайт 3", "http://site3.com"],
        ["Сайт 3", "http://site3.com"],
        ["Сайт 3", "http://site3.com"],
        ["Сайт 3", "http://site3.com"],
        ["Сайт 3", "http://site3.com"],
        ["Сайт 3", "http://site3.com"],
        ["Сайт 3", "http://site3.com"],
        ["Сайт 3", "http://site3.com"],
        ["Сайт 3", "http://site3.com"],
        ["Сайт 3", "http://site3.com"],
        ["Сайт 3", "http://site3.com"],
        ["Сайт 3", "http://site3.com"],
        ["Сайт 3", "http://site3.com"],
        ["Сайт 3", "http://site3.com"],
        ["Сайт 3", "http://site3.com"],
        ["Сайт 3", "http://site3.com"],
        // Добавьте другие строки данных, если необходимо
    ];

    // Создание элемента div с классом "scroll-table"
    var scrollTableDiv = document.createElement("div");
    scrollTableDiv.className = "scroll-table";

    // Создание элемента table
    var table = document.createElement("table");

    // Создание элемента thead
    var thead = document.createElement("thead");

    // Создание строки заголовка (thead)
    var headerRow = document.createElement("tr");

    // Заголовки столбцов
    var headers = ["Сайт", "URL"];

    // Добавление заголовков в строку заголовка
    headers.forEach(function(headerText) {
        var th = document.createElement("th");
        th.textContent = headerText;
        headerRow.appendChild(th);
    });

    // Добавление строки заголовка в thead
    thead.appendChild(headerRow);

    // Добавление thead в таблицу
    table.appendChild(thead);

    // Создание элемента tbody
    var tbody = document.createElement("tbody");

    // Создание строк и ячеек для тела таблицы
    Arr.forEach(function(rowData) {
        var row = document.createElement("tr");

        rowData.forEach(function(cellData, index) {
            var td = document.createElement("td");
            if (index === 1) {
                // Если это второй столбец, создаем ссылку
                var link = document.createElement("a");
                link.href = cellData;
                link.textContent = cellData;
                td.appendChild(link);
            } else {
                td.textContent = cellData;
            }
            row.appendChild(td);
        });

        tbody.appendChild(row);
    });

    // Добавление tbody в таблицу
    table.appendChild(tbody);

    // Добавление таблицы в div с классом "scroll-table"
    scrollTableDiv.appendChild(table);

    // Получение контейнера по id "container"
    var container = document.getElementById("container2");

    // Добавление div с классом "scroll-table" в контейнер
    container.appendChild(scrollTableDiv);
}