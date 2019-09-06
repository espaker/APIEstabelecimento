#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import signal

from flask import Flask, request
from flask_cors import CORS
from logging.handlers import RotatingFileHandler
from cheroot.wsgi import Server as WSGIServer
from cheroot.ssl.builtin import BuiltinSSLAdapter

from Classes.Utils import Utils
from Classes.Parser import Parser
from Classes.RequestFormater import RequestFormatter
from Classes.Cache_control import CacheControl
from Classes.JsonWorker import JsonFormater
from Classes.Database import Database

app_version = '1.0.1'

token = None
server = None
database = None

cache_control = CacheControl()
json_result = JsonFormater.json_result

app = Flask(__name__)
CORS(app)


@app.route('/api/v1/Estabelecimento', methods=['GET'])
def get_estabelecimentos():
    global database
    log_main.info('--> /api/v1/Estabelecimento [GET]')
    try:
        tkn = request.headers['token_auth']
        if token == tkn:
            try:
                result = database.query_exec('SELECT * FROM estabelecimentos;')
                if result['State']:
                    if result['Result']:
                        return json_result(200, {'state': 'Sucess', 'message': result['Result']})
                    else:
                        return json_result(200, {'state': 'Sucess', 'message': 'Não existem estabelecimentos cadastrados'})
                else:
                    log_main.exception('--> /api/v1/Estabelecimento [GET]: [{}]'.format(result['Result']))
                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
                return json_result(200, {'state': 'Sucess', 'message': result})
            except Exception as e:
                log_main.exception('--> /api/v1/Estabelecimento [GET]: [{}]'.format(e))
                return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Invalido'})
    except:
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Não Informado'})


@app.route('/api/v1/Estabelecimento', methods=['POST'])
def post_estabelecimento():
    global database
    log_main.info('--> /api/v1/Estabelecimento [POST]')
    try:
        tkn = request.headers['token_auth']
        if token == tkn:
            try:
                idEstabelecimento = request.json.get('idEstabelecimento', None)
                try:
                    idEstabelecimento = int(idEstabelecimento)
                except:
                    return json_result(400, {'state': 'Bad Request', 'message': "idEstabelecimento inválido"})

                nmEstabelecimento = request.json.get('nmEstabelecimento', None)
                if not nmEstabelecimento:
                    return json_result(400, {'state': 'Bad Request', 'message': "nmEstabelecimento inválido"})

                nrCodigoOficial = request.json.get('nrCodigoOficial', None)
                if not nrCodigoOficial:
                    return json_result(400, {'state': 'Bad Request', 'message': "nrCodigoOficial inválido"})

                idPais = request.json.get('idPais', None)
                try:
                    idPais = int(idPais)
                except:
                    return json_result(400, {'state': 'Bad Request', 'message': "idPais inválido"})

                idUf = request.json.get('idUf', None)
                try:
                    idUf = int(idUf)
                except:
                    return json_result(400, {'state': 'Bad Request', 'message': "idUf inválido"})

                idMunicipio = request.json.get('idMunicipio', None)
                try:
                    idMunicipio = int(idMunicipio)
                except:
                    return json_result(400, {'state': 'Bad Request', 'message': "idMunicipio inválido"})

                nmLocalidade = request.json.get('nmLocalidade', None)
                if not nmLocalidade:
                    return json_result(400, {'state': 'Bad Request', 'message': "nmLocalidade inválido"})

                nmLocalidade = request.json.get('nmLocalidade', None)
                if not nmLocalidade:
                    return json_result(400, {'state': 'Bad Request', 'message': "nmLocalidade inválido"})

                nrLatitude = request.json.get('nrLatitude', None)
                try:
                    nrLatitude = float(nrLatitude)
                except:
                    return json_result(400, {'state': 'Bad Request', 'message': "nrLatitude inválido"})

                nrLongitude = request.json.get('nrLongitude', None)
                try:
                    nrLongitude = float(nrLongitude)
                except:
                    return json_result(400, {'state': 'Bad Request', 'message': "nrLongitude inválido"})

                stAtivo = request.json.get('stAtivo', None)
                try:
                    stAtivo = int(bool(stAtivo) == True)
                except:
                    return json_result(400, {'state': 'Bad Request', 'message': "stAtivo inválido"})

                idCliente = request.json.get('idCliente', None)
                try:
                    idCliente = int(idCliente)
                except:
                    return json_result(400, {'state': 'Bad Request', 'message': "idCliente inválido"})

                result = database.query_exec('SELECT * FROM Estabelecimentos WHERE idEstabelecimento = {};'.format(idEstabelecimento))
                if result['State']:
                    if result['Result']:
                        result = database.query_exec("UPDATE Estabelecimentos SET "
                                                         "nmEstabelecimento = '{}', "
                                                         "nrCodigoOficial = '{}', "
                                                         "idPais = {}, "
                                                         "idUf = {}, "
                                                         "idMunicipio = {}, "
                                                         "nmLocalidade = '{}', "
                                                         "nrLatitude = {}, "
                                                         "nrLongitude = {}, "
                                                         "stAtivo = {}, "
                                                         "idCliente = {} "
                                                     "WHERE idEstabelecimento = {}".format(
                                                                                           nmEstabelecimento,
                                                                                           nrCodigoOficial,
                                                                                           idPais,
                                                                                           idUf,
                                                                                           idMunicipio,
                                                                                           nmLocalidade,
                                                                                           nrLatitude,
                                                                                           nrLongitude,
                                                                                           stAtivo,
                                                                                           idCliente,
                                                                                           idEstabelecimento))
                        if result['State']:
                            return json_result(200,
                                               {'state': 'Sucess', 'message': 'Estabelecimento atualizado com sucesso'})
                        else:
                            log_main.exception('--> /api/v1/Estabelecimento [POST]: [{}]'.format(result['Result']))
                            return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
                    else:
                        result = database.query_exec("INSERT INTO Estabelecimentos ("
                                                        "idEstabelecimento, "
                                                        "nmEstabelecimento, "
                                                        "nrCodigoOficial, "
                                                        "idPais, "
                                                        "idUf, "
                                                        "idMunicipio, "
                                                        "nmLocalidade, "
                                                        "nrLatitude, "
                                                        "nrLongitude, "
                                                        "stAtivo, "
                                                        "idCliente"
                                                     ") VALUES ("
                                                         "{}, "
                                                         "'{}', "
                                                         "'{}', "
                                                         "{}, "
                                                         "{}, "
                                                         "{}, "
                                                         "'{}', "
                                                         "{}, "
                                                         "{}, "
                                                         "{}, "
                                                         "{}"
                                                     ");".format(idEstabelecimento,
                                                                nmEstabelecimento,
                                                                nrCodigoOficial,
                                                                idPais,
                                                                idUf,
                                                                idMunicipio,
                                                                nmLocalidade,
                                                                nrLatitude,
                                                                nrLongitude,
                                                                stAtivo,
                                                                idCliente))
                        if result['State']:
                            return json_result(200, {'state': 'Sucess', 'message': 'Estabelecimento inserido com sucesso'})
                        else:
                            log_main.exception('--> /api/v1/Estabelecimento [POST]: [{}]'.format(result['Result']))
                            return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
            except Exception as e:
                log_main.exception('--> /api/v1/Estabelecimento [POST]: [{}]'.format(e))
                return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Invalido'})
    except:
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Não Informado'})


