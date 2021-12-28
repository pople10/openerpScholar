from openerp.osv import osv,fields
import openerp

class scholar_speciality(osv.osv):
    _name="scholar.speciality"
    _columns={
        "idSpeciality":fields.char("Speciality ID",required=True,select=True),
        "name":fields.char("Label",size=255,required=True),
        "professor_ids":fields.one2many('scholar.professor', 'speciality', string='Professors'),
    }
    _sql_constraints = [
        ('id_spec_uniq', 'unique(idSpeciality)', 'ID Speciality already exists'),
    ]
scholar_speciality()