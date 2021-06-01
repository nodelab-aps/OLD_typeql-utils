import re
import typeql_utils

# principle
# if there are no matches, return [] if syntax is valid, else None 
def complete_empty(string): 
    '''
    @usage given with an empty string, return a list of example query beginnings 
    @return list of str if string is empty else None 
    ''' 
    return [
        "$x isa! person;"
        "$x has name like '$.*'; ",
        "$rel (role1:$x, role2:$player2) isa relation;",
        ] if string == "" else None 


def complete_var(string, vars_thingType):
    '''
    @usage check if string is a substring of vars_thingType and return a list of matches 
    @return list of str if regex matches string (empty list if no variables match string) else None 
    '''
    if re.match(pattern=re.compile(r"^\$$|^\$[a-zA-Z]+[a-zA-Z0-9-_]*"),string=string): 
        list_out = [var for var in vars_thingType if string in var]
    else:  
        list_out = None 
    
    return list_out 


def complete_thing_var_verb(string):
    '''
    @usage treat string like a variable bound to a thing and provide verb options
    @return list of str if regex matches string else None 
    '''
    # TODO make examples from schema
    if re.match(pattern=re.compile(r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* $"),string=string): 
        list_out = [
            string + token for token in [
                "isa","isa!",
                "has","key",
                "contains","like","==", "<", " >", 
                "'Joe Bloggs'", "2.3", "true", "14-02-2005"
                "("]
        ] 
    else: 
        list_out = None 

    return list_out 


def complete_thingType_var_verb(string):
    '''
    @usage treat string like a variable bound to a thingType and provide verb options
    @return list of str if regex matches string else None 
    '''
    if re.match(re.compile(r"^\$[a-zA-Z]+[a-zA-Z0-9-_]*$"),string): 
        list_out = [
            string + " " + token for token in ["relates","plays", "owns","type", "sub", "sub!"]
        ] 
    else: 
        list_out = None 
    return list_out 


def complete_predicate_isa(string, vars_thingType, thingTypes):
    '''
    @usage takes a partial isa clause (not isa relation) from a typeql query and returns autocomplete options
    NB: string must have already been stripped of whitespace
    @return list of str if regex matches any string (empty list if no variable or type names do) else None 
    '''
    any_matches = False 

    list_complete_var = complete_var(string, vars_thingType)
    if list_complete_var == None: 
        list_complete_var = [] 

    dict_pattern_list_out = {
        # $
        r"^\$$": [],#vars_thingType,

        # $x
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]*$": [],#[string +  " isa"] + list_complete_var,

        # $x is?
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* i?$|^\$\w+ is?$":[
            string.split(" ")[0] + f" {verb}" for verb in ["isa", "isa!"]
        ], 

        # $x isa!?
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* isa!?$":[
            string +  f" {thingType}" for thingType in thingTypes
        ], 
        
        # $x isa!? perso
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* isa!? [a-zA-Z]+[a-zA-Z0-9-_]*$": [" ".join(string.split(" ")[0:-1]) + f" {thingType}" for thingType in thingTypes if string.split(" ")[-1].strip() in thingType], 

        # $x isa!? person
        r"|".join([rf"^\$[a-zA-Z]+[a-zA-Z0-9-_]* isa!? {thingType}$" for thingType in thingTypes]):[
            string + punct for punct in [",",";"]
        ],
    } 
    list_out = []
    for pattern, list_options in dict_pattern_list_out.items():
        if re.match(pattern=re.compile(pattern), string=string):
            list_out += list_options 
            any_matches = True 
            break 
    return list_out if any_matches else None 


