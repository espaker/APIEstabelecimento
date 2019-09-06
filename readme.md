#API Estabelecimento

<b>Rotas:</b><br>
GET:   /api/v1/Estabelecimento<br>
GET:   /api/v1/Estabelecimento/{id}<br>
GET:   /api/v1/Estabelecimento/{id}/Produtor<br>
GET:   /api/v1/Estabelecimento/{id}/UnidadeExploracao<br>
GET:   /api/v1/Produtor/{id}<br>
GET:   /api/v1/Produtor<br>
GET:   /api/v1/UnidadeExploracao/{id}<br>

PUT:   /api/v1/Estabelecimento/{id}<br>
PUT:   /api/v1/Estabelecimento/{id}/unidadeExploracao/{idUep}/ativar<br>
PUT:   /api/v1/Estabelecimento/{id}/unidadeExploracao/{idUep}/desativar<br>
PUT:   /api/v1/Produtor/{id}<br>

POST:   /api/v1/Estabelecimento/{id}/produtor<br>
POST:   /api/v1/Estabelecimento/{id}/unidadeExploracao<br>
POST:   /api/v1/Produtor<br>

DELETE: /api/v1/Estabelecimento/{id}/produtor/{idProdutor}<br>
DELETE: /api/v1/Estabelecimento/{id}/unidadeExploracao/{idUep}<br>


<b>Execução no linux</b>:<br>
Para execução no linux antes é necessario instalar alguns pacotes no python:
- python3 -m pip install flask_cors
- python3 -m pip install flask
- python3 -m pip install cheroot

Por fim basta executar: <i>python3 	&lt;caminho&gt;/APIEstabelecimento.py


