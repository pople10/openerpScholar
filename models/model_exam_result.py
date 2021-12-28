# coding=utf-8
from openerp.osv import osv,fields
import openerp
import smtplib

class scholar_exam_result(osv.osv):
    _name="scholar.exam.result"
    _columns={
        "idExam":fields.many2one('scholar.exam','Exam',ondelete='cascade', required=True),
        "idInscription":fields.many2one('scholar.inscription','Inscription',ondelete='cascade',required=True),
        "note":fields.char("Note",size=255),
        "report":fields.text("Report"),
        "mark":fields.float('Mark'),
        "originalMark":fields.float('Original Mark',required=True)
    }

    def create(self, cr, uid, vals, context=None):
        maxMark=self.pool.get('scholar.exam').browse(cr, uid, vals['idExam'], context=context).maxMark
        if "originalMark" in vals and maxMark:
            mark = float((float)(vals['originalMark']*20)/maxMark)
            vals['mark'] = mark
            vals['note'] = self.noteMark(mark)
        return super(scholar_exam_result, self).create(cr, uid, vals ,context=context)
    def Student(self, cr, uid, ids,vals, context=None):
        obj=self.pool.get('scholar.exam.result').browse(cr, uid,ids[0], context=context)
        maxMark=self.pool.get('scholar.exam').browse(cr, uid, obj.idExam.id, context=context).maxMark
        if "originalMark" in vals and maxMark:
            mark = float((float)(vals['originalMark']*20)/maxMark)
            vals['mark'] = mark
            vals['note'] = self.noteMark(mark)
        return super(scholar_exam_result, self).Student(cr, uid,ids, vals ,context=context)

    def noteMark(self, note):
        if note < 20 and note > 17:
            return "Excellent"
        if note < 17 and note > 15:
            return "Outstanding"
        if note < 15 and note > 13:
            return "Very good"
        if note < 13 and note > 10:
            return "Good"
        if note == 10:
            return "Passed"
        if note < 10 and note > 5:
            return "Failed"
        if note < 5 and note > 0:
            return "Catastrophic"
        if note==0:
            return "Einstein"        



    def onchange_mark(self, cr, uid, ids, idExam, mark, context=None):
        if not idExam :
                    return {
                        'warning': {
                            'title':'Wrong order',
                            'message':'Please fill out the exam input first.'
                        }
                        ,'value': {'idExam' : "" ,'originalMark': 1,'mark':0}
                    } 
        exam=self.pool.get('scholar.exam').browse(cr, uid, idExam, context=context)
        maxMark = exam.maxMark
        if mark > maxMark or mark < 0:
            return {
                'warningSwal': {
                    'title':'Invalid mark',
                    'message':'Mark shouldn\'t be above '+ repr(maxMark) +' or less than 0!'
                }
                ,'value': {'originalMark' : 0,'mark':0}
            } 
        maxMark=self.pool.get('scholar.exam').browse(cr, uid, idExam, context=context)
        if maxMark:
            value=int(maxMark.maxMark)
            return {'value': {'mark':float((float)(mark*20)/value)}}
        return {}
    def onchange_student(self, cr, uid, ids, idExam, idInsc, context=None):
        data=self.pool.get('scholar.exam.result').search(cr, uid, [('idExam', '=', idExam),('idInscription',"=",idInsc)], limit=1, context=context)
        if data:
            if ids:
                if data[0]!=ids[0]:
                    return {
                            'warningSwal': {
                                'title':'Duplicated data',
                                'message':'You have already added a mark to this student for this exam!'
                            }
                            ,'value': {'idExam' : "" ,'idInscription': ""}
                        } 
            else:
                return {
                        'warningSwal': {
                            'title':'Duplicated data',
                            'message':'You have already added a mark to this student for this exam!'
                            }
                            ,'value': {'idExam' : "" ,'idInscription': ""}
                        } 
        return{}
scholar_exam_result()