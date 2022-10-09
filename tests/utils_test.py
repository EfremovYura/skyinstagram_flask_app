import pytest

from utils import load_json, get_comments_ending_form, add_tag_list, remove_tags_keys

from config import POSTS_FILE_PATH, COMMENTS_FILE_PATH, BOOKMARKS_FILE_PATH


load_json_params = [
    (POSTS_FILE_PATH, "<class 'list'>"),
    (COMMENTS_FILE_PATH, "<class 'list'>"),
    (BOOKMARKS_FILE_PATH, "<class 'list'>"),
]


@pytest.mark.parametrize('file, result', load_json_params)
def test_load_json(file, result):
    assert str(type(load_json(file))) == result


get_comments_ending_form_params =[
    (1, "1 комментарий"),
    (2, "2 комментария"),
    (3, "3 комментария"),
    (4, "4 комментария"),
    (5, "5 комментариев"),
    (11, "11 комментариев"),
    (22, "22 комментария")
]

@pytest.mark.parametrize('number, comments_form', get_comments_ending_form_params)
def test_get_comments_ending_form(number, comments_form):
    assert get_comments_ending_form(number) == comments_form


post_with_tag = {'content': 'Ага, опять #еда!'}
post_with_live_tag = {'content': 'Ага, опять #еда!',
                      'tags_list': '<a href="/tag/еда" class="item__tag">#еда</a>',
                      'content_with_links': 'Ага, опять <a href="/tag/еда" class="item__tag">#еда</a>!'
}


def test_add_tag_list(post=post_with_tag):
    assert add_tag_list(post) == post_with_live_tag

def test_remove_tags_keys(post=post_with_live_tag):
    assert remove_tags_keys(post) == post_with_tag
