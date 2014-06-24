# -*- coding: utf-8 -*-

#########################################################################
## Este controlador ejecuta la configuración de los datos iniciales
## - index is the default action of any application
## - empresa crea los datos de las empresas
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))


def empresa():
    """
    Útil para introducir los datos iniciales de una empresa
    """

    form = SQLFORM.factory(db.pais, db.estado, db.municipio,  db.localidad,\
            db.empresa)

    if form.process().accepted:
        response.flash = 'OK'
    elif form.errors:
        response.flash = 'Errores en el formulario'
    else:
        response.flash = 'Formulario incompleto'

    return dict(form=form)
