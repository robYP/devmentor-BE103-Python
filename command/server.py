from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from api.index import init_api_list
from infrastructure.mysql import engine, Base
from fastapi.middleware.cors import CORSMiddleware


class ServerCreator:
    def __init__(self):
        self.app = FastAPI()
        self.init_router()

    def init_router(self):
        # init_example_app(self.app)
        init_api_list(self.app)

    def get_app(self):
        return self.app

    def database_init(self):
        Base.metadata.create_all(bind=engine)


server_creator = ServerCreator()
server_creator.database_init()
app = server_creator.get_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html
@app.get("/")
async def read_index():
    return FileResponse('static/signin.html')

@app.get("/main.html")
async def read_index():
    return FileResponse('static/main.html')