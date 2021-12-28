from openerp.osv import osv,fields
import openerp

class scholar_room(osv.osv):
    _name="scholar.room"
    _columns={
        "idRoom":fields.char("ID Room"),
        "room":fields.integer("Room Number",required=True,select=True),
        "name":fields.char("Label",size=255),
        "timetable_ids":fields.one2many('scholar.timetable', 'idRoom', string='Timetables'),
        "exam_ids":fields.one2many('scholar.exam', 'idRoom', string='Timetables'),
        "idEtablishement":fields.many2one('scholar.etablishement','Etablishement',ondelete='cascade',required=True)
    }
    _sql_constraints = [
        ('id_room_uniq', 'unique(idEtablishement,room)', 'Room already exists')
    ]
    def create(self, cr, uid, vals, context=None):
        sequence=self.pool.get('ir.sequence').get(cr, uid, 'idRoom')
        vals['idRoom']=sequence
        if vals["room"] and vals["idEtablishement"]:
            vals["name"]="Room Num "+str(vals["room"])+" "+self.pool.get("scholar.etablishement").browse( cr, uid, vals["idEtablishement"],context=context).name
        return super(scholar_room, self).create(cr, uid, vals, context=context)
    def onchange_data(self, cr, uid, ids, room,idEtablishement, context=None):
        rooms = self.pool.get('scholar.room').search(cr, uid, [('idEtablishement', '=', idEtablishement),('room', '=', room)], limit=1, context=context)
        if rooms:
            if ids:
                if rooms[0]!=ids[0]:
                    return {
                        'warningSwal': {
                            'title':'Duplicated Room',
                            'message':'You should have unique room number for each etablishment!'
                        }
                        ,'value': {'room' : ""}
                    }
            else:
                return {
                    'warningSwal': {
                        'title':'Duplicated Room',
                        'message':'You should have unique room number for each etablishmen!'
                    }
                    ,'value': {'room' : ""}
                }
        return {}
scholar_room()