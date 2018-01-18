from models.session import Session
from routes import (
    random_str,
    redirect,
    http_response,
    current_user,
    login_required,
)
from utils import log
from utils import template
from models.user import User


def route_login(request):
    """
    登录页面的路由函数
    """
    log('login, cookies', request.cookies)
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            session_id = random_str()
            u = User.find_by(username=u.username)
            s = Session.new(dict(
                session_id=session_id,
                user_id=u.id,
            ))
            s.save()
            log('session', s)
            headers = {
                'Set-Cookie': 'sid={}'.format(session_id)
            }
            # 登录后定向到 /
            return redirect('/', headers)
    # 显示登录页面
    body = template('login.html')
    return http_response(body)


def route_register(request):
    """
    注册页面的路由函数
    """
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            # 注册成功后 定向到登录页面
            return redirect('/login')
        else:
            # 注册失败 定向到注册页面
            return redirect('/register')
    # 显示注册页面
    body = template('register.html')
    return http_response(body)


def edit_password(request):
    """
    修改用户密码的路由函数
    """
    u = current_user(request)
    user_id = int(request.query.get('id', -1))
    # 若当前用户与需要修改密码的用户一致，允许修改
    if u.id == user_id:
        body = template('admin_password_edit.html')
        return http_response(body)
    # 否则重定向到主页
    else:
        return redirect('/')


def update_user_password(request):
    """
    更新用户密码
    """
    u = current_user(request)
    old_password = request.form().get('old_password')
    # 若输入的旧密码与当前用户密码一致，允许更新密码
    if u.password == User.salted_password(old_password):
        u.update(request.form().get('new_password'))
        return redirect('/login')
    # 否则重定向到首页
    else:
        return redirect('/')


def route_dict():
    r = {
        '/login': route_login,
        '/register': route_register,
        '/edit/password': login_required(edit_password),
        '/update/password': login_required(update_user_password),
    }
    return r
