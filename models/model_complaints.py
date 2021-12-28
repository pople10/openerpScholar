from openerp.osv import osv,fields
import openerp
import logging

class scholar_complaints(osv.osv):
    _name="scholar.complaints"
    _inherit = ['mail.thread']
    _columns={
        "Idcomplaints":fields.char("Complaints ID"),
        "idProfessor":fields.many2one('scholar.professor', 'Professor', ondelete='cascade'),
        "idEleve":fields.many2one('scholar.eleve', 'Eleve', ondelete='cascade'),
        "subject":fields.char("Subject",size=255),
        "body":fields.text("Body")
    }
    def create(self, cr, uid, vals, context=None):
        sequence=self.pool.get('ir.sequence').get(cr, uid, 'Idcomplaints')
        vals['Idcomplaints']=sequence
        return super(scholar_complaints, self).create(cr, uid, vals, context=context)


"""         mail_ids = []
        for result_line in wizard_data.result_line_ids:
            email_to = result_line.user_id.email
            if not email_to:
                continue
            subject = wizard_data.name
            body = _("Hello,\n\n")
            body += _("I've shared %s with you!\n\n") % wizard_data.name
            mail_ids.append(mail.create(cr, uid, {
                    'email_from': professor_mail,
                    'email_to': parent_mail,
                    'subject': subject,
                    'body_html': '<pre>%s</pre>' % body}, context=context))
        # force direct delivery, as users expect instant notification
        mail.send(cr, uid, mail_ids, context=context)
        logging.warning('%d share notification(s) sent.', len(mail_ids)) """

scholar_complaints()


