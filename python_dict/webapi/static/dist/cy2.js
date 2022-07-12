document.querySelector('#answer').addEventListener('click', function() {
    $('#cy2').show();
    var cy2 = window.cy2 = cytoscape({
    container: document.getElementById('cy2'),

    layout: {
      name: 'grid',
      rows: 8,
      cols: 8
    },

    style: [
      {
        selector: 'node[name]',
        style: {
          'content': 'data(name)'
        }
      },

      {
        selector: 'edge',
        style: {
          'curve-style': 'bezier',
          'target-arrow-shape': 'triangle'
        }
      },

    ],

    

    elements: elements
  });
  });