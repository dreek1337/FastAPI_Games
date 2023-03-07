from pydantic import BaseModel, validator
from fastapi import FastAPI,Depends
app = FastAPI()


class Test(BaseModel):
    phone: str

    @validator('phone', pre=True)
    def qwe(cls, inf: str):
        res = inf.replace(' ', '+')

        return res


@app.get('/qwe')
async def qwe(a: Test = Depends()):
    return a


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('test:app')
