import pytest

from main import manager


@pytest.fixture()
def posts_dict_keys_list():
    posts_dict_keys_list = ['poster_name', 'poster_avatar', 'pic', 'content', 'views_count', 'likes_count', 'pk']
    return posts_dict_keys_list


@pytest.fixture()
def posts_with_live_tags_dict_keys_list():
    posts_with_live_tags_keys = ['poster_name', 'poster_avatar', 'pic', 'content', 'views_count', 'likes_count', 'pk',
                                 'tags_list', 'content_with_links']
    return posts_with_live_tags_keys


class TestManager:

    def test_init(self):
        assert isinstance(manager.all_posts, list), "all_posts не список"
        assert isinstance(manager.all_comments, list), "all_comments не список"
        assert isinstance(manager.bookmarks, list), "bookmarks не список"
        assert isinstance(manager.all_posts[0], dict), "all_posts[0] не словарь"
        assert isinstance(manager.all_comments[0], dict), "all_comments[0] не словарь"
        assert isinstance(manager.bookmarks[0], dict), "bookmarks[0] не словарь"

    def test_repr(self):
        assert str(manager) == 'class Manager', "repr not correct"

    def test_get_posts_all(self):
        assert isinstance(manager.get_posts_all(), list), "get_posts_all не список"
        assert isinstance(manager.get_posts_all()[0], dict), "get_posts_all[0] не словарь"

    def test_get_bookmarks(self):
        assert isinstance(manager.get_bookmarks(), list), "get_bookmarks не список"
        assert isinstance(manager.get_bookmarks()[0], dict), "get_bookmarks[0] не словарь"

    def test_is_user_in_posts(self):
        assert manager.is_user_in_posts('leo'), "should find leo"
        assert manager.is_user_in_posts('unknown_user') is None, "must not find name 'unknown_user'"

    def test_is_user_in_comments(self):
        assert manager.is_user_in_comments('leo'), "should find leo"
        assert manager.is_user_in_comments('unknown_user') is None, "must not find name 'unknown_user'"

    def test_get_posts_by_user(self):
        assert isinstance(manager.get_posts_by_user('leo'), list), "not a list of posts for leo"
        with pytest.raises(ValueError):
            manager.get_posts_by_user('unknown_user')

    def test_get_post_by_pk(self, posts_with_live_tags_dict_keys_list):
        assert isinstance(manager.get_post_by_pk(1), dict), "post 1 is not dict"
        assert list(
            manager.get_post_by_pk(1).keys()) == posts_with_live_tags_dict_keys_list, "posts_dict_keys_list not equal"
        assert manager.get_post_by_pk(1)['pk'] == 1, "post 1 pk is not 1"
        assert manager.get_post_by_pk(999) is None, "return not None for pk not in posts list"

    def test_get_post_for_api_by_pk(self, posts_dict_keys_list):
        assert isinstance(manager.get_post_for_api_by_pk(1), dict), "post 1 is not dict"
        assert list(manager.get_post_for_api_by_pk(1).keys()) == posts_dict_keys_list, "posts keys not match"
        assert manager.get_post_for_api_by_pk(1)['pk'] == 1, "post 1 pk is not 1"
        assert manager.get_post_for_api_by_pk(999) is None, "return not None for pk not in posts list"

    def test_get_all_posts_for_api(self, posts_dict_keys_list):
        assert isinstance(manager.get_all_posts_for_api(), list), "return not list"
        assert isinstance(manager.get_all_posts_for_api()[1], dict), "return not dict in list"
        assert len(manager.get_all_posts_for_api()) == len(manager.all_posts), "return not all posts"
        assert list(manager.get_all_posts_for_api()[1].keys()) == posts_dict_keys_list, "posts keys not match"

    def test_get_comments_by_post_id(self):
        with pytest.raises(ValueError):
            manager.get_comments_by_post_id(999)
        assert isinstance(manager.get_comments_by_post_id(1), list)

    def test_add_tags_to_all_posts(self, posts_with_live_tags_dict_keys_list):
        assert manager.add_tags_to_all_posts() is None
        assert list(manager.all_posts[1].keys()) == posts_with_live_tags_dict_keys_list

    def test_search_for_posts(self):
        assert manager.search_for_posts('ага') == [manager.all_posts[0]]
        assert manager.search_for_posts('') == manager.all_posts

    def test_get_postids_with_bookmarks(self):
        assert isinstance(manager.get_postids_with_bookmarks(), list)
        assert len(manager.get_postids_with_bookmarks()) == len(manager.bookmarks)
        assert manager.get_postids_with_bookmarks()[0] == 1

    def test_add_bookmark(self):
        assert manager.add_bookmark(7) is None
        # Новый пост в закладке
        bookmarks_total = len(manager.bookmarks)
        manager.add_bookmark(6)
        assert len(manager.bookmarks) == bookmarks_total + 1
        # Пост уже есть в закладках
        bookmarks_total = len(manager.bookmarks)
        manager.add_bookmark(6)
        assert len(manager.bookmarks) == bookmarks_total

    def test_remove_bookmark(self):
        # удалить пост из списка
        bookmarks_total = len(manager.bookmarks)
        manager.remove_bookmark(1)
        assert len(manager.bookmarks) == bookmarks_total - 1
        # если поста нет в закладках
        bookmarks_total = len(manager.bookmarks)
        manager.remove_bookmark(999)
        assert len(manager.bookmarks) == bookmarks_total

    def test_get_posts_with_bookmark(self, posts_with_live_tags_dict_keys_list):
        assert isinstance(manager.get_posts_with_bookmark(), list)
        assert isinstance(manager.get_posts_with_bookmark()[0], dict)
        assert list(manager.get_posts_with_bookmark()[0]) == posts_with_live_tags_dict_keys_list
