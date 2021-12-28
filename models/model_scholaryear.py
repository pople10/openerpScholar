from openerp.osv import osv,fields
import openerp
from datetime import datetime

class scholar_scholaryear(osv.osv):
    _name="scholar.scholaryear"
    _columns={
        "idScholarYear":fields.char("Scholar Year",size=9,required=True,select=True),
        "name":fields.char("Label",required=True),
        "startDate":fields.date("Start Date",required=True),
        "endDate":fields.date("Ending Date",required=True),
        "idEtablishement":fields.many2one('scholar.etablishement','Etablishement',ondelete='cascade'),
        "class_ids":fields.one2many('scholar.class', 'idScholarYear', string='Classes'),
        "holiday_ids":fields.one2many('scholar.holiday', 'idScholarYear', string='Holidays'),
    }
    _sql_constraints = [
        ('id_scholar_uniq', 'unique(idScholarYear,idEtablishement)', 'Scholar year for each etablishement'),
    ]
    def _check_date(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        start = datetime.strptime(obj.startDate, "%Y-%m-%d") 
        end = datetime.strptime(obj.endDate, "%Y-%m-%d")
        if(end<=start):
            return False
        return True
    _constraints = [(_check_date, 'End Date should be greater than Start Date.', ['endDate','startDate'])]
    _defaults={
        'idScholarYear': lambda *a:datetime.now().strftime('%Y')+"-"+str(int(datetime.now().strftime('%Y'))+1), 
        "name": lambda *a:"Scholar Year "+datetime.now().strftime('%Y')+"-"+str(int(datetime.now().strftime('%Y'))+1),
    }
    def onchange_idEtablishement(self, cr, uid, ids, id, context=None):
        thisyear = datetime.now().strftime('%Y')+"-"+str(int(datetime.now().strftime('%Y'))+1)
        data = self.pool.get('scholar.scholaryear').search(cr, uid, [('idEtablishement', '=', id),("idScholarYear","=",thisyear)], limit=1, context=context)
        if data:
            if ids:
                if data[0]!=ids[0]:
                    return {
                        'warningSwal': {
                            'title':'Invalid Etablishement',
                            'message':'A unique scholar should for an etablishement!'
                        }
                        ,'value': {'idEtablishement' : ""}
                    }
            else:
                return {
                    'warningSwal': {
                        'title':'Invalid Etablishement',
                        'message':'A unique scholar should for an etablishement!'
                    }
                    ,'value': {'idEtablishement' : ""}
                }
        return {}
    def name_get(self, cr, uid, ids, context=None):
        res = []
        if not ids:
            return res
        for r in self.browse(cr, uid, ids, context=context):
            name = str(r.name or '')  + ' - ' + str(r.idEtablishement.name or '')
            res.append((r.id, name))
        return res
scholar_scholaryear()