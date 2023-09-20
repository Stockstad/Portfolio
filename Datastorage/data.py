import json
__package__ = None

def load(filename):
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

def get_project_count(db):
    return len(db)                                        
def get_project(db, id):
    for i in db:
        if i["project_id"] == id: 
            return i
    return None

def search(db, sort_by="start_date", sort_order="desc", techniques=[], search=None, search_fields=None):
    response = []
    for project in db:
        if search_fields == []:
            return []
        elif search_fields == None:
            if search == None:
                if techniques_allowed(project, techniques):
                    response.append(project)
            else:
                for key in project:
                    if type(project[key]) == str:
                        if project[key].lower() == search.lower() and techniques_allowed(project, techniques):
                            response.append(project)
        else:
            if search == None:
                if techniques_allowed(project, techniques):
                    response.append(project)
            else:
                for field in search_fields:
                    if type(project[field]) == str:
                        if project[field].lower() == search.lower() and techniques_allowed(project, techniques):
                            response.append(project)
    sorted_list = sorted(response, key=lambda x: x[sort_by])
    if sort_order == "desc":
        return sorted_list[::-1]
    else:
        return sorted_list


def techniques_allowed(pro, tech):
    if tech != None:
        if len(tech) > 0:
            return all(t in pro["techniques_used"] for t in tech)
        
    return True
    

def get_techniques(db):
    tech_list = []
    for project in db:
        for tech in project["techniques_used"]:
            tech_list.append(tech)
    
    tech_list  = list(dict.fromkeys(tech_list)) 
    return sorted(tech_list)

def get_technique_stats(db):
    stats = dict.fromkeys(get_techniques(db))
    for tech in stats:
        t_list = []
        for project in db:
            if tech in project["techniques_used"]:
                t_list.append({"id": project["project_id"], "name": project["project_name"]})
        stats[tech] = t_list
    return stats



    




