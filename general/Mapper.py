from abc import ABCMeta, abstractmethod
from .geomodel import GeoModel
import json
import copy

# SUMMARY: Class abtracts with methods to change the structure of json.
#     You can create your own definitions from it.
class AbstractMapper(object):

    # SUMMARY: Is established as an abstract class
    __metaclass__ = ABCMeta
    
    # SUMMARY: It is an abstract method that allows to change the structure 
    #     of the json format obtained from an API
    @abstractmethod
    def mapout_API(self,data_not_mapped):
        pass
    
    # SUMMARY: It is an abstrac method that allows to change the structure
    #    of the json format obtained from an unstructed db
    @abstractmethod
    def  mapout_DB_Unstructed(self,data_not_mapped):
        pass

# SUMMARY: This is a default mapper that implements the methods 
#     from AbstractMapper
class DefaultMapper(AbstractMapper):

    # SUMMARY: Method that restructures the json object consulted, and 
    #     returns it in the form of a list of the GeoModel type
    # PARAM obj_json: Object json consulted
    # PARAM common_data: Dictionary with the common data keys that will 
    #     be extracted from the json consulted
    # PARAM metadata: Dictionary with the metadata keys will be extracted 
    #     from the json consulted.
    # RETURN: A json of GeoModel with all the restructured information 
    #     of obj_json

    def mapout_API(self, obj_json, common_data, metadata):
        
        copy_metadata = {}
        objs_list = []

        for data_obj in obj_json:

            copy_metadata = metadata.copy()
            
            # Extract common data

            longitude = data_obj[common_data['longitud']]

            latitude = data_obj[common_data['latitud']]

            data = data_obj[common_data['data']]

            # Extract metadata
            # the cycle obtains each key of the dictionary, and verifies if 
            # it has value in the obj_json, if not, it eliminates the key of 
            # the metadata
            for key in metadata.keys():
                if data_obj[key] != '':
                    copy_metadata[key] = data_obj[key]
                else:
                    del copy_metadata[key]

            # A GeoModel object is created
            model = GeoModel(data,copy_metadata,latitude,longitude)

            # __dict__ -> Convert the object to a dictionary
            # and it is added to the GeoModel object list
            objs_list.append(model.__dict__)
            copy_metadata.clear()

        # return a list of geomodel class in json format
        return json.dumps(objs_list, indent=4)

    @staticmethod
    def  mapout_crawler(data_not_mapped):
        node_list = []
        dict_node = {}
        for node  in data_not_mapped:
            metadata = copy.copy(node.get('metadata'))
            dict_node[metadata["url"]] = GeoModel(node.get('data'), metadata)
            node_list.append(dict_node)

        return dict_node