from openerp.osv import osv,fields
import openerp
from datetime import datetime

class scholar_class(osv.osv):
    _name="scholar.class"
    _columns={ 
        "idClass":fields.char("Class ID",select=True),
        "name":fields.char("Label",size=255,required=True),
        "idLevel":fields.many2one('scholar.level','Level',ondelete='cascade',required=True),
        "idScholarYear":fields.many2one('scholar.scholaryear','Scholar Year',ondelete='cascade',required=True),
        "mainProfessor":fields.many2one('scholar.professor','Main Professor',ondelete='cascade'),
        "inscription_ids":fields.one2many('scholar.inscription', 'idClass', string='Inscriptions'),
        "module_ids":fields.one2many('scholar.module', 'idClass', string='Modules')
    }
    def create(self, cr, uid, vals, context=None):
        sequence=self.pool.get('ir.sequence').get(cr, uid, 'idClass')
        if vals['idLevel']:
            idLevel=self.pool.get('scholar.level').browse(cr, uid,[vals['idLevel']], context=context)[0].idLevel
            vals['idClass']=str(idLevel)+"-"+str(int(sequence))+"-"+str(datetime.now().year)
        return super(scholar_class, self).create(cr, uid, vals, context=context)
    _sql_constraints = [
        ('id_class_uniq', 'unique(idClass,idScholarYear)', 'ID Class already exists for this scholar year'),
    ]
    def onchange_prof(self, cr, uid, ids, prof,  context=None):
        if prof:
            prof = self.pool.get('scholar.professor').browse(cr ,uid, prof, context=context)
            if not prof.inService:
                return {
                        'warningSwal': {
                            'title':'Professor incorrect!',
                            'message':'This professor is not in service any more!'
                        }
                        ,'value': {'idProfessor':''}}    
        return {}
scholar_class()