

class Graph{

    static graph = ForceGraph()

    static{
        Graph.graph(document.getElementById('container')).graphData({"nodes":[],"links":[]})
      .nodeId('id')
      .nodeLabel('domain')
      .linkSource('source')
      .linkTarget('target')
      .nodeAutoColorBy('group')
      .onNodeClick(node=>{
        window.open(node.url,'_blank')
      })

      Graph.graph.width(document.getElementById('container').offsetWidth);
      Graph.graph.height(document.getElementById('container').offsetHeight);
    }

    static update_data(){
        fetch("/graph_data").then(res => res.json()).then(input =>{
        Graph.graph.graphData(input)
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
    Graph.update_data();
    })
}
