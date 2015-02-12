one=" "
while True:
    print """(1)取五个数的和
(2)取五个数的平均值
(x)退出"""
    one=raw_input('请输入编号:')
    if one=='x':
        print '成功退出'
        break
    elif  one.isdigit()and int(one)==1:
        print "handle with add"
        
    elif  one.isdigit()and int(one)==2:
        print "handle with average"
        
    else:
        print '重新输入'