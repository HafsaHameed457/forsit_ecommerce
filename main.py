from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from connections.database import Base, engine, get_db
from utlis.res import create_success_response
from routers import sales
from routers import inventory


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all database tables on startup
    Base.metadata.create_all(bind=engine)
    get_db()
    print("✅ Server started - Database tables initialized")
    
    yield
    
    print("🛑 Server shutting down")

app = FastAPI(
    lifespan=lifespan,
    root_path="/api/forsit",
    redirect_slashes=False,
    title="Forsit Mall API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(sales.router, prefix="/sales")
app.include_router(inventory.router, prefix="/inventory")



@app.get("/")
async def root(request: Request):

    return create_success_response(200,
                                   content={
            "message": "Welcome to Forsit Mall",
            
        }
    )
