import time
from pushnotification import botNotification
from ethermine import Ethermine
import traceback

if __name__ == "__main__":
    noti = botNotification()
    etherm = Ethermine()

    add = '0xEe80049fC7DCEEba1629D5814F32b1aB2d611dd5'

    lastime = time.time()
    lastpay = time.time()
    retries=0
    re_aleart = 0
    while True:
        try:
            pay = etherm.miner_payouts(add)
            dash = etherm.miner_dashboard(add)
            print('%.1f: %s' %(time.time(), str(pay[0])))
            
            if (dash['statistics'][-1]['activeWorkers'] == 1):
                re_aleart = 0

            elif (dash['statistics'][-1]['time'] != lastime):
                noti.broadtext('Worker offline check now')
                if re_aleart < 5:
                    re_aleart +=1
                    time.sleep(5*60)
                else:
                    re_aleart = 0
                    time.sleep(24*3600)     #1day
            
            lastime = dash['statistics'][-1]['time']

            if time.time() > (lastpay + 24*2*3600):
                noti.broadtext('Peding payout more than 2days ! check now')
                lastpay = time.time()-24*3600

            elif pay[0]['paidOn'] != lastpay:
                noti.broadtext('Pay:' + str(pay[0]))

            lastpay = pay[0]['paidOn']

        except Exception:
            noti.broadtext(traceback.print_exc())
            if retries > 10:
                break
            else:
                retries = retries+1
                time.sleep(3600)

        time.sleep(6)



