from openerp.osv import osv,fields
import openerp

class scholar_module(osv.osv):
    _name="scholar.module"
    _columns={
        "idModule":fields.char("Module ID",required=True,select=True),
        "name":fields.char("Label",size=255,required=True),
        "idClass":fields.many2one('scholar.class','Class',ondelete='cascade',required=True),
        "timetable_ids":fields.one2many('scholar.timetable', 'idModule', string='Timetables'),
        "exam_ids":fields.one2many('scholar.exam', 'idModule', string='Exams'),
        "course_ids":fields.one2many('scholar.course', 'idModule', string='Courses')
    }
    _sql_constraints = [
        ('id_module_uniq', 'unique(idModule)', 'ID Module already exists'),
        ('id_code_uniq', 'unique(idModule,idClass)', 'You should have unique module'),
    ]
    def create(self, cr, uid, vals, context=None):
        sequence=self.pool.get('ir.sequence').get(cr, uid, 'idModule')
        vals['idModule']=sequence
        return super(scholar_module, self).create(cr, uid, vals, context=context)
    def onchange_data(self, cr, uid, ids, code,idClass, context=None):
        modules = self.pool.get('scholar.module').search(cr, uid, [('idModule', '=', code),('idClass', '=', idClass)], limit=1, context=context)
        if modules:
            if ids:
                if modules[0]!=ids[0]:
                    return {
                        'warningSwal': {
                            'title':'Duplicated Module',
                            'message':'You should have unique module!'
                        }
                        ,'value': {'idModule' : ""}
                    }
            else:
                return {
                    'warningSwal': {
                        'title':'Duplicated Module',
                        'message':'You should have unique module!'
                    }
                    ,'value': {'idModule' : ""}
                }
        return {}
scholar_module()