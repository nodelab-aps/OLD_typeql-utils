
import re 
import typeql_utils 

def get_attr_value_type(string):
    ''' 
        @usage infer the typeql value type of a string
        @return 
            one match -> Str: one of "LONG", "DOUBLE", "STRING", "BOOLEAN", "DATETIME"
            no matches -> False
            multiple matches -> None 
    '''
    string = typeql_utils.tidy_typeql_query(string)
    dict_value_pattern = {
        "LONG" : r"^\d+$",
        "DOUBLE" : r"^\d+\.\d+$" ,
        "STRING" : r"^'.*'$",
        "BOOLEAN" : r"^true$|^false$",
        "DATETIME" : r"^\d{4}-\d{2}-\d{2}$|^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$|^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$|^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.d$|^d{4}-d{2}-d{2}Td{2}:d{2}:d{2}\.d{2}$|^d{4}-d{2}-d{2}Td{2}:d{2}:d{2}\.d{3}$" 
    }
    value_out = False 
    for attr_value, pattern in dict_value_pattern.items(): 
        if re.match(pattern=re.compile(pattern), string=string):
            value_out = attr_value if not value_out else None 
    return value_out 

def check_clause_syntax(string):
    '''
        @usage evaluate syntax of a TypeQL query 
        @param string: a clause from a typeql query e.g. "$x isa person"
        @return True if valid else False 
        
        !!! WORK IN PROGRESS !!!

    '''
    verdict = True 
    
    string = typeql_utils.tidy_typeql_query(string)

    pattern_1_var = r"^\$[a-zA-z]+[a-zA-z0-9-_]*"
    # https://docs.vaticle.com/docs/schema/concepts#define-an-attribute
    pattern_1_has = "^has"
    pattern_2_var = "isa!?|has|key|sub!?|type|plays|relates|owns"
    
    list_substring = string.split(" ")
    if len(list_substring) == 2:
        # "$x 'Sarah'";
        verdict = isa_attr_clause_value_only(string)
    elif len(list_substring) == 3:
        # $x isa/isa!/sub/sub!/type type
        # $x has $attr
        # $x relates $attr

        if list_substring[0] == "has":
            #$x has $attr
            pass 
    elif len(list_substring) == 4:
        pass 
    elif len(list_substring) == 5:
        pass 
    return None 


def check_query_syntax(
    query
    ):
    '''@usage if query is syntactically invalid, raise ValueError
    @param query: typeql query, string 
    @return None
    TODO: finish check_clause_syntax and run it on each string
    TODO: this is a hack - need to anchor to typeql syntax 
    '''
    reason = None
    
    if "{" in query and "}" in query:
        if query.index("}") < query.index("{"):
            reason = "unmatched } in query"
        elif query.count("{") == 1 and query.count("}") == 1:
            reason = "unnecessary curly brackets around a single clause"
    else:
        if query.count("{") > query.count("}"):
            reason = "unmatched { in query"
        elif query.count("}") > query.count("{"):
            reason = "unmatched } in query"
    if reason:
        raise ValueError(reason)


def check_clause_schema_validity(string, dict_rootType_type_dict):
    '''
    @param dict_rootType_type_dict
        @return 
            if clause is syntactically and semantically valid:
                {
                    "variable": {
                        "concept_class": one of "thingType", "thing", "role", if it can be inferred else None 
                        "rootType": one of "entity", "relation", "attribute", "relation:role" if this can be inferred else None 
                        "isa": thingType to which variable is constrained as an instance, else None 
                        "type": thingType to which variable is constrained as a type, else None 
                        "owns": 
                        "role_played": 
                        "playing":
                        "constraint_relating":  one of isa, isa!, sub, sub!, type if present else None 
                        "constraint_playing":  one of isa, isa!, sub, sub!, type if present else None 
                        "value":  one of <, >, == 
                    }
                }
            else if clause is syntactically invalid:
                False
            else if clause is semantically invalid 
                None 
    
    !!! WORK IN PROGRESS !!!
    
    '''
    pass 