def complete_predicate_isa_relation(
    string, 
    vars_thingType, 
    dict_rootType_type_dict
    ):
    '''
    @usage takes a partial isa relation query and returns autocomplete options
    NB: string must have already been stripped of whitespace
    @return list of str if regex matches any string (empty list if no variable or type names do) else None 
    '''
    any_matches = False 
    list_complete_var = complete_var(string, vars_thingType)
    if list_complete_var == None: 
        list_complete_var = [] 
    dict_pattern_list_out = {
        r"^$": [],

        # $
        r"^\$$": [],#vars_thingType,
        
        # $rel 
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]*$":[],#list_complete_var+[string +  " ("],
        
        # $rel ( 
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* \($": [ # role name 
            string + f"{role}" + ":" for role in [role for rel in dict_rootType_type_dict["relation"].keys() for role in dict_rootType_type_dict["relation"][rel]["relates"].keys()] 
        ] + [ 
            string + var_thingType for var_thingType in list(set(vars_thingType + ["$roleplayer"])) if not var_thingType in string
        ],# + [ # assign role to a variable instead 
          #  string + f"${role}" for role in [role for rel in dict_rootType_type_dict["relation"].keys() for role in dict_rootType_type_dict["relation"][rel]["relates"].keys()] 
        #], # or just use a variable for the role_player 

        # $rel (role_label 
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* \([a-zA-Z]+[a-zA-Z0-9-_]*$": [ 
            re.sub(re.compile(r"[a-zA-Z]+[a-zA-Z0-9-_]*$"), "", string) +  f"{role}" for role in [role for rel in dict_rootType_type_dict["relation"].keys() for role in dict_rootType_type_dict["relation"][rel]["relates"].keys()] if string.split("(")[-1] in role and not string.split("(")[-1] == role
        ] + [
            string + ":"
        ], 

        # $rel ($
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* \(\$$":[
            string + var_thingType.replace("$","") for var_thingType in list(set(vars_thingType + ["$roleplayer"])) if not var_thingType in string
        ],
        
        #+ [ 
          #  string + f"{role}" for role in [role for rel in dict_rootType_type_dict["relation"].keys() for role in dict_rootType_type_dict["relation"][rel]["relates"].keys()] 
        #],

        # $rel ($role
        # $rel ($roleplayer 
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* \(\$[a-zA-Z]+[a-zA-Z0-9-_]*$":[ 
            re.sub(re.compile(r"[a-zA-Z]+[a-zA-Z0-9-_]*$"), "", string) +  f"{role}" for role in [role for rel in dict_rootType_type_dict["relation"].keys() for role in dict_rootType_type_dict["relation"][rel]["relates"].keys()] if string.split("$(")[-1] in role and not string.split("($")[-1] == role
        ] + [
            string + punct for punct in [":",",",")"]
        ],

        # ( 
        # relation is not assigned to variable
        r"^\($":[ 
            string + f"{role}" + "" for role in [role for rel in dict_rootType_type_dict["relation"].keys() for role in dict_rootType_type_dict["relation"][rel]["relates"].keys()] 
        ] + [
            string + var_thingType for var_thingType  in list(set(vars_thingType + ["$roleplayer"])) 
        ],# + [ # assign role to a variable instead 
         #  string + f"${role}" for role in [role for rel in dict_rootType_type_dict["relation"].keys() for role in dict_rootType_type_dict["relation"][rel]["relates"].keys()] 
        #] , # or just use a variable for the role_player 

        # (role_label 
        r"^\([a-zA-Z]+[a-zA-Z0-9-_]*$":[
            "(" +  f"{role}" for role in [role for rel in dict_rootType_type_dict["relation"].keys() for role in dict_rootType_type_dict["relation"][rel]["relates"].keys()] if string.replace("(","") in role and not string.replace("(","") == role
        ] + [
            string + ":"
        ], 

        # ($
        r"^\(\$$":[
            "(" + var_thingType for var_thingType in list(set(vars_thingType + ["$roleplayer"])) 
        ],#+ [ 
          #  string + f"{role}" for role in [role for rel in dict_rootType_type_dict["relation"].keys() for role in dict_rootType_type_dict["relation"][rel]["relates"].keys()] 
        #],

        # ($role
        # ($roleplayer 
        r"^\(\$[a-zA-Z]+[a-zA-Z0-9-_]*$":[
            "(" +  f"${role}" for role in [role for rel in dict_rootType_type_dict["relation"].keys() for role in dict_rootType_type_dict["relation"][rel]["relates"].keys()] if string.replace("($","") in role and not string.replace("($","") == role
        ] + [
            string + punct for punct in [":",",",")"]
        ],

        # $rel (role_label: 
        # $rel ($role:
        # $rel ($roleplayer:
        # (role_label: 
        # ($role:
        # ($roleplayer:
        r"\(\$?[a-zA-Z]+[a-zA-Z0-9-_]*:$":[
            string + rp_var for rp_var in set(["$role_player"]+ vars_thingType)  # TODO keep track of these variables
        ], 

        # ... (...)
        r"\(.+\)$":[
            string + f" isa {rel}" for rel in dict_rootType_type_dict["relation"].keys() # a relationtype 
        ] + [
            string + f" isa $relation"
            ],
        
        r"\(.+\) is?a?$":[
            " ".join(string.split(" ")[0:-1]) + f" isa {rel}" for rel in dict_rootType_type_dict["relation"].keys() # a relationtype 
        ] + [
            " ".join(string.split(" ")[0:-1]) + " isa $relation"
        ], 

        # "\(\w*\) isa$":[
        #     string + f" {rel}" for rel in dict_rootType_type_dict["relation"].keys() # a relationtype 
        # ] + [
        #     string + " $relation"
        # ], 
    }

    list_out = []
    for pattern, list_options in dict_pattern_list_out.items():
        if re.search(pattern=re.compile(pattern), string=string):
            list_out += list_options
            any_matches = True   
            break 
    return list_out if any_matches else None 


