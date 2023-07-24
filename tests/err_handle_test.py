class TestErrHendler:

    def test_status_404(self, test_client):
        """ Проверяем, получается ли нужный статус-код """
        page = '/myay'
        response = test_client.get(page, follow_redirects=True)
        assert response.status_code == 404, f"Статус-код страницы '{page}' неверный"

    def test_content_404(self, test_client):
        """ Проверяем, есть ли текст на странице """
        page = '/myay'
        text = 'Страница не найдена'
        response = test_client.get(page, follow_redirects=True)
        assert text in response.data.decode("utf-8"), f"Контент страницы {page} неверный"

    def test_status_500(self, test_client):
        """ Проверяем, получается ли нужный статус-код """
        page = '/post/999'
        response = test_client.get(page, follow_redirects=True)
        assert response.status_code == 500, f"Статус-код страницы '{page}' неверный"

    def test_content_500(self, test_client):
        """ Проверяем, есть ли текст на странице """
        page = '/post/999'
        text = 'Внутренняя ошибка сервера'
        response = test_client.get(page, follow_redirects=True)
        assert text in response.data.decode("utf-8"), f"Контент страницы {page} неверный"
