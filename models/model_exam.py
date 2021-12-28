from openerp.osv import osv,fields
import openerp
from datetime import datetime,timedelta

class scholar_exam(osv.osv):
    _name="scholar.exam"
    _columns={
        "idExam":fields.char("Exam ID",select=True),
        "name":fields.char("Label",size=255,required=True),
        "from":fields.datetime("From"),
        "to":fields.datetime("To"),
        "idModule":fields.many2one('scholar.module','Module',ondelete='cascade',required=True),
        "maxMark":fields.integer('Max Marks',required=True),
        "exam_result_ids":fields.one2many('scholar.exam.result', 'idExam', string='Exam\'s Results'),
        "idRoom":fields.many2one('scholar.room','Room',ondelete='cascade')
    }
    _sql_constraints = [
        ('id_exam_uniq', 'unique(idExam)', 'ID Exam already exists'),
    ]

    def checkMaxMark(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        mark = obj.maxMark
        if mark < 0 or mark > 100:
            return False
        return True

    _constraints = [(checkMaxMark, 'Max mark should be less than 100 and greater than 0', ['maxMark'])]
    def create(self, cr, uid, vals, context=None):
        sequence=self.pool.get('ir.sequence').get(cr, uid, 'idExam')
        vals['idExam']=sequence
        return super(scholar_exam, self).create(cr, uid, vals, context=context)
    def onchange_dates(self, cr, uid, ids,fromDate,toDate, context=None):
        if fromDate and toDate:
            d_date = datetime.strptime(toDate,"%Y-%m-%d %H:%M:%S")
            c_date = datetime.strptime(fromDate,"%Y-%m-%d %H:%M:%S")
            if c_date > d_date:
                return {
                    'warningSwal': {
                        'title':'Invalid dates',
                        'message':'From date should be greater than to date!'
                    }
                    ,'value': {'to' : str(c_date+timedelta(hours=2))}
                }
            if(d_date.date()!=c_date.date()):
                return {
                    'warningSwal': {
                            'title':'Invalid dates',
                            'message':'Dates should be in same day!'
                        }
                        ,'value': {'to' : str(c_date+timedelta(hours=2))}
                    }
        return {}
scholar_exam()