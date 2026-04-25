from django.shortcuts import render
from rabbitmq.producer import publish_message


# Create your views here.
def home_page(request):
    publish_message("first_queue", {"message": "Hello from first_queue!"})
    publish_message("second_queue", {"message": "Hello from second_queue!"})

    return render(request, "main/home.html")
