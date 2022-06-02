from make_node_and_relationship import App

scheme = "neo4j"
host_name = "neo4j"
port = 7687
url = "{scheme}://{host_name}:{port}".format(scheme=scheme, host_name=host_name, port=port)
user = "neo4j"
password = "test"
app = App(url, user, password)
app.create_Node(node_name="シンジ", type="パイロット")
app.create_Node(node_name="アスカ", type="パイロット")
app.create_Node(node_name="カオル", type="ゼーレ")
app.create_Node(node_name="アヤナミ", type="クローン人間")
app.create_relationship("シンジ", "アスカ", "大切な仲間")
app.create_relationship("アスカ", "シンジ", "昔好きだった")
app.create_relationship("シンジ", "アヤナミ", "好き")
app.create_relationship("アヤナミ", "シンジ", "好き")
app.create_relationship("シンジ", "カオル", "親友")
app.create_relationship("カオル", "シンジ", "親友")
app.create_relationship("アスカ", "カオル", "知り合い")
app.create_relationship("カオル", "アスカ", "知り合い")
app.create_relationship("アヤナミ", "カオル", "知り合い")
app.create_relationship("カオル", "アヤナミ", "知り合い")