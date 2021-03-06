# -*- coding:utf8 -*-
import MySQLdb
import time
import json

# 获取系统时间 time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))

conn=MySQLdb.connect(host='localhost',user='root',passwd='1234',port=3306,charset = 'utf8')
cur=conn.cursor()
cur.execute("use electronics")


def Main_list():
    goods_dict = {}
    return_dict = {}
    sqlstr = "SELECT id,name, price,discount FROM goods_table"
    count = cur.execute(sqlstr)
    result = cur.fetchall()
    for item in result:
        if item[3]:
            discount = int(item[3])
        else:
            discount = 1
        goods_id = "%03d"%int(item[0])
        goods_dict[goods_id] = [str(item[1]), int(item[2]), discount]
    return_dict['length'] = int(count)
    return_dict['data'] = goods_dict
    print return_dict
    return return_dict


# 查询功能，根据商品类别查出所有商品，并返回   注：没有考虑查不到的情况, length = 0
def List_function(ttype):
    goods_dict = {}
    return_dict = {}
    sqlstr = "SELECT id,name, price,discount FROM goods_table WHERE kind = '%s'" %ttype
    count = cur.execute(sqlstr)
    if count == 0:
        return_dict['length'] = int(count)
        print return_dict
        return return_dict
    else:
        result = cur.fetchall()
        for item in result:
            if item[3]:
                discount = int(item[3])
            else:
                discount = 1
            goods_id = "%03d"%int(item[0])
            goods_dict[goods_id] = [str(item[1]), int(item[2]), discount]
        return_dict['length'] = int(count)
        return_dict['data'] = goods_dict
        print return_dict
        return return_dict


# 查询功能，根据商品名称查出所有商品，并返回    注：没有考虑查不到的情况 length = 0
def Search_function(item):
    goods_dict = {}
    return_dict = {}
    sqlstr = "SELECT id,name, price,discount FROM goods_table WHERE name = '%s'" %item
    count = cur.execute(sqlstr)
    if count == 0:
        return_dict['length'] = int(count)
        print return_dict
        return return_dict
    else:
        result = cur.fetchall()
        for item in result:
            if item[3]:
                discount = int(item[3])
            else:
                discount = 1
            goods_id = "%03d"%int(item[0])
            goods_dict[goods_id] = [str(item[1]), int(item[2]), discount]
        return_dict['length'] = int(count)
        return_dict['data'] = goods_dict
        print return_dict
        return return_dict


# 根据id返回表中的detail字段 ,  如果不存在此id，返回0
def Detail_functioni(id):
    id = int(id)
    details = {}
    sqlstr = "SELECT name, detail, price, discount, kind FROM  goods_table WHERE id = %s" %id
    count = int(cur.execute(sqlstr))
    if count != 0:
        result = cur.fetchone()
        # print result
        details['name'] = str(result[0])
        details['detail'] = str(result[1])
        details['price'] = int(result[2])
        details['discount'] = int(result[3])
        details['tag'] = str(result[4])
    print details
    return details


# 登录成功返回用户id，失败返回0
def Login_function(acc, passwd):
    sqlstr = "SELECT id FROM user_table WHERE account = '%s' AND password = '%s'" %(acc, passwd)
    count = int(cur.execute(sqlstr))
    if count == 0:
        id =  0
    else:
        id = cur.fetchone()[0]
    id = "%03d"%id
    print id
    return id


