from flask import jsonify, url_for

# url_for allows us to generate html inside python 

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def generate_sitemap(app):
    links = ['/admin/']
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if "/admin/" not in url:
                links.append(url)

    links_html = "".join(["<li><a href='" + y + "' style='color: white';>" + y + "</a></li>" for y in links])
    return """
        <body style="text-align: center; background: black; color: white">
        <div>
        <img src="https://wikiwandv2-19431.kxcdn.com/_next/image?url=https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Star_Wars_Logo.svg/langes-1500px-Star_Wars_Logo.svg.png&w=1200&q=50" width="325" height="200" alt="Star Wars Logo" style="margin-bottom: 10px">
        <br>
        <h1 style="color: yellow">The API Awakens</h1>
        <p style="font-size: 18px">API HOST: <script>document.write('<input style="padding: 5px; width: 300px" type="text" value="'+window.location.href+'" />');</script></p>
        <p style="font-size: 18px">Start working on your proyect by following the <a href="https://start.4geeksacademy.com/starters/flask" target="_blank">Quick Start</a></p>
        <p style="font-size: 18px">Remember to specify a real endpoint path like: </p>
        <ul style="text-align: center; list-style-type: none; font-size: 18px">"""+links_html+"</ul></div></body>"

    # Parte visual del API live 
    # All styles have to be inline here 
    # Gastón: added html head and body in order to affect styling 