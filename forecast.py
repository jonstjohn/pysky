import dwml
def process_xml(xml, include_hourly = False):

    return dwml.parse_xml(xml)
    #return {'daily': []}
