import unittest
from unittest.mock import AsyncMock, MagicMock
from app.services.label_processor import LabelProcessor
from app.services.database_service import DatabaseService
from app.models.harmful_e_number_additive import HarmfulENumberAdditive
import asyncio


VALID_LABEL_WITH_E = "Valid label with E222 and E3333"
VALID_LABEL_WITHOUT_E = "Valid label"

VALID_LABEL_CHAT_RESPONSE = """ ```json
{
"harmful_ingredients": "High fructose corn syrup is linked to various health problems, including weight gain, insulin resistance, and metabolic syndrome. Palm oil, depending on its source and production methods, may raise concerns regarding deforestation and environmental impact.  Artificial flavor (Vanillin) may have potential health effects depending on its source and purity.",
"harmful_in_excess": "Sugar and palm/canola oil are listed among the first ingredients, suggesting a high concentration that might be harmful if consumed excessively.",
"allergens": "Wheat and soy are listed as allergens.",
"is_highly_processed": true,
"food_additives": "High fructose corn syrup, baking soda, calcium phosphate, soy lecithin, vanillin are food additives.  Some might be considered harmless in moderation, while others like high fructose 
corn syrup raise health concerns.",
"contains_gluten": true,
"is_vegan": false,
"is_vegetarian": true
}
``` """

INVALID_LABEL_CHAT_RESPONSE = "I coould not analyze this label"

add1 = HarmfulENumberAdditive(code = "E111", name = "add1", desc = "desc1")
add2 = HarmfulENumberAdditive(code = "E222", name = "add2", desc = "desc2")
add3 = HarmfulENumberAdditive(code = "E3333", name ="add3", desc = "desc3")



class TestLabelProcessor(unittest.TestCase):



    def setUp(self):


        async def mock_database_service_side_effect(code):

        

            if code == "E111":
                return add1
            elif code == "E222":
                return add2
            elif code == "E3333":
                return add3
            else:
                return None
            


        async def mock_gemini_service_side_effect(label_text):

            if label_text == VALID_LABEL_WITH_E or label_text == VALID_LABEL_WITHOUT_E:
                return VALID_LABEL_CHAT_RESPONSE
            else:
                return INVALID_LABEL_CHAT_RESPONSE


        self.mock_gemini_service = AsyncMock()
        self.mock_gemini_service.analyze_label.side_effect = mock_gemini_service_side_effect

        self.mock_database_service: DatabaseService = AsyncMock()
        self.mock_database_service.get_additive_by_code.side_effect = mock_database_service_side_effect

        self.processor = LabelProcessor(self.mock_gemini_service, self.mock_database_service)





    # is_label_valid


    def test__label_validation_should_return_true_when_label_OK(self):

        label_text = "This is valid label"

        result = self.processor.is_label_valid(label_text)
        self.assertTrue(result)


    def test_label_validation_should_return_false_when_label_only_whitchars(self):

        label_text = "   "

        result = self.processor.is_label_valid(label_text)
        self.assertFalse(result)



    def test_label_validation_should_return_false_when_label_empty(self):

        label_text = ""

        result = self.processor.is_label_valid(label_text)
        self.assertFalse(result)


    def test_label_validation_should_return_false_when_label_is_none(self):

        label_text = None

        result = self.processor.is_label_valid(label_text)
        self.assertFalse(result)
        

    def test_label_validation_should_return_false_when_label_is_no_isalnum(self):

        label_text = "&&&&"

        result = self.processor.is_label_valid(label_text)
        self.assertFalse(result)



    #parse_response_to_json


    def test_parse_json_should_return_result_when_response_OK(self):

        response = '{"ala" : "ma kota", "is_OK": true}'
        expected = {"ala": "ma kota", "is_OK": True}

        parsed_response = self.processor.parse_response_to_json(response)

        self.assertDictEqual(parsed_response, expected)


    def test_parse_json_should_return_result_when_response_with_prefix_and_sufix(self):

        response = 'this is prefix {"ala" : "ma kota", "is_OK": true} this is suffix'
        expected = {"ala": "ma kota", "is_OK": True}

        parsed_response = self.processor.parse_response_to_json(response)

        self.assertDictEqual(parsed_response, expected)


    def test_parse_json_should_return_none_when_response_has_no_json(self):

        response = 'no json here'

        parsed_response = self.processor.parse_response_to_json(response)

        self.assertIsNone(parsed_response)


    def test_parse_json_should_return_none_when_response_has_invalid_json(self):

        response = '{"ala" : "ma kota" "is_OK": true}'

        parsed_response = self.processor.parse_response_to_json(response)

        self.assertIsNone(parsed_response)




# find additives


    def test_find_additives_should_return_empty_list_when_no_additives(self):

        label_text = "No e in this testing label"
        loop = asyncio.get_event_loop()
        add_list = loop.run_until_complete(self.processor.find_additives(label_text))
        self.assertEquals(len(add_list), 0)




    def test_find_additives_should_return_empty_list_when_additives_present(self):


        add1 = HarmfulENumberAdditive(code = "E111", name = "add1", desc = "desc1")
        add2 = HarmfulENumberAdditive(code = "E222", name = "add2", desc = "desc2")
    
        label_text = "Contains E111 and E222"
        loop = asyncio.get_event_loop()
        add_list = loop.run_until_complete(self.processor.find_additives(label_text))

        self.assertEquals(len(add_list), 2)
        self.assertIn(add1, add_list)
        self.assertIn(add2, add_list)



    def test_find_additives_should_return_empty_list_when_additives_present_but_not_in_db(self):

        label_text = "Contains E3333 and E444"
        loop = asyncio.get_event_loop()
        add_list = loop.run_until_complete(self.processor.find_additives(label_text))

        self.assertEquals(len(add_list), 1)
        self.assertIn(add3, add_list)


# process_label


    def test_process_label_should_return_none_as_chat_response_when_label_not__chat_valid_no_additives(self):

        invalid_label = "not valid label"


        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.processor.process_label(invalid_label))

        chat_response, additives_list = result["chat_response"], result["harmful_additive_list"]

        self.assertIsNone(chat_response)
        self.assertEqual(len(additives_list), 0)



    def test_process_label_should_return_none_as_chat_response_when_label_not__chat_valid_with_additives(self):

        invalid_label = "not valid label with E3333"


        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.processor.process_label(invalid_label))

        chat_response, additives_list = result["chat_response"], result["harmful_additive_list"]

        self.assertIsNone(chat_response)
        self.assertEqual(len(additives_list), 1)
        self.assertIn(add3, additives_list)



    def test_process_label_should_return_chat_response_when_label__valid_without_additives(self):

        

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.processor.process_label(VALID_LABEL_WITHOUT_E))

        chat_response, additives_list = result["chat_response"], result["harmful_additive_list"]

        self.assertIsNotNone(chat_response)
        self.assertEqual(len(additives_list), 0)





    def test_process_label_should_return_chat_response_when_label__valid_with_additives(self):


        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.processor.process_label(VALID_LABEL_WITH_E))

        chat_response, additives_list = result["chat_response"], result["harmful_additive_list"]

        self.assertIsNotNone(chat_response)
        self.assertEqual(len(additives_list), 2)
        self.assertIn(add2, additives_list)
        self.assertIn(add3, additives_list)
        


    def test_process_label_should_return_none_when_label_is_not_valid(self):

        label_text = "&&&"

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(self.processor.process_label(label_text))
      

        self.assertIsNone(result)
   




        



