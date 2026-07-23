import africastalking
from django.conf import settings

def send_sms_notification(phone_number: str, message: str):
    """
    Sends an SMS via Africa's Talking API.
    Falls back to terminal logging if API key is not configured.
    """
    username = getattr(settings, 'AFRICASTALKING_USERNAME', 'sandbox')
    api_key = getattr(settings, 'AFRICASTALKING_API_KEY', None)

    # Fallback / Mock Mode during local testing
    if not api_key or api_key == 'YOUR_AT_API_KEY':
        print(f"\n================ [MOCK SMS SENT] ================")
        print(f"To: {phone_number}")
        print(f"Message: {message}")
        print(f"=================================================\n")
        return True

    # Real Production / Sandbox SMS Dispatch
    try:
        africastalking.initialize(username, api_key)
        sms = africastalking.SMS
        
        # Format phone number to standard E.164 format (+254...)
        formatted_phone = phone_number if phone_number.startswith('+') else f"+{phone_number}"
        
        response = sms.send(message, [formatted_phone])
        print(f"[Africa's Talking] SMS dispatched successfully: {response}")
        return True
    except Exception as e:
        print(f"[Africa's Talking] Failed to send SMS: {e}")
        return False


def send_payment_receipt_sms(tenant_phone, amount, receipt_no, invoice_id, remaining_balance):
    """
    Helper specifically formatted for automated payment receipts.
    """
    if remaining_balance <= 0:
        balance_msg = "Your invoice is now fully paid. Thank you!"
    else:
        balance_msg = f"Remaining balance: KES {remaining_balance:,.2f}."

    message = (
        f"Payment Received! We have received KES {amount:,.2f} for Invoice #{invoice_id}. "
        f"M-Pesa Ref: {receipt_no}. {balance_msg}"
    )
    return send_sms_notification(tenant_phone, message) 