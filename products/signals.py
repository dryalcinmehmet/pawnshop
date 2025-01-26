from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Product


@receiver(post_save, sender=Product)
def send_product_email(sender, instance, created, **kwargs):
    if created:
        subject = "New Product Added"
        message = f"A new product has been added:\n\nName: {instance.name}\nDescription: {instance.description}\nPrice: ${instance.price}"
        from_email = "your_email@example.com"
        recipient_list = ["recipient@example.com"]
        send_mail(subject, message, from_email, recipient_list)