def Reg_function(account, passwd, addr ,tel):
    # a="%5d"%x
    accounts = []
    sqlstr = "SELECT account FROM user_table"
    cur.execute(sqlstr)
    result = cur.fetchall()
    for item in result:
        accounts.append(str(item[0]))
    if account in accounts:
        id = 0
    else:
        sqlstr = "INSERT INTO user_table(account, password, addr, tel) VALUES('%s','%s','%s','%s') " %(account, passwd, addr,tel)
        cur.execute(sqlstr)
        conn.commit()
        sqlstr = "SELECT id FROM user_table WHERE account = '%s' AND password = '%s'" %(account, passwd)
        cur.execute(sqlstr)
        result = cur.fetchall()
        id = int(result[0][0])
    id = "%03d"%id
    print id
    return id


    def Search_function(item):
        orders_dict = {}
        return_dict = {}
        sqlstr = "SELECT id,name, price,discount FROM goods_table WHERE name = '%s'" %item
        count = cur.execute(sqlstr)
        print count
        if count == 0:
            return_dict['length'] = int(count)
            return_dict['data'] = goods_dict
            print return_dict
            return return_dict
        else:
            result = cur.fetchall()
            for item in result:
                if item[3]:
                    discount = int(item[3])
                else:
                    discount = 1
                goods_id = "%03d"%int(item[0])
                goods_dict[goods_id] = [str(item[1]), int(item[2]), discount]
            return_dict['length'] = int(count)
            return_dict['data'] = goods_dict
            print return_dict
            return return_dict


# 生成订单，成功返回int 1， 失败返回 int 2
def Purchase_function(good_id, num, user_id):
    try:
         sqlstr = "SELECT id,name, price,discount FROM goods_table WHERE id = '%s'" %good_id
         cur.execute(sqlstr)
         result = cur.fetchone()
         price = int(result[2])
         sum = price * num
         now_time = time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))
         sqlstr = "INSERT INTO order_table(user_id, good_id, goods_name, goods_num, sum, deal_time) VALUES('%s', %s, '%s', %s, %s, '%s')" %(user_id, good_id, str(result[1]), num, sum, now_time)
         cur.execute(sqlstr)
         conn.commit()
         print "Order ok ..."
         return 1
    except:
        return 0


# 确认支付
def Purchase_Ctrl_function(order_id):
    try:
        sqlstr = "UPDATE order_table SET pay = 1 WHERE id = %s" %int(order_id)   
        cur.execute(sqlstr)
        conn.commit()
        print 'result : 1'
        return 1
    except:
        print 'result : 0'
        return 0
    


def Order_function(user_id):
   # 从cookie获取user_idf
    goods_dict = {} #  商品dict
    order_dict = {} # 每条订单dict
    return_dict = {} # 最终返回的dict
    sqlstr = "SELECT id, sum,deal_time,good_id, goods_name, goods_num FROM order_table WHERE user_id = '%s' " %(user_id)
    count = cur.execute(sqlstr)
    result = cur.fetchall()
    if count == 0:
        pass
    else:
        for item in result:
            goods_dict[int(item[3])]=[str(item[4]),int(item[5])]
            order_dict['sum'] = int(item[1])
            order_dict['time'] = str(item[2])
            order_dict['goods']  = goods_dict
            return_dict[int(item[0])] = order_dict
            goods_dict = {}
            order_dict = {}
        print return_dict


def Admin_Order_function():
    order_dict = {}
    data_dict = {}
    return_dict = {}
    sqlstr = "SELECT id, user_id, goods_name, goods_num, sum, deal_time, pay FROM order_table"
    count = cur.execute(sqlstr)
    result = cur.fetchall()
    for item in result:
        order_dict['uid'] = str(item[1])
        order_dict['name'] = str(item[2])
        order_dict['num'] = int(item[3])
        order_dict['sum']= int(item[4])
        order_dict['time'] = str(item[5])
        order_dict['statue'] = int(item[6])
        order_id = "%03d"%int(item[0])
        data_dict[order_id] = order_dict
        order_dict = {}
    return_dict['length'] = int(count)
    return_dict['data'] = data_dict
    print return_dict
    return return_dict


def Admin_Allusers_function():
    return_dict = {}
    data_dict = {}
    user_dict = {}
    sqlstr = "SELECT id, account, password, addr, tel FROM user_table  ORDER BY id"
    count = cur.execute(sqlstr)
    result = cur.fetchall()
    for item in result:
        user_id = "%03d"%int(item[0])
        user_dict['account'] = str(item[1])
        user_dict['addr'] = str(item[3])
        user_dict['tel'] = str(item[4])
        data_dict[user_id] = user_dict
        user_dict = {}
    return_dict['length'] = int(count)
    return_dict['data'] = data_dict
    print return_dict
    return return_dict


