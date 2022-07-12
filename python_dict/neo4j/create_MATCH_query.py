from string import Template

class CreateMATCHQuery:
    def __init__(self, driver):
        """
        コンストラクタ. GraphDatabaseのdriverを受け取りdriverを作成する. 
        """
        self.driver = driver

    def close(self):
        """
        driverを閉じる. 
        """
        self.driver.close()

    def run_MATCH_query(self, **kwargs):
        """
        MATCHクエリの実行. 
        """
        with self.driver.session() as session:
            session.write_transaction(self._create_MATCH_query, **kwargs)
    
    def run_MATCH_score_query(self, **kwargs):
        with self.driver.session() as session:
            session.write_transaction(self._create_MATCH_score_query, **kwargs)

    @staticmethod
    def _create_MATCH_query(**kwargs) -> str:
        """
        MATCHクエリの作成
        """
        query = ""
        len_kwargs = len(kwargs)
        if len_kwargs == 0:
            query = "MATCH (n)-[rel]->(a) RETURN n, rel, a"
        elif len_kwargs == 1:
            query = Template(
                "MATCH (n) WHERE n.name = '${node_name}' "
                "RETURN n"
                ).substitute(node_name=kwargs["node_name"])
        elif len_kwargs == 2:
            try:
                type = kwargs["type"]
                query = Template(
                    "MATCH (n: ${type}) WHERE n.name = '${node_name}' RETURN n"
                ).substitute(node_name=kwargs["node_name"], type=type)
            except KeyError:
                query = Template(
                    "MATCH (n1),(n2) WHERE n1.name = '${node1_name}' AND n2.name = '${node2_name}' "
                ).substitute(node1_name=kwargs["node1_name"], node2_name=kwargs["node2_name"])
        elif len_kwargs == 3:
            query = Template(
                "MATCH (n1)-[rel]->(n2) WHERE n1.name = '${node1_name}' AND n2.name = '${node2_name}' RETURN n1,rel,n2"
            ).substitute(node1_name=kwargs["node1_name"], node2_name=kwargs["node2_name"], relationship=kwargs["relationship"])
        return query

    @staticmethod
    def _create_MATCH_score_query() -> str:
        return "MATCH (n)-[:score]->(m) RETURN n,m"

    @staticmethod
    def _create_MATCH_userscore_query(username) -> str:
        return "MATCH (n)-[rel:score]->(m) WHERE n.name = '" + username +"'RETURN rel.score, m.name"

    @staticmethod
    def _create_MATCH_subject_query(subject) -> str:
        return "MATCH (n)-[rel:have]->(m) WHERE n.name = '" + subject +"'RETURN n,rel,m"