# SOC Webservices

Biblioteca para auxiliar a utilizar os *webservices* disponíveis do sistema [SOC](https://soc.com.br).

## Instalação

```bash

$ pip install socws
```

## Desenvolvimento


Clonar o repositório:

```bash

$ git clone https://github.com/qualitaocupacional/socws.git
```

Instalar a lib em modo desenvolvimento:

```bash

(virtualenv) user@host:~/socws$ pip install -e .
```

## Usando

```python

import socws

# Ver documentação do SOC para obter as credenciais de autenticação

credentials = {
    'username': 'usuário',
    'password': 'senha',
    'user_id': 'código do usuário',
    'user_incharge_id': 'código do usuário responsável'
}

company = socws.client.Company(**credentials)

# Ver na documentação do SOC os campos que podem ser passados para cada serviço

response = company.add(
    {
        'dadosEmpresaWsVo': {
            'nomeAbreviado': 'nome da empresa',
            # ... demais campos
        }
    }
)

# Dependendo do serviço, response vai ter uma estrutura diferente. Ver na documentação
```

Verifique na documentação do **SOC** os parâmetros aceitos para cada serviço. Entretanto, para todos os serviços, a estrutura "*identificacaoWsVo*" é baseada nas credenciais passadas, então a biblioteca **socws** já cria essa estrutura automáticamente para cada requisição, não precisando passar novamente.

Para todas as requisições o parâmetro passado é um dicionário contento os campos de acordo com o serviço. Por exemplo, a classe *DataExport* implementa a chamada ao serviço *Exporta dados*, que após configurado no perfil do usuário no **SOC**, pode ser invocado da seguinte maneira:

```python
import socws

data = socws.client.DataExport(**credentials)
response = data.request(
    {
        'empresa': 'código da empres',
        'codigo': 'código do tipo de exporta dados',
        'chave': 'chave do tipo de exporta dados',
        'tipoSaida': 'json',
        # ... demais campos do "exporta dados"
    }
)
```

Cada tipo de *exporta dados* vai requerer parâmetros adicionais e tipos de saídas diferenciados. Consultar a documentação de cada *exporta dados* disponível no sistema SOC para a correta parametrização.

E novamente, dependendo do *exporta dados*, **response** vai ter uma estrutura de acordo com o tipo de saída escolhida disponível.

# Serviços implementados

- **Empresa**: *socws.client.Company*

>>**Métodos**: *add*, *update*

- **Unidade**: *socws.client.Unit*

>>**Métodos**: *get*, *add*, *update*

- **Funcionário**: *socws.client.Employee*

>>**Métodos**: *import_employee*

- **Exporta dados**: *socws.client.DataExport*

>>**Métodos**: *request*

# Licença

O **socws** é um projeto de código aberto, desenvolvido pelo departamento de
Pesquisa e Desenvolvimento e Tecnologia da Informação da [Qualitá Segurança e Saúde Ocupacional](https://qualitaocupacional.com.br)
e está licenciada pela [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).
