from models.comment import Comment
from models.todo import Todo
from models.weibo import Weibo
from models.user import User
from utils import log


def test_tweet():
    # 用户 1 发微博
    form = {
        'content': 'hello tweet'
    }
    t = Weibo(form, 1)
    t.save()
    # 用户 2 评论微博
    form = {
        'content': '楼主说得对'
    }
    c = Comment(form, 2)
    c.tweet_id = 1
    c.save()
    # 取出微博 1 的所有评论
    t = Weibo.find(1)
    print('comments, ', t.comments())
    pass


# 假设要更新 id 1 的 todo 的完成状态
# 那么我们可以有两种方案
# # 方案 1 类方法
# form = {
#     'task': '游泳',
#     'completed': True,
# }
# Todo.update(1, form)
#
# # 方案 2 查找出来再用实例方法更新
# t = Todo.get(1)
# t.update(form)
#
# # 方案 3 最野鸡的方案
# t = Todo.get(1)
# t.task = form.get('task', '')
# t.completed = True


def test_create():
    form = {
        'task': '吃瓜'
    }
    Todo.new(form)


def test_read():
    t = Todo.find(1)
    assert t is not None, 't is none'
    assert t.id == 1, 'id error'
    log('id 1 的 todo 是 ', t.task)


def test_update():
    form = {
        'id': 100,
        'task': '喝水 喝水',
    }
    Todo.update(1, form)
    t = Todo.find(1)
    assert t.id == 1
    assert t.task == '喝水 喝水'


def test_delete():
    Todo.delete(2)
    t = Todo.find(2)
    assert t is None, '删除失败'


def test():
    cs = Comment.find_all(user_id=2)
    print(cs, '评论数', len(cs))
    test_tweet()
    # 测试数据关联
    form = {
        'task': 'gua 的 todo'
    }
    Todo.new(form, 1)
    # 得到 user 的所有 todos
    u1 = User.find(1)
    u2 = User.find(2)
    ts1 = u1.todos()
    ts2 = u2.todos()
    log('gua de todos', ts1)
    log('xiao de todos', ts2)
    assert len(ts1) > 0
    assert len(ts2) == 0

    test_create()
    test_read()
    test_update()
    test_delete()
    Todo.complete(1, True)

def hash():
    import hashlib
    # 要加密的是 'jim'
    # 用 ascii 编码转换成 bytes 对象
    password = 'dsaasd'.encode('ascii')
    # password = '202cb962ac59075b964b07152d234b70'.encode('ascii')

    # 创建 md5 对象
    m = hashlib.md5(password)
    # 返回摘要字符串, 这里是 c9c1ebed56b2efee7844b4158905d845
    print('md5', m.hexdigest())

    # 创建 sha1 对象
    s1 = hashlib.sha1(password)
    # 返回摘要字符串, 这里是 4843c628d74aa10769eb21b832f00a778db8b17e
    print('sha1', s1.hexdigest())

    # 创建 sha256 对象
    s256 = hashlib.sha256(password)
    # 返回摘要字符串, 这里是 d669b44e486c80ef96eb45528411b6f782c7d8086095183db89f0d65f828d1f7
    print('sha256', s256.hexdigest())

    password = '202cb962ac59075b964b07152d234b70'
    for i in range(0, 999):
        # i=1 p=001
        p = str(i).zfill(3)
        # print(p)
        b = p.encode('ascii')
        hash = hashlib.md5(b).hexdigest()
        if password == hash:
            print('原始密码是', p)


if __name__ == '__main__':
    # test()
    hash()
