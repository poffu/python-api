import uvicorn
from logic import web_user_logic
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from model import web_user_dto
from auth.auth import AuthHandler

# from mangum import Mangum

app = FastAPI(title="Web User")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

web_user_logic = web_user_logic.WebUserLogic()

auth_handler = AuthHandler()


@app.get('/')
async def Root():
    return {"message": "hello"}


@app.post('/api/login')
async def Login(user: web_user_dto.LoginDto):
    model = web_user_logic.login(user)
    if model is not None:
        token = auth_handler.generate_token(user.email)
        return {
            'token': token
        }
    else:
        raise HTTPException(status_code=400, detail="Username or Password is not correct.")


@app.post('/api/add-user')
async def Insert(user: web_user_dto.InsertDto):
    check = web_user_logic.check_email(0, user.email)
    if check:
        raise HTTPException(status_code=400, detail="Email is exist.")
    return web_user_logic.insert(user)


@app.get('/api/list-user', dependencies=[Depends(auth_handler.validate_token)])
async def GetAllUser(name: str):
    return web_user_logic.get_all_user(name)


@app.get('/api/get-user')
async def GetUser(userId: int):
    return web_user_logic.get_user(userId)


@app.put('/api/edit-user')
async def Update(user: web_user_dto.UpdateDto):
    check = web_user_logic.check_email(user.userId, user.email)
    if check:
        raise HTTPException(status_code=400, detail="Email is exist.")
    return web_user_logic.update(user)


@app.delete('/api/delete-user')
async def Delete(userId: int):
    return web_user_logic.delete(userId)


if __name__ == "__main__":
    uvicorn.run(app)

# handler = Mangum(app)
