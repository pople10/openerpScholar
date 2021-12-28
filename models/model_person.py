from openerp.osv import osv,fields
import openerp
from datetime import datetime,timedelta
from openerp import tools

class scholar_person(osv.osv):
    _name="scholar.person"
    GENDER_TYPE_SELECTION = [
        ('male', 'Male'),
        ('female', 'Female')
    ]
    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.photo)
        return result
    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'photo': tools.image_resize_image_big(value)}, context=context)  
    _columns={
        "firstname":fields.char("First Name",size=255,required=True),
        "lastname":fields.char("Last Name",size=255,required=True),
        "dateofbirth":fields.date("Date of Birth",required=True),
        "cityofbirth":fields.char("City of Birth",required=True),
        "email":fields.char("Email",size=1024,required=True),
        "photo":fields.binary('Picture',filters='*.png,*.jpeg,*.jpg',attachment=True),
        "gender":fields.selection(GENDER_TYPE_SELECTION, 'Gender',required=True),
        'image_small':fields.function(_get_image,fnct_inv=_set_image, type="binary", multi="_get_image",string='Small Picture',
            store={
                'scholar.person': (lambda self, cr, uid, ids, c={}: ids, ['photo'], 10),
            }),
        'image_medium':fields.function(_get_image, fnct_inv=_set_image,type="binary", multi="_get_image",string='Medium Picture',
            store={
                'scholar.person': (lambda self, cr, uid, ids, c={}: ids, ['photo'], 10),
            }),
    }
    _sql_constraints = [
        ('email_uniq', 'unique(email)', 'Email already exists'),
    ]
    def checkDob(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        current = (datetime.today()).strftime("%Y-%m-%d")
        c_date = datetime.strptime(current,"%Y-%m-%d").date()
        d_date = datetime.strptime(obj.dateofbirth,"%Y-%m-%d").date()
        if c_date <= d_date:
            return False
        return True
    def _get_default_image(self, cr, uid, context=None):
        image_path = openerp.addons.get_module_resource('scholar', 'static/src/img', 'm2.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))
    _constraints = [(checkDob, 'Date of birth should be less than today\'s date.', ['dateofbirth'])]
    _defaults = {
        'gender': 'male',
        'photo':_get_default_image
    }
    def onchange_dob(self, cr, uid, ids, dateofbirth, context=None):
        tmp = dateofbirth
        current = (datetime.today() - timedelta(days=5*360)).strftime("%Y-%m-%d")
        c_date = datetime.strptime(current,"%Y-%m-%d").date()
        d_date = datetime.strptime(tmp,"%Y-%m-%d").date()
        if c_date <= d_date:
            return {
                'warningSwal': {
                    'title':'Invalid date of birth',
                    'message':'Date of birth should be valid and more than 5 years!'
                }
                ,'value': {'dateofbirth' : str(c_date)}
            }
        return {}
    def onchange_email(self, cr, uid, ids, email, context=None):
        emails = self.pool.get('scholar.person').search(cr, uid, [('email', '=', email)], limit=1, context=context)
        if emails:
            if ids:
                if emails[0]!=ids[0]:
                    return {
                        'warningSwal': {
                            'title':'Invalid email',
                            'message':'This email already exists!'
                        }
                        ,'value': {'email' : ""}
                    }
            else:
                return {
                    'warningSwal': {
                        'title':'Invalid email',
                        'message':'This email already exists!'
                    }
                    ,'value': {'email' : ""}
                }
        return {}
    def name_get(self, cr, uid, ids, context=None):
        res = []
        if not ids:
            return res
        for r in self.browse(cr, uid, ids, context=context):
            name = str(r.lastname or '').upper()  + ' ' + str(r.firstname or '')
            res.append((r.id, name))
        return res
    def create_professor(self,cr, uid, ids,context=None):
        datos=self.browse(cr ,uid, ids[0], context=context)
        if not datos:
            return {"undoneSwal":"Something went wrong."}
        teacher = self.pool.get('scholar.professor').search(cr, uid, [('email', '=', datos.email)], limit=1, context=context)
        if teacher:
            return {"undoneSwal":"Professor already exists for this person."}
        data={"firstname":datos.firstname,"lastname":datos.lastname,
            "dateofbirth":datos.dateofbirth,"cityofbirth":datos.cityofbirth,"email":datos.email
            ,"photo":datos.photo,"gender":datos.gender}
        out=self.pool.get('scholar.professor').create(cr, uid, data, context=context)
        if not out:
            return {"undoneSwal":"Operation is not successful."}
        return {"doneSwal":"Professor created successfully."}
    def create_parent(self,cr, uid, ids,context=None):
        datos=self.browse(cr ,uid, ids[0], context=context)
        if not datos:
            return {"undoneSwal":"Something went wrong."}
        teacher = self.pool.get('scholar.parent').search(cr, uid, [('email', '=', datos.email)], limit=1, context=context)
        if teacher:
            return {"undoneSwal":"Parent already exists for this person."}
        data={"firstname":datos.firstname,"lastname":datos.lastname,
            "dateofbirth":datos.dateofbirth,"cityofbirth":datos.cityofbirth,"email":datos.email
            ,"photo":datos.photo,"gender":datos.gender,"address":"Default","job":"Default","phone":"0666666666"}
        out=self.pool.get('scholar.parent').create(cr, uid, data, context=context)
        if not out:
            return {"undoneSwal":"Operation is not successful."}
        return {"doneSwal":"Parent created successfully."}    
scholar_person()