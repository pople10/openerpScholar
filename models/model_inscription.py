from openerp.osv import osv,fields
import openerp
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import date,datetime

class scholar_inscription(osv.osv):
    _name="scholar.inscription"
    _columns={
        'idInscription':fields.char("Inscription ID",select=True),
        'idClass':fields.many2one('scholar.class','Class',ondelete='cascade',required=True),
        'idEleve':fields.many2one('scholar.eleve','Student',ondelete='cascade',required=True),
        'created_at':fields.datetime("Created time",required=True),
        "exam_result_ids":fields.one2many('scholar.exam.result', 'idInscription', string='Exam\'s Results')
    }
    _defaults = {
        'created_at': (date.today()).strftime(DEFAULT_SERVER_DATE_FORMAT),
        'idInscription':lambda self, cr, uid, context: self.pool.get('ir.sequence').get(cr, uid, 'sequence.inscription'),
    }
    _sql_constraints = [
        ('id_inscription_uniq', 'unique(idInscription)', 'ID Inscription already exists'),
        ('id_inscription_eleve_uniq', 'UNIQUE(idInscription,idEleve,idClass)', 'Student already registred')
    ]
    def onchange_data(self, cr, uid, ids, eleve,idClass, context=None):
        if idClass:
            classes = self.pool.get('scholar.class').browse(cr, uid, idClass, context=context)
            etablishement = classes.idScholarYear.idEtablishement
            maxTotal=etablishement.maxStudentTotal
            maxClass=etablishement.maxStudentPerClass
            if len(classes.inscription_ids)>=int(maxClass):
                return {
                        'warningSwal': {
                            'title':'Max reached',
                            'message':'This establishment has reached its maximum for each class!'
                        }
                        ,'value': {'idClass' : ""}
                    }
            cmp=0
            for i in classes.idScholarYear.class_ids:
                cmp+=len(classes.inscription_ids)
            if cmp>=int(maxTotal):
                return {
                        'warningSwal': {
                            'title':'Max reached',
                            'message':'This establishment has reached its maximum in total!'
                        }
                        ,'value': {'idClass' : ""}
                    }
        eleves = self.pool.get('scholar.inscription').search(cr, uid, [('idEleve', '=', eleve),('idClass', '=', idClass)], limit=1, context=context)
        if eleves:
            if ids:
                if eleves[0]!=ids[0]:
                    return {
                        'warningSwal': {
                            'title':'Duplicated Inscription',
                            'message':'This student is already registred for this class!'
                        }
                        ,'value': {'idEleve' : "","idClass":""}
                    }
            else:
                return {
                    'warningSwal': {
                    'title':'Duplicated Inscription',
                    'message':'This student is already registred for this class!'
                    }
                    ,'value': {'idEleve' : "","idClass":""}
                }
        return {}
    def name_get(self, cr, uid, ids, context=None):
        res = []
        if not ids:
            return res
        for r in self.browse(cr, uid, ids, context=context):
            name = str(r.idEleve.lastname or '').upper()  + ' ' + str(r.idEleve.firstname or '')
            res.append((r.id, name))
        return res
scholar_inscription()