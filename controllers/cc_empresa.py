# coding: utf8
# try something like
def index(): return dict(message="hello from cc_empresa.py")

def listar():
    form = SQLFORM.smartgrid(db.cc_empresa, linked_tables=['empresa'])
    return dict(form=form)
