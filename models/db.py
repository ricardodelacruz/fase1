# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
## auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
#from gluon.contrib.login_methods.janrain_account import use_janrain
#use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)


db.define_table('pais',
    Field('nombre', 'string', length=128),
    format='%(nombre)s'
    )

db.define_table('estado',
    Field('clave_interna', 'string', length=2),
    Field('nombre', 'string', length=128),
    Field('pais_id', 'reference pais'),
    format='%(nombre)s'
    )

db.define_table('municipio',
    Field('clave_interna', 'string', length=3),
    Field('nombre', 'string', length=128),
    Field('estado_id', 'reference estado'),
    format='%(nombre)s'
    )
        
db.define_table('localidad',
    Field('clave_interna', 'string', length=4),
    Field('nombre', 'string', length=128),
    Field('lat_grad', 'string'),
    Field('lon_grad', 'string'),
    Field('lat_dec', 'string'),
    Field('lon_dec', 'string'),
    Field('municipio_id', 'reference municipio'),
    format='%(nombre)s'
    )

db.define_table('banco',
    Field('nombre','string', length=128, label='Nombre del Banco'),
    format='%(nombre)s'
    )

db.define_table('persona',
    Field('registro_fiscal','string', length=15, requires=IS_NOT_EMPTY(), label='Registro Fiscal'),
    Field('dir_calle', 'string', length=128, label='Calle'),
    Field('dir_num_ext', 'string', length=40, label='Número Exterior'),
    Field('dir_num_int', 'string', length=40, label='Número Interior'),
    Field('dir_colonia', 'string', length=128, label='Colonia'),
    Field('dir_cp', 'string', length=10, label='CP'),
    Field('dir_telefono', 'string', length=10, label='Teléfono'),
    Field('dir_movil', 'string', length=10, label='Móvil'),
    Field('dir_email', requires=IS_EMAIL(), length=128, label='Email'),
    Field('localidad_id', 'reference localidad', label='Localidad/Ciudad')
    )

db.define_table('empleado',
    Field('nombre', 'string', label='Nombre'),
    Field('ap_paterno', 'string', label='Apellido Paterno'),
    Field('ap_materno', 'string', label='Apellido Materno'),
    db.persona,
    format='%(nombre)s %(ap_paterno)s %(ap_materno)s'
    )

db.define_table('proveedor',
    Field('razon_social','string', requires=IS_NOT_EMPTY(), label='Razón Social'),
    Field('nombre_comercial', 'string', label='Nombre Comercial'),
    db.persona,
    Field('producto_comercial', 'string', length=128, label='Producto comercial'),
    format='%(razon_social)s'
    )

db.define_table('proveedor_banco',
    Field('proveedor_id','reference proveedor'),
    Field('banco_id','reference banco'),
    Field('clabe','string', label='Número de Cuenta Interbancaria'),
    Field('cuenta','string', label='Número de Cuenta Bancaria'),
    format='%(banco_id)s %(cuenta)s'
    )

db.define_table('empresa', db.persona,
    Field('razon_social','string', label='Razón Social'),
    format='%(razon_social)s'
    )
db.define_table('empresa_banco',
    Field('empresa_id','reference empresa'),
    Field('banco_id','reference banco'),
    Field('clabe','string', label='Número de Cuenta Interbancaria'),
    Field('cuenta','string', label='Número de Cuenta Bancaria'),
    format='%(banco_id)s %(cuenta)s'
    )

db.define_table('sucursal',
    Field('empresa_id', 'reference empresa', label='Empresa'),
    Field('nombre', 'string', length=128, label='Nombre de la Sucursal'),
    db.persona,
    format='%(nombre)s'
    )

db.define_table('departamento',
    Field('sucursal_id', 'reference sucursal', label='Sucursal'),
    Field('nombre', 'string', length=128),
    format='%(nombre)s'
    )

auth.settings.extra_fields['auth_user']= [
    Field('empleado_id', 'reference empleado'),
    ]

auth.define_tables(username=False, signature=False, migrate=False) ##creamos las tablas auth
##auth.define_tables(username=False, signature=False)

db.auth_user._format = '%(first_name)s %(last_name)s (%(email)s)'
auth.settings.everybody_group_id = 1 ##asignar a nuevos usuarios a un grupo por default 1=ADMIN, 2=BASICO, 3=ETC
auth.settings.create_user_groups = None

db.define_table('cc_empresa',
    Field('empresa_id', 'reference empresa', label='Empresa'),
    Field('num_cc', 'string', length=128, label='Número de Cuenta Contable'),
    Field('descripcion', 'string', length=128, label='Descripción'),
    Field('nivel', 'integer'),
    Field('naturaleza', 'string', length=40),
    format='%(num_cc)s %(descripcion)s'
    )
