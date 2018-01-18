from models.comment import Comment
from models.user import User
from models.weibo import Weibo
from routes import (
    redirect,
    http_response,
    current_user,
    login_required,
    error,
)
from utils import template, log


# 微博相关页面
def index(request):
    author_id = int(request.query.get('user_id', -1))
    user = current_user(request)
    if author_id == -1:
        author_id = user.id

    weibos = Weibo.all()
    body = template('weibo_index.html', weibos=weibos, user=user)
    return http_response(body)


def new(request):
    body = template('weibo_new.html')
    return http_response(body)


def add(request):
    u = current_user(request)
    # 创建微博
    form = request.form()
    w = Weibo.new(form)
    w.user_id = u.id
    w.save()
    return redirect('/weibo/index')


def delete(request):
    u = current_user(request)
    # 删除微博
    weibo_id = int(request.query.get('id', None))
    Weibo.delete(weibo_id)
    return redirect('/weibo/index')


def edit(request):
    u = current_user(request)
    weibo_id = int(request.query.get('id', -1))
    w = Weibo.find(weibo_id)
    # 若当前用户为微博作者，允许编辑
    if w.user_id == u.id:
        # 生成一个 edit 页面
        body = template('weibo_edit.html', weibo_id=w.id, weibo_content=w.content)
        return http_response(body)
    # 重定向到用户微博的主页
    else :
        return redirect('/weibo/index')


def update(request):
    u = current_user(request)
    form = request.form()
    content = form.get('content', '')
    weibo_id = int(form.get('id', -1))
    w = Weibo.find(weibo_id)
    # 若当前用户为微博作者，允许更新
    if w.user_id == u.id:
        w.content = content
        w.save()
        # 重定向到用户微博的主页
        return redirect('/weibo/index')
    # 否则返回 404 错误
    else:
        return error(request)


def comment_add(request):
    u = current_user(request)
    # 创建微博
    form = request.form()
    c = Comment.new(form)
    c.user_id = u.id
    c.save()
    log('comment add', c, u, form)
    weibo = Weibo.find(id=int(form['weibo_id']))
    return redirect('/weibo/index?user_id={}'.format(weibo.user_id))


def comment_edit(request):
    u = current_user(request)
    comment_id = int(request.query.get('id', -1))
    comment = Comment.find_by(id=comment_id)
    # 若当前用户为 comment 的作者，允许修改
    if comment.user_id == u.id:
        body = template('comment_edit.html', id=comment.id, content=comment.content)
        return http_response(body)
    # 否则重定向到用户微博的主页
    else:
        return redirect('/weibo/index?user_id={}'.format(comment.user_id))


def comment_update(request):
    u = current_user(request)
    comment_id = int(request.form().get('id', -1))
    comment = Comment.find_by(id=comment_id)
    # 若当前用户为 comment 作者，允许更新
    if comment.user_id == u.id:
        comment.content = request.form().get('content')
        comment.save()
        return redirect('/weibo/index?user_id={}'.format(comment.user_id))
    # 否则返回 404 错误
    else:
        return error(request)


def comment_delete(request):
    u = current_user(request)
    comment_id = int(request.query.get('id', -1))
    comment = Comment.find_by(id=comment_id)
    weibo = Weibo.find_by(id=comment.weibo_id)
    # 若当前用户为 comment 作者 或 相应的微博作者，允许删除
    if u.id in (comment.user_id, weibo.user_id):
        comment.delete(comment.id)
        return redirect('/weibo/index?user_id={}'.format(u.id))
    # 否则直接重定向到当前用户微博页面
    else:
        return redirect('/weibo/index?user_id={}'.format(u.id))


def route_dict():
    r = {
        '/weibo/index': login_required(index),
        '/weibo/new': login_required(new),
        '/weibo/edit': login_required(edit),
        '/weibo/add': login_required(add),
        '/weibo/update': login_required(update),
        '/weibo/delete': login_required(delete),
        # 评论功能
        '/comment/add': login_required(comment_add),
        '/comment/edit': login_required(comment_edit),
        '/comment/update': login_required(comment_update),
        '/comment/delete': login_required(comment_delete),
    }
    return r