@app.route('/api/v1/Estabelecimento/<int:id>', methods=['GET'])
def get_estabelecimento(id):
    global database
    log_main.info('--> /api/v1/Estabelecimento/{} [GET]'.format(id))
    try:
        tkn = request.headers['token_auth']
        if token == tkn:
            try:
                result = database.query_exec('SELECT * FROM estabelecimentos WHERE idEstabelecimento = {};'.format(id))
                if result['State']:
                    if result['Result']:
                        return json_result(200, {'state': 'Sucess', 'message': result['Result']})
                    else:
                        return json_result(200, {'state': 'Sucess', 'message': 'Id Consultado não existe!'})
                else:
                    log_main.exception('--> /api/v1/Estabelecimento/{} [GET]: [{}]'.format(id, result['Result']))
                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
            except Exception as e:
                log_main.exception('--> /api/v1/Estabelecimento/{} [GET]: [{}]'.format(id, e))
                return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Invalido'})
    except:
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Não Informado'})


@app.route('/api/v1/Estabelecimento/<int:id>', methods=['PUT'])
def put_estabelecimento(id):
    global database
    log_main.info('--> /api/v1/Estabelecimento/{} [PUT]'.format(id))
    try:
        tkn = request.headers['token_auth']
        if token == tkn:
            try:
                result = database.query_exec('INSERT INTO estabelecimentos (idEstabelecimento) VALUES ({})'.format(id))
                if result['State']:
                    return json_result(200, {'state': 'Sucess', 'message': 'Id inserido com sucesso'})
                elif str(result['Result']) == "UNIQUE constraint failed: estabelecimentos.idEstabelecimento":
                    return json_result(400, {'state': 'Bad Request', 'message': "O Id já existe"})
                else:
                    log_main.exception('--> /api/v1/Estabelecimento/{} [PUT]: [{}]'.format(id, result['Result']))
                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
            except Exception as e:
                log_main.exception('--> /api/v1/Estabelecimento/{} [PUT]: [{}]'.format(id, e))
                return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Invalido'})
    except:
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Não Informado'})


@app.route('/api/v1/Estabelecimento/<int:id>/Produtor', methods=['GET'])
def get_produtores_using_estabelecimento(id):
    global database
    log_main.info('--> /api/v1/Estabelecimento/{}/Produtor [GET]'.format(id))
    try:
        tkn = request.headers['token_auth']
        if token == tkn:
            try:
                result = database.query_exec(
                    'SELECT * FROM Estabelecimentos WHERE idEstabelecimento = {};'.format(id))
                if result['State']:
                    if result['Result']:
                        result = database.query_exec('SELECT * FROM produtores WHERE cdEstabelecimento = {};'.format(id))
                        if result['State']:
                            if result['Result']:
                                return json_result(200, {'state': 'Sucess', 'message': result['Result']})
                            else:
                                return json_result(200, {'state': 'Sucess', 'message': 'Não existem produtores cadastrados nesse estabelecimento'})
                    else:
                        return json_result(400, {'state': 'Bad Request',
                                                 'message': 'O estabelecimento informado não existe'})
                else:
                    log_main.exception('--> /api/v1/Estabelecimento/{}/Produtor [GET]: [{}]'.format(id, result['Result']))
                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
            except Exception as e:
                log_main.exception('--> /api/v1/Estabelecimento/{}/Produtor [GET]: [{}]'.format(id, e))
                return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Invalido'})
    except:
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Não Informado'})

