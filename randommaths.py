from random import randint

class RandomMathsProblems():
    def __init__(self,digits) -> None:
        #self.operation=operation
        self.digits=digits

    def summation(self):
        result=randint(10**(self.digits-1),10**self.digits-1)
        num_1=randint(1,result)
        num_2=result - num_1 
        return(num_1,num_2,result,'+')
    
    def subtraction(self):
        num_upper=randint(10**(self.digits-1),10**self.digits-1)
        num_lower=randint(1,num_upper)
        result=num_upper-num_lower
        return(num_upper,num_lower,result,'-')
    def product(self):
        num=[]
        num_upper_digits=randint(1,self.digits-1)
        num_lower_digits=self.digits-num_upper_digits
        num.append(randint(10**(num_upper_digits-1),10**num_upper_digits-1))
        num.append(randint(10**(num_lower_digits-1),10**num_lower_digits-1))
        num.sort(reverse=True)
        result=num[0]*num[1]
        return(num[0],num[1],result,'×')
