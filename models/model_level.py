from openerp.osv import osv,fields
import openerp

class scholar_level(osv.osv):
    _name="scholar.level"
    _columns={
        "idLevel":fields.char("Level ID",required=True,select=True),
        "name":fields.char("Label",size=255,required=True),
        "class_ids":fields.one2many('scholar.class', 'idLevel', string='Classes'),
    }
    _sql_constraints = [
        ('id_level_uniq', 'unique(idLevel)', 'ID Level already exists'),
    ]
scholar_level()