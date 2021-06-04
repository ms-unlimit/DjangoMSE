from django.http import HttpResponse

print("im algorithmic trading")
# Create your views here.
htm="<html> <head>   <title>lovely dream</title> </head> <body>  <span> &#128153; &#128156;  &#128155;  &#128154; &#128147;   </span> i love you sahar <span>&#128147; &#128154; &#128155; &#128156; &#128153; </span> </div> </body> </html>"
def hi(request):
    return HttpResponse(htm)