@app.route('/api/v1/Estabelecimento/<int:id>/produtor', methods=['POST'])
def post_produtor_using_estabelecimento(id):
    global database
    log_main.info('--> /api/v1/Estabelecimento/{}/produtor [POST]'.format(id))
    try:
        tkn = request.headers['token_auth']
        if token == tkn:
            try:
                result = database.query_exec(
                    'SELECT * FROM Estabelecimentos WHERE idEstabelecimento = {};'.format(id))
                if result['State']:
                    if result['Result']:
                        idProdutor = request.json.get('idProdutor', None)
                        try:
                            idProdutor = int(idProdutor)
                        except:
                            return json_result(400, {'state': 'Bad Request', 'message': "idProdutor inválido"})

                        nrDocumento = request.json.get('nrDocumento', None)
                        if not nrDocumento:
                            return json_result(400, {'state': 'Bad Request', 'message': "nrDocumento inválido"})

                        nmProdutor = request.json.get('nmProdutor', None)
                        if not nmProdutor:
                            return json_result(400, {'state': 'Bad Request', 'message': "nmProdutor inválido"})

                        nrTelefone = request.json.get('nrTelefone', None)
                        if not nrTelefone:
                            return json_result(400, {'state': 'Bad Request', 'message': "nrTelefone inválido"})

                        dsEmail = request.json.get('dsEmail', None)
                        if not dsEmail:
                            return json_result(400, {'state': 'Bad Request', 'message': "dsEmail inválido"})

                        cdEstabelecimento = request.json.get('cdEstabelecimento', None)
                        try:
                            cdEstabelecimento = int(cdEstabelecimento)
                        except:
                            return json_result(400, {'state': 'Bad Request', 'message': "cdEstabelecimento inválido"})

                        result = database.query_exec(
                            'SELECT * FROM produtores WHERE idProdutor = {};'.format(idProdutor))
                        if result['State']:
                            if result['Result']:
                                result = database.query_exec(
                                    'SELECT * FROM produtores WHERE idProdutor = {} AND cdEstabelecimento = {};'.format(idProdutor, id))
                                if result['State']:
                                    if result['Result']:
                                        result = database.query_exec("UPDATE produtores SET "
                                                                     "nrDocumento = '{}', "
                                                                     "nmProdutor = '{}', "
                                                                     "nrTelefone = '{}', "
                                                                     "dsEmail = '{}', "
                                                                     "cdEstabelecimento = {} "
                                                                     "WHERE idProdutor = {}".format(nrDocumento,
                                                                                                    nmProdutor,
                                                                                                    nrTelefone,
                                                                                                    dsEmail,
                                                                                                    cdEstabelecimento,
                                                                                                    idProdutor))
                                        if result['State']:
                                            return json_result(200,
                                                               {'state': 'Sucess',
                                                                'message': 'Produtor atualizado com sucesso'})
                                    else:
                                        return json_result(400, {'state': 'Bad Request',
                                                                 'message': 'O produtor informado não está relacionado com este estabelecimento'})

                                else:
                                    log_main.exception('--> --> /api/v1/Estabelecimento/{}/produtor [POST]: [{}]'.format(id, result['Result']))
                                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
                            else:
                                if id == cdEstabelecimento:
                                    result = database.query_exec("INSERT INTO produtores ("
                                                                 "idProdutor, "
                                                                 "nrDocumento, "
                                                                 "nmProdutor, "
                                                                 "nrTelefone, "
                                                                 "dsEmail, "
                                                                 "cdEstabelecimento"
                                                                 ") VALUES ("
                                                                 "{}, "
                                                                 "'{}', "
                                                                 "'{}', "
                                                                 "'{}', "
                                                                 "'{}', "
                                                                 "{}"
                                                                 ");".format(idProdutor,
                                                                             nrDocumento,
                                                                             nmProdutor,
                                                                             nrTelefone,
                                                                             dsEmail,
                                                                             cdEstabelecimento))
                                else:
                                    return json_result(400, {'state': 'Bad Request',
                                                             'message': 'O Id de estabelecimento informado na URL é diferente do cdEstabelecimento'})

                                if result['State']:
                                    return json_result(200, {'state': 'Sucess',
                                                             'message': 'Produtor inserido com sucesso'})
                                else:
                                    log_main.exception('--> /api/v1/Estabelecimento/{}/produtor [POST]: [{}]'.format(id, result['Result']))
                                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
                    else:
                        return json_result(400, {'state': 'Bad Request',
                                                 'message': 'O estabelecimento informado não existe'})
                else:
                    log_main.exception('--> /api/v1/Estabelecimento/{}/produtor [POST]: [{}]'.format(id, result['Result']))
                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
            except Exception as e:
                log_main.exception('--> /api/v1/Estabelecimento/{}/produtor [POST]: [{}]'.format(id, e))
                return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Invalido'})
    except:
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Não Informado'})


