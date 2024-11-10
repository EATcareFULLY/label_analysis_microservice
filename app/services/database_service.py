from ..models.harmful_e_number_additive import HarmfulENumberAdditive



mock_db_list = [

HarmfulENumberAdditive(code = "E210", name = "Kwas benzoesowy", desc = "Może wywoływać reakcje alergiczne, szczególnie u osób z astmą, i podejrzewany jest o działanie rakotwórcze przy długotrwałym spożyciu."),
HarmfulENumberAdditive(code ="E226",name ="Siarczyn wapnia",desc ="Może powodować problemy żołądkowe i alergie, zwłaszcza u astmatyków."),
HarmfulENumberAdditive(code ="E385",name ="Sól wapniowo-disodowa EDTA (EDTA)",desc ="Stabilizator i przeciwutleniacz stosowany do zachowania koloru i smaku, może powodować reakcje alergiczne, a w nadmiernych ilościach jest toksyczny dla nerek i wątroby oraz zaburza wchłanianie minerałów."),

]


def get_additive_by_code(code: str):

    temp = [additive for additive in mock_db_list if additive.code == code]

    return None if len(temp) == 0 else temp[0]

