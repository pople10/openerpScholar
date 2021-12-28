{
    'name':'Scholar',
    'version':'1.0',
    'author':'Mohammed Amine Ayache && Omar Ezzarqtouni && Tayeb Hamdaoui',
    'category':'ENSAH ERP',
    'sequence':1,
    'description':"Managing a school staffs",
    'images':[''],
    'init_xml':['sequences/sequences.xml',
        'security/scholar_security.xml',
        'access/access_data.xml',
        'security/ir.model.access.csv',
        'data/email_template.xml'],
    'depends':['base','hr','mail', 'email_template'],
    'data':[
        'views/view_etablishement.xml',
        'views/view_scholaryear.xml',
        'views/view_class.xml',
        'views/view_timetable.xml',
        'views/view_person.xml',
        'views/view_professor.xml', 
        'views/view_level.xml', 
        'views/view_eleve.xml',
        'views/view_inscription.xml',
        'views/view_speciality.xml',
        'views/view_parent.xml',
        'views/view_exam.xml',
        'views/view_exam_result.xml',
        'views/view_module.xml',
        'views/view_course_prof.xml',
        'views/view_course_student.xml',
        'views/view_holiday.xml',
        'views/view_room.xml',
        'views/view_complaints.xml',
        'workflows/wkf_eleve.xml'
    ],
    'website':'https://ensah.trackiness.com',
    'update_xml':[],
    'js':['static/src/js/swal.js','static/src/js/main.js','static/src/js/scholarApplication.js'],
    'qweb':[],
    'css':['static/src/css/person.css','static/src/css/main.css','static/src/css/style.css'],
    'demo':[],
    'test':[],
    'images':[],
    'installable':True,
    'auto_install':True
}