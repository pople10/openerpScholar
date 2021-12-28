from openerp.osv import osv,fields
import openerp
import re

class scholar_course(osv.osv):
    _name="scholar.course"
    _columns={
        "idModule":fields.many2one('scholar.module','Module',ondelete='cascade',required=True),
        "name":fields.char('Title',required=True),
        "videoLink":fields.char('Video Link'),
        "content":fields.text('Content',required=True),
        "attachement":fields.binary('Attachement')
    }
    _sql_constraints = [
        ('id_course_uniq', 'unique(idCourse)', 'ID Course already exists'),
    ]
    def onchange_url(self, cr, uid, ids, url, context=None):
        pattern = (r'(https?://)?(www\.)?''(youtube|youtu|youtube-nocookie)\.(com)/''(embed/)([^&=%\?]{11})')
        result=True
        if url:
            result = re.match(pattern, url)
        if not result:
            return {
                        'warningSwal': {
                            'title':'Invalid Video Link',
                            'message':'It should be an embedded youtube video URL!'
                        }
                        ,'value': {'videoLink' : ""}
                    }
        return {}
    def get_formview_action(self, cr, uid, ids, context=None):
        idView = self.pool.get("ir.model.data").search(cr, uid, [('name', '=', 'scholar_course_edu_form_view')], limit=1, context=context)
        if idView:
            view=self.pool.get('ir.model.data').browse(cr, uid, idView[0], context=context)
            return  {
                    'type': 'ir.actions.act_window',
                    'res_model': 'scholar.course',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'view_id': view.res_id,
                    'target': 'current',
                    'res_id':ids[0]
            }
        return {}
scholar_course()