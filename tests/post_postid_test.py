class TestPostPostid:

    def test_status(self, test_client):
        """ Проверяем, получается ли нужный статус-код """
        page = '/post/1'
        response = test_client.get(page, follow_redirects=True)
        assert response.status_code == 200, f"Статус-код страницы '{page}' неверный"

    def test_content(self, test_client):
        """ Проверяем, есть ли текст на странице """
        page = '/post/1'
        text = '<title>SKYPROGRAM post</title>'
        response = test_client.get(page, follow_redirects=True)
        assert text in response.data.decode("utf-8"), f"Контент страницы {page} неверный"
