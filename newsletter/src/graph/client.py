import os
from neo4j import GraphDatabase
from src.utils.logger import get_logger

logger = get_logger(__name__)


class GraphClient:
    def __init__(self, uri: str, user: str, password: str, database: str = "neo4j"):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self._database = database

    def query(self, cypher: str, params: dict = None) -> list:
        with self._driver.session(database=self._database) as session:
            result = session.run(cypher, params or {})
            return [record.data() for record in result]

    def write(self, cypher: str, params: dict = None):
        with self._driver.session(database=self._database) as session:
            session.execute_write(lambda tx: tx.run(cypher, params or {}))

    def close(self):
        self._driver.close()


def get_graph_client(config: dict) -> GraphClient:
    g = config.get("graph", {})
    return GraphClient(
        uri=os.environ.get("NEO4J_URI", g.get("uri", "bolt://localhost:7687")),
        user=os.environ.get("NEO4J_USER", g.get("user", "neo4j")),
        password=os.environ.get("NEO4J_PASSWORD", g.get("password", "neo4j")),
        database=g.get("database", "neo4j"),
    )
