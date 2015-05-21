from collections import OrderedDict
from flask.ext.restful import fields
from flask.ext.restful_swagger import swagger
from Countermeasure import Countermeasure

from EnvironmentParameters import EnvironmentParameters
from RoleEnvironmentProperties import RoleEnvironmentProperties


__author__ = 'Robin Quetin'
obj_id_field = '__python_obj__'
def gen_class_metadata(class_ref):
    return {
        "enum": [class_ref.__module__+'.'+class_ref.__name__]
    }


@swagger.model
class SecurityAttribute(object):
    def __init__(self, name=None, value=None, rationale=None):
        """
        :type name: str
        :type value: str
        :type rationale: str
        """
        self.name = name
        self.value = value
        self.rationale = rationale

    # region Swagger Doc
    resource_fields = {
        "__python_obj__": fields.String,
        "name": fields.String,
        "value": fields.String,
        "rationale": fields.String
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    swagger_metadata = {
        "__python_obj__": {
            "enum": ["tools.PseudoClasses.SecurityAttribute"]
        },
        "name": {
            "enum": [
                'Confidentiality',
                'Integrity',
                'Availability',
                'Accountability',
                'Anonymity',
                'Pseudonymity',
                'Unlinkability',
                'Unobservability'
            ]
        },
        "value": {
            "enum": [
                "None",
                "Low",
                "Medium",
                "High"
            ]
        }
    }
    # endregion

    def get_attr_value(self, enum_obj):
        """
        Gets the database value for the security attribute
        :type enum_obj: list|tuple
        """
        value = 0

        if self.value is not None:
            found = False
            idx = 0

            while not found and idx < len(enum_obj):
                if enum_obj[idx] == self.value:
                    value = idx
                    found = True
                else:
                    idx += 1

        return value


@swagger.model
class EnvironmentTensionModel(object):
    # region Swagger Doc
    resource_fields = {
        obj_id_field: fields.String,
        "base_attr_id": fields.Integer,
        "attr_id": fields.Integer,
        "value": fields.Integer,
        "rationale": fields.String
    }
    required = resource_fields.keys()
    required.remove(obj_id_field)
    swagger_metadata = {
        obj_id_field: {
            "enum": ["tools.PseudoClasses."+__name__]
        },
        "base_attr_id": {
            "enum": range(0,4)
        },
        "attr_id": {
            "enum": range(4,8)
        },
        "value": {
            "enum": [-1,0,1]
        }
    }
    attr_dictionary = {
        'Confidentiality': 0,
        'Integrity': 1,
        'Availability': 2,
        'Accountability': 3,
        'Anonymity': 4,
        'Pseudonymity': 5,
        'Unlinkability': 6,
        'Unobservability': 7
    }
    attr_dictionary = OrderedDict(sorted(attr_dictionary.items(), key=lambda t: t[1]))
    # endregion

    base_attr_values = range(-1,4)
    attr_values = range(4,8)
    attr_values.append(-1)

    def __init__(self, base_attr_id=-1, attr_id=-1, value=0, rationale='None', key=None):
        """
        :type base_attr_id: int
        :type attr_id: int
        :type value: int|tuple
        :type rationale: str
        :type key: tuple
        """
        if key is not None:
            base_attr_id = key[0]
            attr_id = key[1]
            rationale = value[1]
            value = value[0]

        if base_attr_id not in self.base_attr_values or attr_id not in self.attr_values:
            raise ValueError('Base attribute or subattribute value is incorrect.')

        self.base_attr_id = base_attr_id
        self.attr_id = attr_id
        self.value = value
        self.rationale = rationale