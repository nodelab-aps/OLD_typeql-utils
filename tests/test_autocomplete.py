import pytest  
import typeql_utils 
from .fixtures import * 

class Test_complete_empty:
    @pytest.mark.parametrize(
        "string,result",
        [
            (
                "", 
                [
                "$x isa! person;"
                "$x has name like '$.*'; ",
                "$rel (role1:$x, role2:$player2) isa relation;",
                ]
            ), 
            (
                "$x", None 
            )
        ])
    def test1(self, string, result):
        assert typeql_utils.complete_empty(string) == result 

class Test_complete_var:  
    @pytest.mark.parametrize(
        "string,vars_thingType,result",
        [
            (
                "",
                ["$x","$y", "$rel_1", "$rp-1"], 
                None
            ),
            (
                "$",
                ["$x","$y", "$rel_1", "$rp-1"],
                ["$x","$y", "$rel_1", "$rp-1"]
            ),
            (
                "$r",
                ["$x","$y", "$rel_1", "$rp-1"],
                ["$rel_1", "$rp-1"]
            ),
            (
                "$x",
                [],
                []
            ),
            (
                "r$",
                ["$x","$y", "$rel_1", "$rp-1"],
                None
            ),
            (
                "r",
                ["$x","$y", "$rel_1", "$rp-1"],
                None 
            ),
            (
                "3",
                ["$x","$y", "$rel_1", "$rp-1"],
                None 
            ),
            (
                "-",
                ["$x","$y", "$rel_1", "$rp-1"],
                None 
            ),
        ])
    def test1(self,string,vars_thingType,result):
        assert typeql_utils.complete_var(string=string, vars_thingType=vars_thingType) == result 
        
class Test_complete_thing_var_verb: 
    @pytest.mark.parametrize(
        "string, result",
        [
            (
                "$x ",
                ["$x" + " " + token for token in [
                "isa","isa!",
                "has","key",
                "contains","like","==", "<", " >", 
                "'Joe Bloggs'", "2.3", "true", "14-02-2005"
                "("]],
            ), 
            (
                "$2 ",
                None
            ), 
            (
                "$-",
                None
            ), 
            (
                "$",
                None
            ), 
            (
                "m$",
                None
            ), 
            (
                "2$",
                None
            ), 
            (
                "",
                None
            ), 
        ])
    def test1(self, string, result):
        assert typeql_utils.complete_thing_var_verb(string) == result 


class Test_complete_thingType_var_verb:
    @pytest.mark.parametrize(
        "string, result",
        [
            (
                "$x", 
                ["$x" + " " + token for token in ["relates","plays", "owns","type", "sub", "sub!"]]
            ), 
            ("x$", None), 
            ("$-", None),
            ("$1", None),
            ("$1", None)
        ])
    def test1(self, string, result):
        assert typeql_utils.complete_thingType_var_verb(string) == result  

class Test_complete_predicate_isa:
    @pytest.mark.parametrize(
        "string, vars_thingType, thingTypes, list_result_expected",
        [
            (
                "", 
                ["$rel", "$relative", "$person1", "$house1"],
                ["relative", "person", "house"],
                None
            ), 
            (
                "$", 
                ["$rel", "$relative", "$person1", "$house1"],
                ["relative", "person", "house"],
                [],
            ), 
            (
                "$r", 
                ["$rel", "$relative", "$person1", "$house1"],
                ["relative", "person", "house"],
                [],
            ), 
            (
                "$rel i", 
                ["$rel", "$relative", "$person1", "$house1"],
                ["relative", "person", "house"],
                ["$rel isa", "$rel isa!"],
            ), 
            (
                "$rel isa", 
                ["$rel", "$relative", "$person1", "$house1"],
                ["relative", "person", "house"],
                ["$rel isa relative", "$rel isa person", "$rel isa house"],
            ), 
            (
                "$rel isa!",
                ["$rel", "$relative", "$person1", "$house1"],
                ["relative", "person", "house"],
                ["$rel isa! relative", "$rel isa! person", "$rel isa! house"],
            ), 
            (
                "$rel isa pe", 
                ["$rel", "$relative", "$person1", "$house1"],
                ["relative", "person", "pensioner", "house"],
                ["$rel isa person", "$rel isa pensioner"],
            ), 
            (
                "$rel isa person", 
                ["$rel", "$relative", "$person1", "$house1"],
                ["relative", "person", "pensioner", "house"],
                ["$rel isa person"],
            ), 
            (
                "$rel sub person", 
                ["$rel", "$relative", "$person1", "$house1"],
                ["relative", "person", "pensioner", "house"],
                None
            ), 
            (
                "rel is person", 
                ["$rel", "$relative", "$person1", "$house1"],
                ["relative", "person", "pensioner", "house"],
                None
            ),
            (
                "$rel isa!! -person", 
                ["$rel", "$relative", "$person1", "$house1"],
                ["relative", "person", "pensioner", "house"],
                None
            )

        ])
    def test1(self, string, vars_thingType, thingTypes, list_result_expected):
        assert typeql_utils.complete_predicate_isa(string, vars_thingType, thingTypes) == list_result_expected 
                        
