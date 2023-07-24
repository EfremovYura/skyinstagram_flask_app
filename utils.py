import json
from copy import copy


def load_json(file: str) -> list[dict]:
    """Загружает список из файла json."""
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_comments_ending_form(number: int) -> str:
    """Возвращает форму слова комментарий в зависимости от количества."""
    if number in [11, 12, 13, 14]:
        return f"{number} комментариев"
    elif number % 10 == 1:
        return f"{number} комментарий"
    elif number % 10 in [2, 3, 4]:
        return f"{number} комментария"
    else:
        return f"{number} комментариев"


def add_tag_list(post: dict) -> dict:
    """Добавляет 2 параметра с живыми  тэгами в пост."""
    post = copy(post)
    words_list = post['content'].split(' ')

    # список живых тэгов
    tags_list = []

    # список слов из контента с живыми тэгами
    content_with_links_list = []

    for word in words_list:
        if word.startswith('#'):

            # убираем # из начала
            word = word[1:]

            word_end = ''
            if word[-1] in ",.!?:;":
                # сохраняем окончание
                word_end = word[-1]
                # убираем знак препинания, прикрепленный к слову
                word = word[0:-1]

            tag_link = f'<a href="/tag/{word}" class="item__tag">#{word}</a>'
            tags_list.append(tag_link)
            content_with_links_list.append(tag_link + word_end)
        else:
            content_with_links_list.append(word)

    post['tags_list'] = ', '.join(tags_list)
    post['content_with_links'] = ' '.join(content_with_links_list)

    return post


def remove_tags_keys(post: dict) -> dict:
    """Удаляет ключи с живыми тэгами из поста."""
    post = copy(post)
    tags_to_del = ['tags_list', 'content_with_links']
    post_keys = post.keys()

    for tag in tags_to_del:
        if tag in post_keys:
            del post[tag]

    return post