@app.route('/api/v1/Estabelecimento/<int:id>/produtor/<int:idprodutor>', methods=['DELETE'])
def delete_produtor(id, idprodutor):
    global database
    log_main.info('--> /api/v1/Estabelecimento/{}/produtor/{} [DELETE]'.format(id, idprodutor))
    try:
        tkn = request.headers['token_auth']
        if token == tkn:
            try:
                result = database.query_exec('SELECT * FROM estabelecimentos WHERE idEstabelecimento = {};'.format(id))
                if result['State']:
                    if result['Result']:
                        result = database.query_exec(
                            'SELECT * FROM produtores WHERE idProdutor = {};'.format(idprodutor))
                        if result['State']:
                            if result['Result']:
                                result = database.query_exec(
                                    'SELECT * FROM estabelecimentos WHERE idEstabelecimento = {};'.format(id))
                                if result['State']:
                                    if result['Result']:
                                        result = database.query_exec(
                                            'DELETE FROM produtores WHERE idProdutor = {};'.format(idprodutor))
                                        if result['State']:
                                            return json_result(200, {'state': 'Sucess', 'message': 'Produtor removido com sucesso!'})
                                        else:
                                            log_main.exception(
                                                '--> /api/v1/Estabelecimento/{}/produtor/{} [DELETE]: [{}]'.format(id,
                                                                                                                   idprodutor,
                                                                                                                   result[
                                                                                                                       'Result']))
                                            return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
                            else:
                                return json_result(200, {'state': 'Sucess',
                                                         'message': 'O produtor informado não existe!'})
                        else:
                            log_main.exception(
                                '--> /api/v1/Estabelecimento/{}/produtor/{} [DELETE]: [{}]'.format(id, idprodutor,
                                                                                                   result['Result']))
                            return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
                    else:
                        return json_result(200, {'state': 'Sucess', 'message': 'O estabelecimento informado não existe!'})
                else:
                    log_main.exception('--> /api/v1/Estabelecimento/{}/produtor/{} [DELETE]: [{}]'.format(id, idprodutor, result['Result']))
                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
            except Exception as e:
                log_main.exception('--> /api/v1/Estabelecimento/{}/produtor/{} [DELETE]: [{}]'.format(id, idprodutor, e))
                return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Invalido'})
    except:
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Não Informado'})


@app.route('/api/v1/Estabelecimento/<int:id>/unidadeExploracao', methods=['POST'])
def post_unidadeExploracao(id):
    global database
    log_main.info('--> /api/v1/Estabelecimento/{}/unidadeExploracao [POST]'.format(id))
    try:
        tkn = request.headers['token_auth']
        if token == tkn:
            try:
                result = database.query_exec(
                    'SELECT * FROM Estabelecimentos WHERE idEstabelecimento = {};'.format(id))
                if result['State']:
                    if result['Result']:
                        idUnidadeExploracao = request.json.get('idUnidadeExploracao', None)
                        try:
                            idUnidadeExploracao = int(idUnidadeExploracao)
                        except:
                            return json_result(400, {'state': 'Bad Request', 'message': "idUnidadeExploracao inválido"})

                        nrUnidadeExploracao = request.json.get('nrUnidadeExploracao', None)
                        try:
                            nrUnidadeExploracao = int(nrUnidadeExploracao)
                        except:
                            return json_result(400, {'state': 'Bad Request', 'message': "nrUnidadeExploracao inválido"})

                        cdEstabelecimento = request.json.get('cdEstabelecimento', None)
                        try:
                            cdEstabelecimento = int(cdEstabelecimento)
                        except:
                            return json_result(400, {'state': 'Bad Request', 'message': "cdEstabelecimento inválido"})

                        qtCapacidadeAlojamento = request.json.get('qtCapacidadeAlojamento', None)
                        try:
                            qtCapacidadeAlojamento = int(qtCapacidadeAlojamento)
                        except:
                            return json_result(400, {'state': 'Bad Request', 'message': "qtCapacidadeAlojamento inválido"})

                        csTipoUnidadeExploracao = request.json.get('csTipoUnidadeExploracao', None)
                        if not csTipoUnidadeExploracao:
                            return json_result(400, {'state': 'Bad Request', 'message': "csTipoUnidadeExploracao inválido"})

                        stAtiva = request.json.get('stAtiva', None)
                        try:
                            stAtiva = int(bool(stAtiva) == True)
                        except:
                            return json_result(400, {'state': 'Bad Request', 'message': "stAtiva inválido"})

                        csTipoAnimal = request.json.get('csTipoAnimal', None)
                        if not csTipoAnimal:
                            return json_result(400,
                                               {'state': 'Bad Request', 'message': "csTipoAnimal inválido"})

                        result = database.query_exec(
                            'SELECT * FROM UnidadeExploracao WHERE idUnidadeExploracao = {};'.format(idUnidadeExploracao))
                        if result['State']:
                            if result['Result']:
                                result = database.query_exec(
                                    'SELECT * FROM UnidadeExploracao WHERE idUnidadeExploracao = {} AND cdEstabelecimento = {};'.format(idUnidadeExploracao, id))
                                if result['State']:
                                    if result['Result']:
                                        result = database.query_exec("UPDATE UnidadeExploracao SET "
                                                                     "nrUnidadeExploracao = {}, "
                                                                     "cdEstabelecimento = {}, "
                                                                     "qtCapacidadeAlojamento = {}, "
                                                                     "csTipoUnidadeExploracao = '{}', "
                                                                     "stAtiva = {}, "
                                                                     "csTipoAnimal = '{}'"
                                                                     "WHERE idUnidadeExploracao = {}".format(nrUnidadeExploracao,
                                                                                                    cdEstabelecimento,
                                                                                                    qtCapacidadeAlojamento,
                                                                                                    csTipoUnidadeExploracao,
                                                                                                    stAtiva,
                                                                                                    csTipoAnimal,
                                                                                                    idUnidadeExploracao))
                                        if result['State']:
                                            return json_result(200,
                                                               {'state': 'Sucess',
                                                                'message': 'Unidade de Expoloração atualizada com sucesso'})
                                    else:
                                        return json_result(400, {'state': 'Bad Request',
                                                                 'message': 'A Unidade de Expoloração informada não está relacionado com este estabelecimento'})

                                else:
                                    log_main.exception('--> --> /api/v1/Estabelecimento/{}/unidadeExploracao [POST]: [{}]'.format(id, result['Result']))
                                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
                            else:
                                if id == cdEstabelecimento:
                                    result = database.query_exec("INSERT INTO UnidadeExploracao ("
                                                                 "idUnidadeExploracao, "
                                                                 "nrUnidadeExploracao, "
                                                                 "cdEstabelecimento, "
                                                                 "qtCapacidadeAlojamento, "
                                                                 "csTipoUnidadeExploracao, "
                                                                 "stAtiva, "
                                                                 "csTipoAnimal"
                                                                 ") VALUES ("
                                                                 "{}, "
                                                                 "{}, "
                                                                 "{}, "
                                                                 "{}, "
                                                                 "'{}', "
                                                                 "{}, "
                                                                 "'{}'"
                                                                 ");".format(idUnidadeExploracao,
                                                                            nrUnidadeExploracao,
                                                                            cdEstabelecimento,
                                                                            qtCapacidadeAlojamento,
                                                                            csTipoUnidadeExploracao,
                                                                            stAtiva,
                                                                            csTipoAnimal))
                                else:
                                    return json_result(400, {'state': 'Bad Request',
                                                             'message': 'O Id de estabelecimento informado na URL é diferente do cdEstabelecimento'})

                                if result['State']:
                                    return json_result(200, {'state': 'Sucess',
                                                             'message': 'Unidade de Exploração inserida com sucesso'})
                                else:
                                    log_main.exception('--> /api/v1/Estabelecimento/{}/produtor [POST]: [{}]'.format(id, result['Result']))
                                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
                    else:
                        return json_result(400, {'state': 'Bad Request',
                                                 'message': 'O estabelecimento informado não existe'})
                else:
                    log_main.exception('--> /api/v1/Estabelecimento/{}/unidadeExploracao [POST]: [{}]'.format(id, result['Result']))
                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
            except Exception as e:
                log_main.exception('--> /api/v1/Estabelecimento/{}/unidadeExploracao [POST]: [{}]'.format(id, e))
                return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Invalido'})
    except:
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Não Informado'})


