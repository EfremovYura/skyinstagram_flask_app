import logging
from sys import exception
from urllib import response

from flask import Flask, render_template, jsonify, request, redirect

from manager import Manager
from config import POSTS_FILE_PATH, COMMENTS_FILE_PATH, BOOKMARKS_FILE_PATH, TAGS_DISPLAY_LIMIT
from utils import get_comments_ending_form
from logger import log_config

app = Flask(__name__, template_folder="templates")

# Настройка логирования в файл
log_config()
api_logger = logging.getLogger('api_logger')

# Загрузить данные из файлов
manager = Manager(POSTS_FILE_PATH, COMMENTS_FILE_PATH, BOOKMARKS_FILE_PATH)

# Добавить в данные переменные с живыми тэгами
manager.add_tags_to_all_posts()

# Все посты
all_posts = manager.get_posts_all()


@app.route("/")
def page_main() -> str:
    bookmarks_total = len(manager.get_bookmarks())
    return render_template("index.html", posts=all_posts, bookmarks_total=bookmarks_total)


@app.route("/post/<int:postid>")
def page_post(postid: int) -> str:
    post = manager.get_post_by_pk(postid)
    comments = manager.get_comments_by_post_id(postid)
    comments_counter_header = get_comments_ending_form(len(comments))
    return render_template("post.html", post=post, comments=comments, comments_counter_header=comments_counter_header)


@app.route("/tag/<tagname>")
def page_tags(tagname: str) -> str:
    # Показать только TAGS_DISPLAY_LIMIT постов, если найдено больше.
    requested_posts = manager.search_for_posts(f"#{tagname}")[:TAGS_DISPLAY_LIMIT]
    return render_template("tag.html", tagname=tagname, posts=requested_posts)


@app.route("/users/<username>")
def page_users(username: str) -> str:
    posts = manager.get_posts_by_user(username)
    return render_template('user-feed.html', posts=posts, username=username)


@app.route("/search")
def page_search() -> str:
    user_request = request.args.get('s')
    requested_posts = manager.search_for_posts(user_request)
    posts_found_total = len(requested_posts)
    return render_template('search.html', posts_found_total=posts_found_total, posts=requested_posts,
                           user_request=user_request)


@app.route("/bookmarks")
def page_bookmarks() -> str:
    posts = manager.get_posts_with_bookmark()
    return render_template('bookmarks.html', posts=posts)


@app.route("/bookmarks/remove/<int:postid>", methods=['GET', 'POST'])
def page_remove_bookmark(postid: int) -> response:
    manager.remove_bookmark(postid)
    return redirect("/", code=302)


@app.route("/bookmarks/add/<int:postid>", methods=['POST', 'GET'])
def page_add_bookmark(postid: int) -> response:
    manager.add_bookmark(postid)
    return redirect("/", code=302)


@app.errorhandler(404)
def not_found_error(error: exception) -> tuple[str, int]:
    return f'Страница не найдена', 404


@app.errorhandler(500)
def internal_error(error) -> tuple[str, int]:
    return f'Внутренняя ошибка сервера', 500


@app.route('/api/posts', methods=["GET"])
def api_posts() -> response:
    api_logger.debug(f"Запрос /api/posts")
    posts = manager.get_all_posts_for_api()
    return jsonify(posts)


@app.route('/api/posts/<int:postid>', methods=["GET"])
def api_posts_post(postid: int) -> response:
    api_logger.debug(f"Запрос /api/posts/{postid}")
    return jsonify(manager.get_post_for_api_by_pk(postid))


if __name__ == "__main__":
    app.run()
