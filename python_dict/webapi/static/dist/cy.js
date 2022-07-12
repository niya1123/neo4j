var data_json;
      let parent;
      let children;
      let relationship;
      $.ajax({
          url: '/get/all_graphs',
          type: 'GET',
          dataType: 'json',
          async: false,
      })
      .done(function (data) {
          const data_stringify = JSON.stringify(data);
          data_json = JSON.parse(data_stringify);
          parent = data_json['parent'];
          children = data_json['children'];
          relationship = data_json['relationship'];
      })
      .fail(function (data) {
          console.log('error');
      });
      let elements_node_list = [];
      let elements_edge_list = [];
      let elements = [];

      $.each(relationship,function(index,r){
          elements_node_list.push({data: {id: 'p'+ parent[index], ele: '親: '+ parent[index]}});
          elements_node_list.push({data: {id: 'c' + children[index], ele: '子: ' + children[index]}});
          elements_edge_list.push({data: {id: 'r'+index, source: 'p'+ parent[index], target: 'c' + children[index], relationship: r}});
          elements.push({data: {id: 'p'+ parent[index], ele: '親: '+ parent[index]}});
          elements.push({data: {id: 'c' + children[index], ele: '子: ' + children[index]}});
          elements.push({data: {id: 'r'+index, source: 'p'+ parent[index], target: 'c' + children[index], relationship: r}});
      });
      
      document.addEventListener('DOMContentLoaded', function(){

        var cy = window.cy = cytoscape({
          container: document.getElementById('cy'),

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

            // some style for the extension

            {
              selector: '.eh-handle',
              style: {
                'background-color': 'red',
                'width': 12,
                'height': 12,
                'shape': 'ellipse',
                'overlay-opacity': 0,
                'border-width': 12, // makes the handle easier to hit
                'border-opacity': 0
              }
            },

            {
              selector: '.eh-hover',
              style: {
                'background-color': 'red'
              }
            },

            {
              selector: '.eh-source',
              style: {
                'border-width': 2,
                'border-color': 'red'
              }
            },

            {
              selector: '.eh-target',
              style: {
                'border-width': 2,
                'border-color': 'red'
              }
            },

            {
              selector: '.eh-preview, .eh-ghost-edge',
              style: {
                'background-color': 'red',
                'line-color': 'red',
                'target-arrow-color': 'red',
                'source-arrow-color': 'red'
              }
            },

            {
              selector: '.eh-ghost-edge.eh-preview-active',
              style: {
                'opacity': 0
              }
            }
          ],

          elements: elements_node_list
        });
        cy.on('dbltap', 'node', function(evt){
          alert(this.data('ele'));
          console.log( 'clicked ' + this.id() + ' ' + this.data('ele'));
        });
        let count = 0;
        cy.on('taphold', 'node', function(evt){
          switch (count) {
            case 0:
              this.style('background-color', 'green');
              count++;
              break;
            case 1:
              this.style('background-color', 'gold');
              count++;
            break;
            case 2:
              this.style('background-color', 'orange');
              count++;
            break;
            case 3:
              this.style('background-color', 'red');
              count=0;
            break;
            default:
              break;
          }
        });
        cy.on('tap', 'edge', function(evt){
            console.log( 'clicked ' + this.id() );
            this.remove();
        });

        var eh = cy.edgehandles();

        var popperEnabled = false;

        document.querySelector('#popper').addEventListener('click', function() {
          if (popperEnabled) { return; }

          popperEnabled = true;

          // example code for making your own handles -- customise events and presentation where fitting
          // var popper;
          var popperNode;
          var popper;
          var popperDiv;
          var started = false;
          
          function start() {
            eh.start(popperNode);
          }

          function stop() {
            eh.stop();
          }

          function setHandleOn(node) {
            if (started) { return; }

            removeHandle(); // rm old handle

            popperNode = node;

            popperDiv = document.createElement('div');
            popperDiv.classList.add('popper-handle');
            popperDiv.addEventListener('mousedown', start);
            document.body.appendChild(popperDiv);

            popper = node.popper({
              content: popperDiv,
              popper: {
                placement: 'top',
                modifiers: [
                  {
                    name: 'offset',
                    options: {
                      offset: [0, -10],
                    },
                  },
                ]
              }
            });
          }
        

          function removeHandle() {
            if (popper){
              popper.destroy();
              popper = null;
            }

            if (popperDiv) {
              document.body.removeChild(popperDiv);
              popperDiv = null;
            }

            popperNode = null;
          }

          cy.on('mouseover', 'node', function(e) {
            setHandleOn(e.target);
          });

          cy.on('grab', 'node', function(){
            removeHandle();
          });

          cy.on('tap', function(e){
            if (e.target === cy) {
              removeHandle();
            }
          });

          cy.on('zoom pan', function(){
            removeHandle();
          });

          window.addEventListener('mouseup', function(e){
            stop();
          });

          cy.on('ehstart', function(){
            started = true;
          });

          cy.on('ehstop', function(){
            started = false;
          });

        });

      });