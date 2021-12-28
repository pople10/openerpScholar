from openerp.osv import osv,fields
import math
import openerp
import logging
from datetime import datetime,timedelta

class scholar_holiday(osv.osv):
    _name="scholar.holiday"
    _columns={
        "from":fields.date("From",required=True),
        "to":fields.date("To",required=True),
        "name":fields.char("Label",required=True),
        "idScholarYear":fields.many2one('scholar.scholaryear','Scholar Year',ondelete='cascade',required=True)
    }
    _sql_constraints = [
        ('id_timetable_uniq', 'unique(idScholarYear,from,to)', 'Holiday already exists'),
    ]
    def onchange_dates(self, cr, uid, ids,fromDate,toDate, context=None):
        if fromDate and toDate:
            d_date = datetime.strptime(toDate.split(" ")[0],"%Y-%m-%d").date()
            c_date = datetime.strptime(fromDate.split(" ")[0],"%Y-%m-%d").date()
            if c_date > d_date:
                return {
                    'warningSwal': {
                        'title':'Invalid dates',
                        'message':'From date should be greater than to date!'
                    }
                    ,'value': {'to' : str(c_date)}
                }
        return {}
scholar_holiday()