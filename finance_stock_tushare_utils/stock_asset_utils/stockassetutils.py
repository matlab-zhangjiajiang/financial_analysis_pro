#coding=utf-8
class stockassetutils(object):

    def __init__(self,currentPrice,isRise,riseFallSpot):
        self.currentPrice = currentPrice
        self.isRise = isRise
        self.riseFallSpot = riseFallSpot

    def upOrDownShowPrice(self):
        if(self.isRise):
            return self.currentPrice*self.riseFallSpot+self.currentPrice
        else:
            return self.currentPrice-self.currentPrice*self.riseFallSpot


if __name__ == '__main__':
    currentPrice = input('please input current price:')
    currentPrice = float(currentPrice)
    riseOrDown = input('rise or down ?(Y/N)')
    if riseOrDown == 'Y':
        riseOrDown =True
    else:
        riseOrDown = False
    riseFallSpot = input('please input rise flot  or down flot:')

    riseFallSpot = float(riseFallSpot)
    stock = stockassetutils(currentPrice,riseOrDown,riseFallSpot)

    print(stock.upOrDownShowPrice())
