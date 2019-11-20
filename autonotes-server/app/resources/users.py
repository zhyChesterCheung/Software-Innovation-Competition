from flask import g
from flask_restplus import Namespace, fields, Resource
from ..models import Spot, Comment
from .. import db
from ..helper.authentication import tkauth

ns = Namespace('spots', description='位置')

spot_base = ns.model('地点基本信息', {
    'id': fields.Integer(readonly=True, description='地点ID'),
    'x': fields.Float(description='坐标x'),
    'y': fields.Float(description='坐标y'),
    'name': fields.String(description='地点名称'),
})

spot = ns.clone('地点详细信息', spot_base,  {
    'pH': fields.Float(description='pH值'),
    'DO': fields.Float(description='溶解氧'),
    'PP': fields.Float(description='高锰酸盐'),
    'AN': fields.Float(description='氨氮'),
    'P': fields.Float(description='磷'),
    'Cd': fields.Float(description='镉'),
    'As': fields.Float(description='砷'),
    'Pb': fields.Float(description='铅'),
    'level': fields.Integer(description='等级')
})


@ns.route('/')
class SpotListResource(Resource):
    @ns.marshal_list_with(spot_base)
    def get(self):
        '''获取所有地点'''
        return Spot.query.all()

@ns.route('/<int:id>')
@ns.response(404, '不存地点与此ID匹配')
@ns.param('id', '地点ID')
class SpotResource(Resource):
    @ns.marshal_with(spot)
    def get(self, id):
        '''获取一个地点（通过地点ID）'''
        return Spot.query.get_or_404(id)




comment = ns.model('评论信息', {
    'id' : fields.Integer(description='ID', readonly=True),
    'content': fields.String(description='评论内容'),
    'user_id': fields.String(description='用户ID', readonly=True),
    'spot_id': fields.Integer(description='地点ID',readonly=True)
})

@ns.route('/<int:id>/comments')
@ns.response(404, '不存地点与此ID匹配')
@ns.response(401, 'Unauthorized Access')
@ns.param('id', '地点ID')
class CommentListOfSpotResource(Resource):
    @tkauth.login_required
    @ns.marshal_list_with(comment)
    @ns.doc(security='apikey')
    def get(self, id):
        '''获取一个地点的评论（通过地点ID）'''
        s = Spot.query.get_or_404(id)
        return s.comments.all()

    @tkauth.login_required
    @ns.expect(comment)
    @ns.marshal_with(comment, code=201)
    @ns.doc(security='apikey')
    def post(self, id):
        '''创建一个地点的评论（通过地点ID）'''
        s = Spot.query.get_or_404(id)
        c = Comment(content=ns.payload['content'], spot=s, user=g.current_user)
        db.session.add(c)
        db.session.commit()
        return c, 201