@app.route('/api/v1/Estabelecimento/<int:id>/unidadeExploracao/<int:idUep>', methods=['DELETE'])
def delete_unidadeExploracao(id, idUep):
    global database
    log_main.info('--> /api/v1/Estabelecimento/{}/unidadeExploracao/{} [DELETE]'.format(id, idUep))
    try:
        tkn = request.headers['token_auth']
        if token == tkn:
            try:
                result = database.query_exec('SELECT * FROM estabelecimentos WHERE idEstabelecimento = {};'.format(id))
                if result['State']:
                    if result['Result']:
                        result = database.query_exec(
                            'SELECT * FROM UnidadeExploracao WHERE idUnidadeExploracao = {};'.format(idUep))
                        if result['State']:
                            if result['Result']:
                                result = database.query_exec(
                                    'SELECT * FROM estabelecimentos WHERE idEstabelecimento = {};'.format(id))
                                if result['State']:
                                    if result['Result']:
                                        result = database.query_exec(
                                            'DELETE FROM UnidadeExploracao WHERE idUnidadeExploracao = {};'.format(idUep))
                                        if result['State']:
                                            return json_result(200, {'state': 'Sucess', 'message': 'Unidade de Exploração removida com sucesso!'})
                                        else:
                                            log_main.exception(
                                                '--> /api/v1/Estabelecimento/{}/unidadeExploracao/{} [DELETE]: [{}]'.format(id,
                                                                                                                   idUep,
                                                                                                                   result[
                                                                                                                       'Result']))
                                            return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
                            else:
                                return json_result(200, {'state': 'Sucess',
                                                         'message': 'A Unidade de Exploração informada não existe!'})
                        else:
                            log_main.exception(
                                '--> /api/v1/Estabelecimento/{}/unidadeExploracao/{} [DELETE]: [{}]'.format(id, idUep,
                                                                                                   result['Result']))
                            return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
                    else:
                        return json_result(200, {'state': 'Sucess', 'message': 'O estabelecimento informado não existe!'})
                else:
                    log_main.exception('--> /api/v1/Estabelecimento/{}/unidadeExploracao/{} [DELETE]: [{}]'.format(id, idUep, result['Result']))
                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
            except Exception as e:
                log_main.exception('--> /api/v1/Estabelecimento/{}/unidadeExploracao/{} [DELETE]: [{}]'.format(id, idUep, e))
                return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Invalido'})
    except:
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Não Informado'})


@app.route('/api/v1/Estabelecimento/<int:id>/unidadeExploracao', methods=['GET'])
def get_unidadeExploracao_using_estabelecimento(id):
    global database
    log_main.info('--> /api/v1/Estabelecimento/{}/unidadeExploracao [GET]'.format(id))
    try:
        tkn = request.headers['token_auth']
        if token == tkn:
            try:
                result = database.query_exec(
                    'SELECT * FROM Estabelecimentos WHERE idEstabelecimento = {};'.format(id))
                if result['State']:
                    if result['Result']:
                        result = database.query_exec('SELECT * FROM UnidadeExploracao WHERE cdEstabelecimento = {};'.format(id))
                        if result['State']:
                            if result['Result']:
                                return json_result(200, {'state': 'Sucess', 'message': result['Result']})
                            else:
                                return json_result(200, {'state': 'Sucess', 'message': 'Não existem Unidades de Exploração cadastradas nesse estabelecimento'})
                    else:
                        return json_result(400, {'state': 'Bad Request',
                                                 'message': 'O estabelecimento informado não existe'})
                else:
                    log_main.exception('--> /api/v1/Estabelecimento/{}/unidadeExploracao [GET]: [{}]'.format(id, result['Result']))
                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
            except Exception as e:
                log_main.exception('--> /api/v1/Estabelecimento/{}/unidadeExploracao [GET]: [{}]'.format(id, e))
                return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Invalido'})
    except:
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Não Informado'})


