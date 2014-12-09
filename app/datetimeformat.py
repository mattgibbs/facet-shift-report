from app import app

@app.template_filter()
def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    return value.strftime(format)