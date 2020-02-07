"""
>>> x = ESArray([1, -3, 10, 5])
>>> x.join('**')
'1**-3**10**5'
>>> x.every(lambda v: v > 0)
False
>>> x.every(lambda v: isinstance(v, int))
True
>>> x.for_each(print)
1
-3
10
5
>>> y = ESArray([[3, 4], [5], 6, [7, [8, [9, 10]]]])
>>> y.flatten()
[3, 4, 5, 6, 7, 8, 9, 10]
"""


class ESArray(list):
    def join(self, s):
        res = ""
        if len(s) ==1:
            res = str(s)
        else:
            for i in range(0,len(self)-1):
                res += str(self[i])
                res += str(s)
            res += str(self[len(self)-1])
        return res

    def every(self, func):
        flag = True
        for i in self:
            if func(i) == False:
                flag = False
        return flag

    def some(self, func):
        pass

    def for_each(self, func):
        for i in self:
            func(i)

    def flatten(self):
        ## recursive function to flatten the list
        res = []
        def recur(input,output):
            for i in input:
                if isinstance(i,list):
                    recur(i,output)
                else:
                    output.append(i)
        recur(self,res)
        return res
