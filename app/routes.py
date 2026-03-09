from fastapi import APIRouter
import dal

route = APIRouter(
    prefix='/priority',
    tags=['/priority']
)

@route.get('/')
def get_avg_percent():
    return dal.avg_percent()

@route.get('/percent')
def percent():
    return dal.get_priority()
