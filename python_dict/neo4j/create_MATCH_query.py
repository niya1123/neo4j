from string import Template

from connection_neo4j import ConnectNeo4j as cn
from neo4j import GraphDatabase

class CreateMATCHQuery:
    def __init__(self):
        """
        コンストラクタ. GraphDatabaseのdriverの生成を行う. 
        """
        self.cn = cn()
        self.driver = self.cn.driver

    def close(self):
        """
        driverを閉じる. 
        """
        self.cn.close()

    def run_MATCH_query(self, **kwargs):
        """
        MATCHクエリの実行. 
        """
        with self.driver.session() as session:
            session.write_transaction(self._create_MATCH_query, **kwargs)

    @staticmethod
    def _create_MATCH_query(**kwargs) -> str:
        """
        MATCHクエリの作成
        """
        pass