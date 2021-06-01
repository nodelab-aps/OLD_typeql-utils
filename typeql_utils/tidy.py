import re 

def wrap_in_quotes(value, single=True):
    '''@usage check if value already has quotes. If not, add them.
    @param value: a value to be wrapped in quotes. Anything that can be coerced to string.
    @param single: wrap string in single quotes? bool
    @return a string wrapped in quotes e.g. "'jenna331@hotmail.com'"
    '''
    value = str(value)
    if '"' in value:
        value = value.replace('"',"")
    if "'" in value:
        value = value.replace("'","")
    value = "'" + value + "'" if single else '"' + value + '"'
    return value

def as_numeric(value, decimal_separator="."):
    '''@usage check if value already is numeric. If not, try to convert to float or integer
    @param value: a value to be returned as numeric
    @return float or int
    '''
    if not (isinstance(value, int) or isinstance(value, float)):
        if value.isnumeric():
            value = int(value)
        elif value.replace(decimal_separator,"").isnumeric():
            value = float(value.replace(".",decimal_separator).replace(",",decimal_separator))
    return value
        

def format_value_for_query(value, ValueType):
    '''
    @usage given some value and a grakn ValueType, return value in the appropriate format for a query
    ''' 
    if ValueType == "STRING":
        value = wrap_in_quotes(value, single=True)
    else:
        value = str(value)
        if ValueType == "BOOLEAN":
            value = value.lower()
    return value 


def tidy_typeql_query(string):
    '''@usage remove extra and trailing spaces and replace double with single quotes
    '''
    return re.sub(" +", " ", string).strip().replace('"',"'")

