import collections

from user_agents import parse
from collections import OrderedDict


def sorted_descending(dictionary):
    if dictionary == {}:
        #print('Cannot sort an empty dict')
        return
    # Referenced from: https://thomas-cokelaer.info/blog/2017/12/how-to-sort-a-dictionary-by-values-in-python/
    sorted_dict = OrderedDict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))
    return sorted_dict


class ProcessData:

    def get_countries(self, doc_uuid, json_data):
        """
            Firstly checks that the json data is not null/empty.
            If not, checks that docID, country and user tags are present.
            Ensures that docID matches the param docID + user hasn't been seen before.
            If true, increments counter OR sets to 1 if first visitor from that country.
        """
        if json_data == {}:
            print('JSON data appears to be empty! Cannot get countries with no data to process')
            return
        countries = {}
        visitor_ids = set()
        for line in json_data.read_json():
            if 'subject_doc_id' in line and 'visitor_country' in line and 'visitor_uuid' in line and 'event_type' in line:
                if line['event_type'] != 'read':  # 30/11/20 Added as per email instructions
                    continue  # Skip over this line
                if line['subject_doc_id'] == doc_uuid:  # i.e. The document matches the one we're currently looking for
                    if line['visitor_uuid'] not in visitor_ids:  # not taking repeated visitors into account
                        visitor_ids.add(line['visitor_uuid'])  # adding current visitor to set
                        if line['visitor_country'] in countries:
                            countries[line['visitor_country']] += 1
                        else:
                            countries[line['visitor_country']] = 1
        return countries

    def get_continents(self, countries):
        """
            Checks that countries dictionary contains values.
            For every key,value pair in countries, checks that key belongs to a valid continent.
            If it does, get value of continent and increment counter by 1.
        """
        # Constants: Sourced from http://www.macs.hw.ac.uk/~hwloidl/Courses/F21SC/Samples/simple_histo.py
        cntry_to_cont = {'AF': 'AS', 'AX': 'EU', 'AL': 'EU', 'DZ': 'AF', 'AS': 'OC', 'AD': 'EU', 'AO': 'AF', 'AI': 'NA',
                         'AQ': 'AN', 'AG': 'NA', 'AR': 'SA', 'AM': 'AS', 'AW': 'NA', 'AU': 'OC', 'AT': 'EU', 'AZ': 'AS',
                         'BS': 'NA', 'BH': 'AS', 'BD': 'AS', 'BB': 'NA', 'BY': 'EU', 'BE': 'EU', 'BZ': 'NA', 'BJ': 'AF',
                         'BM': 'NA', 'BT': 'AS', 'BO': 'SA', 'BQ': 'NA', 'BA': 'EU', 'BW': 'AF', 'BV': 'AN', 'BR': 'SA',
                         'IO': 'AS', 'VG': 'NA', 'BN': 'AS', 'BG': 'EU', 'BF': 'AF', 'BI': 'AF', 'KH': 'AS', 'CM': 'AF',
                         'CA': 'NA', 'CV': 'AF', 'KY': 'NA', 'CF': 'AF', 'TD': 'AF', 'CL': 'SA', 'CN': 'AS', 'CX': 'AS',
                         'CC': 'AS', 'CO': 'SA', 'KM': 'AF', 'CD': 'AF', 'CG': 'AF', 'CK': 'OC', 'CR': 'NA', 'CI': 'AF',
                         'HR': 'EU', 'CU': 'NA', 'CW': 'NA', 'CY': 'AS', 'CZ': 'EU', 'DK': 'EU', 'DJ': 'AF', 'DM': 'NA',
                         'DO': 'NA', 'EC': 'SA', 'EG': 'AF', 'SV': 'NA', 'GQ': 'AF', 'ER': 'AF', 'EE': 'EU', 'ET': 'AF',
                         'FO': 'EU', 'FK': 'SA', 'FJ': 'OC', 'FI': 'EU', 'FR': 'EU', 'GF': 'SA', 'PF': 'OC', 'TF': 'AN',
                         'GA': 'AF', 'GM': 'AF', 'GE': 'AS', 'DE': 'EU', 'GH': 'AF', 'GI': 'EU', 'GR': 'EU', 'GL': 'NA',
                         'GD': 'NA', 'GP': 'NA', 'GU': 'OC', 'GT': 'NA', 'GG': 'EU', 'GN': 'AF', 'GW': 'AF', 'GY': 'SA',
                         'HT': 'NA', 'HM': 'AN', 'VA': 'EU', 'HN': 'NA', 'HK': 'AS', 'HU': 'EU', 'IS': 'EU', 'IN': 'AS',
                         'ID': 'AS', 'IR': 'AS', 'IQ': 'AS', 'IE': 'EU', 'IM': 'EU', 'IL': 'AS', 'IT': 'EU', 'JM': 'NA',
                         'JP': 'AS', 'JE': 'EU', 'JO': 'AS', 'KZ': 'AS', 'KE': 'AF', 'KI': 'OC', 'KP': 'AS', 'KR': 'AS',
                         'KW': 'AS', 'KG': 'AS', 'LA': 'AS', 'LV': 'EU', 'LB': 'AS', 'LS': 'AF', 'LR': 'AF', 'LY': 'AF',
                         'LI': 'EU', 'LT': 'EU', 'LU': 'EU', 'MO': 'AS', 'MK': 'EU', 'MG': 'AF', 'MW': 'AF', 'MY': 'AS',
                         'MV': 'AS', 'ML': 'AF', 'MT': 'EU', 'MH': 'OC', 'MQ': 'NA', 'MR': 'AF', 'MU': 'AF', 'YT': 'AF',
                         'MX': 'NA', 'FM': 'OC', 'MD': 'EU', 'MC': 'EU', 'MN': 'AS', 'ME': 'EU', 'MS': 'NA', 'MA': 'AF',
                         'MZ': 'AF', 'MM': 'AS', 'NA': 'AF', 'NR': 'OC', 'NP': 'AS', 'NL': 'EU', 'NC': 'OC', 'NZ': 'OC',
                         'NI': 'NA', 'NE': 'AF', 'NG': 'AF', 'NU': 'OC', 'NF': 'OC', 'MP': 'OC', 'NO': 'EU', 'OM': 'AS',
                         'PK': 'AS', 'PW': 'OC', 'PS': 'AS', 'PA': 'NA', 'PG': 'OC', 'PY': 'SA', 'PE': 'SA', 'PH': 'AS',
                         'PN': 'OC', 'PL': 'EU', 'PT': 'EU', 'PR': 'NA', 'QA': 'AS', 'RE': 'AF', 'RO': 'EU', 'RU': 'EU',
                         'RW': 'AF', 'BL': 'NA', 'SH': 'AF', 'KN': 'NA', 'LC': 'NA', 'MF': 'NA', 'PM': 'NA', 'VC': 'NA',
                         'WS': 'OC', 'SM': 'EU', 'ST': 'AF', 'SA': 'AS', 'SN': 'AF', 'RS': 'EU', 'SC': 'AF', 'SL': 'AF',
                         'SG': 'AS', 'SX': 'NA', 'SK': 'EU', 'SI': 'EU', 'SB': 'OC', 'SO': 'AF', 'ZA': 'AF', 'GS': 'AN',
                         'SS': 'AF', 'ES': 'EU', 'LK': 'AS', 'SD': 'AF', 'SR': 'SA', 'SJ': 'EU', 'SZ': 'AF', 'SE': 'EU',
                         'CH': 'EU', 'SY': 'AS', 'TW': 'AS', 'TJ': 'AS', 'TZ': 'AF', 'TH': 'AS', 'TL': 'AS', 'TG': 'AF',
                         'TK': 'OC', 'TO': 'OC', 'TT': 'NA', 'TN': 'AF', 'TR': 'AS', 'TM': 'AS', 'TC': 'NA', 'TV': 'OC',
                         'UG': 'AF', 'UA': 'EU', 'AE': 'AS', 'GB': 'EU', 'US': 'NA', 'UM': 'OC', 'VI': 'NA', 'UY': 'SA',
                         'UZ': 'AS', 'VU': 'OC', 'VE': 'SA', 'VN': 'AS', 'WF': 'OC', 'EH': 'AF', 'YE': 'AS', 'ZM': 'AF',
                         'ZW': 'AF'}
        continentsList = {'AF': 'Africa', 'AS': 'Asia', 'EU': 'Europe', 'NA': 'North America', 'SA': 'South America',
                          'OC': 'Oceania', 'AN': 'Antarctica'}
        if countries == {}:
            print('Please identify countries first before attempting to identify continents.')
            return
        else:
            continents_counter = {}
            for instance, count in countries.items():
                if instance in cntry_to_cont:  # i.e. this is a valid continent code
                    if cntry_to_cont[instance] in continents_counter:
                        continents_counter[continentsList[[instance]]] += count
                    else:
                        continents_counter[continentsList[cntry_to_cont[instance]]] = count
                else:
                    print('instance did not match with a valid continent code')
        return continents_counter

    def get_browsers(self, json_data, formatted):
        """ Q3.a Returns a list of unique browsers used to access documents within the data set """
        if json_data == {}:
            print('JSON data appears to be empty! Cannot get browsers with no data to process')
            return
        visitor_ids = set()
        browsers = {}
        for line in json_data.read_json():
            if 'visitor_useragent' in line and 'visitor_uuid' in line and 'event_type' in line:
                if line['event_type'] != 'read':  # 30/11/20 Added as per email instructions
                    continue  # Skip over this line
                if line['visitor_uuid'] not in visitor_ids:  # Not adding repeat visitors to results
                    visitor_ids.add(line['visitor_uuid'])  # adding current visitor to set
                    if line['visitor_useragent'] in browsers:
                        browsers[line['visitor_useragent']] += 1
                    else:
                        browsers[line['visitor_useragent']] = 1
        if formatted:  # A.K.A. Q3.b) Returns a formatted list of browser families from data set in Q3.a"
            if browsers == {}:
                return browsers
            browsers_formatted = {}
            for browser in browsers:  # Iterate through all keys in the unformatted dictionary
                user_agent = parse(browser)
                if user_agent.browser.family not in browsers_formatted:
                    browsers_formatted[user_agent.browser.family] = browsers[browser]
                else:
                    browsers_formatted[user_agent.browser.family] += browsers[
                        browser]  # incase same browser family, just different OS etc.
            browsers = browsers_formatted
        return browsers

    def get_avid_readers(self, json_data):
        """ Q4. Calculates read time for each userID and returns top 10"""
        if json_data == {}:
            print('JSON data appears to be empty! Cannot calculate most active readers in empty data set')
            return
        readers = {}
        for line in json_data.read_json():
            if 'visitor_uuid' in line and 'event_readtime' in line and 'event_type' in line:
                # event_readtime not in every entry
                # print(line['event_type'])
                if line['event_type'] != "pagereadtime":  # Special case!!
                    continue  # Skip over this line
                if line['visitor_uuid'] not in readers:
                    readers[line['visitor_uuid']] = line['event_readtime']
                else:
                    readers[line['visitor_uuid']] += line['event_readtime']
        return sorted_descending(readers)

    def get_doc_reader_uuids(self, json_data, doc_uuid):  # Q5a. Get the UUIDs of all readers of a document
        if json_data == {}:
            print('JSON data appears to be empty! Cannot identify users in empty data set')
            return
        visitor_uuids = set()
        for line in json_data.read_json():
            if 'visitor_uuid' in line and 'subject_doc_id' in line and 'event_type' in line:
                if line['event_type'] != 'read':  # 30/11/20 Added as per email instructions
                    continue  # Skip over this line
                if line['subject_doc_id'] == doc_uuid:  # i.e. We're looking at the correct document
                    if line['visitor_uuid'] not in visitor_uuids:  # set so guaranteed no repeated elements
                        visitor_uuids.add(line['visitor_uuid'])
        return visitor_uuids

    def get_reader_doc_uuids(self, json_data, visitor_uuid):  # Q5b. Get the DocUUIDs for a given reader
        if json_data == {}:
            print('JSON data appears to be empty! Cannot identify documents in an empty data set')
            return
        visitor_doc_uuids = set()
        for line in json_data.read_json():
            if 'visitor_uuid' in line and 'subject_doc_id' in line and 'event_type' in line:
                if line['event_type'] != 'read':  # 30/11/20 Added as per email instructions
                    continue  # Skip over this line
                if line['visitor_uuid'] == visitor_uuid:
                    visitor_doc_uuids.add(line['subject_doc_id'])
        return visitor_doc_uuids

    def also_likes(self, json_data, doc_uuid, visitor_uuid=None, sorting_function=sorted_descending):
        """
            Q5.c Implementation of also_likes functionality.
            Gets other readers of doc. For each reader gets the other docs they've read and adds them to new dict.
            Returns the dict after it's been processed by the sorting function specified in the parameter.
        """
        if json_data == {}:
            print('JSON data is empty, cannot find other documents in an empty data set')
            return
        other_docs = {}
        visitors = self.get_doc_reader_uuids(json_data, doc_uuid)  # Get readers of doc
        if visitor_uuid is not None:  # We don't want results from this user
            visitors.discard(visitor_uuid)  # Graceful way to attempt to remove from set.
        for visitor in visitors:  # For every unique visitor to the doc
            # print('Visitor =  \'%s\'' % visitor)
            visitor_docs = self.get_reader_doc_uuids(json_data, visitor)  # Get all documents they've visited
            # print('Visitor_Docs len =  \'%d\'' % len(visitor_docs))
            visitor_docs.discard(doc_uuid)
            if len(visitor_docs) == 0:
                # print('No other documents were accessed by this documents visitors')
                continue
            for doc in visitor_docs:
                if doc not in other_docs:  # If document not visited before, add it to dict, otherwise increment
                    other_docs[doc] = 1
                else:
                    other_docs[doc] += 1
        return sorting_function(other_docs)

    def get_visitors_documents(self, json_data):
        """
            Used for making the graph in Q6).
            Generates Dictionaries for every document in the JSON data, and each unique visitor to that document,
            As well as for visitors and each document that they have visited.
        """
        if json_data == {}:
            print('JSON data is empty, cannot find other documents or visitors in empty data set')
            return
        visitor_uuids = {}
        doc_uuids = {}

        for line in json_data.read_json():
            if 'visitor_uuid' in line and 'subject_doc_id' in line and 'event_type' in line:
                if line['event_type'] != 'read':  # 30/11/20 Added as per email instructions
                    continue  # Skip over this line
                if line['subject_doc_id'] not in doc_uuids:
                    doc_uuids[line['subject_doc_id']] = [line['visitor_uuid']]  # Seen new document, add it to dict.
                else:
                    if line['visitor_uuid'] not in doc_uuids[line['subject_doc_id']]:  # No repeats
                        doc_uuids[line['subject_doc_id']].append(line['visitor_uuid'])  # Append not replace!
                # As we did above; if not already existing, create new key/value in dict, otherwise append value
                if line['visitor_uuid'] not in visitor_uuids:
                    visitor_uuids[line['visitor_uuid']] = [line['subject_doc_id']]
                else:
                    if line['subject_doc_id'] not in visitor_uuids[line['visitor_uuid']]:
                        visitor_uuids[line['visitor_uuid']].append(line['subject_doc_id'])
        return visitor_uuids, doc_uuids

    def also_likes_graph(self, json_data, doc_uuid, visitor_uuid=None):
        """
            Generates Data for DOT Graph by invoking get_visitors_documents.
            Then goes through data returned by get_visitors_documents, checking that current visitor has actually
            accessed specified doc ID and that they've also accessed more than this doc. If so, add to graph_data
            dictionary.
            At the end, graph_data is returned to be passed to the dot_graph method in questions.py
        """
        if json_data == {} or doc_uuid is None:
            print('Please ensure you provide valid JSON data, document UUID and visitor UUID parameters')
            return  # Error handling, can't complete question without all those parameters containing valid data.

        graph_data = collections.defaultdict(set)  # No duplicate entries in value field!
        visitors, other_docs = self.get_visitors_documents(json_data)

        if doc_uuid not in other_docs:
            return "The provided document ID does not appear in the data set."

        if visitors.get(visitor_uuid) is not None:  # Had concurrency bug so needed to scope this check for entire
            # method
            graph_data[visitor_uuid[-4:]] = [doc_uuid]  # Only want last 4 digits of uuid
            visitors.pop(visitor_uuid, None)
            # Attempt to pop the visitor's uuid from the visitors stack, don't need their results.

        #print(other_docs[doc_uuid])
        if other_docs is not None and doc_uuid in other_docs:  # Input doc exists!
            input_doc_users = other_docs[doc_uuid]
            for visitor in visitors:
                if visitor in input_doc_users and len(visitors[visitor]) > 1:
                    # Many users have only visited the input doc!
                    #print(visitors[visitor])
                    graph_data[visitor[-4:]] = visitors[visitor]
        else:
            return "The document UUID could not be found in the data set; are you sure you entered it correctly?"
        #else:
            #return "The provided User ID does not access the supplied Document ID."
        return graph_data
