from graphviz import Digraph
import processData as pd
import importData as id
import numpy as np
import matplotlib.pyplot as plt


class QuestionTasks:

    def visualizeCountries(self):  # Q2.a
        """
            Functionality is that asked in Q2.a.
            Provides the processData class object with the input json data and the Document ID being searched for.
            The results are stored in 'countries' dictionary which is passed to the graph class to draw
            a barchart.
        """
        countries = self.data_processor.get_countries(self.doc_uuid, self.data_handler)
        if countries == {}:  # Nothing was found for supplied Document ID.
            return "No countries were found for supplied document uuid."
        self.graphs.barchart(countries, 'Country Initials', 'Number of Visitors',
                                    'Visits by Country')

    def visualizeContinents(self):  # Q2.b
        """
            Functionality is asked for in Q2.b.
            Provides the processData class object with the input json data and the Document ID being searched for.
            The results are stored in a Dictionary called 'Countries' which is passed to
            the get_continents method. Results of this function are then passed to graph class to draw a barchart.
        """
        countries = self.data_processor.get_countries(self.doc_uuid, self.data_handler)
        if countries == {}:
            return "No countries were found for supplied document uuid: cannot make Continents graph."
        continents = self.data_processor.get_continents(countries)
        self.graphs.barchart(continents, 'Continent Details', 'Number of Visitors',
                                    'Visits by Continent')

    def visualizeUnformattedBrowsers(self):  # Q3.a
        """
            Functionality asked for in Q3.a. Provides the processData class object with the input json data which
            is parsed in the get_browsers module. The results of this module are stored in a browsers Dictionary,
            which is passed to the graph class to draw a barchart of the results.
        """
        browsers = self.data_processor.get_browsers(self.data_handler, False)
        if browsers == {}:
            return "No browsers were found in the input file: does your JSON contain 'visitor_useragent'?"
        self.graphs.barchart(browsers, 'Browser Name', 'Number of Visitors',
                                    'Visits by Browser')

    def visualizeFormattedBrowsers(self):  # Q3.b
        """
            Functionality asked for in Q3.b. Provides the processData class object with the input json data which
            is parsed in the get_browsers module. The results of this module are stored in a browsers Dictionary,
            which is used in the format_browsers module to identify only the browser
            family. Afterwards, the results are stored in a new Dictionary, browsers_formatted, and passed to the
            graph class to create a barchart of the results.
        """
        browsers = self.data_processor.get_browsers(self.data_handler, True)
        if browsers == {}:
            return "No browsers were found in the input file: does your JSON contain 'visitor_useragent'?"
        self.graphs.barchart(browsers, 'Browser name', 'Occurrence',
                                    'Browsers used to access documents')

    def getTop10Readers(self):  # Q4.
        """
            Functionality asked for in Q4. Provides the processData class object with the input json data which is
            parsed in the get_avid_readers module. Within this module (getTop10Readers), an Ordered Dictionary is returned
            by descending value. The first 10 results are then printed to the console.
         """
        readers = self.data_processor.get_avid_readers(self.data_handler)
        if readers == {} or readers is None:
            return "No readers were found in the JSON file."
        return dict(list(readers.items())[0:10])

    def getVisitorDocs(self):  # Q5b.
        """
            Functionality is asked for in Q5.b. Provides the processData class object with the input json data which
            is parsed in the get_reader_doc_uuids along with a userID to find all relevant documents.
        """
        if self.doc_uuid is not None:
            visitorDocUUIDs = self.data_processor.get_reader_doc_uuids(self.data_handler, self.visitor_uuid)
            if len(visitorDocUUIDs) == 0:  # No matching docs found
                print('No matching documents found for the user \'%s\'' % self.visitor_uuid)
                return
            print(visitorDocUUIDs)
        else:
            return "DocumentUUID is null"

    def alsoLike(self, visitor_uuid=None):
        other_docs = self.data_processor.also_likes(self.data_handler, self.doc_uuid, visitor_uuid,
                                                    pd.sorted_descending)  # Only want first object returned by method
        if len(other_docs) > 0:  # Other documents were found
            print('Other documents visited by users include: ')
            for doc in other_docs:
                print(doc)
        else:
            return "No other documents were accessed by this documents visitors"

    def alsoLikeTop10(self, visitor_uuid):
        docs = self.data_processor.also_likes(self.data_handler, self.doc_uuid, visitor_uuid,
                                              pd.sorted_descending)
        if docs == {} or docs is None:
            return "No other 'also likes' documents were found."
        return(dict(list(docs.items())[0:10]))

    def alsoLikeGraph(self, visitor_uuid):
        """Q6. Display DOT graph using graphviz package the results of Q5.c)"""
        res = self.data_processor.also_likes_graph(self.data_handler, self.doc_uuid, visitor_uuid)
        # print(res)
        if res == {} or res is None:
            return "The provided User ID does not access the supplied Document ID."
        if isinstance(res, str):  # Error message supplied by res.
            return res
        self.graphs.dot_graph(res, self.doc_uuid, visitor_uuid)

    def __init__(self, filename, doc_uuid=None, visitor_uuid=None):
        """
            Class constructor module. Takes the filename of the json data document and optionally a documentID and/or
            visitor uuid to find, then sets the internal class variables to these parameters and creates data_handler,
            data_processor and graphs objects to be used throughout the class modules.
        """
        self.filename = filename
        self.doc_uuid = doc_uuid  # Optional: Get browsers doesn't require this info
        self.visitor_uuid = visitor_uuid  # Optional: Many tasks don't require this information

        self.data_handler = id.ImportData(filename)
        self.data_processor = pd.ProcessData()
        self.graphs = DrawGraphs()  # Used only by this class, and directly related due to dependency.


class DrawGraphs:

    def barchart(self, json_data, x_axis_label, y_axis_label, chart_title):
        """
            Very simple barchart method from the matplotlib.pyplot library.
            Graph style is set to GGPlot so that there are grid lines
        """
        if json_data == {} or json_data is None:
            return "Graph was attempted with no data."
        width = 0.5

        plt.style.use('ggplot')
        plt.bar(*zip(*json_data.items()))
        plt.title(chart_title)
        plt.xlabel(x_axis_label)
        plt.ylabel(y_axis_label)
        plt.xticks(rotation=90)
        plt.show()

    def dot_graph(self, json_data, doc_uuid, visitor_uuid):
        """
            Takes the data captured in also_likes_graph and turns it into a DOT graph before
            converting to a .pdf
        """
        if json_data == {}:
            print('JSON data is empty, cannot produce graph with empty data set')
            return

        graph = Digraph(name='AlsoLikesGraph', format='pdf')
        graph.node("Readers")
        graph.node("Documents")
        graph.edge("Readers", "Documents")

        for visitor in json_data:
            if visitor == visitor_uuid[-4:]:
                graph.node(visitor, fillcolor='red', style='filled', shape='box')
            else:
                graph.node(visitor, shape='box')

            for line in json_data[visitor]:
                if line == doc_uuid:
                    graph.node(line[-4:], fillcolor='red', style='filled', shape='circle')
                else:
                    graph.node(line[-4:], shape='circle')
                graph.edge(visitor, line[-4:])

        try:  # This will fail if system path variable is not set! I learnt the hard way...
            graph.render('alsoLikeResults.ps', view=True)
        except Exception as e:
            # print(e)
            return e
