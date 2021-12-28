from openerp.osv import osv,fields
import openerp
from datetime import datetime

class scholar_etablishement(osv.osv):
    _name="scholar.etablishement"
    _columns={
        "idEtablishement":fields.integer("Etablishement ID",required=True,select=True),
        "name":fields.char("Label",size=255,required=True),
        "maxStudentTotal":fields.integer("Max Student Total",required=True),
        "maxStudentPerClass":fields.integer("Max Student per class",required=True),
        "scholaryear_ids":fields.one2many('scholar.scholaryear', 'idEtablishement', string='Scholar Years'),
        "room_ids":fields.one2many('scholar.room', 'idEtablishement', string='Rooms'),
    }
    _sql_constraints = [
        ('id_etablishment_uniq', 'unique(idEtablishement)', 'Id Etablishement already exists')
    ]
    def _check_places(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        total = int(obj.maxStudentTotal)
        perClass = int(obj.maxStudentPerClass)
        if(total<=perClass):
            return False
        return True
    _constraints = [(_check_places, 'Total max should be greater than class max students.', ['maxStudentPerClass','maxStudentTotal'])]
    def create(self, cr, uid, vals, context=None):
        sequence=self.pool.get('ir.sequence').get(cr, uid, 'idEtablishement')
        vals['idEtablishement']=sequence
        try:
            d={"name":vals['name'],"paper_format":'a4'}
            vals['idEtablishement']=self.pool.get('res.company').create(cr, uid, d, context=context)
        except:
            None
        return super(scholar_etablishement, self).create(cr, uid, vals, context=context)
    def onchange_places(self, cr, uid, ids, totalMax,classMax,context=None):
        total = int(totalMax)
        perClass = int(classMax)
        if(totalMax and classMax and total<=perClass):
            return {
                'warningSwal': {
                    'title':'Invalid places',
                    'message':'Total max students should be greater than class max students!'
                }
                ,'value': {'maxStudentTotal' : (perClass+1)}
            }
        return {}
    def create_scholar_year(self,cr, uid, ids,context=None):
        thisyear = datetime.now().strftime('%Y')+"-"+str(int(datetime.now().strftime('%Y'))+1)
        data = self.pool.get('scholar.scholaryear').search(cr, uid, [('idEtablishement', '=', ids[0]),("idScholarYear","=",thisyear)], limit=1, context=context)
        if data:
            return {"undoneSwal":"Scholar Year aleady exists"}
        year=datetime.now().year
        start=datetime.strptime(str(year)+"-10-01","%Y-%m-%d").date()
        end=datetime.strptime(str(year+1)+"-07-31","%Y-%m-%d").date()
        data={"idEtablishement":ids[0],"idScholarYear":thisyear,"name":"Scholar Year "+thisyear,"startDate":start,"endDate":end}
        self.pool.get('scholar.scholaryear').create(cr, uid, data, context=context)
        return {"doneSwal":"Scholar Year has been added successfully"}
scholar_etablishement()