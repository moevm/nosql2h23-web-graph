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
            
            var data =
                [{domain: "github.com", url: "wikipedia.org/some_page"},
                {domain: "wikipedia",url: "wikipedia.org/some_page"}];
            createTable(data);
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
    window.location.href = "/page-rank";
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

function getStrong(){
    window.location.href = "/strong-component";
}


function createTable(data) {

    var scrollTableDiv = document.createElement("div");
    scrollTableDiv.className = "scroll-table";

    var table = document.createElement("table");
    var thead = document.createElement("thead");
    var headerRow = document.createElement("tr");

    // Заголовки столбцов
    var headers = ["Домен", "URL"];

    headers.forEach(function(headerText, index) {
        var th = document.createElement("th");
        th.textContent = headerText;

        // Установка ширины столбцов
        if (index === 0) {
            th.style.width = "30%";
        } else if (index === 1) {
            th.style.width = "70%";
        }

        headerRow.appendChild(th);
    });

    thead.appendChild(headerRow);
    table.appendChild(thead);

    var tbody = document.createElement("tbody");

    data.forEach(function(rowData) {
        var row = document.createElement("tr");

        Object.values(rowData).forEach(function(cellData, index) {
            var td = document.createElement("td");
            if (index === 0) { // Домен
                td.textContent = cellData;
            } else if (index === 1) { // URL
                var link = document.createElement("a");
                link.href = cellData;
                link.textContent = cellData;
                td.appendChild(link);
            }
            row.appendChild(td);
        });

        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    scrollTableDiv.appendChild(table);

    var container = document.getElementById("container2");
    container.appendChild(scrollTableDiv);
}