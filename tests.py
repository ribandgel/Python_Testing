from .server import create_app  # Flask instance of the API


def test_index_route():
    response = create_app().test_client().get("/")
    assert response.status_code == 200
    assert "Please enter your secretary email to continue:" in response.data.decode("utf-8")


def test_summary_route():
    response = create_app().test_client().post("/showSummary")
    assert response.status_code == 400
    response = create_app().test_client().post("/showSummary", data={"email": "john@simplylift.co"})
    assert "Welcome, john@simplylift.co" in response.data.decode("utf-8")
    assert "Number of Places: 25" in response.data.decode("utf-8")


def test_book_route():
    response = create_app().test_client().get("/book/blob/blob")
    assert response.status_code == 500
    response = create_app().test_client().get("/book/Spring Festival/Simply Lift")
    assert response.status_code == 200
    assert (
        "Spring Festival</h2>\n    Places available: 25\n    /!\\ You can't book more than 12 places"
        in response.data.decode("utf-8")
    )


def test_purchase_route():
    response = create_app().test_client().post("/purchasePlaces")
    assert response.status_code == 400
    response = (
        create_app()
        .test_client()
        .post("/purchasePlaces", data={"competition": "Spring Festival", "club": "Simply Lift", "places": 50})
    )
    assert response.status_code == 200
    assert "You are not allowed to book more places than your amount of points" in response.data.decode("utf-8")
    response = (
        create_app()
        .test_client()
        .post("/purchasePlaces", data={"competition": "Spring Festival", "club": "Simply Lift", "places": 1})
    )
    assert response.status_code == 200
    assert "Great-booking complete!" in response.data.decode("utf-8")
