from string import Template

class CreateDELETEQuery:
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

    def run_DELETE(self, **kwargs):
        """
        DELETEクエリの実行. 
        """
        with self.driver.session() as session:
            session.write_transaction(self._run_DELETE_query, **kwargs)
    
    @staticmethod
    def _create_DELETE_query(**kwargs) -> str:
        """
        DELETEクエリの作成
        """
        query = ""
        len_kwargs = len(kwargs)
        if len_kwargs == 0:
            query = "MATCH (n) DETACH DELETE n"
        elif len_kwargs == 1:
            # ノードとそれにかかわるすべての関係性の削除
            query = Template("MATCH (n {name: '${node_name}'}) DETACH DELETE n").substitute(node_name=kwargs["node_name"])
        return query
    
    @staticmethod
    def _run_DELETE_query(tx, **kwargs):
        """
        ノードを削除する. 
        """
        try:
            node_name = kwargs["node_name"]
            tx.run(CreateDELETEQuery._create_DELETE_query(node_name=node_name))
        except KeyError:
            tx.run(CreateDELETEQuery._create_DELETE_query())