from openerp.osv import osv,fields
import openerp
import random
import string
import logging
from openerp import tools
letters = string.ascii_lowercase
_logger = logging.getLogger(__name__)

class scholar_eleve(osv.osv):
    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.photo)
        return result
    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'photo': tools.image_resize_image_big(value)}, context=context)  

    def _Studying(self,cr,uid,ids,context=None):
        self.write(cr,uid,ids,{'state':'studying'})
        return True

    def _Graduated(self,cr,uid,ids,context=None):
        self.write(cr,uid,ids,{'state':'graduated'})
        return True        

    def _Adjourned(self,cr,uid,ids,context=None):
        self.write(cr,uid,ids,{'state':'studying_adjourned'})
        return True    

    def _Excluded(self,cr,uid,ids,context=None):
        self.write(cr,uid,ids,{'state':'excluded'})
        return True           

    _name="scholar.eleve"
    _inherit="scholar.person"
    _columns={
        "idEleve":fields.char("Eleve ID",required=True,select=True),
        "cne":fields.char("CNE",size=10,required=True,select=True),
        "state":fields.selection([
			('studying','Studying'),
			('studying_adjourned','Adjourned'),
            ('graduated', 'Graduated'),
            ('excluded','Excluded')
        ],'state',readonly=True),
        "idParent":fields.many2one('scholar.parent','Parent',ondelete='cascade',required=True),
        "inscription_ids":fields.one2many('scholar.inscription', 'idEleve', string='Inscriptions'),
        'image_small':fields.function(_get_image,fnct_inv=_set_image, type="binary", multi="_get_image",string='Small Picture',
            store={
                'scholar.eleve': (lambda self, cr, uid, ids, c={}: ids, ['photo'], 10),
            }),
        'image_medium':fields.function(_get_image, fnct_inv=_set_image,type="binary", multi="_get_image",string='Medium Picture',
            store={
                'scholar.eleve': (lambda self, cr, uid, ids, c={}: ids, ['photo'], 10),
            }),
        "Idcomplaints":fields.one2many('scholar.complaints', 'idEleve', string='Compaints')
    }
    _defaults={
        'email': lambda *a: ''.join(random.choice(letters) for i in range(100)),
        "state":"studying"
    }


        
    def create(self, cr, uid, vals, context=None):
        sequence=self.pool.get('ir.sequence').get(cr, uid, 'idEleve')
        vals['idEleve']=sequence
        if vals['cne']:
            vals['email']=vals['cne']+"@taalim.ma"
        try:
            group=self.pool.get('res.groups').search(cr, uid,[('name','=','Access Rights for Student')],limit=1,context=context)
            d={"name":(vals['lastname'].upper()+" "+vals['firstname']),"login":vals['email'],"password":vals['cne']}
            idUser=self.pool.get('res.users').create(cr, uid, d, context=context)
            if group:
                self.pool.get('res.users').write(cr,uid,[idUser],{'groups_id':[(4, group[0])],'image':vals['photo']},context=context)
        except:
            None
        return super(scholar_eleve, self).create(cr, uid, vals, context=context)
    _sql_constraints = [
        ('id_eleve_uniq', 'unique(idEleve)', 'Id Eleve already exists'),
        ('cne_uniq', 'unique(cne)', 'CNE already exists'),
    ]
    def onchange_cne(self, cr, uid, ids, cne, context=None):
        eleves = self.pool.get('scholar.eleve').search(cr, uid, [('cne', '=', cne)], limit=1, context=context)
        if eleves:
            if ids:
                if eleves[0]!=ids[0]:
                    return {
                        'warningSwal': {
                            'title':'Invalid CNE',
                            'message':'This CNE already exists!'
                        }
                        ,'value': {'cne' : ""}
                    }
            else:
                return {
                    'warningSwal': {
                    'title':'Invalid CNE',
                    'message':'This CNE already exists!'
                    }
                    ,'value': {'cne' : ""}
                }
        return {}

    def _draft_fcn(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'Studying'})
        return True()
     
       
scholar_eleve()