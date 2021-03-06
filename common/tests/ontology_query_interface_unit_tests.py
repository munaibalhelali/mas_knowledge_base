import unittest
import os
from mas_knowledge_utils.ontology_query_interface import OntologyQueryInterface

class ontology_query_interface_test(unittest.TestCase):
    '''Implements unit tests for the OntologyQueryInterface APIs
    using the sample.owl ontology

    @author Sushant Chavan
    @contact sushant.chavan@smail.inf.h-brs.de

    '''

    def setUp(self):
        # Get directory paths
        script_dir = os.path.abspath(os.path.dirname(__file__))
        ontology_dir = os.path.join(os.path.dirname(script_dir), "ontology")

        # Get the filepath and namespace for the ontology
        self.ontology_file_path = "file://" + os.path.join(ontology_dir, "sample.owl")
        self.ontology_ns = "apartment"

        # Create an instance of the ontology interface
        self.ont_if = OntologyQueryInterface(ontology_file=self.ontology_file_path,
                                             class_prefix=self.ontology_ns)

    def test_get_classes(self):
        validation_data = ['Drinkware', 'Furniture', 'Location', 'Mug', 
                           'Object', 'Room', 'Table', 'WorkTable']
        acquired_data = sorted(self.ont_if.get_classes())
        self.assertEqual(acquired_data, validation_data)

    def test_get_object_properties(self):
        validation_data = ['defaultStoringLocation', 'heightOf', 'locatedAt']
        acquired_data = sorted(self.ont_if.get_object_properties())
        self.assertEqual(acquired_data, validation_data)

    def test_get_instances(self):
        validation_data = ['CoffeeMug', 'Desk', 'HomeOffice']
        acquired_data = sorted(self.ont_if.get_instances())
        self.assertEqual(acquired_data, validation_data)

    def test_is_instance_of(self):
        self.assertTrue(self.ont_if.is_instance_of("CoffeeMug", "Mug"))
        self.assertFalse(self.ont_if.is_instance_of("Desk", "Mug"))

    def test_get_class_hierarchy(self):
        validation_data = {'Drinkware': ['Mug'], 'Mug': [], 'WorkTable': [],
                           'Table': ['WorkTable'], 'Location': ['Room'],
                           'Room': [], 'Furniture': ['Table', 'WorkTable'],
                           'Object': ['Drinkware', 'Furniture', 'Mug', 'Table', 'WorkTable']
                          }
        acquired_data = self.ont_if.get_class_hierarchy()
        self.assertEqual(sorted(list(acquired_data.keys())),
                         sorted(list(validation_data.keys())))

        for class_name in acquired_data.keys():
            self.assertEqual(sorted(acquired_data[class_name]), 
                             validation_data[class_name])

    def test_get_instances_of(self):
        validation_data = ['HomeOffice']
        acquired_data = sorted(self.ont_if.get_instances_of("Room"))
        self.assertEqual(acquired_data, validation_data)

    def test_get_subclasses_of(self):
        validation_data = ['Furniture', 'Table', 'WorkTable']
        acquired_data = self.ont_if.get_subclasses_of("Furniture")
        self.assertEqual(acquired_data, validation_data)

        validation_data = ['Table']
        acquired_data = self.ont_if.get_subclasses_of("Furniture", only_children=True)
        self.assertEqual(acquired_data, validation_data)

        validation_data = ['Drinkware', 'Furniture']
        acquired_data = sorted(self.ont_if.get_subclasses_of("Object", only_children=True))
        self.assertEqual(acquired_data, validation_data)

    def test_get_parent_classes_of(self):
        validation_data = ['Table', 'Furniture', 'Object']
        acquired_data = self.ont_if.get_parent_classes_of("Table")
        self.assertEqual(acquired_data, validation_data)

        validation_data = ['Furniture']
        acquired_data = self.ont_if.get_parent_classes_of("Table", only_parents=True)
        self.assertEqual(acquired_data, validation_data)

        validation_data = []
        acquired_data = self.ont_if.get_parent_classes_of("Object", only_parents=True)
        self.assertEqual(acquired_data, validation_data)

    def test_get_objects_of(self):
        validation_data = ['HomeOffice']
        acquired_data = sorted(self.ont_if.get_objects_of("locatedAt", "Desk"))
        self.assertEqual(acquired_data, validation_data)

    def test_get_subjects_of(self):
        validation_data = ['Desk']
        acquired_data = sorted(self.ont_if.get_subjects_of("locatedAt", "HomeOffice"))
        self.assertEqual(acquired_data, validation_data)

    def test_get_all_subjects_and_objects(self):
        validation_data = [('Desk', 'HomeOffice')]
        acquired_data = sorted(self.ont_if.get_all_subjects_and_objects("locatedAt"))
        self.assertEqual(acquired_data, validation_data)

    def test_get_property_domain_range(self):
        validation_data = ('Object', 'Room')
        acquired_data = self.ont_if.get_property_domain_range("locatedAt")
        self.assertEqual(acquired_data, validation_data)

    def test_is_class(self):
        self.assertTrue(self.ont_if.is_class("Table"))
        self.assertFalse(self.ont_if.is_class("Desk"))
        self.assertFalse(self.ont_if.is_class("locatedAt"))

    def test_is_property(self):
        self.assertTrue(self.ont_if.is_property("locatedAt"))
        self.assertFalse(self.ont_if.is_property("Table"))
        self.assertFalse(self.ont_if.is_property("Desk"))

    def test_is_instance(self):
        self.assertTrue(self.ont_if.is_instance("Desk"))
        self.assertFalse(self.ont_if.is_instance("Table"))
        self.assertFalse(self.ont_if.is_instance("locatedAt"))

    def test_get_property_types(self):
        self.assertEqual(sorted(self.ont_if.get_property_types("locatedAt")),
                         ['FunctionalProperty', 'ObjectProperty'])
        self.assertEqual(sorted(self.ont_if.get_property_types("heightOf")),
                         ['ObjectProperty'])

    def test_get_associated_properties(self):
        self.assertEqual(sorted(self.ont_if.get_associated_properties("Object")),
                         ["defaultStoringLocation", "heightOf", "locatedAt"])
        self.assertEqual(sorted(self.ont_if.get_associated_properties("Furniture")),
                         ["defaultStoringLocation"])
        self.assertEqual(sorted(self.ont_if.get_associated_properties("Room")),
                         ["locatedAt"])

    def test_insert_class_definition(self):
        top_level_class = "TopLevelClass"
        sub_class_1 = "SubClass1"
        sub_class_2 = "SubClass2"
        hybrid_class = "HybridClass"

        # Ensure that the classes does not exist in the ontology
        self.assertFalse(self.ont_if.is_class(top_level_class))
        self.assertFalse(self.ont_if.is_class(sub_class_1))
        self.assertFalse(self.ont_if.is_class(sub_class_2))
        self.assertFalse(self.ont_if.is_class(hybrid_class))

        # Add the classes to the ontology
        self.ont_if.insert_class_definition(top_level_class)
        self.ont_if.insert_class_definition(sub_class_1, [top_level_class])
        self.ont_if.insert_class_definition(sub_class_2, [top_level_class])
        self.ont_if.insert_class_definition(hybrid_class, [sub_class_1, sub_class_2])

        # Verify if the class names have been added to the ontology
        self.assertTrue(self.ont_if.is_class(top_level_class))
        self.assertTrue(self.ont_if.is_class(sub_class_1))
        self.assertTrue(self.ont_if.is_class(sub_class_2))
        self.assertTrue(self.ont_if.is_class(hybrid_class))

        # Verify if the hierarchy is properly established
        self.assertEqual(len(self.ont_if.get_parent_classes_of(top_level_class)), 1)
        self.assertTrue(sub_class_1 in self.ont_if.get_subclasses_of(top_level_class))
        self.assertTrue(sub_class_2 in self.ont_if.get_subclasses_of(top_level_class))
        self.assertTrue(hybrid_class in self.ont_if.get_subclasses_of(sub_class_1))
        self.assertTrue(hybrid_class in self.ont_if.get_subclasses_of(sub_class_2))

    def test_insert_property_definition(self):
        prop_1_name = "TestFuncProp"
        prop_1_domain_ns = None
        prop_1_domain = "Object"
        prop_1_range_ns = None
        prop_1_range = "Location"
        prop_1_type = 'FunctionalProperty'

        prop_2_name = "TestFloatProp"
        prop_2_domain_ns = None
        prop_2_domain = "Object"
        prop_2_range_ns ='xsd'
        prop_2_range = "float"
        prop_2_type = None

        # Ensure that the properties does not exist in the ontology
        self.assertFalse(self.ont_if.is_property(prop_1_name))
        self.assertFalse(self.ont_if.is_property(prop_2_name))

        # Add the properties to the ontology
        self.ont_if.insert_property_definition(prop_1_name, prop_1_domain,
                                               prop_1_range, prop_1_type,
                                               prop_1_domain_ns, prop_1_range_ns)
        self.ont_if.insert_property_definition(prop_2_name, prop_2_domain,
                                               prop_2_range, prop_2_type,
                                               prop_2_domain_ns, prop_2_range_ns)

        # Validate that the properties have been added to the ontology
        self.assertTrue(self.ont_if.is_property(prop_1_name))
        self.assertTrue(self.ont_if.is_property(prop_2_name))

        # Validate the domain-range of the properties
        self.assertEqual(("Object", "Location"), 
                         self.ont_if.get_property_domain_range(prop_1_name))
        self.assertEqual(("Object", "float"),
                         self.ont_if.get_property_domain_range(prop_2_name))

        # Validate the property types
        self.assertEqual(['FunctionalProperty', 'ObjectProperty'],
                         sorted(self.ont_if.get_property_types(prop_1_name)))
        self.assertEqual(['ObjectProperty'],
                         sorted(self.ont_if.get_property_types(prop_2_name)))

    def test_insert_class_assertion(self):
        # Ensure that the instances don't already exist
        self.assertFalse(self.ont_if.is_instance("Kitchen"))
        self.assertFalse(self.ont_if.is_instance("DiningTable"))
        self.assertFalse(self.ont_if.is_instance("Cup"))

        # Assert new instances
        self.ont_if.insert_class_assertion("Room", "Kitchen")
        self.ont_if.insert_class_assertion("Table", "DiningTable")
        self.ont_if.insert_class_assertion("Drinkware", "Cup")

        # Check if the new instances are added to the ontology
        self.assertTrue(self.ont_if.is_instance("Kitchen"))
        self.assertTrue(self.ont_if.is_instance("DiningTable"))
        self.assertTrue(self.ont_if.is_instance("Cup"))

        # Check if the new instances are setup from the right classes
        self.assertTrue(self.ont_if.is_instance_of("Kitchen", "Room"))
        self.assertTrue(self.ont_if.is_instance_of("DiningTable", "Table"))
        self.assertTrue(self.ont_if.is_instance_of("Cup", "Drinkware"))

    def test_insert_property_assertion(self):
        # Insert class assertions
        self.ont_if.insert_class_assertion("Room", "Kitchen")
        self.ont_if.insert_class_assertion("Table", "DiningTable")
        self.ont_if.insert_class_assertion("Drinkware", "Cup")

        # Ensure that the property assertions do not exist in the ontology
        self.assertEqual(self.ont_if.get_objects_of("defaultStoringLocation", "Cup"), [])
        self.assertEqual(self.ont_if.get_objects_of("locatedAt", "DiningTable"), [])
        self.assertEqual(self.ont_if.get_objects_of("heightOf", "DiningTable"), [])

        # Setup property assertions
        self.ont_if.insert_property_assertion("defaultStoringLocation", ("Cup", "DiningTable"))
        self.ont_if.insert_property_assertion("locatedAt", ("DiningTable", "Kitchen"))
        self.ont_if.insert_property_assertion("heightOf", ("DiningTable", 1.0))

        # Validate the newly asserted properties
        self.assertEqual(self.ont_if.get_objects_of("defaultStoringLocation", "Cup"), ["DiningTable"])
        self.assertEqual(self.ont_if.get_objects_of("locatedAt", "DiningTable"), ["Kitchen"])
        self.assertEqual(self.ont_if.get_objects_of("heightOf", "DiningTable"), ['1.0'])

    def test_remove_class_definition(self):
        class_1 = "Furniture"
        class_2 = "Mug"

        # Ensure that the classes exist
        self.assertTrue(self.ont_if.is_class(class_1))
        self.assertTrue(self.ont_if.is_class(class_2))
        # Ensure that the right instances are loaded for the classes
        self.assertEqual(self.ont_if.get_instances_of(class_1), [])
        self.assertEqual(self.ont_if.get_instances_of(class_2), ["CoffeeMug"])
        # Ensure that the right properties are associated with the classes
        self.assertEqual(self.ont_if.get_associated_properties(class_1), ["defaultStoringLocation"])
        self.assertEqual(self.ont_if.get_associated_properties(class_2), [])
        # Ensure that the loaded instances and properties exist in the ontology
        self.assertTrue(self.ont_if.is_instance("CoffeeMug"))
        self.assertTrue(self.ont_if.is_property("defaultStoringLocation"))

        # Get a superset of all the sub classes of the classes to be removed
        sub_classes = self.ont_if.get_subclasses_of(class_1)
        sub_classes.extend(self.ont_if.get_subclasses_of(class_2))
        sub_classes.remove(class_1)
        sub_classes.remove(class_2)

        # Remove the classes
        self.ont_if.remove_class_definition(class_1)
        self.ont_if.remove_class_definition(class_2)

        # Validate that the classes has been removed
        self.assertFalse(self.ont_if.is_class(class_1))
        self.assertFalse(self.ont_if.is_class(class_2))
        # Validate that the related instances and properties have been removed from the ontology
        self.assertFalse(self.ont_if.is_instance("CoffeeMug"))
        self.assertFalse(self.ont_if.is_property("defaultStoringLocation"))
        # Validate that no sub-classes have been removed
        for name in sub_classes:
            self.assertTrue(self.ont_if.is_class(name))

    def test_remove_property_definition(self):
        prop_list = ["defaultStoringLocation", "heightOf", "locatedAt"]
        subj_list = ["Desk"]

        # Ensure that the properties exist in the ontology
        for p in prop_list:
            self.assertTrue(self.ont_if.is_property(p))
        self.assertEqual(sorted(self.ont_if.get_associated_properties("Object")), prop_list)

        # Remove some properties from the ontology
        self.ont_if.remove_property_definition(prop_list[1])
        self.ont_if.remove_property_definition(prop_list[2])

        # Validate that only the specified properties have been removed from the ontology
        self.assertTrue(self.ont_if.is_property(prop_list[0]))
        self.assertFalse(self.ont_if.is_property(prop_list[1]))
        self.assertFalse(self.ont_if.is_property(prop_list[2]))

        # Validate that the domain and range relations of the property have been removed
        self.assertEqual(sorted(self.ont_if.get_associated_properties("Object")), ["defaultStoringLocation"])

    def test_remove_class_assertion(self):
        # Ensure that the instances already exist
        self.assertTrue(self.ont_if.is_instance("HomeOffice"))
        self.assertTrue(self.ont_if.is_instance("Desk"))
        self.assertTrue(self.ont_if.is_instance("CoffeeMug"))

        # Remove existing class assertions
        self.ont_if.remove_class_assertion("Room", "HomeOffice")
        self.ont_if.remove_class_assertion("WorkTable", "Desk")
        self.ont_if.remove_class_assertion("Mug", "CoffeeMug")

        # Check if the instances have been removed from the ontology
        self.assertFalse(self.ont_if.is_instance("HomeOffice"))
        self.assertFalse(self.ont_if.is_instance("Desk"))
        self.assertFalse(self.ont_if.is_instance("CoffeeMug"))

    def test_remove_property_assertion(self):
        # Ensure that the property assertions already exist in the ontology
        self.assertEqual(self.ont_if.get_objects_of("defaultStoringLocation", "CoffeeMug"), ["Desk"])
        self.assertEqual(self.ont_if.get_objects_of("locatedAt", "Desk"), ["HomeOffice"])
        self.assertEqual(self.ont_if.get_objects_of("heightOf", "Desk"), ['0.7'])

        # Remove property assertions
        self.ont_if.remove_property_assertion("defaultStoringLocation", ("CoffeeMug", "Desk"))
        self.ont_if.remove_property_assertion("locatedAt", ("Desk", "HomeOffice"))
        self.ont_if.remove_property_assertion("heightOf", ("Desk", '0.7'))

        # Ensure that the property assertions do not exist in the ontology
        self.assertEqual(self.ont_if.get_objects_of("defaultStoringLocation", "CoffeeMug"), [])
        self.assertEqual(self.ont_if.get_objects_of("locatedAt", "Desk"), [])
        self.assertEqual(self.ont_if.get_objects_of("heightOf", "Desk"), [])

class ontology_query_interface_test_no_class_prefix(ontology_query_interface_test):
    '''Implements unit tests for the OntologyQueryInterface APIs
    using an ontology that has no namespace (or class_prefix)

    @author Sushant Chavan
    @contact sushant.chavan@smail.inf.h-brs.de

    '''

    def setUp(self):
        # Get directory paths
        script_dir = os.path.abspath(os.path.dirname(__file__))
        ontology_dir = os.path.join(os.path.dirname(script_dir), "ontology")

        # Get the filepath for the ontology
        self.ontology_file_path = "file://" + os.path.join(ontology_dir, "sample_no_namespace.owl")
        # This ontology does not have a namespace, hence None
        self.ontology_ns = None

        # Create an instance of the ontology interface
        self.ont_if = OntologyQueryInterface(ontology_file=self.ontology_file_path,
                                             class_prefix=self.ontology_ns)

if __name__ == '__main__':
    unittest.main()