@app.route('/api/v1/Estabelecimento/<int:id>/unidadeExploracao/<int:idUep>/ativar', methods=['PUT'])
def put_unidadeExploracao_using_estabelecimento_ativar(id, idUep):
    global database
    log_main.info('--> /api/v1/Estabelecimento/{}/unidadeExploracao/{}/ativar [PUT]'.format(id, idUep))
    try:
        tkn = request.headers['token_auth']
        if token == tkn:
            try:
                result = database.query_exec(
                    'SELECT * FROM Estabelecimentos WHERE idEstabelecimento = {};'.format(id))
                if result['State']:
                    if result['Result']:
                        result = database.query_exec('SELECT * FROM UnidadeExploracao WHERE idUnidadeExploracao = {};'.format(idUep))
                        if result['State']:
                            if result['Result']:
                                result = database.query_exec(
                                    'SELECT * FROM UnidadeExploracao WHERE cdEstabelecimento = {};'.format(id))
                                if result['State']:
                                    if result['Result']:
                                        result = database.query_exec(
                                            'SELECT * FROM UnidadeExploracao WHERE idUnidadeExploracao = {} AND stAtiva = 0;'.format(idUep))
                                        if result['State']:
                                            if result['Result']:
                                                result = database.query_exec(
                                                    'UPDATE UnidadeExploracao SET stAtiva = 1 WHERE idUnidadeExploracao = {};'.format(
                                                        idUep))
                                                if result['State']:
                                                    return json_result(200,
                                                                       {'state': 'Sucess',
                                                                        'message': 'Unidade de Exploração ativada com sucesso'})
                                            else:
                                                return json_result(200, {'state': 'Sucess',
                                                                         'message': 'Unidade de Exploração já ativa!'})
                                    else:
                                        return json_result(200, {'state': 'Sucess',
                                                                 'message': 'Unidade de Exploração não está relacionada ao estabelecimento informado'})
                            else:
                                return json_result(200, {'state': 'Sucess', 'message': 'Unidade de Exploração informada não existe'})
                    else:
                        return json_result(400, {'state': 'Bad Request',
                                                 'message': 'O estabelecimento informado não existe'})
                else:
                    log_main.exception('--> /api/v1/Estabelecimento/{}/unidadeExploracao/{}/ativar [PUT]: [{}]'.format(id, idUep, result['Result']))
                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
            except Exception as e:
                log_main.exception('--> /api/v1/Estabelecimento/{}/unidadeExploracao/{}/ativar [PUT]: [{}]'.format(id, idUep, e))
                return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Invalido'})
    except:
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Não Informado'})


@app.route('/api/v1/Estabelecimento/<int:id>/unidadeExploracao/<int:idUep>/desativar', methods=['PUT'])
def put_unidadeExploracao_using_estabelecimento_desativar(id, idUep):
    global database
    log_main.info('--> /api/v1/Estabelecimento/{}/unidadeExploracao/{}/desativar [PUT]'.format(id, idUep))
    try:
        tkn = request.headers['token_auth']
        if token == tkn:
            try:
                result = database.query_exec(
                    'SELECT * FROM Estabelecimentos WHERE idEstabelecimento = {};'.format(id))
                if result['State']:
                    if result['Result']:
                        result = database.query_exec('SELECT * FROM UnidadeExploracao WHERE idUnidadeExploracao = {};'.format(idUep))
                        if result['State']:
                            if result['Result']:
                                result = database.query_exec(
                                    'SELECT * FROM UnidadeExploracao WHERE cdEstabelecimento = {};'.format(id))
                                if result['State']:
                                    if result['Result']:
                                        result = database.query_exec(
                                            'SELECT * FROM UnidadeExploracao WHERE idUnidadeExploracao = {} AND stAtiva = 1;'.format(idUep))
                                        if result['State']:
                                            if result['Result']:
                                                result = database.query_exec(
                                                    'UPDATE UnidadeExploracao SET stAtiva = 0 WHERE idUnidadeExploracao = {};'.format(
                                                        idUep))
                                                if result['State']:
                                                    return json_result(200,
                                                                       {'state': 'Sucess',
                                                                        'message': 'Unidade de Exploração desativada com sucesso'})
                                            else:
                                                return json_result(200, {'state': 'Sucess',
                                                                         'message': 'Unidade de Exploração já inativa!'})
                                    else:
                                        return json_result(200, {'state': 'Sucess',
                                                                 'message': 'Unidade de Exploração não está relacionada ao estabelecimento informado'})
                            else:
                                return json_result(200, {'state': 'Sucess', 'message': 'Unidade de Exploração informada não existe'})
                    else:
                        return json_result(400, {'state': 'Bad Request',
                                                 'message': 'O estabelecimento informado não existe'})
                else:
                    log_main.exception('--> /api/v1/Estabelecimento/{}/unidadeExploracao/{}/desativar [PUT]: [{}]'.format(id, idUep, result['Result']))
                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
            except Exception as e:
                log_main.exception('--> /api/v1/Estabelecimento/{}/unidadeExploracao/{}/desativar [PUT]: [{}]'.format(id, idUep, e))
                return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Invalido'})
    except:
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Não Informado'})


