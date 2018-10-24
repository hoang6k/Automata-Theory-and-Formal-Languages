import sys
from neo4j.v1 import GraphDatabase

class GraphDtb(object):

    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="neo4j"):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), connection_timeout=15)

    def close(self):
        self._driver.close()

    def make_node(self, name):
        with self._driver.session() as session:
            notification = session.write_transaction(self._create_and_return_state, name)
            print(notification)

    def make_relationship(self, _from, _to, _c):
        with self._driver.session() as session:
            session.write_transaction(self._create_and_return_character, _from, _to, _c)

    def delete_nodes(self):
        self.delete_relationships()
        with self._driver.session() as session:
            session.run("MATCH (n:State) DELETE n")

    def delete_relationships(self):
        with self._driver.session() as session:
            session.run("MATCH ()-[n:Symbol]->() DELETE n")

    @staticmethod
    def _create_and_return_state(tx, name):
        result = tx.run("MERGE (q:State {name: $name})"
                        "RETURN q.name + ' is created as node ' + id(q)", name=name)
        return result.single()[0]

    def _create_and_return_character(cls, tx, _from, _to, _c):
        tx.run("MATCH (from:State {name: $_from})"
               "MATCH (to:State {name: $_to})"
               "MERGE (from)-[c:Symbol {char: $_c}]->(to)", _from=_from, _to=_to, _c=_c)

def create_graph_FA(FA, type='NFA'):
    print('\n\nTao graph cho {}:'.format(type))
    dtb = GraphDtb(password='dota2')
    if type == 'NFA':
        dtb.delete_nodes()
    for item in FA.Q:
        dtb.make_node(str(item))
    for item in FA.delta:
        if type == 'NFA':
            for q in item.set:
                dtb.make_relationship(item.q, q, item.a)
        else:
            dtb.make_relationship(str(item.q), str(item.set), item.a)
    dtb.close()

if __name__ == "__main__":
    create_graph_FA(sys.argv[0])