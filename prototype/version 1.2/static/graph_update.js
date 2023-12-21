const Centrality_types={
    DEGREE:"degree",
    ClOSENESS:"closeness",
    BETWEENNESS:"betweenness"
}

class Graph_transformer{
    static _path_mode = false;
    static _path_mode_need_clean = false;

    static update_graph_data(){
       let input_val = document.getElementById('input').value;
        fetch("/",{
            method:'POST',
            body: input_val
        }).then(res=>{
        Graph.update_data();
        });
    }

    /*callback-функция, имеющая один параметр-data. Когда пользователь выберет две точки для пути, будет послан запрос на сервер.
    Сервер вернет путь в виде массива id вершин(включая стартовую и финишную).Пример:[200,215,467,1978] или[]( если пути нет) 
    Именно ответ сервера(т.е. список id вешрин) будет передан в качестве агрумента функции callback
    */ 
    static find_path_mode(callback=null){
        Graph_transformer._path_mode = true;
        let id=[];
        Graph.graph.autoPauseRedraw(false);
        Graph.graph.nodeColor("color");
        Graph.graph.linkWidth((link)=>{
            if(link.width){
                return link.width;

            }
            return Graph.link_width;

        });
        Graph.graph.onNodeClick((node)=>{
            if(Graph_transformer._path_mode_need_clean){
                Graph.clear_color_and_width_prop(true);
                Graph_transformer._path_mode_need_clean = false;
            }
            node.color = "#FF0000";
            if(!id[0] || id[0] !=node.id){
                id.push(node.id);
            }
            if(id.length==2){
                Graph_transformer.find_path_algortithm(id[0],id[1],callback);
                id = [];
            }
        })
    }

    //возврат графа в исходное состояние
    static to_inital_state(){
        if(Graph_transformer._path_mode){
            Graph.graph.autoPauseRedraw(true);
            Graph_transformer._path_mode=false;
        }
        Graph.inital_state();
    }

    static find_path_algortithm(start_id,finish_id,callback){
        let promise = fetch(`/algorithms/find_path?start_id=${start_id}&finish_id=${finish_id}`);
        promise.then(resp=>resp.json()).then(((ans)=>{
            Graph_transformer._process_find_path(ans)
            if(callback){
            callback(ans);
            }
        }));
    }

    static _process_find_path(data){
        if(data.length==0){
            Graph.clear_color_and_width_prop();
            return;
        }
        Graph.color_path(data,"#FFFF00");
        Graph_transformer._path_mode_need_clean = true;
    }


    /*callback-функция, имеющая один параметр-data. В эту функцию при ее вызове будет передан ответ сервера на запрос
    получения сильных компонент связности.Этот ответ будет иметь следующий вид: {235:0, 236:0, 237:1, 238:4, 239:0 }
    т.е. это будет объект ключи которого -id вершин, а значения этих ключей- номер компоненты сильной связности,которой эта
    вершина принадлежит.  */
    static  strongly_connected_algorithm(callback=null){
        let data= fetch('/algorithms/strongly_connected_components');
        data.then(response => response.json()).then((ans) => {
            Graph_transformer._process_strongly_connected(ans);
            if(callback){
            callback(ans);
            }
        })
    }

    static _process_strongly_connected(data){
        let color_func = function(node){
            let component_id = data[node.id] 
            if(!component_id){ //!!!!!!!!!!!!!!!!!!!
                return "#008080"
            }
        return Graph.color_palette[(component_id*43)%Graph.color_palette.length].hexString
        }

        Graph.graph.linkWidth((link)=>{
            if(link.width){
                return link.width;

            }
            return Graph.link_width;

        });
        for(let link of Graph.graph.graphData().links){
            let source_id = link.source.id
            let target_id = link.target.id
            if(data[source_id] == data[target_id]){
                link.color = Graph.color_palette[(data[source_id]*43)%Graph.color_palette.length].hexString
                link.width = 0.3
            }
        }
        Graph.graph.nodeColor(color_func);
    }

/*callback-функция, имеющая один параметр-data. В эту функцию при ее вызове будет передан ответ сервера на запрос
    получения page rank(этот показатель рассчитывается для каждой вершины).
    Этот ответ будет иметь следующий вид: {235:0.153, 236:0.458, 237:0.786, 238:0.12, 239:0.141 }
    т.е. это будет объект ключи которого -id вершин, а значения этих ключей- значение page_rank для вершины с этим id.  */
    static page_rank_algorithm(callback=null){
        let res = {}
        let promise = fetch("/algorithms/page_rank")
        promise.then(resp=> resp.json()).then((ans)=>{
            res = Graph_transformer._process_page_rank(ans);
            if(callback){
            callback(ans);
            }
            return res; 
        })

    }

    static _process_page_rank(data){
        let sizes = Graph_transformer._calculate_sizes(data,5, 0.1,1,300)
        Graph.init_values(sizes);
        Graph.reheat();

    }

    static _calculate_sizes(data,max_size,min_size,default_size,sensitivity){
        let mean_square = 0;
        let data_map  = new Map(Object.entries(data));
        let scores = Array.from(data_map.values());
        for(let score of scores){
            mean_square += Math.pow(score,2)
        }
        mean_square = Math.pow(mean_square/scores.length, 0.5)
        let percent_scores = scores.map((x)=> (x/mean_square)*100)
        let ids = Array.from(data_map.keys())
        for(let i=0; i<ids.length;i++){
            let percent = percent_scores[i]
            data_map.set(ids[i],Graph_transformer._calculate_one_size(percent,max_size,min_size,default_size,sensitivity));
        }
        return data_map;
    }

