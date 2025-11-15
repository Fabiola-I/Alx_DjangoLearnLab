from celery import shared_task
import time

@shared_task
def send_new_book_notification_email(book_title, recipient_email):
    """
    Simulates a long-running task (sending an email) in the background.
    """
    
    # Simulate work delay
    time.sleep(5) 
    
    # In a real app, use Django's send_mail or EmailMessage here.
    print(f"--- CELERY TASK COMPLETE ---")
    print(f"To: {recipient_email}")
    print(f"Subject: New Book Added: {book_title}")
    
    return f"Notification sent for {book_title}"