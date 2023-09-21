import json
__package__ = None

def load(filename): #Loads projects from JSON and formats them to a list of dicts sorted by id.
    projects = []
    try:
        file = open(filename)
        data = json.load(file)

        for i in data:
            if "project_id" in i:
                projects.append(i)

        sorted_projects = sorted(projects, key=lambda x: x["project_id"])
        file.close()
        return sorted_projects
    except:
        return None

def get_project_count(db): #Returns the amount of projects, i.e. the length of the list.
    return len(db)                                        
def get_project(db, id): #Retrives a project from the list by id.
    for i in db:
        if i["project_id"] == id: 
            return i
    return None

def search(db, sort_by="start_date", sort_order="desc", techniques=[], search=None, search_fields=None): #Returns a list of projects from the specified parametres.
    response = []
    for project in db:
        if search_fields == []: #If all fields are empty, return an empty list.
            return []
        elif search_fields == None: #If the fields are none, search all fields.
            if search == None:
                if techniques_allowed(project, techniques):
                    response.append(project)
            else:
                for key in project:
                    if type(project[key]) == str:
                        if project[key].lower() == search.lower() and techniques_allowed(project, techniques):
                            response.append(project)
        else:
            if search == None: #If search is none, return everything in the field
                if techniques_allowed(project, techniques):
                    response.append(project)
            else:
                for field in search_fields: 
                    if type(project[field]) == str:
                        if project[field].lower() == search.lower() and techniques_allowed(project, techniques):
                            response.append(project)
    sorted_list = sorted(response, key=lambda x: x[sort_by]) #Sorts the list by the given information.
    if sort_order == "desc":
        return sorted_list[::-1] #Returns a reversed list.
    else:
        return sorted_list


def techniques_allowed(pro, tech): #Checks if a project includes a searched for technique. Returns True if None.
    if tech != None:
        if len(tech) > 0:
            return all(t in pro["techniques_used"] for t in tech)
        
    return True
    

def get_techniques(db): #Returns a list of all techniques in the database.
    tech_list = []
    for project in db:
        for tech in project["techniques_used"]:
            tech_list.append(tech)
    
    tech_list  = list(dict.fromkeys(tech_list)) 
    return sorted(tech_list)

def get_technique_stats(db): #Returns a list of project per technique used. 
    stats = dict.fromkeys(get_techniques(db))
    for tech in stats:
        t_list = []
        for project in db:
            if tech in project["techniques_used"]:
                t_list.append({"id": project["project_id"], "name": project["project_name"]})
        stats[tech] = t_list
    return stats






