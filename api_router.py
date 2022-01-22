from urllib import response
from fastapi import APIRouter
#from home_assistant import home_assistant
from client_copy import ApiRpcClient
from client import ApiRpcClientPost
from measurer import Measurer
from Models.Estado_model import Model
router = APIRouter()

@router.get('/')
def test():
    return 'API is running'


@router.get('/temperature')
def obterTemperatura():
    print("Tomando a temperatura")
    rpc = ApiRpcClient('temp')
    response = rpc.call()
    print("Resposta")
    print(response)
    return response


@router.get('/ligh')
def obterLuminosidade():
    print("Tomando a luminosidade")
    rpc = ApiRpcClient('light')
    response = rpc.call()
    print("Resposta")
    print(response)
    return response

@router.get('/hum')
def obterHumidaade():
    print("Tomando a humidade")
    rpc = ApiRpcClient('hum')
    response = rpc.call()
    print("Resposta")
    print(response)
    return response


@router.post('/air')
def alterarTemperatura(inputData:Model):
    print("alterando a temperatura")
    rpc = ApiRpcClientPost(inputData.estado, inputData.name)
    response = rpc.call()
    print("Resposta")
    print(response)
    return response


@router.post('/onlight')
def LigaLampada(inputData:Model):
    print("Ligando a Lampada")
    rpc = ApiRpcClientPost("1", inputData.name)
    response = rpc.call()
    print("Resposta")
    print(response)
    return response

@router.post('/offlight')
def DesigaLampada(inputData:Model):
    print("Desligando a Lampada")
    rpc = ApiRpcClientPost("0", inputData.name)
    response = rpc.call()
    print("Resposta")
    print(response)
    return response


@router.post('/offwat')
def DesligaIrrigador(inputData:Model):
    print("Desligando o Irrigador")
    rpc = ApiRpcClientPost("0", inputData.name)
    response = rpc.call()
    print("Resposta")
    print(response)
    return response

@router.post('/onwat')
def LigaIrrigador(inputData:Model):
    print("Ligando o Irrigador")
    rpc = ApiRpcClientPost("1", inputData.name)
    response = rpc.call()
    print("Resposta")
    print(response)
    return response

