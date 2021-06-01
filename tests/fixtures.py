import pytest 

@pytest.fixture(scope="module")
def dict_rootType_type_dict_tenancy():
    return {
        "entity": {
            "agent": {
                "key": {
                    "UID": "STRING"
                },
                "owns": {
                    "name": "STRING"
                },
                "plays": {
                    "subtenancy": [
                        "sublandlord"
                    ],
                    "tenancy": [
                        "landlord",
                        "tenant"
                    ],
                    "tenancy-dispute": [
                        "disputing-landlord",
                        "disputing-tenant"
                    ],
                    "neighbourship": [
                        "is-neighbour"
                    ]
                },
                "relates": {},
                "abstract": True
            },
            "corporation": {
                "key": {
                    "UID": "STRING"
                },
                "owns": {
                    "name": "STRING"
                },
                "plays": {
                    "neighbourship": [
                        "is-neighbour"
                    ],
                    "tenancy-dispute": [
                        "disputing-tenant",
                        "disputing-landlord"
                    ],
                    "tenancy": [
                        "tenant",
                        "landlord"
                    ],
                    "subtenancy": [
                        "sublandlord"
                    ]
                },
                "relates": {},
                "abstract": False
            },
            "organisation": {
                "key": {
                    "UID": "STRING"
                },
                "owns": {
                    "name": "STRING"
                },
                "plays": {
                    "neighbourship": [
                        "is-neighbour"
                    ],
                    "tenancy-dispute": [
                        "disputing-tenant",
                        "disputing-landlord"
                    ],
                    "tenancy": [
                        "tenant",
                        "landlord"
                    ],
                    "subtenancy": [
                        "sublandlord"
                    ]
                },
                "relates": {},
                "abstract": False
            },
            "person": {
                "key": {
                    "UID": "STRING"
                },
                "owns": {
                    "name": "STRING"
                },
                "plays": {
                    "subtenancy": [
                        "subtenant",
                        "sublandlord"
                    ],
                    "birth": [
                        "birthed-child"
                    ],
                    "neighbourship": [
                        "is-neighbour"
                    ],
                    "tenancy-dispute": [
                        "disputing-tenant",
                        "disputing-landlord"
                    ],
                    "tenancy": [
                        "tenant",
                        "landlord"
                    ]
                },
                "relates": {},
                "abstract": False
            },
            "house": {
                "key": {
                    "UID": "STRING"
                },
                "owns": {
                    "address": "STRING"
                },
                "plays": {
                    "tenancy": [
                        "rented-property"
                    ],
                    "subtenancy": [
                        "rented-property"
                    ]
                },
                "relates": {},
                "abstract": False
            }
        },
            "relation": {
                "birth": {
                    "key": {
                        "UID": "STRING"
                    },
                    "owns": {
                        "starting-date": "DATETIME"
                    },
                    "plays": {},
                    "relates": {
                        "birthed-child": [
                            "person"
                        ]
                    },
                    "abstract": False
                },
                "tenancy": {
                    "key": {
                        "UID": "STRING"
                    },
                    "owns": {
                        "starting-date": "DATETIME"
                    },
                    "plays": {
                        "tenancy-dispute": [
                            "disputed-tenancy"
                        ],
                        "subtenancy": [
                            "main-tenancy"
                        ]
                    },
                    "relates": {
                        "landlord": [
                            "agent"
                        ],
                        "tenant": [
                            "agent"
                        ],
                        "rented-property": [
                            "house"
                        ]
                    },
                    "abstract": False
                },
                "subtenancy": {
                    "key": {
                        "UID": "STRING"
                    },
                    "owns": {
                        "starting-date": "DATETIME"
                    },
                    "plays": {
                        "tenancy-dispute": [
                            "disputed-tenancy"
                        ],
                        "subtenancy": [
                            "main-tenancy"
                        ]
                    },
                    "relates": {
                        "sublandlord": [
                            "agent"
                        ],
                        "main-tenancy": [
                            "tenancy"
                        ],
                        "subtenant": [
                            "person"
                        ],
                        "rented-property": [
                            "house"
                        ]
                    },
                    "abstract": False
                },
                "neighbourship": {
                    "key": {
                        "UID": "STRING"
                    },
                    "owns": {},
                    "plays": {},
                    "relates": {
                        "is-neighbour": [
                            "agent"
                        ]
                    },
                    "abstract": False
                },
                "dispute": {
                    "key": {
                        "UID": "STRING"
                    },
                    "owns": {
                        "starting-date": "DATETIME"
                    },
                    "plays": {},
                    "relates": {
                        "party": [],
                        "disputed-subject": []
                    },
                    "abstract": True
                },
                "tenancy-dispute": {
                    "key": {
                        "UID": "STRING"
                    },
                    "owns": {
                        "starting-date": "DATETIME"
                    },
                    "plays": {},
                    "relates": {
                        "disputed-tenancy": [
                            "tenancy"
                        ],
                        "disputing-landlord": [
                            "agent"
                        ],
                        "disputing-tenant": [
                            "agent"
                        ]
                    },
                    "abstract": False
                }
            },

        "attribute": {
            "UID": {
                "key": {},
                "owns": {},
                "plays": {},
                "relates": {},
                "abstract": False
            },
            "address": {
                "key": {},
                "owns": {},
                "plays": {},
                "relates": {},
                "abstract": False
            },
            "name": {
                "key": {},
                "owns": {},
                "plays": {},
                "relates": {},
                "abstract": False
            },
            "starting-date": {
                "key": {},
                "owns": {},
                "plays": {},
                "relates": {},
                "abstract": False
            }
        }

    }

# @pytest.fixture(scope="module")
# def list_roles_tenancy(dict_rootType_type_dict_tenancy):
#     return [role for role in [role for rel in dict_rootType_type_dict_tenancy["relation"].keys() for role in dict_rootType_type_dict_tenancy["relation"][rel]["relates"].keys()]]