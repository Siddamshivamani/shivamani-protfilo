
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", name="home")
def home(request: Request):

    theme = request.cookies.get("theme", "dark")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"theme": theme}
    )


@app.post("/toggle-theme", name="toggle_theme")
def toggle_theme(request: Request):

    current_theme = request.cookies.get("theme", "dark")

    new_theme = "light" if current_theme == "dark" else "dark"

    response = RedirectResponse(
        url="/",
        status_code=303
    )

    response.set_cookie(
        key="theme",
        value=new_theme,
        httponly=True,
        samesite="lax",
        path="/"
    )

    return response
