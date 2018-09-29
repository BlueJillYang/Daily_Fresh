# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import transaction
from datetime import datetime
from django.shortcuts import render
from df_user.user_decorator import decorator
from df_user.models import *
from .models import *
from goods.models import *
from cart.models import *
from django.shortcuts import redirect

# Create your views here.


# 如何使用事务 point=transaction.savepoint() 保存一个点
# 回退 transaction.savepoint_rollback(point)
# 提交 transaction.savepoint_commit(point)
@transaction.atomic()
@decorator
def order(request):
    uname = request.session.get('uname', '')
    users = UserInfo.objects.get(username=uname)
    # 接收参数
    cart_ids = request.GET.getlist('cart_id')

    cart = []
    cart_string = ''
    cart_list = [str(c) for c in cart]
    cart_string = ','.join(cart_list)
    request.session['cart_string'] = cart_string
    for cart_id in cart_ids:
        cart.append(CartInfo.objects.filter(user_id_id=users.id, goods_id_id=cart_id)[0])

    context = {'username': uname, 'users': users, 'cart': cart}
    return render(request, 'order/place_order.html', context)


@transaction.atomic()
@decorator
def create(request):
    uname = request.session.get('uname', '')
    users = UserInfo.objects.get(username=uname)
    uid = users.id
    # 接收参数
    cart_ids = request.session.get('cart_string', '').split(',')
    cart = []
    for cart_id in cart_ids:
        cart.append(CartInfo.objects.filter(user_id_id=users.id, goods_id_id=int(cart_id))[0])

    total = 0
    for c in cart:
        total1 = c.goods_id.price * c.amount
        total += total1
    # 创建事务保存点
    transPoint = transaction.savepoint()

    # 创建order对象
    order = OrderInfo()
    order_detail = OrderDetailInfo()
    try:
        # order信息
        now = datetime.now()
        order.oid = int(now.strftime('%Y%m%d%H%M%S'))*(10**-14) + int(uid)
        order.user_id = users.id
        order.oIsPay = True
        order.ototal = total
        order.oaddress = users.uaddress
        order.save()

        # orderdetail信息
        for c in cart:
            order_detail.id = 1
            order_detail.price = c.goods_id.price
            order_detail.count = c.amount
            order_detail.goods_id = c.goods_id_id
            order_detail.order_id = order.id
            order_detail.save()
    except Exception as e:
        # 异常就回滚数据 报错
        message = e
    else:
        # 删除购物车信息 库存减少
        transaction.savepoint_commit(transPoint)
        for c in cart:
            c.goods_id.reserve -= c.amount
            c.goods_id.save()
            c.delete()
        # 成功就提交
        message = 'done'
    context = {'mes': message}
    # return redirect('/user_center_order/')
    return render(request, 'order/pay.html', context)