@app.route('/api/v1/Produtor/<int:id>', methods=['GET'])
def get_produtor(id):
    global database
    log_main.info('--> /api/v1/Produtor/{} [GET]'.format(id))
    try:
        tkn = request.headers['token_auth']
        if token == tkn:
            try:
                result = database.query_exec('SELECT * FROM produtores WHERE idProdutor = {};'.format(id))
                if result['State']:
                    if result['Result']:
                        return json_result(200, {'state': 'Sucess', 'message': result['Result']})
                    else:
                        return json_result(200, {'state': 'Sucess', 'message': 'Id Consultado não existe!'})
                else:
                    log_main.exception('--> /api/v1/Produtor/{} [GET]: [{}]'.format(id, result['Result']))
                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
            except Exception as e:
                log_main.exception('--> /api/v1/Produtor/{} [GET]: [{}]'.format(id, e))
                return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Invalido'})
    except:
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Não Informado'})


@app.route('/api/v1/Produtor/<int:id>', methods=['PUT'])
def put_produtor(id):
    global database
    log_main.info('--> /api/v1/Produtor/{} [PUT]'.format(id))
    try:
        tkn = request.headers['token_auth']
        if token == tkn:
            try:
                result = database.query_exec('INSERT INTO produtores (idProdutor) VALUES ({})'.format(id))
                if result['State']:
                    return json_result(200, {'state': 'Sucess', 'message': 'Id inserido com sucesso'})
                elif str(result['Result']) == "UNIQUE constraint failed: produtores.idProdutor":
                    return json_result(400, {'state': 'Bad Request', 'message': "O Id já existe"})
                else:
                    log_main.exception('--> /api/v1/Produtor/{} [PUT]: [{}]'.format(id, result['Result']))
                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
            except Exception as e:
                log_main.exception('--> /api/v1/Produtor/{} [PUT]: [{}]'.format(id, e))
                return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Invalido'})
    except:
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Não Informado'})


@app.route('/api/v1/Produtor', methods=['GET'])
def get_produtores():
    global database
    log_main.info('--> /api/v1/Produtor [GET]')
    try:
        tkn = request.headers['token_auth']
        if token == tkn:
            try:
                result = database.query_exec('SELECT * FROM produtores;')
                if result['State']:
                    if result['Result']:
                        return json_result(200, {'state': 'Sucess', 'message': result['Result']})
                    else:
                        return json_result(200, {'state': 'Sucess', 'message': 'Não existem estabelecimentos cadastrados'})
                else:
                    log_main.exception('--> /api/v1/Produtor [GET]: [{}]'.format(result['Result']))
                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
                return json_result(200, {'state': 'Sucess', 'message': result})
            except Exception as e:
                log_main.exception('--> /api/v1/Produtor [GET]: [{}]'.format(e))
                return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Invalido'})
    except:
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Não Informado'})


@app.route('/api/v1/Produtor', methods=['POST'])
def post_produtor():
    global database
    log_main.info('--> /api/v1/Produtor [POST]'.format(id))
    try:
        tkn = request.headers['token_auth']
        if token == tkn:
            try:
                idProdutor = request.json.get('idProdutor', None)
                try:
                    idProdutor = int(idProdutor)
                except:
                    return json_result(400, {'state': 'Bad Request', 'message': "idProdutor inválido"})

                nrDocumento = request.json.get('nrDocumento', None)
                if not nrDocumento:
                    return json_result(400, {'state': 'Bad Request', 'message': "nrDocumento inválido"})

                nmProdutor = request.json.get('nmProdutor', None)
                if not nmProdutor:
                    return json_result(400, {'state': 'Bad Request', 'message': "nmProdutor inválido"})

                nrTelefone = request.json.get('nrTelefone', None)
                if not nrTelefone:
                    return json_result(400, {'state': 'Bad Request', 'message': "nrTelefone inválido"})

                dsEmail = request.json.get('dsEmail', None)
                if not dsEmail:
                    return json_result(400, {'state': 'Bad Request', 'message': "dsEmail inválido"})

                cdEstabelecimento = request.json.get('cdEstabelecimento', None)
                try:
                    cdEstabelecimento = int(cdEstabelecimento)
                except:
                    return json_result(400, {'state': 'Bad Request', 'message': "cdEstabelecimento inválido"})

                result = database.query_exec(
                    'SELECT * FROM produtores WHERE idProdutor = {};'.format(idProdutor))
                if result['State']:
                    if result['Result']:
                        result = database.query_exec("UPDATE produtores SET "
                                                     "nrDocumento = '{}', "
                                                     "nmProdutor = '{}', "
                                                     "nrTelefone = '{}', "
                                                     "dsEmail = '{}', "
                                                     "cdEstabelecimento = {} "
                                                     "WHERE idProdutor = {}".format(nrDocumento,
                                                                                    nmProdutor,
                                                                                    nrTelefone,
                                                                                    dsEmail,
                                                                                    cdEstabelecimento,
                                                                                    idProdutor))
                        if result['State']:
                            return json_result(200,
                                               {'state': 'Sucess',
                                                'message': 'Produtor atualizado com sucesso'})
                        else:
                            log_main.exception('--> --> /api/v1/Produtor [POST]: [{}]'.format(result['Result']))
                            return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
                    else:
                        result = database.query_exec("INSERT INTO produtores ("
                                                     "idProdutor, "
                                                     "nrDocumento, "
                                                     "nmProdutor, "
                                                     "nrTelefone, "
                                                     "dsEmail, "
                                                     "cdEstabelecimento"
                                                     ") VALUES ("
                                                     "{}, "
                                                     "'{}', "
                                                     "'{}', "
                                                     "'{}', "
                                                     "'{}', "
                                                     "{}"
                                                     ");".format(idProdutor,
                                                                 nrDocumento,
                                                                 nmProdutor,
                                                                 nrTelefone,
                                                                 dsEmail,
                                                                 cdEstabelecimento))
                        if result['State']:
                            return json_result(200, {'state': 'Sucess',
                                                     'message': 'Produtor inserido com sucesso'})
                        else:
                            log_main.exception('--> /api/v1/Produtor [POST]: [{}]'.format(id, result['Result']))
                            return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})

                else:
                    log_main.exception('--> /api/v1/Produtor [POST]: [{}]'.format(result['Result']))
                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
            except Exception as e:
                log_main.exception('--> /api/v1/Produtor [POST]: [{}]'.format(e))
                return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Invalido'})
    except:
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Não Informado'})


