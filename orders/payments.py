import razorpay
from decouple import config



class RazorPayPayment:
    def __init__(self,currency="INR"):
        self.currency=currency
        self.client = razorpay.Client(auth=(config('RazorPay_YOUR_API_KEY'), config('RazorPay_YOUR_API_SECRET')))

    def process_payment(self,amount,receipt_name):
        
        return self.client.order.create({
            "amount": amount*100,
            "currency": self.currency,
            "receipt": receipt_name,
            "partial_payment":False,
            "payment_capture":"1",
            "notes": {}
        })
        
        