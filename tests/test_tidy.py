import pytest  
import typeql_utils 


class Test_wrap_in_quotes:
    @pytest.mark.parametrize(
        "value,result",
        [
            ("'Daniel'","'Daniel'"),
            ("Daniel","'Daniel'"),
        ]
    )
    def test1(self, value, result):
            assert typeql_utils.wrap_in_quotes(value) == result 


class Test_as_numeric:
    @pytest.mark.parametrize(
        "value,decimal_separator,result",
        [
            ("2",".",2),
            ("2.1",".",2.1),
            ("2.1f",".","2.1f"),
            ("09-02-1912",".","09-02-1912")
        ]
    )
    def test1(self, value, decimal_separator, result):
        assert typeql_utils.as_numeric(value, decimal_separator) == result 


class Test_format_value_for_query:
    @pytest.mark.parametrize(
        "value,ValueType,result",
        [
            ("2","LONG","2"),
            ("2.1","FLOAT","2.1"),
            ("2.1f","STRING","'2.1f'"),
            ("TRUE","BOOLEAN","true"),
            ("09-02-1912","DATETIME","09-02-1912")
        ]
    )
    def test1(self, value, ValueType, result):
        assert typeql_utils.format_value_for_query(value, ValueType) == result


class Test_tidy_typeql_query:
    @pytest.mark.parametrize(
        "string,result",
        [
            (' Bob has  nickname  "the builder";', "Bob has nickname 'the builder';"),
        ]
    )
    def test1(self, string, result):
        assert typeql_utils.tidy_typeql_query(string) == result
