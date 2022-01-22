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
def obterHumidade():
    print("Tomando a humidade")
    rpc = ApiRpcClient('hum')
    response = rpc.call()
    print("Resposta")
    print(response)
    return response

@router.get('/lamp')
def ObterStatusLampada():
    print("Recuperando o Estado da Lampada")
    rpc = ApiRpcClient('Lamp')
    response = rpc.call()
    print("Resposta")
    if(response ==""):
        response = 'OFF'
    print(response)
    return response

@router.get('/air')
def ObterStatusAr():
    print("Recuperando o estado do Ar")
    rpc = ApiRpcClient('Air')
    response = rpc.call()
    print("Resposta")
    if(response ==""):
        response = 'OFF'
    print(response)
    return response

@router.get('/wat')
def obterStatusWat():
    print("Recuperando o estado do Irrigador")
    rpc = ApiRpcClient('Wat')
    response = rpc.call()
    print("Resposta")
    if(response ==""):
        response = 'OFF'
    print(response)
    return response

@router.post('/air')
def alterarTemperatura(inputData:Model):
    print("alterando a temperatura")
    rpc = ApiRpcClientPost(inputData.estado, inputData.name)
    response = rpc.call()
    if(response ==""):
        response = 'OFF'
    print("Resposta")
    print(response)
    return response


@router.post('/onlight')
def ligaLampada(inputData:Model):
    print("Ligando a Lampada")
    rpc = ApiRpcClientPost("1", inputData.name)
    response = rpc.call()
    print("Resposta")
    print(response)
    return response

@router.post('/offlight')
def desigaLampada(inputData:Model):
    print("Desligando a Lampada")
    rpc = ApiRpcClientPost("0", inputData.name)
    response = rpc.call()
    if(response ==""):
        response = 'OFF'
    print("Resposta")
    print(response)
    return response


@router.post('/offwat')
def desligaIrrigador(inputData:Model):
    print("Desligando o Irrigador")
    rpc = ApiRpcClientPost("0", inputData.name)
    response = rpc.call()
    if(response ==""):
        response = 'OFF'
    print("Resposta")
    print(response)
    return response

@router.post('/onwat')
def ligaIrrigador(inputData:Model):
    print("Ligando o Irrigador")
    rpc = ApiRpcClientPost("1", inputData.name)
    response = rpc.call()
    print("Resposta")
    print(response)
    return response