def Admin_AllGoods_function():
    return_dict = {}
    data_dict = {}
    good_dict = {}
    sqlstr = "SELECT id, name, kind, price, discount  FROM goods_table  ORDER BY id"
    count = cur.execute(sqlstr)
    result = cur.fetchall()
    for item in result:
        good_id = "%03d"%int(item[0])
        good_dict['name'] = str(item[1])
        good_dict['type'] = str(item[2])
        good_dict['price'] = int(item[3])
        good_dict['off'] = int(item[4])
        data_dict[good_id] = good_dict
        good_dict = {}
    return_dict['length'] = int(count)
    return_dict['data'] = data_dict
    print return_dict
    return return_dict

# 修改商品价格
def  Admin_Modify_Price_function(good_id, price):
    try:
        sqlstr = "UPDATE goods_table SET price = %s" %price
        cur.execute(sqlstr)
        conn.commit()
        print 'result : 1'
        return 1
    except:
        print 'result : 0'
        return 0


# 修改商品折扣
def Admin_Modify_Discount_function(good_id, re_discount):
    try:
        sqlstr = "UPDATE goods_table SET discount = %s" %re_discount
        cur.execute(sqlstr)
        conn.commit()
        print 'result : 1'
        return 1
    except:
        print 'result : 0'
        return 0


# 删除订单
def Admin_Del_Order_function(order_id):
    try:
        sqlstr = " DELETE FROM order_table WHERE id  = %s" %int(order_id)
        cur.execute(sqlstr)
        conn.commit()
        print 'result : 1'
        return 1
    except:
        print 'result : 0'
        return 0


# 删除用户
def Admin_Del_User_function(user_id):
    try:
        sqlstr = " DELETE FROM user_table WHERE id  = %s" %int(user_id)
        cur.execute(sqlstr)
        conn.commit()
        print 'result : 1'
        return 1
    except:
        print 'result : 0'
        return 0



def Home_Userinfo_function(user_id):
    user_id = int(user_id)
    user_dict = {}
    sqlstr = "SELECT account, addr, tel FROM user_table  WHERE id = %s" %user_id
    cur.execute(sqlstr)
    user_info = cur.fetchone()
    user_dict['account'] = str(user_info[0])
    user_dict['addr'] = str(user_info[1])
    user_dict['tel'] = str(user_info[2])
    return user_dict


def Home_Orderinfo_function(user_id):
    user_id = int(user_id)
    order_dict = {}
    data_dict = {}
    return_dict = {}
    sqlstr = "SELECT id, user_id, good_id, goods_name, goods_num,  sum, deal_time, pay FROM order_table  WHERE user_id = %s" %user_id
    count = cur.execute(sqlstr)
    result = cur.fetchall()
    for item in result:
        order_dict['uid'] = str(item[1])
        order_dict['id'] = "%03d"%int(item[2])
        order_dict['name'] = str(item[3])
        order_dict['num'] = str(item[4])
        order_dict['sum'] = int(item[5])
        order_dict['deal_time'] = str(item[6])
        order_dict['statue'] = int(item[7])
        data_dict["%03d"%int(item[0])] = order_dict
        order_dict = {}
    return_dict['length'] = int(count)
    return_dict['data'] = data_dict
    print return_dict
    return return_dict








# 确认购买时候，还需要确定是为哪一条记录确认购买，参数只有uid不够
# 库存不足需要说明是哪个货物不足吗？？
# def Purchasefunction(dict):





if __name__ == '__main__':
    # Main_list()
   #  Login_function('123', 'abc123')
   # List_function('A')
    # Detail_functioni('001')
    # Reg_function('795', 'abc123', 'HIT' ,'18963166073')
   #  Search_function('computer')
  #  Order_function('002')
  # Admin_Order_function()
 # Admin_Allusers_function()
 # Admin_Modify_Price_function(1, 50)
 # Admin_Modify_Discount_function(2, 9)
 # Admin_Del_Order_function('003')
 # Admin_Del_User_function('013')
 # Purchase_Ctrl_function('001')
 # Admin_AllGoods_function()
 # Home_function('012')
 # Home_Orderinfo_function(2)
 Purchase_function(2, 3, '002')
