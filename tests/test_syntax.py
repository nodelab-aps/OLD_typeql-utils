import pytest  
import typeql_utils 


class Test_get_attr_value_type:
    @pytest.mark.parametrize(
        "string,result",
        [
            ("2","LONG"),
            ("2.1","DOUBLE"),
            ("'Daniel'","STRING"),
            ("true","BOOLEAN"),
            ("1912-01-14", "DATETIME"),
            ("abc-09-02-1912", False),
        ]
    )
    def test1(self, string, result):
            assert typeql_utils.get_attr_value_type(string) == result 

class Test_check_query_syntax:
    @pytest.mark.parametrize(
        "query,result",
        [
            ("match {$x isa thing;} or {$x isa process;};",None),
        ]
    )
    def test1(self, query, result):
            assert typeql_utils.check_query_syntax(query) == result 
    
    @pytest.mark.parametrize(
        "query,result",
        [
            ("match {$x isa thing;} or $x isa process;}; ",None),
            ("match {$x isa thing;}; ",None),
        ]
    )
    def test_fails_1(self, query, result):
        with pytest.raises(ValueError):
            assert typeql_utils.check_query_syntax(query) == result 