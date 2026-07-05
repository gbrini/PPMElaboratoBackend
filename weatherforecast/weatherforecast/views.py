from django.http import HttpResponse

def api_home(request):
    return HttpResponse("""
        <h1>Weather API</h1>
        <p>Welcome to the weather forecast API designed by Guido Brini</p>
        <ul>
            <li><a href="/admin/">Administration panel</a></li>
            <li>For information on using the API, please refer to the README.md file in the project repository</li>
        </ul>
    """)