class Test_complete_predicate_isa_relation():
    @pytest.mark.parametrize(
        "string, list_result_expected",
        [
            ( # 0 
                "",
                [],
            ), 
            ( 
                "$",
                []
            ), 
            (
                "x",
                None
            ),
            (
                "$r",
                [],
            ), 
            (
                "$rel (",
                [
                    '$rel (party:',
                    '$rel (disputing-landlord:',
                    '$rel (main-tenancy:',
                    '$rel (sublandlord:',
                    '$rel (subtenant:',
                    '$rel (disputed-tenancy:',
                    '$rel (disputing-tenant:',
                    '$rel (disputed-subject:',
                    '$rel (is-neighbour:',
                    '$rel (birthed-child:', 
                    '$rel (landlord:', 
                    '$rel (tenant:', 
                    '$rel (rented-property:', 
                    '$rel ($person',
                    '$rel ($attr',
                    '$rel ($relation',
                    '$rel ($x',
                    '$rel ($address',
                    '$rel ($rented',
                    '$rel ($roleplayer'
                    ] 
            ), 
            ( # 5
                "$rel (is-neighbour",
                ["$rel (is-neighbour:"]
            ),
            (
                "$rel ($is-neighbour",
                ["$rel ($is-neighbour:", "$rel ($is-neighbour,", "$rel ($is-neighbour)"]
            ), 
            (
                "(",
                [
                    '(tenant',
                    '(birthed-child',
                    '(subtenant',
                    '(is-neighbour',
                    '(landlord',
                    '(main-tenancy',
                    '(disputing-tenant',
                    '(disputing-landlord',
                    '(party',
                    '(disputed-subject',
                    '(disputed-tenancy',
                    '(sublandlord',
                    '(rented-property',
                    '($person',
                    '($attr',
                    '($relation',
                    '($x',
                    '($address',
                    '($rented',
                    '($roleplayer'
                ] 
            ), 
            (
                "(is-neighbour",
                ["(is-neighbour:",] 
            ), 
            (
                "($",
                ['($address', '($attr', '($person', '($relation', '($rented', '($roleplayer', '($x'] 
            ), 
            ( # 10
                "($x",
                ["($x:","($x,","($x)"] 
            ), 
            ( 
                "($role1:",
                ['($role1:$address','($role1:$attr', '($role1:$person', '($role1:$relation', '($role1:$rented', '($role1:$role_player', '($role1:$x']
            ), 
            (
                "$rel ($role1:rp1)",
                [   
                    "$rel ($role1:rp1) isa $relation",
                    "$rel ($role1:rp1) isa birth", 
                    "$rel ($role1:rp1) isa tenancy", 
                    "$rel ($role1:rp1) isa subtenancy", 
                    "$rel ($role1:rp1) isa subtenancy", 
                    "$rel ($role1:rp1) isa neighbourship", 
                    "$rel ($role1:rp1) isa dispute", 
                    "$rel ($role1:rp1) isa tenancy-dispute"
                    ]
            ), 
            (
                "$rel ($role1:rp1) i",
                [   
                    "$rel ($role1:rp1) isa $relation",
                    "$rel ($role1:rp1) isa birth", 
                    "$rel ($role1:rp1) isa tenancy", 
                    "$rel ($role1:rp1) isa subtenancy", 
                    "$rel ($role1:rp1) isa subtenancy", 
                    "$rel ($role1:rp1) isa neighbourship", 
                    "$rel ($role1:rp1) isa dispute", 
                    "$rel ($role1:rp1) isa tenancy-dispute"
                    ]
            )
        ])
    def test1(self, string, dict_rootType_type_dict_tenancy, list_result_expected):
        vars_thingType = ["$x", "$rented", "$relation", "$person", "$attr", "$address"]
        #vars_role_player = ["$x", "$rented", "$person"]

        list_result = typeql_utils.complete_predicate_isa_relation(
                    string=string, 
                    vars_thingType=vars_thingType, 
                    dict_rootType_type_dict=dict_rootType_type_dict_tenancy
                    ) 
        if list_result:
            assert set(list_result) == set(list_result_expected)
        else: 
            assert list_result == list_result_expected 

