import re 
import typeql_utils


def parse_attr_clause(string):
    '''
        @usage determine if a string is an attribute clause and return a dict with the variable 
            assumes that query has been tidied up to remove double quotes and excess whitespace
        @return 
            dict {var_name: {}}
            if True, return a dict {}
        
    '''
    out = {
        
        "attribute_value":None
    }

    pattern_var = "^\$[a-zA-z]+[a-zA-z0-9-_]*"
    list_substring = string.split(" ")
    if len(list_substring) == 2:   
        # form "$x 'Sarah'"     
        check_1 = re.match(pattern=re.compile(pattern_var), string=list_substring[0])
        check_2 = get_attr_value_type(list_substring[1])
        if not all([check_1, check_2]):
            verdict = False 
        else:
            pass 
    elif len(list_substring) == 3:   
        # form "$x has $name"
        pass 
        #TODO
    elif len(list_substring) == 4:
        pass 
    return verdict


def check_query_schema_validity(query):
    '''
    @usage 
    @return a dict 
    #       keys: clause index
    #       values: list of errors 
    #       "syntax"
    #           arise when no suggestions are found and the query is not valid
    #       thing_thingType_conflict
    #              "thing_cannot_type"
    #              "isa_sub_conflcit"
    #              "thing_cannot_play", 
    #              "thing_cannot_relate", 
    #              "thing_cannot_own", 
    #       thingType_thing_conflict
    #               "type_cannot_isa"
    #               "type_cannot_has"
    #               "type_cannot_play"
    #               "type_cannot_relate"
    #               "type_cannot_key"
    #       schema conflicts
    #           playing    
    #               "ineligible_role_player", 
    #               "ineligible_relates" # incorrect role for relation
    #           attributes 
    #               "ineligible_has"
    #               "ineligible_key"
    '''


def get_query_vars(query, errors):
    
    dict_vars = {}

    # TODO this should be a dict describing, for each variable
    #   "concept": one of "thingType", "thing", "role", if it can be inferred else None 
    #   "rootType": one of "entity", "relation", "attribute", "relation:role" if this can be inferred else None 
    #   "type_constraint":  one of isa, isa!, sub, sub!, type if present else None 
    #   "outer_scope": whether the variable is referenced outside disjunctions, True or False 

    return dict_vars