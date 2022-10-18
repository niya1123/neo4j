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
    let nodes = cy2.nodes();
    let ins = [];
    nodes.forEach(element => {
      const sub_score = score_subject[element.data('ele').slice(3)];
      if(0 <= sub_score && sub_score < 25){
        element.style('background-color', 'red');
      }else if(sub_score >= 25 &&  sub_score < 50){
        element.style('background-color', 'orange');
      }else if(sub_score >= 50 &&  sub_score < 75){
        element.style('background-color', 'gold');
      }else if(sub_score >= 75 &&  sub_score <= 100){
        element.style('background-color', 'green');
      }else{
        element.style('background-color', 'gray');
      }
    });

    var makeTippy = function(ele, text){
      var ref = ele.popperRef();

      // Since tippy constructor requires DOM element/elements, create a placeholder
      var dummyDomEle = document.createElement('div');

      var tip = tippy( dummyDomEle, {
        getReferenceClientRect: ref.getBoundingClientRect,
        trigger: 'manual', // mandatory
        // dom element inside the tippy:
        content: function(){ // function can be better for performance
          var div = document.createElement('div');

          div.innerHTML = text;

          return div;
        },
        // your own preferences:
        arrow: true,
        placement: 'bottom',
        hideOnClick: false,
        sticky: "reference",
        theme: 'white',

        // if interactive:
        interactive: true,
        appendTo: document.body // or append dummyDomEle to document.body
      } );

      return tip;
    };

    for (let index = 0; index < nodes.length; index++) {
      let text = nodes[index].data('ele').slice(3)+ " " + score_subject[nodes[index].data('ele').slice(3)] + "点";
      console.log(text);
      ins.push(makeTippy(nodes[index], text));
    }

    for (let index = 0; index < ins.length; index++) {
      ins[index].show();
    }

    jQuery('#click').on('click', ".hyouji", function() {
      if (this.value === "ON") {
          jQuery('input').addClass("clicked");
          jQuery('.hyouji').replaceWith('<input type="button" class="hyouji btn_center" value="OFF" style="font-size: 1em;color: #D30E1B;">');
          for (let index = 0; index < ins.length; index++) {
            ins[index].show();
          }
      } else {
          jQuery('input').removeClass('clicked');
          jQuery('.hyouji').replaceWith('<input type="button" class="hyouji btn_cente" value="ON" style="font-size: 1em;color: #028760;">');
          for (let index = 0; index < ins.length; index++) {
            ins[index].hide();
          }
      }
  });
  });

// document.querySelector('#answer_r').addEventListener('click', function() {
//   cy2.on('taphold', 'node', function(evt){
//     const sub_score = score_subject[this.data('ele').slice(3)]
//     if(0 <= sub_score && sub_score < 25){
//       this.style('background-color', 'green');
//     }else if(sub_score >= 25 &&  sub_score < 50){
//       this.style('background-color', 'gold');
//     }else if(sub_score >= 50 &&  sub_score < 75){
//       this.style('background-color', 'orange');
//     }else if(sub_score >= 75 &&  sub_score <= 100){
//       this.style('background-color', 'red');
//     }else{
//       this.style('background-color', 'gray');
//     }
//     this.lock();
//     if(!alert(this.data('ele')+"\n"+sub_score+"点")){
//       setTimeout(unlock(this), 5000);
//     }

//     function unlock(obj) {
//       obj.unlock();
//     }
    
//   });
// });