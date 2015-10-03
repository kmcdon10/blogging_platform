db = DAL('sqlite://storage.sqlite')

from gluon.tools import *
auth = Auth(db)

#from gluon.contrib.login_methods.rpx_account import RPXAccount
#auth.settings.actions_disabled=['register','change_password','request_reset_password']
#auth.settings.login_form = RPXAccount(request,
#     api_key='569ddf3abd8a0704347caa9e8bb7370a14905b04 ',
#     domain='localhost:8000/blogging_platform3/default/index',
#     url = "http://localhost:8000/blogging_platform3/%s/default/user/login" % request.application)

db.define_table("image",
    Field("title", unique=True),
    Field("file", "upload"),
    format = "%(title)s")

db.define_table('document',
    Field('name'),
    Field('file', 'upload'),
    Field('created_on', 'datetime', default=request.now),
    format='%(name)s')

auth.settings.extra_fields['auth_user']= [
  Field('photo_id', 'reference image', readable=False, writable=False)]

auth.define_tables(username=False)


db.define_table('page',
    Field('title'),
    Field('body', 'text'),
    Field('created_on', 'datetime', default=request.now),
    Field('created_by', 'reference auth_user', readable=False, writable=False))

db.define_table('blogpost',
    Field('title'),
    Field('body', 'text'),
    Field('tags', 'list:string'),
    Field('photo_id', 'reference image'),
    Field('document_id', 'reference document', readable=False, writable=False),
    Field('created_on', 'datetime', default=request.now),
    Field('blogpage_id', 'reference page', readable=False, writable=False))

db.define_table('comment',
    Field('body', 'text'),
    Field('created_by'),
    Field('created_on', 'datetime', default=request.now),
    Field('blogpost_id', 'reference blogpost', readable=False, writable=False))


db.document.name.requires = IS_NOT_IN_DB(db, 'document.name')
db.document.created_on.readable = db.document.created_on.writable = False

db.comment.body.requires = IS_NOT_EMPTY()
db.comment.created_by.requires = IS_NOT_EMPTY()
db.comment.created_on.readable = db.comment.created_on.writable = False
db.comment.blogpost_id.requires = IS_IN_DB(db,db.blogpost)

db.blogpost.title.requires = IS_NOT_EMPTY()
db.blogpost.body.requires = IS_NOT_EMPTY()
db.blogpost.blogpage_id.requires = IS_IN_DB(db,db.page)
db.blogpost.photo_id.readable = db.blogpost.photo_id.writable = False
db.blogpost.created_on.readable = db.blogpost.created_on.writable = False

db.page.title.requires = IS_NOT_EMPTY()
db.page.body.reference = IS_NOT_EMPTY()
db.page.created_by.requires = IS_IN_DB(db, db.auth_user)
db.page.created_on.readable = db.page.created_on.writable = False
