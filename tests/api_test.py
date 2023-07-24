class TestApi:

    def test_api_post_1(self, test_client):
        """ Проверяем, получается ли пост в виде словаря с нужными ключами"""
        page = '/api/posts/1'
        response = test_client.get(page, follow_redirects=True)

        assert isinstance(response.json, dict), "Возвращается не словарь"

        keys_to_check = ['content', 'likes_count', 'pic', 'pk', 'poster_avatar', 'poster_name', 'views_count']
        response_keys_list = response.json.keys()
        for key in keys_to_check:
            assert key in response_keys_list, f"Нет {key} в ответе api"

        assert response.json.get('pk') == 1, f"pk неверный"

    def test_api_posts(self, test_client):
        """ Проверяем, получается ли посты в виде списка словарей с нужными ключами"""
        page = '/api/posts'
        response = test_client.get(page, follow_redirects=True)

        assert isinstance(response.json, list), "Возвращается не список"

        posts_list = response.json
        for post in posts_list:
            assert isinstance(post, dict), "Элемент списка не словарь"

            keys_to_check = ['content', 'likes_count', 'pic', 'pk', 'poster_avatar', 'poster_name', 'views_count']
            post_keys_list = post.keys()
            for key in keys_to_check:
                assert key in post_keys_list, f"Нет {key} в ответе"
