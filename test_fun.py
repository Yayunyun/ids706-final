import application
def test_app():
    assert application.get_recommendations("Avatar").iloc[0] == "Cypher"