// initialize global variables.
var edges;
var nodes;
var network;
var container;
var options, data;


// This method is responsible for drawing the graph, returns the drawn network
function drawGraph() {
    var container = document.getElementById("{{wave_name}}");

    {% if use_DOT %}

    var DOTstring = "{{dot_lang|safe}}";
    var parsedData = vis.network.convertDot(DOTstring);

    data = {
      nodes: parsedData.nodes,
      edges: parsedData.edges
    }

    var options = parsedData.options;
    options.nodes = {
        shape: "dot"
    }

    {% else %}

    // parsing and collecting nodes and edges from the python
    nodes = new vis.DataSet({{nodes|tojson}});
    edges = new vis.DataSet({{edges|tojson}});

    // adding nodes and edges to the graph
    data = {nodes: nodes, edges: edges};

    var options = {{options|safe}};

    options.manipulation['addNode'] = function (data, callback) {
        params = {}
        params.event = "add__node"
        data.label = ""
        params.data = data
        wave.emit("{{wave_name}}", 'params', params);
        callback(data);
    };

    options.manipulation['deleteNode'] = function (data, callback) {
        params = {}
        params.event = "delete__node"
        params.data = data
        wave.emit("{{wave_name}}", 'params', params);
        callback(data);
    };  // Deleting a node will delete all edges that connected it (see inside params)

    options.manipulation['addEdge'] = function (data, callback) {
        params = {}
        params.event = "add__edge"
        params.data = data
        wave.emit("{{wave_name}}", 'params', params);
        callback(data);
    };

    options.manipulation['deleteEdge'] = function (data, callback) {
        params = {}
        params.event = "delete__edge"
        params.data = data
        wave.emit("{{wave_name}}", 'params', params);
        callback(data);
    };


    options.manipulation['editEdge'] = function (data, callback) {
        params = {}
        params.event = "edit__edge"
        params.data = data
        wave.emit("{{wave_name}}", 'params', params);
        callback(data);
    };

    options.manipulation['editNode'] = function (data, callback) {
        params = {}
        params.event = "edit__node"
        params.data = data
        wave.emit("{{wave_name}}", 'params', params);
        callback(data);
    };



    {% endif %}

    {% if conf %}
    // if this network requires displaying the configure window,
    // put it in its div
    options.configure["container"] = document.getElementById("config");
    {% endif %}

    network = new vis.Network(container, data, options);

    {% if tooltip_link %}
    // make a custom popup
    var popup = document.createElement("div");
    popup.className = 'popup';
    popupTimeout = null;
    popup.addEventListener('mouseover', function () {
        console.log(popup)
        if (popupTimeout !== null) {
            clearTimeout(popupTimeout);
            popupTimeout = null;
        }
    });
    popup.addEventListener('mouseout', function () {
        if (popupTimeout === null) {
            hidePopup();
        }
    });
    container.appendChild(popup);


    // use the popup event to show
    network.on("showPopup", function (params) {
        showPopup(params);
    });

    // use the hide event to hide it
    network.on("hidePopup", function (params) {
        hidePopup();
    });


    // hiding the popup through css
    function hidePopup() {
        popupTimeout = setTimeout(function () { popup.style.display = 'none'; }, 500);
    }

    // showing the popup
    function showPopup(nodeId) {
        // get the data from the vis.DataSet
        var nodeData = nodes.get([nodeId]);
        popup.innerHTML = nodeData[0].title;

        // get the position of the node
        var posCanvas = network.getPositions([nodeId])[nodeId];

        // get the bounding box of the node
        var boundingBox = network.getBoundingBox(nodeId);

        //position tooltip:
        posCanvas.x = posCanvas.x + 0.5 * (boundingBox.right - boundingBox.left);

        // convert coordinates to the DOM space
        var posDOM = network.canvasToDOM(posCanvas);

        // Give it an offset
        posDOM.x += 10;
        posDOM.y -= 20;

        // show and place the tooltip.
        popup.style.display = 'block';
        popup.style.top = posDOM.y + 'px';
        popup.style.left = posDOM.x + 'px';
    }
    {% endif %}

    // Add wave emit instructions
    // Click -> click__node or click__edge
    network.on("click", function (params) {
        if (params.nodes.length >= 1) {
            params.event = 'click__node';
        } else if (params.edges.length >= 1) {
            params.event = 'click__edge';
        } else {
            params.event = 'click__nothing';
        }

        if (params.event != 'click__nothing') {
            wave.emit("{{wave_name}}", 'params', params);
        }
    });
    // Double click -> double_click__node or double_click__edge
    network.on("doubleClick", function (params) {
        if (params.nodes.length >= 1) {
            params.event = 'double_click__node';
        } else if (params.edges.length >= 1) {
            params.event = 'double_click__edge';
        } else {
            params.event = 'double_click__nothing';
        }
        if (params.event != 'double_click__nothing') {
            wave.emit("{{wave_name}}", 'params', params);
        }
    });

    // Zoom in or out ->
    network.on("zoom", function (params) {
        if (params.direction == '+') {
            params.event = 'zoom__in';
        } else {
            params.event = 'zoom__out';
        }
        wave.emit("{{wave_name}}", 'params', params);
    });

    if (options.interaction['hover_callback']) {
        // Hover node
        network.on("hoverNode", function (params) {
            params.event = 'hover__node';
            wave.emit("{{wave_name}}", 'params', params);
        });

        // Hover edge
        network.on("hoverEdge", function (params) {
            params.event = 'hover__edge';
            wave.emit("{{wave_name}}", 'params', params);
        });
    }

    return network;

}

drawGraph();
