from openerp.osv import osv,fields
import math
import openerp
import logging
from datetime import datetime,timedelta
def getScoreDate(date):
    score=date.hour
    if(date.minute>=30):
        return score+0.5
    if(date.minute>30):
        return score+0.51
    return score
def checkIntervalScore(date):
    score=getScoreDate(date)
    if score<8 or (score>12.50 and score<14) or score>18.5:
        return False
    return True
def checkHoliday(holidays,date):
    if len(holidays)==0:
        return False
    for i in holidays:
        fromy=datetime.strptime(i["from"],'%Y-%m-%d').date()
        toy=datetime.strptime(i["to"],'%Y-%m-%d').date()
        if fromy<=date and toy>=date:
            return True
    return False


class scholar_timetable(osv.osv):
    _name="scholar.timetable"
    _columns={#msba7 o ana n9alab 3la error, dayrlo prefix char o base de donne dayrlo Integer, why do this to me?
        "idTimetable":fields.char("ID Timetable",required=True,select=True),
        "from":fields.datetime("From",required=True),
        "to":fields.datetime("To",required=True),
        "name":fields.char("Label",required=True),
        "exceptional":fields.boolean("Exeptional?"),
        "idModule":fields.many2one('scholar.module','Module',ondelete='cascade',required=True),
        "idProfessor":fields.many2one('scholar.professor','Professor',ondelete='cascade',required=True),
        "idRoom":fields.many2one('scholar.room','Room',ondelete='cascade',required=True)
    }
    def create(self, cr, uid, vals, context=None):
        sequence=self.pool.get('ir.sequence').get(cr, uid, 'idTimetable')
        professor=self.pool.get('scholar.professor').browse(cr, uid, vals['idProfessor'], context=context)
        moduleSelected=self.pool.get('scholar.module').browse(cr, uid, vals['idModule'], context=context)
        room=self.pool.get('scholar.room').browse(cr, uid, vals['idRoom'], context=context)
        vals['idTimetable']=sequence
        vals["name"]=moduleSelected.name+": "+professor.firstname+" "+professor.lastname+"\n"+room.name
        classSelected=self.pool.get('scholar.class').browse(cr, uid, moduleSelected.idClass.id, context=context)
        scholarYear=self.pool.get('scholar.scholaryear').browse(cr, uid, classSelected.idScholarYear.id, context=context)
        start = datetime.strptime(str(scholarYear.startDate),'%Y-%m-%d')
        end = datetime.strptime(str(scholarYear.endDate),'%Y-%m-%d')
        holidays = scholarYear.holiday_ids
        given=datetime.strptime(vals['from'],'%Y-%m-%d %H:%M:%S')
        if vals["exceptional"]:
            if not checkHoliday(holidays,given.date()):
                return super(scholar_timetable, self).create(cr, uid, vals, context=context)
            else:
                return 0
        diff=end-start
        dayName=given.strftime("%A")
        out=0
        tmp=None
        for i in range(diff.days):
            curr = start+timedelta(days=i)
            if curr.strftime("%A")==dayName:
                data={}
                fromy=str(curr.date())+" "+(str(vals['from'])).split(" ")[1]
                to=str(curr.date())+" "+(str(vals['to'])).split(" ")[1]
                data["idTimetable"]=sequence
                data["from"]=fromy
                data["to"]=to
                data["idModule"]=vals["idModule"]
                data["idProfessor"]=vals["idProfessor"]
                data["idRoom"]=vals["idRoom"]
                data["name"]=vals["name"]
                if not checkHoliday(holidays,curr.date()):
                    tmp=super(scholar_timetable, self).create(cr, uid, data, context=context)
                    if data["from"]==vals["from"]:
                        out=tmp
        if tmp!=None and out==0:
            return tmp
        return out
    _sql_constraints = [
        ('id_timetable_uniq', 'unique(idTimetable)', 'ID Timetable already exists'),
    ]
    #add the time limit for a module
    #sunday shouldn't be added 
    def checkDates(self, cr, uid, ids, context=None):
        obj = self.browse(cr, uid, ids[0], context=context)
        d_date = datetime.strptime(obj.to,"%Y-%m-%d %H:%M:%S")
        c_date = datetime.strptime(obj["from"],"%Y-%m-%d %H:%M:%S")
        if c_date >= d_date:
            return False
        return True
    _constraints = [(checkDates, 'To Date should be greater than From Date.', ['from','to'])]
    def onchange_dates(self, cr, uid, ids,fromDate,toDate, context=None):
        if fromDate and toDate:
            d_date = datetime.strptime(toDate,"%Y-%m-%d %H:%M:%S")
            c_date = datetime.strptime(fromDate,"%Y-%m-%d %H:%M:%S")
            if c_date >= d_date:
                return {
                    'warningSwal': {
                        'title':'Invalid dates',
                        'message':'From date should be greater than to date!'
                    }
                    ,'value': {'to' : str(c_date+timedelta(hours=2))}
                }
            if(d_date.date()!=c_date.date()):
                return {
                    'warningSwal': {
                        'title':'Invalid dates',
                        'message':'Dates should be in same day!'
                    }
                    ,'value': {'to' : str(c_date+timedelta(hours=2))}
                }
            certainSunday=datetime.strptime("2021-12-26 10:10:10","%Y-%m-%d %H:%M:%S")
            if(d_date.strftime("%A")==certainSunday.strftime("%A")):
                return {
                    'warningSwal': {
                        'title':'Invalid dates',
                        'message':'We don\'t work sunday!'
                    }
                    ,'value': {'to' : '','from':''}
                }
            if(getScoreDate(d_date)<14 and getScoreDate(c_date)>12.5):
                return {
                    'warningSwal': {
                        'title':'Invalid dates',
                        'message':'We only work from 8:00 to 12:30 or 14:00 to 18:30!'
                    }
                    ,'value': {'to' : '','from':''}
                }
            if((not checkIntervalScore(d_date)) or (not checkIntervalScore(c_date))):
                return {
                    'warningSwal': {
                        'title':'Invalid dates',
                        'message':'We only work from 8:00 to 12:30 or 14:00 to 18:30!'
                    }
                    ,'value': {'to' : '','from':''}
                }
        return {}

    #check if other modules with the same class start at the same date
    #or are between specific hours of the same day 
    #how to select all modules of the same class? browse maybe
    #module can start where other module finished (inclusive)
    #
    #     
    def two_hour_constraint():
        return ""
    
    def onchange_module(self, cr, uid, ids, idModule, fromm, to, context=None): 
        #find the class of the module

        module = self.pool.get('scholar.module').browse(cr ,uid, idModule, context=context)        
        classe = int(module.idClass)
        logging.warning('1-module: '+repr(classe+1))
           
        #retrieve all modules that have the same class with the current moddule
        modules = self.pool.get('scholar.module').search(cr, uid, [('idClass', '=', classe)], context=context)
        #test if the dates don't conflict
        for i in modules:
            logging.warning('1-module: '+repr(i))
            if i != idModule:
                logging.warning('module: '+repr(i))
                tableId=self.pool.get('scholar.timetable').search(cr, uid, [('idModule', '=', i)], context=context)
                if not tableId:
                    return {
                        'warningSwal': {
                                    'title':'Duplicate module!',
                                    'message':'Module already has a timetable set.'
                                }
                                ,'value': {}}    
                start=self.browse(cr ,uid, tableId[0], context=context)
                err = self.DateTest(start["from"], fromm)   
                if not err:
                    return {
                        'warningSwal': {
                                    'title':'Date conflict!',
                                    'message':'the dates you have entered for this module conflict with another module'
                                }
                                ,'value': {}}             
        
        return {}
    def DateTest(self, start, end):
        start = datetime.strptime(start,"%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(end,"%Y-%m-%d %H:%M:%S")
        start_hour=start.hour
        end_hour=end.hour
        logging.warning('start day: '+repr(start)+' end day: '+repr(end))
        logging.warning('end_hour: '+repr(end_hour)+' start_hour: '+repr(start_hour))
        #if modules are on the same day 
        diff = start_hour - end_hour
        if start.day == end.day:
            if start_hour == end_hour or math.abs(diff) < 2:
                return False
        
        return True
    def onchange_prof(self, cr, uid, ids, prof,  context=None):
        if prof:
            prof = self.pool.get('scholar.professor').browse(cr ,uid, prof, context=context)
            if not prof.inService:
                return {
                        'warningSwal': {
                            'title':'Professor incorrect!',
                            'message':'This professor is not in service any more!'
                        }
                        ,'value': {'idProfessor':''}}    
        return {}
scholar_timetable()