class Test_complete_predicate_has_attribute():
    @pytest.mark.parametrize(
        "string, list_result_expected",
        [
            ( #0
                "$",[]
            ),
            (
                "$x",[]
            ),
            (
                "$x h",["$x has"]
            ), 
            (
                "$x ke",["$x key"]
            ),
            (  
                "$x has",[
                    '$x has UID', '$x has address', '$x has name', '$x has starting-date', '$x has $address', '$x has $attr', '$x has $attribute', '$x has $person', '$x has $relation', '$x has $rented', '$x has $x'
                ] 
            ),
            (  # 5
                "$x key",[
                    '$x key UID', '$x key address', '$x key name', '$x key starting-date', '$x key $address', '$x key $attr', '$x key $attribute', '$x key $person', '$x key $relation', '$x key $rented', '$x key $x'
                ] 
            ),
            (
                "ha",["has"] # TODO
            ), 
            (
                "ke",["key"]
            ),
            (
                "has",[
                    'has $address', 'has $attr', 'has $attribute', 'has $person', 'has $relation', 'has $rented', 'has $x', 'has UID', 'has address', 'has name', 'has starting-date'
                ] 
            ),
            (
                "key", [
                    'key $address', 'key $attr', 'key $attribute', 'key $person', 'key $relation', 'key $rented', 'key $x', 'key UID', 'key address', 'key name', 'key starting-date'
                ]  
            ), 
            ( # 10
                "$person has $",[
                    '$person has $address', '$person has $attr', '$person has $attribute', '$person has $person', '$person has $relation', '$person has $rented', '$person has $x'
                ] 
            ),
            (
                "$man key $",[
                    '$man key $address', '$man key $attr', '$man key $attribute', '$man key $person', '$man key $relation', '$man key $rented', '$man key $x'
                ] # TODO
            ),
            (
                "has $",[
                    'has $attribute', 'has $address', 'has $attr', 'has $person', 'has $relation', 'has $rented', 'has $x'
                ] # TODO
            ), 
            (
                "key $",[
                    'key $attribute', 'key $address', 'key $attr', 'key $person', 'key $relation', 'key $rented', 'key $x'
                ]# TODO
            ),
            (
                "$p1 has $a", 
                [
                    '$p1 has $a,', '$p1 has $a;',
                    "$p1 has $address", "$p1 has $attr", "$p1 has $attribute"] 
            ),
            
            ( # 15
                "$home has addre",["$home has address"]
            ),
            (
                "$patient-12 key UI",["$patient-12 key UID"]
            ), 
            (
                "has $add",["has $address","has $add,", "has $add;"]
            ),
            (
                "key $addre",["key $address", "key $addre,", "key $addre;"]
            ), 
            (
                "has nam",["has name"]
            ),
            ( # 20
                "key UI",["key UID"]
            ), 
            (
                "has name conta",["has name contains"]
            ),
            (
                "key address cont",["key address contains"]
            ), 
            (
                "$p1 has $attr conta",["$p1 has $attr contains"]
            ),
            (
                "$suspect1 key $ident cont",["$suspect1 key $ident contains"]
            ), 
            ( # 25
                "has $attr conta",["has $attr contains"]
            ),
            (
                "key $ident cont",["key $ident contains"]
            ), 
            (
                "has name lik",["has name like"]
            ),
            (
                "key address li",["key address like"]
            ), 
            (
                "$p1 has $attr l",["$p1 has $attr like"]
            ),
            ( # 30
                "$suspect1 key $ident lik",["$suspect1 key $ident like"]
            ), 
            (
                "has $attr lik",["has $attr like"]
            ),
            (
                "key $ident cont",["key $ident contains"]
            ), 
            (
                "$attr cont",["$attr contains"]
            ),
            (
                "$attr lik",["$attr like"]
            ), 
            ( # 35
                "$person key name 'A",["$person key name 'A'"]
            ),
            (
                "$house has price 23",['$house has price 23,', '$house has price 23;']
            ), 
            (
                "key name 'Sa",["key name 'Sa'"]
            ),
            (
                "has age 23",['has age 23;', 'has age 23,']
            ), 
            (
                "$attribute 'Jor",["$attribute 'Jor'"]
            ),
            ( # 40
                "$attribute 2020-01-01",['$attribute 2020-01-01,', '$attribute 2020-01-01;']
            ), 
        ])
    def test1(self,string, list_result_expected, dict_rootType_type_dict_tenancy):
        vars_thingType = ["$x", "$rented", "$relation", "$person", "$attr", "$address"] 
        list_result = typeql_utils.complete_predicate_has_attribute(
                        string,
                        vars_thingType, 
                        dict_rootType_type_dict_tenancy
                        )
        if list_result:
            assert set(list_result) == set(list_result_expected)
        else: 
            assert list_result == list_result_expected 
            