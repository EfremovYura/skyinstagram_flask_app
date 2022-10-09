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
        assert type(manager.all_posts) == type([]), "all_posts не список"
        assert type(manager.all_comments) == type([]), "all_comments не список"
        assert type(manager.bookmarks) == type([]), "bookmarks не список"
        assert type(manager.all_posts[0]) == type({}), "all_posts[0] не словарь"
        assert type(manager.all_comments[0]) == type({}), "all_comments[0] не словарь"
        assert type(manager.bookmarks[0]) == type({}), "bookmarks[0] не словарь"


    def test_repr(self):
        assert str(manager) == 'class Manager', "repr not correct"


    def test_get_posts_all(self):
        assert type(manager.get_posts_all()) == type([]), "get_posts_all не список"
        assert type(manager.get_posts_all()[0]) == type({}), "get_posts_all[0] не словарь"


    def test_get_bookmarks(self):
        assert type(manager.get_bookmarks()) == type([]), "get_bookmarks не список"
        assert type(manager.get_bookmarks()[0]) == type({}), "get_bookmarks[0] не словарь"


    def test_is_user_in_posts(self):
        assert manager.is_user_in_posts('leo') == True, "should find leo"
        assert manager.is_user_in_posts('unknown_user') == None, "must not find name 'unknown_user'"


    def test_is_user_in_comments(self):
        assert manager.is_user_in_comments('leo') == True, "should find leo"
        assert manager.is_user_in_comments('unknown_user') == None, "must not find name 'unknown_user'"


    def test_get_posts_by_user(self):
        assert type(manager.get_posts_by_user('leo')) == type([]), "not a list of posts for leo"
        with pytest.raises(ValueError):
            manager.get_posts_by_user('unknown_user')


    def test_get_post_by_pk(self, posts_with_live_tags_dict_keys_list):
        assert type(manager.get_post_by_pk(1)) == type({}), "post 1 is not dict"
        assert list(manager.get_post_by_pk(1).keys()) == posts_with_live_tags_dict_keys_list, "posts_dict_keys_list not equal"
        assert manager.get_post_by_pk(1)['pk'] == 1, "post 1 pk is not 1"
        assert manager.get_post_by_pk(999) == None, "return not None for pk not in posts list"


    def test_get_post_for_api_by_pk(self, posts_dict_keys_list):
        assert type(manager.get_post_for_api_by_pk(1)) == type({}), "post 1 is not dict"
        assert list(manager.get_post_for_api_by_pk(1).keys()) == posts_dict_keys_list, "posts keys not match"
        assert manager.get_post_for_api_by_pk(1)['pk'] == 1, "post 1 pk is not 1"
        assert manager.get_post_for_api_by_pk(999) == None, "return not None for pk not in posts list"


    def test_get_all_posts_for_api(self, posts_dict_keys_list):
        assert type(manager.get_all_posts_for_api()) == type([]), "return not list"
        assert type(manager.get_all_posts_for_api()[1]) == type({}), "return not dict in list"
        assert len(manager.get_all_posts_for_api()) == len(manager.all_posts), "return not all posts"
        assert list(manager.get_all_posts_for_api()[1].keys()) == posts_dict_keys_list, "posts keys not match"


    def test_get_comments_by_post_id(self):
        with pytest.raises(ValueError):
            manager.get_comments_by_post_id(999)
        assert type(manager.get_comments_by_post_id(1)) == type([])


    def test_add_tags_to_all_posts(self, posts_with_live_tags_dict_keys_list):
        assert manager.add_tags_to_all_posts() == None
        assert list(manager.all_posts[1].keys()) == posts_with_live_tags_dict_keys_list


    def test_search_for_posts(self):
        assert manager.search_for_posts('ага') == [manager.all_posts[0]]
        assert manager.search_for_posts('') == manager.all_posts


    def test_get_postids_with_bookmarks(self):
        assert type(manager.get_postids_with_bookmarks()) == type([])
        assert len(manager.get_postids_with_bookmarks()) == len(manager.bookmarks)
        assert manager.get_postids_with_bookmarks()[0] == 1


    def test_add_bookmark(self):
        assert manager.add_bookmark(7) == None
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
        assert type(manager.get_posts_with_bookmark()) == type([])
        assert type(manager.get_posts_with_bookmark()[0]) == type({})
        assert list(manager.get_posts_with_bookmark()[0]) == posts_with_live_tags_dict_keys_list


