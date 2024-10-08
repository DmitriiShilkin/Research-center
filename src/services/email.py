
from constants.email_contexts import RateAlertContext
from utilities.email_client import EmailClient


async def send_new_rate_alert_email(
        to_email: str,
        market_name: str,
        total_amount: str,
        difference: str
) -> None:
    context = RateAlertContext(
        market_name=market_name,
        total_amount=total_amount,
        difference=difference
    )
    email_client = EmailClient(email=[to_email])
    await email_client.send_new_rate_alert(context)
