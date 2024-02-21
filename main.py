from fastapi import FastAPI, HTTPException, Request, Depends
import jwt
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from utils import verify_token, public_url

app = FastAPI(title="e-trading")

@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    # Code to be executed before the request is processed by the route handler
    print("Before request")
    req_url = str(request.url).split("/")
    print(req_url)
    try:
        inst_url = req_url[5]
        print(inst_url)
    except Exception:
        inst_url = None
    req_url = "/".join(req_url[5:])
    if req_url not in public_url and inst_url != 'instrument':
        try:
            token_data = await verify_token(request.headers)
            # request.state.user_id
            if token_data:
                request.state.user_id = token_data['id']
            else:
                return JSONResponse(content={'data':{'message':'invalide token!'}}, status_code=401)
            
        except Exception as e:
            print(e)
    response = await call_next(request)  # Pass the request to the next middleware or route handler

    # Code to be executed after the request is processed by the route handler
    print("After request")

    return response

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