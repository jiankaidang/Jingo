from Jingo.models import *

class NoteFilter(HttpRequestResponser, Formatter):
    
    def __init__(self):
        self.sql = SQLExecuter()
    
    def getValuesBasedonKey(self, valueset, key):
        result = []
        for row in valueset:
            result.append(row[key])
        return result
    
    def getNoteInfoList(self, currenttime):
        # retrieve every detail of notes
        strSQL    = 'Select a.*, b.tagid, c.sys_tagid, d.n_start_time, d.n_stop_time, n_repeat From note as a, note_tag as b, tag as c, (Select * From note_time Where %s between n_start_time And n_stop_time And n_repeat=0) as d Where a.noteid=b.noteid And b.tagid=c.tagid And a.noteid=d.noteid Union Select a.*, b.tagid, c.sys_tagid, d.n_start_time, d.n_stop_time, n_repeat From note as a, note_tag as b, tag as c, (Select * From note_time Where %s between n_start_time And n_stop_time And n_repeat=1) as d Where a.noteid=b.noteid And b.tagid=c.tagid And a.noteid=d.noteid'
        noteslist = self.sql.doRawSQL(strSQL, [currenttime, currenttime])
        return noteslist
    
    def getUserCategoryTagsList(self, data):
        args               = {}
        args['columns']    = ['b.*, c.sys_tagid']
        args['tables']     = ['state as a', 'filter as b', 'tag as c']
        args['joins']      = ['a.stateid=b.stateid And a.uid=b.uid And b.tagid=c.tagid And a.is_current=1 And is_checked=1']
        args['conditions'] = [{'criteria': 'b.uid=', 'logic': 'And'}]
        args['values']     = [data['uid']]
        uCTags             = self.sql.doSelectData(args)
        return uCTags
    
    def computeDistance(self, data, n_longitude, n_latitude):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [n_longitude, n_latitude, data['u_longitude'], data['u_latitude']])
        
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a    = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c    = 2 * asin(sqrt(a)) 
        dist = (6367 * c) * 1093.61 # km to yard
        return dist
    
    def filterByTags(self, uProfile, noteslist):
        result  = []
        passset = self.getValuesBasedonKey(uProfile, 'sys_tagid')
        for note in noteslist:
            if note['sys_tagid'] in passset:
                result.append(note)
        return result
    
    def filterByTime(self, uProfile, noteslist, currenttime):
        result      = []
        sys_tagset  = []
        for filter in uProfile:
            if filter.f_repeat:
                current = dateparse.parse_time(currenttime)
                start   = dateparse.parse_time(filter.f_start_time)
                end     = dateparse.parse_time(filter.f_stop_time)
            else:
                current = currenttime
                start   = filter.f_start_time
                end     = filter.f_stop_time
                
            if current >= start and current <= end:
                sys_tagset.append(filter.sys_tagid)
         
        for note in noteslist:
            if note['sys_tagid'] in sys_tagset:
                result.append(note)
        return result
    
    def filterByVisibility(self, data, uProfile, noteslist):
        friendslist = Friend().getFriendsList(data)
        # generalize visibility of user tags based on sys_tags
        sys_visset = {}
        filterset  = []
        for ufilter in uProfile:
            sys_tag    = ufilter.systagid
            visibility = ufilter.f_visibility
            if (sys_tag in sys_visset and sys_visset[sys_tag] < visibility) or (sys_tag not in sys_visset):
                sys_visset[sys_tag] = visibility
        
        for note in noteslist.values('noteid, sys_tagid, n_visibility, uid'):
            if note.sys_tagid in sys_visset and sys_visset[note.sys_tagid] == note.n_visibility:
                if (note.n_visibility == 1 and note.uid in friendslist) or note.n_visibility == 0:
                    filterset.append(note.noteid)
        
        noteslist = noteslist.objects.filter(noteid__in=filterset)
        return noteslist
    
    def filterByLocation(self, data, noteslist):
        filterset = []
        for note in noteslist.values('noteid, n_latitude, n_longitude, radius'):
            dist = self.computeDistance(data, note.n_longitude, note.n_latitude)
            if dist <= note.radius:
                filterset.append(note.noteid)
        noteslist.filter(noteid__in=filterset)
        return noteslist
    
    def filterNotes(self, data):
        currenttime = timezone.now()
        noteslist   = self.getNoteInfoList(currenttime)
        uProfile    = self.getUserCategoryTagsList(data)
        
        # filter by user's tags
        noteslist = self.filterByTags(uProfile, noteslist)
        
        # filter by user's time range
        noteslist = self.filterByTime(uProfile, noteslist, currenttime)
        
        # filter by visibility and friendship
        noteslist = self.filterByVisibility(data, uProfile, noteslist)
        
        # filter by location
        noteslist = self.filterByLocation(data, noteslist)
        return list(noteslist.values())