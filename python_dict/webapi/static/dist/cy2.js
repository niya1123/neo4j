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
    let nodes2 = cy2.filter('node');
    for (let index = 0; index < nodes2.length; index++) {
      const sub_score = score_subject[nodes2[index].data('ele').slice(3)]
      if(0 <= sub_score && sub_score < 25){
        nodes2[index].style('background-color', 'red');
      }else if(sub_score >= 25 &&  sub_score < 50){
        nodes2[index].style('background-color', 'orange');
      }else if(sub_score >= 50 &&  sub_score < 75){
        nodes2[index].style('background-color', 'gold');
      }else if(sub_score >= 75 &&  sub_score <= 100){
        nodes2[index].style('background-color', 'green');
      }else{
        nodes2[index].style('background-color', 'gray');
      }
    };
    
    cy2.on('mouseover', 'node', function(event){
      let data = this.data('ele').slice(3)+"\n"+score_subject[this.data('ele').slice(3)]+"点";
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
    
    let ins2 = [];
    for (let index = 0; index < nodes2.length; index++) {
      const sub_score = score_subject[nodes2[index].data('ele').slice(3)]
      ins2.push(makeTippy(nodes2[index], nodes2[index].data('ele').slice(3)+"\n"+sub_score+"点"));
    }

    for (let index = 0; index < ins2.length; index++) {
      ins2[index].show();
    }
    jQuery('#click').on('click', ".hyouji", function() {
      if (this.value === "ON") {
          jQuery('input').addClass("clicked");
          jQuery('.hyouji').replaceWith('<input type="button" class="hyouji btn_center" value="OFF" style="font-size: 1em;color: #D30E1B;">');
          for (let index = 0; index < ins2.length; index++) {
            ins2[index].show();
          }
      } else {
          jQuery('input').removeClass('clicked');
          jQuery('.hyouji').replaceWith('<input type="button" class="hyouji btn_cente" value="ON" style="font-size: 1em;color: #028760;">');
          for (let index = 0; index < ins2.length; index++) {
            ins2[index].hide();
          }
      }
    });
   
  });