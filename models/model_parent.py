from openerp.osv import osv,fields
import openerp
from openerp import tools

class scholar_parent(osv.osv):
    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.photo)
        return result
    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'photo': tools.image_resize_image_big(value)}, context=context)  
    _name="scholar.parent"
    _inherit="scholar.person"
    _columns={
        "idParent":fields.char("Parent ID",required=True,select=True),
        "address":fields.text("Address",size=1024,required=True),
        "job":fields.char("Job",required=True),
        "phone":fields.char("Phone Number",required=True),
        "eleve_ids":fields.one2many('scholar.eleve', 'idParent', string='Children'),
        'image_small':fields.function(_get_image,fnct_inv=_set_image, type="binary", multi="_get_image",string='Small Picture',
            store={
                'scholar.parent': (lambda self, cr, uid, ids, c={}: ids, ['photo'], 10),
            }),
        'image_medium':fields.function(_get_image, fnct_inv=_set_image,type="binary", multi="_get_image",string='Medium Picture',
            store={
                'scholar.parent': (lambda self, cr, uid, ids, c={}: ids, ['photo'], 10),
            }),
    }
    def create(self, cr, uid, vals, context=None):
        sequence=self.pool.get('ir.sequence').get(cr, uid, 'idParent')
        vals['idParent']=sequence
        return super(scholar_parent, self).create(cr, uid, vals, context=context)
    _sql_constraints = [
        ('id_parent_uniq', 'unique(idParent)', 'Id Parent already exists'),
    ]
    def onchange_email(self, cr, uid, ids, email, context=None):
        emails = self.pool.get('scholar.parent').search(cr, uid, [('email', '=', email)], limit=1, context=context)
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
    def onchange_phone(self, cr, uid, ids, phone, context=None):
        phones = self.pool.get('scholar.parent').search(cr, uid, [('phone', '=', phone)], limit=1, context=context)
        if phones:
            if ids:
                if phones[0]!=ids[0]:
                    return {
                        'warningSwal': {
                            'title':'Invalid phone',
                            'message':'This phone already exists!'
                        }
                        ,'value': {'phone' : ""}
                    }
            else:
                return {
                    'warningSwal': {
                        'title':'Invalid phone',
                        'message':'This phone already exists!'
                    }
                    ,'value': {'phone' : ""}
                }
        return {}
scholar_parent()