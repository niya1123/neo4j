from neo4j import GraphDatabase

uri = "neo4j://neo4j:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "test"))

def create_friend_of(tx, name, friend):
    tx.run("MATCH (a:Person) WHERE a.name = $name "
           "CREATE (a)-[:KNOWS]->(:Person {name: $friend})",
           name=name, friend=friend)

with driver.session() as session:
    session.write_transaction(create_friend_of, "Alice", "Bob")

with driver.session() as session:
    session.write_transaction(create_friend_of, "Alice", "Carl")

driver.close()