    static _calculate_one_size(percent,max_size, min_size,default_size,sensitivity=1){
        let deviation = (sensitivity*(percent-100))/100;
        let expected_size = default_size + default_size*deviation;
        if(expected_size < min_size){
        expected_size = min_size;
        }
        if(expected_size > max_size){
            expected_size = max_size;
        }
        return expected_size;
    }

    /*callback-функция, имеющая один параметр-data. В эту функцию при ее вызове будет передан ответ сервера на запрос
    получения центральности(этот показатель рассчитывается для каждой вершины.Всего еть 3 ее вида: по степени,
        по посредничеству и по близости).
    Этот ответ будет иметь следующий вид: {235:1.78, 236:0, 237:2.45, 238:14.78, 239:0.141 }
    т.е. это будет объект ключи которого -id вершин, а значения этих ключей- величина выбранной центральности(зависит от type)
    для вершины с этим id  */
    static centrality_algorithm(type,callback=null){
        let res= {};
        let promise = fetch(`/algorithms/centrality?type=${type}`)
        promise.then(resp=>resp.json()).then((ans)=>{
            res = Graph_transformer._process_centrality(ans);
            if(callback){
            callback(ans);
            }
            return res; 
        })
    }

    static _process_centrality(data){
        let sizes = Graph_transformer._calculate_sizes(data,10, 0.1,1,10)
        Graph.init_values(sizes);
        Graph.reheat();
    }
}

class Graph{
    static graph = ForceGraph()
    static color_palette =null;
    static id_map = new Map();
    static link_width =0.2

    static{
        Graph.graph(document.getElementById('container')).graphData({"nodes":[],"links":[]})
      .nodeId('id')
      .nodeLabel('domain')
      .linkSource('source')
      .linkTarget('target')
      .linkDirectionalArrowLength(2)
      .linkWidth(Graph.link_width)
      .onNodeClick(node=>{
        window.open(node.url,'_blank')
      })

      fetch('/static/colors.json').then(resp => resp.json()).then((colors)=>{Graph.color_palette=colors});
      Graph.color_by_gropus();
      Graph.graph.width(document.getElementById('container').offsetWidth);
      Graph.graph.height(document.getElementById('container').offsetHeight);
    }

    static update_data(){
        fetch("/graph_data").then(res => res.json()).then(input =>{
        Graph.graph.graphData(input);
        Graph._init_id_map();
        })
    }

    static _init_id_map(){
        let nodes = Graph.graph.graphData().nodes;
        for(let i=0; i<nodes.length;i++){
            Graph.id_map.set(nodes[i].id,i);
        }
        let links = Graph.graph.graphData().links;
        for(let i=0; i<links.length;i++){
           let key = `${links[i].source}_${links[i].target}`
            Graph.id_map.set(key,i);
        }
    }

    static inital_state(){
        for(let node of Graph.graph.graphData().nodes){
            node.val = 1;
        }
        Graph.clear_color_and_width_prop(true)
        Graph.color_by_gropus();
        Graph.reheat();
        Graph.graph.linkWidth(Graph.link_width);
        Graph.graph.onNodeClick(node=>{
        window.open(node.url,'_blank')});
    }

    static init_values(values_map){
        for(let node of Graph.graph.graphData().nodes){
            let size = values_map.get(node.id.toString())
            if(!size){ ///!!!!!!!
                size = 2
            }
            node.val = size;
          }
    }

    static color_by_gropus(){
        Graph.graph.nodeColor((node)=>{
            return Graph.color_palette[(node.group*31+34)%Graph.color_palette.length].hexString;
        });
    }

    static color_path(ids, color){
        let nodes = Graph.graph.graphData().nodes;
        let links = Graph.graph.graphData().links;
        for(let i=0; i<ids.length;i++){
            let node_index = Graph.id_map.get(ids[i]);
            nodes[node_index].color = color;
            if(i==0){
                continue;
            }
            let prev_index =Graph.id_map.get(ids[i-1]);
            let link_key = `${nodes[prev_index].id}_${nodes[node_index].id}`
            let link_index = Graph.id_map.get(link_key);
            links[link_index].color = color;
            links[link_index].width = 2;
        }
    }

    static clear_color_and_width_prop(clear_links = false){ //медленно?
        for(let node of Graph.graph.graphData().nodes){
            if(node.color){
                delete node.color;
            }
        }
        if(!clear_links){
            return;
        }
        for(let link of Graph.graph.graphData().links){
            if(link.color){
                delete link.color;
            }
            if(link.width){
                delete link.width;
            }
        }
    }

    static reheat(){
        Graph.graph.d3Force('collide',null);
        Graph.graph.d3Force('collide', d3.forceCollide((d)=>{
            let res= Math.ceil(d.val);
            return res*2;  }))
        Graph.graph.d3ReheatSimulation()
    }

    //получение объекта {domain:<значение>, url:<значение>} по id узла
    static get_node_info(node_id){
        let nodes = Graph.graph.graphData().nodes;
        let node = nodes[Graph.id_map.get(node_id)];
        return {domain:node.domain, url:node_url};
    }

    //получение списка с информацией обо всех узлах
    static get_all_nodes_info(){
        let nodes = Graph.graph.graphData.nodes;
        let result = [];
        for(let node of nodes){
            result.push({domain:node.domain, url:node.url});
        }
        return result;
    }

}

function load_links(){
   Graph_transformer.update_graph_data();
}
