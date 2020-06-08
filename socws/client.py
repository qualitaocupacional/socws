# Copyright 2020, Qualita Seguranca e Saude Ocupacional. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""SOC Web Service Client

"""
import json

from datetime import (
    datetime,
    timedelta
)

from zeep import Client
from zeep.wsse.username import UsernameToken
from zeep.wsse import utils


class SOCWebService(object):
    WSDL_URI = ''
    
    def __init__(self, username, password, user_id, user_incharge_id, main_company_id=None, homologation=False):
        self.username = username
        self.password = password
        self.user_id = user_id
        self.user_incharge_id = user_incharge_id
        self.homologation = homologation
        if main_company_id is None:
            self.main_company_id = self.username
        else:
            self.main_company_id = main_company_id
    
    def _client(self):
        timestamp_token = utils.WSU('Timestamp')
        # created = datetime.now()
        created = datetime.utcnow()
        expires = created + timedelta(seconds=70)
        timestamp_token.append(utils.WSU('Created', utils.get_timestamp(created)))
        timestamp_token.append(utils.WSU('Expires', utils.get_timestamp(expires)))
        return Client(
            self.WSDL_URI,
            wsse=UsernameToken(
                self.username,
                self.password,
                use_digest=True,
                timestamp_token=timestamp_token,
                created=created
            )
        )

    def _ws_body_auth(self):
        return {
            'identificacaoWsVo': {
                'codigoEmpresaPrincipal': self.main_company_id,
                'chaveAcesso': self.password,
                'codigoResponsavel': self.user_incharge_id,
                'codigoUsuario': self.user_id,
                'homologacao': self.homologation
            },
        }

    def _search_type_rules(self):
        return [
            ('codigo', 'CODIGO'),
            ('codigoRh', 'CODIGO_RH'),
            ('nome', 'NOME'),
            ('razaoSocial', 'RAZAO_SOCIAL')
        ]
    
    def _search_type(self, params):
        rules = self._search_type_rules()
        for k in params:
            for r in rules:
                if k == r[0]:
                    return r[1]
        return None

    def _default_request(self, service_name, arg_name, params):
        ws_body = self._ws_body_auth()
        ws_body.update(params)
        arg0 = {
            arg_name: ws_body
        }
        ws_client = self._client()
        ws_response = getattr(ws_client.service, service_name)(**arg0)
        del ws_client
        return ws_response


class Company(SOCWebService):
    WSDL_URI = 'https://ws1.soc.com.br/WSSoc/EmpresaWs?wsdl'

    def add(self, params):
        return self._default_request(
            service_name='incluirEmpresa',
            arg_name='IncluirEmpresaWsVo',
            params=params
        )

    def update(self, params):
        # params['tipoBusca'] = self._search_type(params)
        return self._default_request(
            service_name='alterarEmpresa',
            arg_name='AlterarEmpresaWsVo',
            params=params
        )


class Unit(SOCWebService):
    WSDL_URI = 'https://ws1.soc.com.br/WSSoc/services/UnidadeWs?wsdl'

    def get(self, params):
        params['tipoBusca'] = self._search_type(params)
        # ws_response = ws_client.create_message(ws_client.service, 'consultarUnidade', unidade=ws_body)
        return self._default_request(
            service_name='consultarUnidade',
            arg_name='unidade',
            params=params
        )

    def add(self, params):
        # ws_response = ws_client.create_message(ws_client.service, 'incluirUnidade', unidade=ws_body)
        return self._default_request(
            service_name='incluirUnidade',
            arg_name='unidade',
            params=params
        )

    def update(self, params):
        return self._default_request(
            service_name='alterarUnidade',
            arg_name='unidade',
            params=params
        )

# class Sector(SOCWebService):
#     WSDL_URI = ''

# class EmployeeJob(SOCWebService):
#     WSDL_URI = ''

class Employee(SOCWebService):
    WSDL_URI = 'https://ws1.soc.com.br/WSSoc/FuncionarioModelo2Ws?wsdl'

    def import_employee(self, params):
        return self._default_request(
            service_name='importacaoFuncionario',
            arg_name='Funcionario',
            params=params
        )


# class ExaminationResult(SOCWebService):
#     WSDL_URI = 'https://ws1.soc.com.br/WSSoc/services/ResultadoExamesWs?wsdl'


class DataExport(SOCWebService):
    WSDL_URI = 'https://ws1.soc.com.br/WSSoc/services/ExportaDadosWs?wsdl'

    def request(self, params):
        ws_body = {
            'parametros': json.dumps(params, ensure_ascii=False),
            'erro': True
        }
        ws_client = self._client()
        ws_response = ws_client.service.exportaDadosWs(arg0=ws_body)
        del ws_client
        return ws_response
