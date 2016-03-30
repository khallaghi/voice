def ss():
    ret = {}
    for i in range(0,14):
        ret['num'] = i
        yield ret
    
ss = ss()
# OUT:   File "<input>", line 7
# OUT:     ss = ss()
# OUT:      ^
# OUT: SyntaxError: invalid syntax
gg = ss()
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT: NameError: name 'ss' is not defined

C
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT: NameError: name 'C' is not defined
