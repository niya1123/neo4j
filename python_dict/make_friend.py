import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_person(self, person1_name, person2_name):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            session.write_transaction(self._return_person, person1_name, person2_name)

    def create_friendship(self, person1_name, person2_name):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            session.write_transaction(self._return_friendship, person1_name, person2_name)
          

    @staticmethod
    def _return_person(tx, person1_name, person2_name):

        # To learn more about the Cypher syntax,
        # see https://neo4j.com/docs/cypher-manual/current/

        # The Reference Card is also a good resource for keywords,
        # see https://neo4j.com/docs/cypher-refcard/current/
        query_p1 = (
                "MATCH (p1:Person) WHERE p1.name = $person1_name "
                "RETURN p1"
            )
        query_p2 = (
            "MATCH (p2:Person) WHERE p2.name = $person2_name "
            "RETURN p2"
        )
        result_p1 = tx.run(query_p1, person1_name=person1_name)
        result_p2 = tx.run(query_p2, person2_name=person2_name)
        if result_p1.single() is None:
            query = (
                "CREATE (p1:Person { name: $person1_name }) "
            )
            tx.run(query, person1_name=person1_name)
        if result_p2.single() is None:
            query = (
                "CREATE (p2:Person { name: $person2_name }) "
            )
            tx.run(query, person2_name=person2_name)

    @staticmethod
    def _return_friendship(tx, person1_name, person2_name):

        # To learn more about the Cypher syntax,
        # see https://neo4j.com/docs/cypher-manual/current/

        # The Reference Card is also a good resource for keywords,
        # see https://neo4j.com/docs/cypher-refcard/current/
        query = (
                "MATCH (p1:Person),(p2:Person) WHERE p1.name = $person1_name AND p2.name = $person2_name "
                "CREATE (p1)-[:KNOWS]->(p2) "
                "RETURN p1, p2"
            )
        tx.run(query, person1_name=person1_name, person2_name=person2_name)

if __name__ == "__main__":
    # See https://neo4j.com/developer/aura-connect-driver/ for Aura specific connection URL.
    scheme = "neo4j"  # Connecting to Aura, use the "neo4j+s" URI scheme
    host_name = "neo4j"
    port = 7687
    url = "{scheme}://{host_name}:{port}".format(scheme=scheme, host_name=host_name, port=port)
    user = "neo4j"
    password = "test"
    app = App(url, user, password)
    app.create_person("アスカ", "シンジ")
    app.create_friendship("アスカ", "シンジ")
    app.close()