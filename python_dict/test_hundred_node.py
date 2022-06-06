from python_dict.create_node_and_relationship import App

scheme = "neo4j"
host_name = "neo4j"
port = 7687
url = "{scheme}://{host_name}:{port}".format(scheme=scheme, host_name=host_name, port=port)
user = "neo4j"
password = "test"
app = App(url, user, password)
for i in range(250):
    app.create_Node(node_name=str(i))
    app.create_Node(node_name=str(i*2))
    app.create_relationship(str(i), str(i*2), "a")
app.close()