@app.route('/api/v1/unidadeExploracao/<int:id>', methods=['GET'])
def get_unidadeExploracao(id):
    global database
    log_main.info('--> /api/v1/unidadeExploracao/{} [GET]'.format(id))
    try:
        tkn = request.headers['token_auth']
        if token == tkn:
            try:
                result = database.query_exec('SELECT * FROM UnidadeExploracao WHERE idUnidadeExploracao = {};'.format(id))
                if result['State']:
                    if result['Result']:
                        return json_result(200, {'state': 'Sucess', 'message': result['Result']})
                    else:
                        return json_result(200, {'state': 'Sucess', 'message': 'Id Consultado não existe!'})
                else:
                    log_main.exception('--> /api/v1/unidadeExploracao/{} [GET]: [{}]'.format(id, result['Result']))
                    return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
            except Exception as e:
                log_main.exception('--> /api/v1/unidadeExploracao/{} [GET]: [{}]'.format(id, e))
                return json_result(500, {'state': 'error', 'message': 'Erro Desconhecido'})
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Invalido'})
    except:
        return json_result(401, {'state': 'unauthorized', 'message': 'Token Não Informado'})


def initiate():
    log_main.info('Iniciando a API versão: {}'.format(app_version))

    signal.signal(signal.SIGTERM, finalize)
    signal.signal(signal.SIGINT, finalize)

    global token, database

    token = conf.get('Auth', 'Token', fallback='14acd1c3b2f50c1e7354668f7d0b4057')

    log_main.warning('Iniciando conexão com banco de dados ...')
    try:
        db = os.path.join(workdir, conf.get('Database', 'Database', fallback='data.db'))
        database = Database(db)
    except Exception as e:
        log_main.exception('Erro ao iniciar a conexão com o banco de dados: [{}]'.format(e))

    _port = conf.getint('Flask', 'Port', fallback=8860)
    _host = conf.get('Flask', 'Host', fallback='0.0.0.0')
    _threads = conf.getint('Flask', 'Threads', fallback=100)
    _ssl_cert = os.path.join(workdir, 'SSL', conf.get('Flask', 'SSL_Cert', fallback=''))
    _ssl_key = os.path.join(workdir, 'SSL', conf.get('Flask', 'SSL_Key', fallback=''))
    try:
        _ssl_enabled = os.path.isfile(_ssl_cert) and os.path.isfile(_ssl_key)
    except Exception:
        _ssl_enabled = False

    if len(sys.argv) > 1:
        if sys.argv[1] in ('-v', '--version'):
            print('API')
            print('Versão: {}'.format(app_version))
            sys.exit(0)
        elif sys.argv[1] in ('-d', '--debug'):
            app.run(host=_host, port=_port, threaded=True, debug=True)
        else:
            print('ERRO | Parâmetro desconhecido: {}'.format(sys.argv))
            sys.exit(2)
    else:
        global server
        server = WSGIServer(bind_addr=(_host, _port), wsgi_app=app, numthreads=_threads)
        if _ssl_enabled:
            server.ssl_adapter = BuiltinSSLAdapter(_ssl_cert, _ssl_key)
        server.start()


def finalize(signum, desc):
    global execute, server, database
    log_main.info('Recebi o sinal [{}] Desc [{}], finalizando...'.format(signum, desc))

    log_main.warning('Limpando Cache Control ...')
    cache_control.clear()

    log_main.warning('Encerrando conexão com banco de dados ...')
    database.db_close()

    if server is not None:
        log_main.warning('Parando Serviço ...')
        server.stop()
    if execute:
        execute = False
    else:
        sys.exit(2)


if __name__ == '__main__':
    execute = True
    workdir = Utils.get_workdir()
    conf = Parser(os.path.join(workdir, 'config.ini')).conf_get()
    _level = conf.getint('Debug', 'Level', fallback=3)
    debug_dir = os.path.join(workdir, 'debug')
    log_file_path = os.path.join(debug_dir, 'API.log')
    if not os.path.exists(debug_dir):
        os.mkdir(debug_dir, 0o775)
    log_handler = RotatingFileHandler(log_file_path, maxBytes=1024 * 1024 * 10, backupCount=10)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(RequestFormatter(
        '[%(asctime)s] | %(levelname)s | %(name)s | %(remote_addr)s | %(method)s | %(url)s | %(message)s'))
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(log_handler)
    log_main = logging.getLogger('API:' + str(os.getpid()))
    app.logger.addHandler(log_handler)
    app.debug = True

    initiate()