def complete_predicate_has_attribute(
    string,
    vars_thingType, 
    dict_rootType_type_dict
    ):
    '''
    @usage takes a partial attribute query and returns autocomplete options
    NB: string must have already been stripped of whitespace
    @return list of str if regex matches any string (empty list if no variable or type names do) else None 
    '''
    any_matches = False 
    list_complete_var = complete_var(string, vars_thingType)
    if list_complete_var == None: 
        list_complete_var = [] 
    dict_pattern_list_out = {
        # $
        r"^\$$": [],#vars_thingType,

        # $x
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]*$":[],#list_complete_var+[string +  " ("],

        # $x ha? 
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* ha?$": [
            string.split(" ")[0] + " has"
        ], 

        # $x ke?
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* ke?$": [
            string.split(" ")[0] + " key"
        ],

        # $x has 
        
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* has$|^\$[a-zA-Z]+[a-zA-Z0-9-_]* key$": [
            string + " " + attr for attr in dict_rootType_type_dict["attribute"].keys()
        ] + list(set([
            string + " $attribute"
        ] + [
            string + " " + var_thingType for var_thingType in vars_thingType
        ])), 

        # ha?
        r"^ha?$": [
            "has"
        ], #TODO

        # ke?
        r"^ke?$": [
            "key"
        ],

        # has
        # key
        r"^has$|^key$": [
            string + " " + attr for attr in dict_rootType_type_dict["attribute"].keys()
        ] + list(set([
            string + " $attribute"
        ] + [
            string + " " + var_thingType for var_thingType in vars_thingType
        ])),

        # $x has $
        # $x key $
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* has \$$|^\$[a-zA-Z]+[a-zA-Z0-9-_]* key \$$": list(set(
        [
            string[0:-1] + "$attribute"
        ] + [
            string[0:-1] + var_thingType for var_thingType in vars_thingType
        ])),

        # has $
        # key $
        r"^has \$$|^key \$$":list(set(
        [
            string[0:-1] + "$attribute"
        ] + [
            string[0:-1] + var_thingType for var_thingType in vars_thingType
        ])),

        # $x has $attr        
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* has \$[a-zA-Z]+[a-zA-Z0-9-_]*$|^\$[a-zA-Z]+[a-zA-Z0-9-_]* key \$[a-zA-Z]+[a-zA-Z0-9-_]*$":[
            " ".join(string.split(" ")[0:-1]) + " " + var_thingType for var_thingType in vars_thingType + ["$attribute"] if string.split(" ")[-1] in var_thingType
        ] + [string + ";", string + ","],
        
        # $x key $attr
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* key \$[a-zA-Z]+[a-zA-Z0-9-_]*$|^\$[a-zA-Z]+[a-zA-Z0-9-_]* key \$[a-zA-Z]+[a-zA-Z0-9-_]*$":[
            " ".join(string.split(" ")[0:-1]) + " " + var_thingType for var_thingType in vars_thingType + ["$attribute"] if string.split(" ")[-1] in var_thingType
        ] + [string + ";", string + ","],

        # $x has heig
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* has [a-zA-Z]+[a-zA-Z0-9-_]*$|^\$[a-zA-Z]+[a-zA-Z0-9-_]* key [a-zA-Z]+[a-zA-Z0-9-_]*$":[
            " ".join(string.split(" ")[0:-1]) + " " + attr for attr in dict_rootType_type_dict["attribute"].keys() if string.split(" ")[-1] in attr
        ],
        
        # $x key UI
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* key [a-zA-Z]+[a-zA-Z0-9-_]*$|^\$[a-zA-Z]+[a-zA-Z0-9-_]* key [a-zA-Z]+[a-zA-Z0-9-_]*$":[
            " ".join(string.split(" ")[0:-1]) + " " + attr for attr in dict_rootType_type_dict["attribute"].keys() if string.split(" ")[-1] in attr
        ],

        # has $attr
        r"^has \$[a-zA-Z]+[a-zA-Z0-9-_]*$|^key \$[a-zA-Z]+[a-zA-Z0-9-_]*$":[
            " ".join(string.split(" ")[0:-1]) + " " + var_thingType for var_thingType in vars_thingType + ["$attribute"] if string.split(" ")[-1] in var_thingType
        ] + [string + ";", string + ","],

        # key $attr
        r"^key \$[a-zA-Z]+[a-zA-Z0-9-_]*$|^key \$[a-zA-Z]+[a-zA-Z0-9-_]*$":[
            " ".join(string.split(" ")[0:-1]) + " " + var_thingType for var_thingType in vars_thingType + ["$attribute"] if string.split(" ")[-1] in var_thingType
        ] + [string + ";", string + ","],

        # has heig
        r"^has [a-zA-Z]+[a-zA-Z0-9-_]*$|^key [a-zA-Z]+[a-zA-Z0-9-_]*$":[
            " ".join(string.split(" ")[0:-1]) + " " + attr for attr in dict_rootType_type_dict["attribute"].keys() if string.split(" ")[-1] in attr
        ],

        # key UI
        r"^key [a-zA-Z]+[a-zA-Z0-9-_]*$|^key [a-zA-Z]+[a-zA-Z0-9-_]*$":[
            " ".join(string.split(" ")[0:-1]) + " " + attr for attr in dict_rootType_type_dict["attribute"].keys() if string.split(" ")[-1] in attr
        ],

        # $x has name contai
        # $x has $attr contai
        r"|".join([
            r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* has \$?[a-zA-Z]+[a-zA-Z0-9-_]* " + r"contain"[0:i] for i in range(1,len("contain"))]) :[
                " ".join(string.split(" ")[0:-1]) + " contains"
            ],

        # $x key name contai
        # $x key $attr contai
        r"|".join([
            r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* key \$?[a-zA-Z]+[a-zA-Z0-9-_]* " + r"contain"[0:i] for i in range(1,len("contain"))]) :[
                " ".join(string.split(" ")[0:-1]) + " contains"
            ],

        # $x has name li
        # $x has $attr lik
        r"|".join([
            r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* has \$?[a-zA-Z]+[a-zA-Z0-9-_]* " + r"like"[0:i] for i in range(1,len("like"))]) :[
                " ".join(string.split(" ")[0:-1]) + " like"
            ],
        
        # $x key name l
        # $x key $attr lik
        r"|".join([
            r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* key \$?[a-zA-Z]+[a-zA-Z0-9-_]* " + r"like"[0:i] for i in range(1,len("like"))]) :[
                " ".join(string.split(" ")[0:-1]) + " like"
            ],

        # has name contai
        # has $attr contai
        r"|".join([
            r"^has \$?[a-zA-Z]+[a-zA-Z0-9-_]* " + r"contain"[0:i] for i in range(1,len("contain"))]) :[
                " ".join(string.split(" ")[0:-1]) + " contains"
            ],
        
        # has name li
        # has $attr lik
        r"|".join([
            r"^has \$?[a-zA-Z]+[a-zA-Z0-9-_]* " + r"like"[0:i] for i in range(1,len("like"))]) :[
                " ".join(string.split(" ")[0:-1]) + " like"
            ],
        
        # key name contai
        # key $attr contai
        r"|".join([
            r"^key \$?[a-zA-Z]+[a-zA-Z0-9-_]* " + r"contain"[0:i] for i in range(1,len("contain"))]) :[
                " ".join(string.split(" ")[0:-1]) + " contains"
            ],
        
        # key name li
        # key $attr lik
        r"|".join([
            r"^key \$?[a-zA-Z]+[a-zA-Z0-9-_]* " + r"like"[0:i] for i in range(1,len("like"))]) :[
                " ".join(string.split(" ")[0:-1]) + " like"
            ],

        # $attr contai
        # $attr con
        # $attr con
        # $attr contai
        r"|".join([
            r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* " + r"contain"[0:i] for i in range(1,len("contain"))]) :[
                " ".join(string.split(" ")[0:-1]) + " contains"
            ],
        
        # $attr li
        # $attr lik
        # $attr l
        # $attr lik
        r"|".join([
            r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* " + r"like"[0:i] for i in range(1,len("like"))]) :[
                " ".join(string.split(" ")[0:-1]) + " like"
            ],
            
        # $x has name 'S
        # $x has $attr 'Sar 
        # $x has attr 123   
        # $x key attr 123.4
        # $x key attr tru
        # $x has attr 20-01-201
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* has \$?[a-zA-Z]+[a-zA-Z0-9-_]* '?.+$|^\$[a-zA-Z]+[a-zA-Z0-9-_]* key \$?[a-zA-Z]+[a-zA-Z0-9-_]* '?.+$": [
            string + punct for punct in [",",";","'"] if punct in [",",";"] or punct in string.split(" ")[-1]
        ] if typeql_utils.get_attr_value_type(string.split(" ")[-1]) else [string + "'"] ,
        # suggest punctuation if the value is valid

        # has name 'S
        # key identifier 'S
        # has $attr 'Sar 
        # has attr 123   
        # has attr 123.4
        # has attr tru
        # has attr 20-01-201
        r"^has \$?[a-zA-Z]+[a-zA-Z0-9-_]* '?.+$|^key \$?[a-zA-Z]+[a-zA-Z0-9-_]* '?.+$": [
            string + punct for punct in [",",";","'"] if punct in [",",";"] or punct in string.split(" ")[-1]
        ] if typeql_utils.get_attr_value_type(string.split(" ")[-1]) else [string + "'"] if "'" in string else  [],
        # suggest punctuation if the value is valid

        # $attr 'Sar 
        # $attr 123   
        # $attr 123.4
        # $attr tru
        # $attr 2020-01-01
        r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* '?.+$": [
            string + punct for punct in [",",";","'"] if punct in [",",";"] or punct in string.split(" ")[-1]
        ] if typeql_utils.get_attr_value_type(string.split(" ")[-1]) else [string + "'"] if "'" in string else [],

    }

    list_out = []
    for pattern, list_options in dict_pattern_list_out.items():
        if re.search(pattern=re.compile(pattern), string=string):
            list_out += list_options
            any_matches = True   
            break 
    return list_out if any_matches else None 


# schema type predicates 
def complete_predicate_type():
    pass 
def complete_predicate_plays():
    pass 
def next_relates():
    pass 
def next_owns():
    pass 
def next_owns():
    pass 

def autocomplete_data_match_query(
    query,
    dict_rootType_type_dict,
    ):
    '''
    @usage auto-complete typeql data read query
           given a user input, suggest list of next token and determine if query is valid
    @param string: user input string
    @param dict_rootType_type_dict: dict as returned by get_schema_types_dict()
    @return 
        a dict containing
            "suggestions": list of autocomplete suggestions (str) 
            "status": one of "valid", "incomplete", "invalid",
            "error": None if query is valid or incomplete else an error describing the problem
    '''

    error=None 
    status=None 

    # Note there are different layers of logic to predict and verify 
    # 1. syntax 
    #   i) clause syntax - in progress
    #   ii) overall query syntax - including disjunctions, negations
    # 2. static schema awareness
    #   i) relations: 
    #       - roles related
    #       - roles played
    #   ii) attributes: 
    #       - attributes owned
    # 3. static variable reuse 
    # 4. query semantics - todo
    #   i) keep track of variable binding 


    # 1. Determine if query is valid, incomplete or invalid
        # infer existing variables and their constraints. 
        # disjunctions
        # negations
    # 2. triage the partial clause, using the dict_vars
    #   variable ... 
    #   variable isa/isa!
    #   variable sub/sub!/type
    #   variable isa/isa! relation
    #   [variable] has/key
    #   variable owns
    #   [variable] plays # is this ok syntax?
    #   variable relates
    #   variable operator [variable/value]

    
    thingTypes = list(dict_rootType_type_dict["entity"].keys()) + list(dict_rootType_type_dict["relation"].keys()) + list(dict_rootType_type_dict["attribute"].keys())
    thingTypes += ["entity", "relation", "attribute"]
    
    # get variables
    # todo: call a function
    #dict_vars = {}
    
    if "$" in query:
        pattern_split = re.compile(r" |,|;|\{|\}|\(|\)")
        list_vars = list(filter(lambda fragment: "$" in fragment, re.split(pattern_split,string=query)))
        list_vars = list(set(list_vars))
    else:
        list_vars = []
        
        # for each_var in list_vars:
        #     dict_vars[each_var] = {"concept":None, "rootType":None, "type_constraint":None, "outer_scope":False, "errors":[]}
    # else:
    #     dict_vars["$x"] = {"concept":None, "rootType":None, "type_constraint":None, "outer_scope":False, "errors":[]}

    query_clean = typeql_utils.tidy_typeql_query(query.replace("match",""))
    string = re.split(r";|,",query_clean)[-1].strip()

    list_out = []
    if string == "":
        list_out += complete_empty(string)
    elif re.match(pattern=re.compile(r"^\$$|^\$[a-zA-Z]+[a-zA-Z0-9-_]*$"), string=string):
        list_out += complete_var(string, list_vars)
    elif re.match(pattern=re.compile(r"^\$[a-zA-Z]+[a-zA-Z0-9-_]*$ "), string=string):
        list_out += complete_thing_var_verb(string)
    else:
        list_out_predicate_isa = complete_predicate_isa(string,list_vars, thingTypes)
        
        if list_out_predicate_isa:
            list_out += list_out_predicate_isa
        
        list_out_predicate_isa_relation = complete_predicate_isa_relation(
            string=string, 
            vars_thingType=list_vars,
            dict_rootType_type_dict=dict_rootType_type_dict)
        
        if list_out_predicate_isa_relation:
            list_out += list_out_predicate_isa_relation
        
        list_out_predicate_has_attribute = complete_predicate_has_attribute(
            string=string, 
            vars_thingType=list_vars,
            dict_rootType_type_dict=dict_rootType_type_dict)

        if list_out_predicate_has_attribute:
            list_out += list_out_predicate_has_attribute

    # if re.match(pattern=r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* i|", string=string): # beginning of isa 
    #     list_out = isa_next(string, vars_thingType, thingTypes)
    # elif re.match(pattern=r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* h", string=string): # beginning of has  
    #     list_out = [string + " has"] # TODO write handler
    # elif re.match(pattern=r"^\$[a-zA-Z]+[a-zA-Z0-9-_]* k", string=string): # beginning of key  
    #     list_out = [string + " key"] # TODO write handler
    # elif re.match(pattern="^h", string=string): # beginning of ", has .. " clause 
    #     pass
        # when are we allowed to do "... , has age < 234 .. "?
    # also allow for $x "Anette", i.e. match any attribute
        
    # deal with types
    
    #   [variable] plays 
    #   role relates
    #   variable operator [variable/value]
    suggestions = [query.replace(string, out) for out in list_out]
    return {"suggestions":suggestions, "status":status, "error":error} 
