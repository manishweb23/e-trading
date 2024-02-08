from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="e-trading")
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from endpoints import user
app.include_router(user.router)

from endpoints import order
app.include_router(order.router)

from endpoints import transaction
app.include_router(transaction.router)

from endpoints import limit
app.include_router(limit.router)

from endpoints import instrument
app.include_router(instrument.router)

from endpoints import watchlist
app.include_router(watchlist.router)


@app.get("/")
async def root():
    return {"message": "Hello Trading Applications!"}