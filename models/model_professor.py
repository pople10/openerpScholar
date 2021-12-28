from openerp.osv import osv,fields
import openerp
from openerp import tools

class scholar_professor(osv.osv):
    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.photo)
        return result
    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'photo': tools.image_resize_image_big(value)}, context=context)  
    _name="scholar.professor"
    _inherit="scholar.person"
    _columns={
        "idProfessor":fields.char("Professor ID",required=True,select=True),
        "speciality":fields.many2one('scholar.speciality','Speciality',ondelete='cascade'),
        "inService":fields.boolean("Still in service"),
        "class_ids":fields.one2many('scholar.class', 'mainProfessor', string='Classes'),
        "timetable_ids":fields.one2many('scholar.timetable', 'idProfessor', string='Timetables'),
        'image_small':fields.function(_get_image,fnct_inv=_set_image, type="binary", multi="_get_image",string='Small Picture',
            store={
                'scholar.professor': (lambda self, cr, uid, ids, c={}: ids, ['photo'], 10),
            }),
        'image_medium':fields.function(_get_image, fnct_inv=_set_image,type="binary", multi="_get_image",string='Medium Picture',
            store={
                'scholar.professor': (lambda self, cr, uid, ids, c={}: ids, ['photo'], 10),
            }),
        "Idcomplaints":fields.one2many('scholar.complaints', 'idProfessor', string='Compaints'),
    }
    def create(self, cr, uid, vals, context=None):
        sequence=self.pool.get('ir.sequence').get(cr, uid, 'idProfessor')
        vals['idProfessor']=sequence
        try:
            d={"name":(vals['lastname'].upper()+" "+vals['firstname']),"work_email":vals['email'],"image":vals['photo']}
            self.pool.get('hr.employee').create(cr, uid, d, context=context)
        except:
            None
        try:
            group=self.pool.get('res.groups').search(cr, uid,[('name','=','Access Rights for Professor')],limit=1,context=context)
            d={"name":(vals['lastname'].upper()+" "+vals['firstname']),"login":vals['email'],"password":vals['email']}
            idUser=self.pool.get('res.users').create(cr, uid, d, context=context)
            if group:
                self.pool.get('res.users').write(cr,uid,[idUser],{'groups_id':[(4, group[0])],'image':vals['photo']},context=context)
        except:
            None
        return super(scholar_professor, self).create(cr, uid, vals, context=context)
    _sql_constraints = [
        ('id_professor_uniq', 'unique(idProfessor)', 'ID Professor already exists'),
    ]
    def onchange_email(self, cr, uid, ids, email, context=None):
        emails = self.pool.get('scholar.professor').search(cr, uid, [('email', '=', email)], limit=1, context=context)
        if emails:
            if ids:
                if emails[0]!=ids[0]:
                    return {
                        'warningSwal': {
                            'title':'Invalid email',
                            'message':'This email already exists!'
                        }
                        ,'value': {'email' : ""}
                    }
            else:
                return {
                    'warningSwal': {
                        'title':'Invalid email',
                        'message':'This email already exists!'
                    }
                    ,'value': {'email' : ""}
                }
        return {}
    def serve(self,cr, uid, ids,context=None):
        data={"inService":True}
        out=self.pool.get('scholar.professor').write(cr, uid,ids, data, context=context)
        if not out:
            return {"undoneSwal":"Operation is not successful."}
        return {"doneSwal":"Professor in service now."}
    def unserve(self,cr, uid, ids,context=None):
        data={"inService":False}
        out=self.pool.get('scholar.professor').write(cr, uid,ids, data, context=context)
        if not out:
            return {"undoneSwal":"Operation is not successful."}
        return {"doneSwal":"Professor in service now."}
scholar_professor()