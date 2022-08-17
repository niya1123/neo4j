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
        selector: 'node[type="c"]',
        style: {
          'shape': 'triangle',
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

    cy2.on('mouseover', 'node', function(event){
      let data = this.data('ele');
      this.qtip({
          content: data,
          show: {
              event: event.type,
              ready: true
          },
          hide: {
              event: 'mouseout unfocus'
          },
          style: {
            classes: 'qtip-bootstrap',
          }
      }, event);
    });
  });

document.querySelector('#answer_r').addEventListener('click', function() {
  cy2.on('taphold', 'node', function(evt){
    const sub_score = score_subject[this.data('ele').slice(3)]
    if(0 <= sub_score && sub_score < 25){
      this.style('background-color', 'green');
    }else if(sub_score >= 25 &&  sub_score < 50){
      this.style('background-color', 'gold');
    }else if(sub_score >= 50 &&  sub_score < 75){
      this.style('background-color', 'orange');
    }else if(sub_score >= 75 &&  sub_score <= 100){
      this.style('background-color', 'red');
    }else{
      this.style('background-color', 'gray');
    }
    this.lock();
    if(!alert(this.data('ele')+"\n"+sub_score+"点")){
      setTimeout(unlock(this), 5000);
    }

    function unlock(obj) {
      obj.unlock();
    }
    
  });
});